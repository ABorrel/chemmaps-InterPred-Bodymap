"""Geometry and one-column feature reads for the chemical maps."""

import math
import re
from collections import OrderedDict
from os import path

from .DBrequest import DBrequest
from .features import USER_DESCRIPTOR
from .toolbox import loadMatrixInfoToDict

MAP_TABLE = {
    "drugbank": ("mvwchemmap_mapdrugbank", "drugbank_id"),
    "pfas": ("mvwchemmap_mappfas", "dsstox_id"),
    "tox21": ("mvwchemmap_maptox21", "dsstox_id"),
    "dsstox": ("mvwchemmap_mapdsstox", "dsstox_id"),
}

_NAME_LISTS = {}
_FULL_COLUMNS = {}
_DSSTOX_CENTERS = OrderedDict()
_DSSTOX_CAP = 32
_DSSTOX_CLOUD = None
NEIGHBORHOOD_LIMIT = 20000
_DTXSID = re.compile(r"^DTXSID\d+$")


def _names(table):
    if table not in _NAME_LISTS:
        rows = DBrequest().extractColoumn(table, "name")
        _NAME_LISTS[table] = [row[0] for row in rows] if isinstance(rows, list) else []
    return _NAME_LISTS[table]


def sql_index(table, name):
    try:
        return _names(table).index(name) + 1
    except ValueError:
        return None


def tox_table(map_name):
    if map_name == "drugbank":
        return "chem_prop_drugbank_name"
    return "chem_toxexp_name"


def class_sql(map_name):
    name = "DRUG_GROUPS" if map_name == "drugbank" else "GHS_category"
    index = sql_index(tox_table(map_name), name)
    if index is None:
        return "NULL"
    return "prop_tox[%d]" % index


def feature_sql(map_name, key):
    opera = sql_index("chem_descriptor_opera_name", key)
    if opera is not None:
        return "prop_value[%d]" % opera
    tox = sql_index(tox_table(map_name), key)
    if tox is not None:
        return "prop_tox[%d]" % tox
    return None


def tox_slot(map_name, key):
    """Index into prop_tox. Opera columns stay on prop_value."""
    if sql_index("chem_descriptor_opera_name", key) is not None:
        return None
    table = tox_table(map_name)
    index = sql_index(table, key)
    if index is None:
        return None
    return index, len(_names(table))


_GROUP_TOKEN = re.compile(
    r"(?:approved|experimental|investigational|nutraceutical|illicit|withdrawn|vet_approved)"
    r"(?:;(?:approved|experimental|investigational|nutraceutical|illicit|withdrawn|vet_approved))*"
)
_NUMBER_TOKEN = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")


def _quote_anchor(text):
    """A later field boundary when a quoted name never received its closing quote."""
    if len(text) > 1 and text[0] in "'\"" and text[-1] == text[0] and text.count(text[0]) % 2 == 0:
        return True
    if text == "NA" or _NUMBER_TOKEN.fullmatch(text) or _GROUP_TOKEN.fullmatch(text):
        return True
    return False


def _opens_quote(text):
    return text[:1] in "'\"" and (
        len(text) == 1 or text[-1] != text[0]
        or text.count(text[0]) % 2 == 1 and not (text[-1] == text[0] and len(text) > 1)
    )


def _reassemble(parts):
    """Join array elements that were split on commas inside quotes."""
    texts = ["" if part is None else str(part) for part in parts]
    out = []
    i = 0
    n = len(texts)
    while i < n:
        text = texts[i]
        if not _opens_quote(text):
            out.append(text)
            i += 1
            continue
        if len(text) > 1 and text[-1] == text[0]:
            out.append(text[1:-1])
            i += 1
            continue
        quote = text[0]
        closer = None
        for j in range(i + 1, n):
            if texts[j].endswith(quote) and texts[j].count(quote) % 2 == 1:
                closer = j
                break
        if closer is not None:
            buf = [text[1:]]
            buf.extend(texts[i + 1:closer])
            buf.append(texts[closer][:-1])
            out.append(",".join(buf))
            i = closer + 1
            continue
        end = i + 1
        while end < n and not _quote_anchor(texts[end]):
            end += 1
        if end > i + 1 and end < n:
            out.append(",".join([text[1:]] + texts[i + 1:end]))
            i = end
            continue
        out.append(",".join(texts[i:]))
        break
    return out


