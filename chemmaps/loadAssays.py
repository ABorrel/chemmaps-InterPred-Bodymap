from django_server import DB


class loadAssays:
    def __init__(self):
        self.cDB = DB.DB()

    def assays_to_dict(self, l_remove=["entrez_gene_id", "assay_source"]):

        l_cols = self.cDB.getColnames("chts_assays")
        l_rows = self.cDB.getTable("chts_assays")
        
        self.cDB.connOpen()
        l_assays_ICE = self.cDB.execCMD("SELECT DISTINCT assay from chts_assays")
        self.cDB.connClose()
        l_assays_ICE = [assay_ICE[0] for assay_ICE in l_assays_ICE]


        d_out = {}
        for row in l_rows:
            if not row[0] in l_assays_ICE:
                continue
            i = 0
            imax = len(l_cols)

            d_out[row[0]] = {}
            while i < imax:
                # remove not interest col
                if not l_cols[i][0] in l_remove:
                    d_out[row[0]][l_cols[i][0]] = row[i]
                i = i + 1


        return d_out