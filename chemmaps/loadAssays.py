from django_server import DB
from copy import deepcopy


class loadAssays:
    def __init__(self):
        self.cDB = DB.DB()

    def assays_to_dict(self, l_remove=("entrez_gene_id", "assay_source")):
        self.cDB.config()
        self.cDB.connOpen()
        if self.cDB.conn is None:
            return {}

        schema = self.cDB.schema or "public"
        l_remove = set(l_remove)
        try:
            cur = self.cDB.conn.cursor()
            cur.execute(
                """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
                """,
                ("chts_assays", schema),
            )
            l_cols = cur.fetchall()
            cur.execute("SELECT * FROM chts_assays")
            l_rows = cur.fetchall()
            cur.execute("SELECT DISTINCT assay FROM chts_assays")
            l_assays_ICE = {assay_row[0] for assay_row in cur.fetchall()}
        finally:
            self.cDB.connClose()

        d_out = {}
        for row in l_rows:
            if row[0] not in l_assays_ICE:
                continue
            l_gene = [""]
            i = 0
            imax = len(l_cols)
            d_out[row[0]] = {}
            while i < imax:
                col_name = l_cols[i][0]
                if col_name in l_remove:
                    i += 1
                    continue
                if col_name == "gene":
                    l_gene = str(row[i]).split(";")
                    d_out[row[0]][col_name] = l_gene[0]
                else:
                    d_out[row[0]][col_name] = row[i]
                i += 1
            if len(l_gene) > 1:
                i_assay = 2
                for gene in l_gene[1:]:
                    dup_key = "%s(%s)" % (row[0], i_assay)
                    d_out[dup_key] = deepcopy(d_out[row[0]])
                    d_out[dup_key]["gene"] = gene
                    i_assay += 1

        return d_out