def align_array(parts, width):
    if not isinstance(parts, (list, tuple)):
        return parts
    if len(parts) == width:
        return parts
    repaired = _reassemble(parts)
    if len(repaired) == width:
        return repaired
    return parts


def _at(parts, index, width):
    aligned = align_array(parts, width)
    if not isinstance(aligned, (list, tuple)) or index < 1 or index > len(aligned):
        return None
    return aligned[index - 1]


def _tox_column(rows, index, width):
    return {row[0]: clean_value(_at(row[1], index, width)) for row in rows}


def class_text(value):
    if value is None or value == "NaN":
        return "NA"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def clean_value(value):
    if value is None or value == -9999 or value == "-9999" or value == "NaN":
        return "NA"
    if isinstance(value, bool):
        return value
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return "NA"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value
    if math.isnan(number) or math.isinf(number):
        return "NA"
    if isinstance(value, str) and not _numeric_text(value):
        return value
    return round(number, 1)


def _numeric_text(value):
    text = value.strip()
    if text[:1] in "+-":
        text = text[1:]
    return text.replace(".", "", 1).isdigit()


def _rows(sql, params):
    db = DBrequest()
    rows = db.execCMD(sql, params)
    if not isinstance(rows, list):
        return []
    return rows


def geometry_rows(map_name):
    table, id_column = MAP_TABLE[map_name]
    db = DBrequest()
    relation = db.relation(table)
    class_name = "DRUG_GROUPS" if map_name == "drugbank" else "GHS_category"
    name_table = tox_table(map_name)
    class_index = sql_index(name_table, class_name)
    width = len(_names(name_table))
    sql = (
        "SELECT %s, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_tox "
        "FROM %s ORDER BY %s"
    ) % (id_column, relation, id_column)
    rows = []
    for row in _rows(sql, None):
        row = list(row)
        row[7] = None if class_index is None else _at(row[7], class_index, width)
        rows.append(row)
    return rows


def _column_dict(rows):
    return {row[0]: clean_value(row[1]) for row in rows}


def full_column(map_name, key):
    cache_key = (map_name, key)
    cached = _FULL_COLUMNS.get(cache_key)
    if cached is not None:
        return cached
    slot = tox_slot(map_name, key)
    expression = None if slot else feature_sql(map_name, key)
    if slot is None and expression is None:
        _FULL_COLUMNS[cache_key] = {}
        return {}
    table, id_column = MAP_TABLE[map_name]
    db = DBrequest()
    relation = db.relation(table)
    if slot:
        index, width = slot
        sql = "SELECT %s, prop_tox FROM %s" % (id_column, relation)
        column = _tox_column(_rows(sql, None), index, width)
    else:
        sql = "SELECT %s, %s FROM %s" % (id_column, expression, relation)
        column = _column_dict(_rows(sql, None))
    _FULL_COLUMNS[cache_key] = column
    return column


def dsstox_column(center, key):
    bucket = _DSSTOX_CENTERS.get(center)
    if bucket is not None and key in bucket:
        _DSSTOX_CENTERS.move_to_end(center)
        return bucket[key]
    slot = tox_slot("dsstox", key)
    expression = None if slot else feature_sql("dsstox", key)
    column = {}
    if (slot or expression) and center:
        db = DBrequest()
        relation = db.relation("mvwchemmap_mapdsstox")
        chosen = "prop_tox" if slot else expression
        sql = (
            "SELECT dsstox_id, %s FROM %s ORDER BY cube(d3_cube) <-> "
            "(SELECT cube(d3_cube) FROM %s WHERE dsstox_id = %%s LIMIT 1) LIMIT %%s"
        ) % (chosen, relation, relation)
        fetched = _rows(sql, [center, NEIGHBORHOOD_LIMIT])
        if slot:
            column = _tox_column(fetched, slot[0], slot[1])
        else:
            column = _column_dict(fetched)
    if center not in _DSSTOX_CENTERS:
        _DSSTOX_CENTERS[center] = {}
        while len(_DSSTOX_CENTERS) > _DSSTOX_CAP:
            _DSSTOX_CENTERS.popitem(last=False)
    _DSSTOX_CENTERS[center][key] = column
    _DSSTOX_CENTERS.move_to_end(center)
    return column


