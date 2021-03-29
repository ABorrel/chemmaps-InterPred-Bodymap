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

        cload = loadingMap("tox21", self.l_desc)
        dmap = cload.loadMap()
        self.dmap = dmap


    def loadAssayResults(self):

        self.cDB.verbose = 1
        self.cDB.connOpen()
        # load assays results
        #l_chemassay = self.cDB.execCMD("SELECT assay_outcome, ac50, dsstox_id, qc_new_spid FROM tox21_tripod INNER JOIN tox21_qc ON tox21_tripod.sample_id = tox21_qc.ncgc_id INNER JOIN chemicals ON tox21_tripod.cas = chemicals.casn WHERE protocol_name='%s'"%(self.assay))
        l_chemassay = self.cDB.execCMD("SELECT dtxsid, new_hitc, new_hitc_flag, qc_omit_src, ac50 FROM ice_tox21 WHERE aenm='%s'"%(self.assay))
        self.cDB.connClose()

        l_dsstoxid_run = []
        nb_active_chemical = 0

        # format output assays
        d_assay = {}
        for chem in l_chemassay:
            dtxsid = chem[0]
            hitc = int(chem[1])
            new_hitc_flag = chem[2]
            qc_omit_src = chem[3]
            ac50 = chem[4]
            if ac50 == None: ac50 = 0.0
            else: ac50 = float(ac50)

            d_assay[dtxsid] = {}
            d_assay[dtxsid]["AC50"] = ac50
            if hitc == 0: 
                d_assay[dtxsid]["Assay Outcome"] = "inactive"
                d_assay[dtxsid]["QC"] = "PASS"
            elif hitc == 2:
                d_assay[dtxsid]["Assay Outcome"] = "inconclusive"
                d_assay[dtxsid]["QC"] = "FAIL"
            elif hitc == 3:
                d_assay[dtxsid]["Assay Outcome"] = "inconclusive"
                d_assay[dtxsid]["QC"] = "FAIL" 
            else:
                d_assay[dtxsid]["Assay Outcome"] = "active"
                nb_active_chemical = nb_active_chemical + 1
                d_assay[dtxsid]["QC"] = "PASS"



        for DTXSID in self.dmap["info"].keys():
            if not DTXSID in list(d_assay.keys()):
                l_dsstoxid_run.append(DTXSID)
                self.dmap["info"][DTXSID]["AC50"] = "NA"
                self.dmap["info"][DTXSID]["Assay Outcome"] = "No tested"
                self.dmap["info"][DTXSID]["QC"] = "NA"
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "No tested"
                self.dmap["SMILESClass"][DTXSID]["QC"] = "NA"

            else:
                self.dmap["info"][DTXSID]["AC50"] = d_assay[DTXSID]["AC50"]
                self.dmap["info"][DTXSID]["Assay Outcome"] = d_assay[DTXSID]["Assay Outcome"]
                self.dmap["info"][DTXSID]["QC"] = d_assay[DTXSID]["QC"]
                self.dmap["SMILESClass"][DTXSID]["QC"] = d_assay[DTXSID]["QC"]
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = d_assay[DTXSID]["Assay Outcome"]

        #print(len(l_chemassay))
        #print(len(l_dsstoxid_run))

        self.nb_active = nb_active_chemical
        self.nb_tested = len(l_dsstoxid_run)



            



