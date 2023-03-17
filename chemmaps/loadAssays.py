from django_server import DB
from copy import deepcopy

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
                if l_cols[i][0] in l_remove:
                    i = i + 1
                    continue
                else:
                    if l_cols[i][0] == "gene":
                        l_gene = str(row[i]).split(";")
                        d_out[row[0]][l_cols[i][0]] = l_gene[0]       
                    else:
                        d_out[row[0]][l_cols[i][0]] = row[i]
                i = i + 1
            if len(l_gene) > 1:
                i_assay = 2
                for gene in l_gene[1:]:
                    d_out[row[0] + "(%s)"%(i_assay)] = deepcopy(d_out[row[0]])
                    d_out[row[0] + "(%s)"%(i_assay)]["gene"] = gene

        return d_out