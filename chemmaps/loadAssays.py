from django_server import DB


class loadAssays:
    def __init__(self):
        self.cDB = DB.DB()

    def DBtoDict(self, name_table):

        l_cols = self.cDB.getColnames("tox21_assays")
        l_rows = self.cDB.getTable("tox21_assays")
        d_out = {}
        for row in l_rows:
            i = 0
            imax = len(l_cols)
            d_out[row[0]] = {}
            while i < imax:
                d_out[row[0]][l_cols[i][0]] = row[i]
                i = i + 1
        return d_out