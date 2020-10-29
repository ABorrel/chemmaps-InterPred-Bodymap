from numpy import setdiff1d, average
#from math import log10
from re import search

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
        l_chemassay = self.cDB.execCMD("SELECT assay_outcome, ac50, dsstox_id, qc_new_spid FROM tox21_tripod INNER JOIN tox21_qc ON tox21_tripod.sample_id = tox21_qc.ncgc_id INNER JOIN chemicals ON tox21_tripod.cas = chemicals.casn WHERE protocol_name='%s'"%(self.assay))
        self.cDB.connClose()

        #INNER JOIN tox21_qc ON tox21_tripod.sample_id = tox21_qc.ncgc_id

        # load cas to DTXSID
        l_dsstoxid_run = []
        for l_propchem in l_chemassay:
            DTXSID = l_propchem[2]
            if DTXSID == None:
                continue
            
            try:
                AC50 = float(l_propchem[1])
                assay_outcome = l_propchem[0]
                if  search("inconclusive", assay_outcome):
                    self.dmap["info"][DTXSID]["AC50"] = 0.0
                elif search("inactive", assay_outcome):
                    self.dmap["info"][DTXSID]["AC50"] = 0.0
                else:
                    if AC50 == 0.0:
                        continue    
                    try:self.dmap["info"][DTXSID]["AC50"].append(AC50)
                    except:
                        self.dmap["info"][DTXSID]["AC50"] = []
                        self.dmap["info"][DTXSID]["AC50"].append(AC50)
                
                self.dmap["info"][DTXSID]["Assay Outcome"] = assay_outcome
                self.dmap["info"][DTXSID]["QC"] = l_propchem[3]
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = assay_outcome
                l_dsstoxid_run.append(DTXSID)
            except:

                pass
        
        #print(len(l_chemassay))
        #print(len(l_dsstoxid_run))
        #print(len(l_add_key_chem))
        #print(l_add_key_chem[1:10])

        for DTXSID in self.dmap["info"].keys():
            
            if not "AC50" in list(self.dmap["info"][DTXSID].keys()):
                self.dmap["info"][DTXSID]["AC50"] = "NA"
                self.dmap["info"][DTXSID]["Assay Outcome"] = "inconclusive"
                self.dmap["info"][DTXSID]["QC"] = "NA"
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "inconclusive"
            
            elif type(self.dmap["info"][DTXSID]["AC50"]) == list:
                self.dmap["info"][DTXSID]["AC50"] = average(self.dmap["info"][DTXSID]["AC50"])
                #print(self.dmap["info"][DTXSID]["AC50"])

            



