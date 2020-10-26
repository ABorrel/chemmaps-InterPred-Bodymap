from django_server import toolbox
from . import DBrequest


class chemOverlap:
    def __init__(self, p_fchem, chem_map, pr_session):
        self.p_fchem = p_fchem
        self.chem_map = chem_map
        self.DB = DBrequest.DBrequest()
        self.pr_session = pr_session

    def runCheck(self, col_name):

        
        l_included = []
        l_noincluded = []
        d_chem = toolbox.loadMatrixToDict(self.p_fchem)
        for chem in d_chem.keys():
            self.DB.openConnection()
            in_chemical_table = self.DB.searchDTXID(d_chem[chem][col_name])
            self.DB.closeConnection()
            if in_chemical_table == 1:
                inchkey = self.DB.DB.extractColoumn("chemicals", "inchikey", "WHERE %s = '%s'"%(col_name, d_chem[chem][col_name]))
                inchkey = inchkey[0][0]
                self.DB.openConnection()
                in_chemical_desc = self.DB.searchInchikey(inchkey, self.chem_map)
                self.DB.closeConnection()
                if in_chemical_desc == 1:
                    l_included.append(d_chem[chem])
                else:
                    l_noincluded.append(d_chem[chem])

        self.l_included = l_included
        self.l_noincluded = l_noincluded


    def prepOutput(self):

        # writes the overlap
        p_filin = self.pr_session + "chemicals.csv"
        filin = open(p_filin, "w")
        filin.write("smiles_origin\tdsstox_id\tname\tcasn\n")
        for chem in self.l_noincluded:
            filin.write("%s\t%s\t%s\t%s\n"%(chem["smiles_origin"], chem["dsstox_id"], chem["name"], chem["casn"]))
        filin.close()