from django_server import DB


class loadAssays:
    def __init__(self):
        self.cDB = DB.DB()

    def DBtoDict(self, name_table):

        l_cols = self.cDB.getColnames("tox21_assays")
        l_rows = self.cDB.getTable("tox21_assays")
        
        self.cDB.connOpen()
        l_assays_ICE = self.cDB.execCMD("SELECT DISTINCT aenm from ice_tox21")
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
                d_out[row[0]][l_cols[i][0]] = row[i]
                i = i + 1

        return d_out