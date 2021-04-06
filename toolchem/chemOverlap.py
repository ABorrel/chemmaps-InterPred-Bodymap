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
        l_topush = []
        d_chem = toolbox.loadMatrixToDict(self.p_fchem)

        self.DB.openConnection()

        # extract all chemicals in the main DB
        l_chem_chemicalsDB = self.DB.DB.execCMD("SELECT dsstox_id FROM chemical_description INNER JOIN chemicals ON chemical_description.inchikey = chemicals.inchikey WHERE map_name = '%s'"%(self.chem_map))
        l_chem_DB = []
        for chem_DB in l_chem_chemicalsDB:
            chem = chem_DB[0]
            if chem == None:
                continue
            else:
                l_chem_DB.append(chem)
        l_chem_DB.sort()

        # extract all chemicals in the update table
        l_chem_updateDB = self.DB.DB.execCMD("SELECT dsstox_id FROM chemicals_user WHERE status='update';")
        l_chem_DB_update = []
        for chem_DB in l_chem_updateDB:
            chem = chem_DB[0]
            if chem == None:
                continue
            else:
                l_chem_DB_update.append(chem)
        
        l_chem_DB_update.sort()

        for chem in d_chem.keys():
            dsstox = d_chem[chem]["dsstox_id"]
            in_main_chemical_table = toolbox.binary_search(l_chem_DB, dsstox)
            if in_main_chemical_table == -1:
                in_user_table = toolbox.binary_search(l_chem_DB_update, dsstox)
                if in_user_table == -1:
                    l_noincluded.append(d_chem[chem])
                else:
                    l_topush.append(d_chem[chem])
            else:
                l_included.append(d_chem[chem])

        self.l_topush = l_topush
        self.l_included = l_included
        self.l_noincluded = l_noincluded

        # check NB chemicals in the descriptor table
        nb_chem_descDB = self.DB.DB.execCMD("SELECT COUNT(*) FROM chemical_description WHERE map_name='%s';"%(self.chem_map))
        self.nbChemDescForMap = nb_chem_descDB[0][0]
        self.DB.closeConnection()

    def prepOutput(self):

        # writes the overlap
        p_filin = self.pr_session + "chemicals.csv"
        filin = open(p_filin, "w")
        filin.write("smiles_origin\tdsstox_id\tname\tcasn\n")
        for chem in self.l_noincluded:
            filin.write("%s\t%s\t%s\t%s\n"%(chem["smiles_origin"], chem["dsstox_id"], chem["name"], chem["casn"]))
        filin.close()