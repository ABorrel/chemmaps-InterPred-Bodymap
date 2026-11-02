#!/bin/bash
# Build chemmaps_dev as a stable 20% chemical sample of chemmaps_local.
# Does not stop Postgres or write to the production database.
set -euo pipefail

SRC=chemmaps_local
DST=chemmaps_dev
PORT=5432
PSQL=(psql -U postgres -p "$PORT" -v ON_ERROR_STOP=1)

if [[ "$("${PSQL[@]}" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='${DST}'")" == "1" ]]; then
  echo "Database ${DST} already exists. Refusing to replace it." >&2
  exit 1
fi

avail_kb=$(df -Pk /home | awk 'NR==2 {print $4}')
if (( avail_kb < 8000000 )); then
  echo "Less than 8 GB free on /home (${avail_kb} KB). Aborting." >&2
  exit 1
fi

echo "Creating ${DST}"
"${PSQL[@]}" -d postgres -c "CREATE DATABASE ${DST} OWNER postgres;"

echo "Loading schema from ${SRC}"
pg_dump -U postgres -p "$PORT" -d "$SRC" --schema-only --no-owner --no-acl \
  | "${PSQL[@]}" -d "$DST"

echo "Disabling triggers on ${DST} for the load"
"${PSQL[@]}" -d "$DST" <<'SQL'
DO $$
DECLARE r record;
BEGIN
  FOR r IN
    SELECT n.nspname, c.relname
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'r' AND n.nspname IN ('public', 'update_public')
  LOOP
    EXECUTE format('ALTER TABLE %I.%I DISABLE TRIGGER ALL', r.nspname, r.relname);
  END LOOP;
END $$;
SQL

table_exists() {
  local schema="$1"
  local table="$2"
  [[ "$("${PSQL[@]}" -d "$SRC" -tAc \
    "SELECT 1 FROM information_schema.tables WHERE table_schema='${schema}' AND table_name='${table}' AND table_type='BASE TABLE'")" == "1" ]]
}

copy_select() {
  local schema="$1"
  local table="$2"
  local select_sql="$3"
  echo "  ${schema}.${table}"
  psql -U postgres -p "$PORT" -d "$SRC" -v ON_ERROR_STOP=1 -c "COPY (${select_sql}) TO STDOUT" \
    | psql -U postgres -p "$PORT" -d "$DST" -v ON_ERROR_STOP=1 -c "COPY ${schema}.${table} FROM STDIN"
}

# Stable 20%: inchikey hash, or id when inchikey is null.
sample_where() {
  local alias="$1"
  printf '%s' "(${alias}.inchikey IS NOT NULL AND mod(abs(hashtext(${alias}.inchikey)::bigint), 5) = 0) OR (${alias}.inchikey IS NULL AND mod(abs(hashtext(${alias}.id::text)::bigint), 5) = 0)"
}

copy_matching() {
  local schema="$1"
  local table="$2"
  local where_sql="$3"
  if table_exists "$schema" "$table"; then
    copy_select "$schema" "$table" "SELECT t.* FROM ${schema}.${table} t WHERE ${where_sql}"
  fi
}

FULL_TABLES=(
  tox21_assays
  chts_assays
  bodymap_genemap
  bodymap_assay_mapping_new
  chem_descriptor_1d2d_name
  chem_descriptor_3d_name
  chem_descriptor_opera_name
  chem_interference_prediction_name
  chem_prop_drugbank_name
  chem_toxexp_name
  chemical_description_user
  chemicals_user
)

DJANGO_TABLES=(
  django_content_type
  auth_permission
  auth_group
  auth_user
  auth_group_permissions
  auth_user_groups
  auth_user_user_permissions
  django_admin_log
  django_migrations
)

for schema in public update_public; do
  echo "Full reference tables in ${schema}"
  for table in "${FULL_TABLES[@]}"; do
    if table_exists "$schema" "$table"; then
      copy_select "$schema" "$table" "SELECT * FROM ${schema}.${table}"
    fi
  done
done

echo "Django auth tables"
for table in "${DJANGO_TABLES[@]}"; do
  if table_exists public "$table"; then
    copy_select public "$table" "SELECT * FROM public.${table}"
  fi
done

for schema in public update_public; do
  echo "20% chemical sample in ${schema}"
  pred=$(sample_where c)
  copy_select "$schema" chemicals "SELECT c.* FROM ${schema}.chemicals c WHERE ${pred}"

  copy_matching "$schema" chemical_description \
    "t.inchikey IN (SELECT c.inchikey FROM ${schema}.chemicals c WHERE c.inchikey IS NOT NULL AND $(sample_where c))"

  copy_matching "$schema" chemical_info \
    "t.chem_id IN (SELECT c.id FROM ${schema}.chemicals c WHERE $(sample_where c))"

  copy_matching "$schema" ice_tox21 \
    "t.dtxsid IN (SELECT c.dsstox_id FROM ${schema}.chemicals c WHERE c.dsstox_id IS NOT NULL AND $(sample_where c))"

  copy_matching "$schema" chem_toxexp_value \
    "t.dsstox_id IN (SELECT c.dsstox_id FROM ${schema}.chemicals c WHERE c.dsstox_id IS NOT NULL AND $(sample_where c))"

  copy_matching "$schema" bodymap_assay_ac50 \
    "t.casn IN (SELECT c.casn FROM ${schema}.chemicals c WHERE c.casn IS NOT NULL AND $(sample_where c))"

  copy_matching "$schema" bodymap_chemsum \
    "t.dsstox_id IN (SELECT c.dsstox_id FROM ${schema}.chemicals c WHERE c.dsstox_id IS NOT NULL AND $(sample_where c)) OR t.casn IN (SELECT c.casn FROM ${schema}.chemicals c WHERE c.casn IS NOT NULL AND $(sample_where c))"

  copy_matching "$schema" chts_chemicalqc \
    "t.dsstox_id IN (SELECT c.dsstox_id FROM ${schema}.chemicals c WHERE c.dsstox_id IS NOT NULL AND $(sample_where c)) OR t.casn IN (SELECT c.casn FROM ${schema}.chemicals c WHERE c.casn IS NOT NULL AND $(sample_where c))"

  if table_exists "$schema" chem_prop_drugbank_value; then
    if [[ "$("${PSQL[@]}" -d "$SRC" -tAc \
      "SELECT 1 FROM information_schema.columns WHERE table_schema='${schema}' AND table_name='chem_prop_drugbank_value' AND column_name='drugbank_id'")" == "1" ]]; then
      copy_matching "$schema" chem_prop_drugbank_value \
        "t.drugbank_id IN (SELECT c.drugbank_id FROM ${schema}.chemicals c WHERE c.drugbank_id IS NOT NULL AND $(sample_where c))"
    else
      copy_matching "$schema" chem_prop_drugbank_value \
        "t.source_id IN (SELECT c.drugbank_id FROM ${schema}.chemicals c WHERE c.drugbank_id IS NOT NULL AND $(sample_where c))"
    fi
  fi
done

echo "Re-enabling triggers"
"${PSQL[@]}" -d "$DST" <<'SQL'
DO $$
DECLARE r record;
BEGIN
  FOR r IN
    SELECT n.nspname, c.relname
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.relkind = 'r' AND n.nspname IN ('public', 'update_public')
  LOOP
    EXECUTE format('ALTER TABLE %I.%I ENABLE TRIGGER ALL', r.nspname, r.relname);
  END LOOP;
END $$;
SQL

echo "Resetting sequences"
"${PSQL[@]}" -d "$DST" <<'SQL'
DO $$
DECLARE
  r record;
  seq text;
  mx bigint;
BEGIN
  FOR r IN
    SELECT n.nspname AS s, c.relname AS t, a.attname AS col
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
    WHERE c.relkind = 'r' AND n.nspname IN ('public', 'update_public')
  LOOP
    seq := pg_get_serial_sequence(format('%I.%I', r.s, r.t), r.col);
    IF seq IS NOT NULL THEN
      EXECUTE format('SELECT max(%I) FROM %I.%I', r.col, r.s, r.t) INTO mx;
      IF mx IS NOT NULL THEN
        PERFORM setval(seq, mx);
      END IF;
    END IF;
  END LOOP;
END $$;
SQL

echo "Refreshing materialized views"
"${PSQL[@]}" -d "$DST" -tAc \
  "SELECT schemaname || '.' || matviewname FROM pg_matviews WHERE schemaname IN ('public', 'update_public') ORDER BY 1" \
  | while read -r view; do
      [[ -z "$view" ]] && continue
      echo "  REFRESH ${view}"
      "${PSQL[@]}" -d "$DST" -c "REFRESH MATERIALIZED VIEW ${view};"
    done

echo "ANALYZE"
"${PSQL[@]}" -d "$DST" -c "ANALYZE;"

echo "Sample check"
"${PSQL[@]}" -d "$DST" -c \
  "SELECT map_name, count(*) FROM public.chemical_description GROUP BY 1 ORDER BY 1;"
"${PSQL[@]}" -d "$DST" -c \
  "SELECT pg_size_pretty(pg_database_size('${DST}')) AS dev_size;"
echo "Done."
