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

    def loadAssayMostActive(self):

        self.cDB.connOpen()
        # load assays results
        l_chemassay = self.cDB.execCMD('SELECT dtxsid, ac50, aenm FROM ice_tox21 WHERE new_hitc = 1')
        self.cDB.connClose()

        #extract QC fail
        self.cDB.connOpen()
        l_chem_fail = self.cDB.execCMD("SELECT DISTINCT dsstox_id, niceatm_qc_summary_call FROM chts_chemicalqc WHERE niceatm_qc_summary_call != 'PASS'")
        self.cDB.connClose()

        d_fail = {}
        for chem_fail in l_chem_fail:
            d_fail[chem_fail[0]] = chem_fail[1]

        # format output assays
        d_assay = {}
        for chem in l_chemassay:
            dtxsid = chem[0]
            ac50 = chem[1]
            if ac50 == None: ac50 = 0.0
            else: ac50 = float(ac50)
            aenm = chem[2]

            if not dtxsid in list(d_assay.keys()):
                d_assay[dtxsid] = {}
                d_assay[dtxsid]["Most active assay"] = "None"
                d_assay[dtxsid]["Active assays"] = 0
                d_assay[dtxsid]["AC50"] = "-"
                d_assay[dtxsid]["Assay Outcome"] = "-"

            d_assay[dtxsid]["Active assays"] =  d_assay[dtxsid]["Active assays"] + 1
            d_assay[dtxsid]["Assay Outcome"] = 'active'
            if d_assay[dtxsid]["AC50"] == "-" or ac50 < d_assay[dtxsid]["AC50"]:
                d_assay[dtxsid]["Most active assay"] = aenm
                d_assay[dtxsid]["AC50"] = ac50
            

        for DTXSID in self.dmap["info"].keys():
            if not DTXSID in list(d_assay.keys()):
                self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "-"
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "Not tested"
                self.dmap["info"][DTXSID]["Most active assay"] = "-"
                self.dmap["info"][DTXSID]["Number of active assay"] = 0
                if DTXSID in list(d_fail.keys()):
                    self.dmap["info"][DTXSID]["Assay Outcome"] = "QC omit"
                    self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = 'QC omit'
                else:
                    self.dmap["info"][DTXSID]["Assay Outcome"] = "-"
            else:
                if d_assay[DTXSID]["AC50"] == 0.0:
                    self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "< 0.001 (%s positive assay(s))"%(d_assay[DTXSID]["Active assays"])
                else:
                    self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "%.2f (%s positive assay(s))"%(d_assay[DTXSID]["AC50"], d_assay[DTXSID]["Active assays"])
                self.dmap["info"][DTXSID]["Assay Outcome"] = "active"
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "active"
                self.dmap["info"][DTXSID]["Most active assay"] = d_assay[DTXSID]["Most active assay"]
                self.dmap["info"][DTXSID]["Number of active assay"] = d_assay[DTXSID]["Active assays"]

        # chemicals active
        nb_active = 0
        for chem in d_assay.keys():
            if d_assay[chem]['Assay Outcome'] == "active":
                nb_active = nb_active + 1
        self.nb_active = nb_active


        # assays targeted - use new assay list from chts
        self.cDB.connOpen()
        # load assays results
        l_assay = self.cDB.execCMD("SELECT DISTINCT assay FROM chts_assays")
        self.cDB.connClose()

        self.nb_assays = len(l_assay)

    def loadAssayTargeted(self):

        self.cDB.connOpen()
        # load assays results
        l_chemassay = self.cDB.execCMD("SELECT dtxsid, new_hitc, ac50, aenm FROM ice_tox21 INNER JOIN chts_assays ON chts_assays.assay = ice_tox21.aenm WHERE gene='%s'"%(self.assay))
        self.cDB.connClose()

        # format output assays
        d_assay = {}
        for chem in l_chemassay:
            dtxsid = chem[0]
            hitc = int(chem[1])
            ac50 = chem[2]
            if ac50 == None: ac50 = 0.0
            else: ac50 = float(ac50)
            aenm = chem[3]

            if not dtxsid in list(d_assay.keys()):
                d_assay[dtxsid] = {}
                d_assay[dtxsid]["Most active assay"] = "None"
                d_assay[dtxsid]["Active assays"] = 0
                if hitc == 0 and hitc == -1: 
                    d_assay[dtxsid]["Assay Outcome"] = "inactive"
                    d_assay[dtxsid]["AC50"] = 0.0
                elif hitc == 2:
                    d_assay[dtxsid]["Assay Outcome"] = "inconclusive"
                    d_assay[dtxsid]["AC50"] = "NA"
                elif hitc == 3:
                    d_assay[dtxsid]["Assay Outcome"] = "inconclusive"
                    d_assay[dtxsid]["AC50"] = "NA"
                else:
                    d_assay[dtxsid]["Assay Outcome"] = "active"
                    d_assay[dtxsid]["AC50"] = ac50
                    d_assay[dtxsid]["Most active assay"] = aenm
                    d_assay[dtxsid]["Active assays"] = d_assay[dtxsid]["Active assays"] + 1
            
            else:
                if hitc == 1: 
                    if d_assay[dtxsid]["AC50"] == "NA" or d_assay[dtxsid]["AC50"] > 0.0 and ac50 < d_assay[dtxsid]["AC50"]:
                        d_assay[dtxsid]["Most active assay"] = aenm
                        d_assay[dtxsid]["AC50"] = ac50
                    d_assay[dtxsid]["Active assays"] =  d_assay[dtxsid]["Active assays"] + 1


        for DTXSID in self.dmap["info"].keys():
            if not DTXSID in list(d_assay.keys()):
                self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "Not tested"
                self.dmap["info"][DTXSID]["Assay Outcome"] = "Not tested"
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "Not tested"
                self.dmap["info"][DTXSID]["Most active assay"] = "None"
                self.dmap["info"][DTXSID]["Number of active assay"] = 0


            else:
                if d_assay[DTXSID]["Assay Outcome"] == "active":
                    if d_assay[DTXSID]["AC50"] == 0.0:
                        self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "< 0.001 (%s positive assay(s))"%(d_assay[DTXSID]["Active assays"])
                    else:
                        self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "%.3f (%s positive assay(s))"%(d_assay[DTXSID]["AC50"], d_assay[DTXSID]["Active assays"])
                    self.dmap["info"][DTXSID]["Number of active assay"] = d_assay[DTXSID]["Active assays"]
                    self.dmap["info"][DTXSID]["Assay Outcome"] = "active"
                    self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "active"
                    self.dmap["info"][DTXSID]["Most active assay"] = d_assay[DTXSID]["Most active assay"]

                elif d_assay[DTXSID]["Assay Outcome"] == "inactive":
                    self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "0.0"
                    self.dmap["info"][DTXSID]["Assay Outcome"] = "inactive"
                    self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "inactive"
                    self.dmap["info"][DTXSID]["Number of active assay"] = 0
                
                else:
                    self.dmap["info"][DTXSID]["Lowest AC50 (µM)"] = "NA"
                    self.dmap["info"][DTXSID]["Assay Outcome"] = "inconclusive"
                    self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "inconclusive"    
                    self.dmap["info"][DTXSID]["Number of active assay"] = 0                


                
        # chemicals active
        nb_active = 0
        for chem in d_assay.keys():
            if d_assay[chem]['Assay Outcome'] == "active":
                nb_active = nb_active + 1
        self.nb_active = nb_active


        # assays targeted
        self.cDB.connOpen()
        # load assays results
        l_assay = self.cDB.execCMD("SELECT DISTINCT aenm FROM ice_tox21 INNER JOIN chts_assays ON chts_assays.assay = ice_tox21.aenm WHERE gene='%s'"%(self.assay))
        self.cDB.connClose()

        self.nb_assays = len(l_assay)

    def loadAssayResults(self):

        self.cDB.connOpen()
        # load assays results
        l_chemassay = self.cDB.execCMD("SELECT dtxsid, new_hitc, ac50 FROM ice_tox21 WHERE aenm='%s'"%(self.assay))
        self.cDB.connClose()

        nb_active_chemical = 0

        # format output assays
        d_assay = {}
        for chem in l_chemassay:
            dtxsid = chem[0]
            hitc = int(chem[1])
            ac50 = chem[2]
            if ac50 == None: ac50 = 0.0
            else: ac50 = float(ac50)

            if not dtxsid in list(d_assay.keys()):
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
                d_assay[dtxsid]["QC"] = "PASS"


        for dtxsid in d_assay.keys():
            if d_assay[dtxsid]["AC50"] != "NA" and  d_assay[dtxsid]["AC50"] != 0.0:
                    nb_active_chemical = nb_active_chemical + 1


        for DTXSID in self.dmap["info"].keys():
            if not DTXSID in list(d_assay.keys()):
                self.dmap["info"][DTXSID]["AC50 (µM)"] = "NA"
                self.dmap["info"][DTXSID]["Assay Outcome"] = "Not tested"
                self.dmap["info"][DTXSID]["QC"] = "NA"
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = "Not tested"
                self.dmap["SMILESClass"][DTXSID]["QC"] = "NA"

            else:
                if d_assay[DTXSID]["AC50"] == 0.0 and d_assay[DTXSID]["Assay Outcome"] == "active":
                    self.dmap["info"][DTXSID]["AC50 (µM)"] = "< 0.001"
                elif d_assay[DTXSID]["Assay Outcome"] == "active":
                    self.dmap["info"][DTXSID]["AC50 (µM)"] = "%.3f"%(d_assay[DTXSID]["AC50"])
                elif d_assay[DTXSID]["Assay Outcome"] == "inactive":
                    self.dmap["info"][DTXSID]["AC50 (µM)"] = "0.0"
                else:
                    self.dmap["info"][DTXSID]["AC50 (µM)"] = "NA"

                self.dmap["info"][DTXSID]["Assay Outcome"] = d_assay[DTXSID]["Assay Outcome"]
                self.dmap["info"][DTXSID]["QC"] = d_assay[DTXSID]["QC"]
                self.dmap["SMILESClass"][DTXSID]["QC"] = d_assay[DTXSID]["QC"]
                self.dmap["SMILESClass"][DTXSID]["Assay Outcome"] = d_assay[DTXSID]["Assay Outcome"]

        #self.cDB.connOpen()
        # load assays results
        #l_unique_chem = self.cDB.execCMD("SELECT DISTINCT dtxsid FROM ice_tox21 WHERE aenm='%s'"%(self.assay))
        #self.cDB.connClose()


        self.nb_active = nb_active_chemical
        self.nb_tested = len(l_chemassay)



            