def ids_column(map_name, key, ids):
    slot = tox_slot(map_name, key)
    expression = None if slot else feature_sql(map_name, key)
    if (slot is None and expression is None) or not ids:
        return {}
    table, id_column = MAP_TABLE[map_name]
    db = DBrequest()
    relation = db.relation(table)
    chosen = "prop_tox" if slot else expression
    sql = "SELECT %s, %s FROM %s WHERE %s = ANY(%%s)" % (id_column, chosen, relation, id_column)
    fetched = _rows(sql, [list(ids)])
    if slot:
        return _tox_column(fetched, slot[0], slot[1])
    return _column_dict(fetched)


def _finite(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return round(number, 5)


def dsstox_cloud():
    """Every DSSTox position and GHS category, ordered by dsstox_id.

    Rows with no DTXSID are left out: the cloud identifies chemicals by that id.
    The result stays in this process until restart.
    """
    global _DSSTOX_CLOUD
    if _DSSTOX_CLOUD is not None:
        return _DSSTOX_CLOUD
    db = DBrequest()
    relation = db.relation("mvwchemmap_mapdsstox")
    sql = (
        "SELECT dsstox_id, dim1d2d[1], dim1d2d[2], dim3d[1], %s "
        "FROM %s WHERE dsstox_id LIKE 'DTXSID%%' ORDER BY dsstox_id"
    ) % (class_sql("dsstox"), relation)
    ids = []
    x_values = []
    y_values = []
    z_values = []
    ghs_values = []
    for row in _rows(sql, None):
        dsstox_id = str(row[0] or "")
        if not _DTXSID.fullmatch(dsstox_id):
            continue
        x_value = _finite(row[1])
        y_value = _finite(row[2])
        z_value = _finite(row[3])
        if x_value is None or y_value is None or z_value is None:
            continue
        ghs = class_text(row[4])
        if not ghs:
            ghs = "NA"
        ids.append(dsstox_id)
        x_values.append(x_value)
        y_values.append(y_value)
        z_values.append(z_value)
        ghs_values.append(ghs)
    payload = {"ids": ids, "x": x_values, "y": y_values, "z": z_values, "ghs": ghs_values}
    if ids:
        _DSSTOX_CLOUD = payload
    return payload


def dsstox_chemical(dsstox_id):
    """SMILES, GHS category, and neighbor DTXSIDs for one DSSTox chemical.

    neighbors_dim3 stores InChIKeys. They are resolved to DTXSIDs in that order.
    """
    if not _DTXSID.fullmatch(dsstox_id or ""):
        return None
    db = DBrequest()
    relation = db.relation("mvwchemmap_mapdsstox")
    sql = (
        "SELECT smiles_clean, inchikey, neighbors_dim3, %s FROM %s WHERE dsstox_id = %%s"
    ) % (class_sql("dsstox"), relation)
    rows = _rows(sql, [dsstox_id])
    if not rows:
        return None
    smiles, inchikey, neighbors, ghs_value = rows[0]
    inchikeys = []
    if isinstance(neighbors, (list, tuple)):
        for item in neighbors:
            text = str(item or "")
            if text and text not in inchikeys:
                inchikeys.append(text)
    by_inchikey = {}
    if inchikeys:
        lookup = "SELECT inchikey, dsstox_id FROM %s WHERE inchikey = ANY(%%s)" % relation
        for found_inchikey, found_id in _rows(lookup, [inchikeys]):
            found_id = str(found_id or "")
            if _DTXSID.fullmatch(found_id):
                by_inchikey[str(found_inchikey)] = found_id
    resolved = []
    for item in inchikeys:
        match = by_inchikey.get(item)
        if match and match not in resolved:
            resolved.append(match)
    ghs = class_text(ghs_value)
    if not ghs:
        ghs = "NA"
    return {
        "smiles": smiles or "",
        "inchikey": inchikey or "",
        "ghs": ghs,
        "neighbors": resolved,
    }


def user_overrides(session_dir, key):
    descriptor = USER_DESCRIPTOR.get(key)
    file_path = path.join(session_dir, "2D.csv")
    if descriptor is None or not path.isfile(file_path):
        return {}
    try:
        table = loadMatrixInfoToDict(file_path)
    except (OSError, IndexError, ValueError):
        return {}
    overrides = {}
    for chem_id, row in table.items():
        overrides[str(chem_id)] = clean_value(row.get(descriptor))
    return overrides
