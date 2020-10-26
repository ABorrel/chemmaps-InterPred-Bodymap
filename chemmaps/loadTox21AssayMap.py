from numpy import setdiff1d

from .uploadMap import loadingMap
from django_server import DB


class loadTox21AssayMap:
    def __init__(self, assay):

        self.assay = assay
        self.l_desc = ["LogP_pred", "MolWeight"]
        self.cDB = DB.DB()
    
    def loadMapCoords(self):

        cload = loadingMap("Tox21Map", self.l_desc)
        dmap = cload.loadMap()
        self.dmap = dmap


    def loadAssayResults(self):

        self.cDB.connOpen()
        # load assays results
        l_chemassay = self.cDB.execCMD("SELECT tox21_id, assay_outcome, ac50, dsstox_id FROM tox21_tripod INNER JOIN chemicals ON tox21_tripod.smiles = chemicals.smiles_origin WHERE protocol_name='%s'"%(self.assay))
        self.cDB.connClose()

        # load cas to DTXSID
        l_dsstoxid_run = []
        for l_propchem in l_chemassay:
            DTXSID = l_propchem[3]
            if DTXSID == None:
                continue
            try:
                self.dmap["info"][DTXSID]["AC50"] = l_propchem[2]
                self.dmap["info"][DTXSID]["Assay Outcome"] = l_propchem[1]
                l_dsstoxid_run.append(DTXSID)
            except:
                pass
            
            l_add_key_chem = setdiff1d(list(self.dmap["info"].keys()), l_dsstoxid_run)
            for add_key_chem in l_add_key_chem:
                 self.dmap["info"][add_key_chem]["AC50"] = 0.0
                 self.dmap["info"][add_key_chem]["Assay Outcome"] = "inconclusive"
            #DTXSID = self.cDB.execCMD("SELECT dsstox_id FROM chemicals WHERE casn='%s'"%(cas))
            #print(DTXSID)


        # rebuild dprop with assays results
        #print(self.dmap["info"])
