from os import system, path, remove
from .toolbox import loadMatrixToDict, loadMatrixInfoToDict, convertSMILEStoINCHIKEY, loadMap1D2D3D
from .DBrequest import DBrequest
from .uploadMap import loadingMap

import math
from copy import deepcopy


# to format desc for map
# DrugMap
DDESCDRUGMAP = {"JCHEM_ROTATABLE_BOND_COUNT":"Rotable bond", "JCHEM_POLAR_SURFACE_AREA": "Polar surface",
               "MOLECULAR_WEIGHT": "Molecular weight", "JCHEM_PHYSIOLOGICAL_CHARGE": "Physio charge",
               "JCHEM_RULE_OF_FIVE": "Rule of five", "JCHEM_VEBER_RULE": "Veber rule", "FORMULA": "Formula",
               "JCHEM_GHOSE_FILTER": "Ghose filter","GENERIC_NAME": "Generic name",
               "JCHEM_TRADITIONAL_IUPAC":"IUPAC", "ALOGPS_SOLUBILITY": "Solubility",
               "JCHEM_MDDR_LIKE_RULE": "MDDR rule", "PRODUCTS": "Product",
               "ALOGPS_LOGP": "ALogP", "JCHEM_PKA_STRONGEST_BASIC": "Pka Basic",
               "JCHEM_NUMBER_OF_RINGS": "Number of rings", "JCHEM_PKA": "PKA",
               "JCHEM_ACCEPTOR_COUNT": "Acceptor count", "JCHEM_PKA_STRONGEST_ACIDIC": "Pka acidic",
               "EXACT_MASS": "Exact mass", "JCHEM_DONOR_COUNT": "Donor count", "INTERNATIONAL_BRANDS": "Brands",
               "JCHEM_AVERAGE_POLARIZABILITY": "Polarizability","JCHEM_BIOAVAILABILITY": "Bioavailability",
               "DATABASE_NAME": "Database", "JCHEM_REFRACTIVITY": "Refractivity", "JCHEM_LOGP": "LogP",
               "JCHEM_FORMAL_CHARGE": "Formal charge", "SALTS": "Salt", "JCHEM_ATOM_COUNT": "Atom count", "SMILES":"SMILES"}

DDESCDSSTOX = {"EPA_category": "EPA category", "LD50_mgkg": "LD50 (mg/kg)",
               "CATMoS_VT_pred": "Acute Tox (very toxic)", "CATMoS_NT_pred": "Acute Tox (no toxic)",
               "CATMoS_EPA_pred": "Acute Tox (EPA)", "CATMoS_GHS_pred": "Acute Tox (GHS)",
               "CATMoS_LD50_pred": "Acute Tox (LD50)", "CERAPP_Ago_pred": "Estrogen Receptor activity (Agonist)",
               "CERAPP_Bind_pred": "Estrogen Receptor activity (binding)", "Clint_pred": "Hepatic clearance",
               "CoMPARA_Anta_pred": "Androgen Receptor Activity (Antogonist)",
               "CoMPARA_Bind_pred": "Androgen Receptor Activity (binding)",
               "FUB_pred": "Plasma fraction unbound", "LogHL_pred": "Henry’s Law constant (atm-mol3/mole)",
               "LogKM_pred": "KM (biotransformation rate)", "LogKOA_pred": "Log Octanol/air partition coefficient",
               "LogKoc_pred": "Log Soil adsorption coefficient (L/Kg)",
               "LogBCF_pred": "Log Fish bioconcentration factor",
               "LogD55_pred": "LogD", "LogP_pred": "LogP", "MP_pred": "Melting Point (C)", "pKa_a_pred": "Pka acid",
               "pKa_b_pred": "Pka basic", "ReadyBiodeg_pred": "Biodegradability", "RT_pred": "HPLC retention time",
               "LogVP_pred": "Log vapor pressure (mmHg)", "LogWS_pred": "Log Water solubility", "MolWeight": "MW",
               "LogOH_pred": "Log Atmospheric constant (cm3/molsec)",
               "BioDeg_LogHalfLife_pred": "Biodegradation half-life",
               "BP_pred": "Boiling Point", "nbLipinskiFailures": "Lipinski Failures"}



class JSbuilder:

    def __init__(self, nameMap, ldescMap = [], prout = ""):
        self.nameMap = nameMap
        self.prout = prout
        self.ldescMap = ldescMap
        self.cDB = DBrequest()
        self.pMap = path.abspath("./static/chemmaps/map/" + self.nameMap + "/") + "/"
        self.cDB.verbose = 0
        self.err = 0


    def loadMap(self):

        cload = loadingMap(self.nameMap, self.ldescMap)
        dmap = cload.loadMap()
        self.map = dmap

    def generateJS(self):
        """Use to combine all of the prop and coords to generate a JS dictionnary"""
        dout = {}

        ###############
        # coordinates #
        ###############

        ##Coordinates ##
        ################
        if "dchemAdd" in self.__dict__:
            self.map["coord"].update(self.dchemAdd["coord"])

        ########
        # Info #
        ########
        if "dchemAdd" in self.__dict__:
            self.map["info"].update(self.dchemAdd["info"])


        #############
        # Neighbors #
        #############

        # maybe transform inch to db id
        if "dchemAdd" in self.__dict__:
            self.map["neighbor"].update(self.dchemAdd["neighbor"])


        ####################
        # SMILES and Class #
        ####################        
        if "dchemAdd" in self.__dict__:
            self.map["SMILESClass"].update(self.dchemAdd["SMILESClass"])


        # exit structure #
        ##################
        dout["coord"] = self.map["coord"]
        dout["info"] = self.map["info"]
        dout["neighbor"] = self.map["neighbor"]
        dout["SMILESClass"] = self.map["SMILESClass"]

        return dout

    ###################
    # MANAGE ADD file #
    ###################

    def generateCoords(self, p1D2D, p3D):
        """
        Case of new chemicals uploaded in the database
        """
        self.inDB = 0

        # load descriptor from prop
        if self.nameMap == "DrugMap":
            table_prop_name = "drugbank_name_prop"
        else:
            table_prop_name = "dsstox_name_prop"

        # load prop from the DB
        lpropDB = self.cDB.extractColoumn(table_prop_name, "name")
        lpropDB = [prop [0] for prop in lpropDB]
        self.lpropDB = lpropDB

        # name descriptor
        lnameDesc = self.cDB.extractColoumn("desc_1d2d_name", "name")
        self.ldesc2D = lnameDesc

        # define the all structure here of output
        if not "dchemAdd" in self.__dict__:
            self.dchemAdd = {}
            self.dchemAdd["p2D"] = p1D2D
            self.dchemAdd["p3D"] = p3D
            self.dchemAdd["db_id"] = {}
            self.dchemAdd["coord"] = {}
            self.dchemAdd["info"] = {}
            self.dchemAdd["SMILESClass"] = {}
            self.dchemAdd["neighbor"] = {}

        # control if included in DB
        filin = open(p1D2D, "r")
        llines = filin.readlines()
        filin.close()

        ldesc = llines[0].strip().split("\t")
        i = 1
        imax = len(llines)
        while i < imax:
            lval = llines[i].strip().split("\t")
            inchikey = lval[2]
            id = lval[0]
            smiles = lval[1]

            # fix descriptor on map
            ddesc = {}
            d = 0
            dmax = len(ldesc)
            while d < dmax:
                ddesc[ldesc[d]] = lval[d]
                d = d + 1


            if self.nameMap == "DrugMap":
                lextract = self.cDB.extractColoumn("mvwchemmap_mapdrugbank", "drugbank_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value", "WHERE inchikey = '%s' limit (1)"%(inchikey))

            elif self.nameMap == "PFASMap":
                lextract = self.cDB.extractColoumn("mvwchemmap_mappfas", "dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value", "WHERE inchikey = '%s' limit (1)"%(inchikey))

            elif self.nameMap == "Tox21Map":
                lextract = self.cDB.extractColoumn("mvwchemmap_maptox21", "dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value", "WHERE inchikey = '%s' limit (1)"%(inchikey))
            
            else:
                lextract = self.cDB.extractColoumn("mvwchemmap_mapdsstox", "dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value", "WHERE inchikey = '%s' limit (1)"%(inchikey))
            
            

            if lextract != []:
                lextract = lextract[0]
                inch = lextract[2]
                smiles = lextract[1]
                db_id = lextract[0]
                xadd = lextract[3]
                yadd = lextract[4]
                zadd = lextract[5]
                lneighbor = lextract[6]
                lprop = lextract[7]

                self.dchemAdd["db_id"][id] = db_id
                self.dchemAdd["coord"][id] = [float(xadd), float(yadd), float(zadd)]

                # take info and neighbor
                dinfo = {}
                p = 0
                pmax = len(lpropDB)
                while p < pmax:
                    dinfo[lprop[p]] = lval[p]
                    p = p + 1

                
                #info
                self.dchemAdd["info"][id] = {}
                self.dchemAdd["SMILESClass"][id]= {}
                self.dchemAdd["SMILESClass"][id]["SMILES"] = smiles
                self.dchemAdd["SMILESClass"][id]["inchikey"] = inch

                if self.nameMap == "DrugMap":
                    self.dchemAdd["SMILESClass"][id]["DRUG_GROUPS"] = "add"
                else:
                    self.dchemAdd["SMILESClass"][id]["GHS_category"] = "add"


                for desc in self.ldescMap:
                    if desc in list(ddesc.keys()):
                        self.dchemAdd["info"][id][desc] = ddesc[desc]
                    elif desc in list(dinfo.keys()):
                        self.dchemAdd["info"][id][desc] = dinfo[desc]
                    else:
                        self.dchemAdd["info"][id][desc] = "NA"
                
                # neighbor
                if lneighbor != [] and lneighbor != "Error":
                    lneighbormap = []
                    for n in lneighbor:
                        try:lneighbormap.append(self.map["inchikey"][n])
                        except: pass
                    self.dchemAdd["neighbor"][id] = lneighbormap

                # dell from the map in case where the map is loaded (not dsstox)
                if self.nameMap != "DSSToxMap":
                    del self.map["coord"][db_id]
                    del self.map["neighbor"][db_id]
                    del self.map["info"][db_id]
                    del self.map["SMILESClass"][db_id]

                del llines[i]
                imax = imax - 1
                continue

            else:
                #Check on the user table
                lextract = self.cDB.extractColoumn("chemmap_coords_user", "source_id, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, desc_1d2d",  "WHERE inchikey = '%s' and map_name = '%s' limit (1)"%(inchikey, self.nameMap))

                if lextract != [] and not None in lextract[0] != None:
                    lextract = lextract[0]
                    inch = lextract[1]
                    smiles = lextract[0]
                    xadd = lextract[2]
                    yadd = lextract[3]
                    zadd = lextract[4]
                    lneighbor = lextract[5]
                    lvaldesc2D = lextract[6]

                    self.dchemAdd["db_id"][id] = ""
                    self.dchemAdd["coord"][id] = [float(xadd), float(yadd), float(zadd)]


                    # take info and neighbor

                    
                    #info
                    self.dchemAdd["info"][id] = {}
                    desc_i = 0
                    desc_imax = len(lvaldesc2D)
                    d2Ddesc = {}
                    while desc_i < desc_imax:
                        desc = self.ldesc2D[desc_i][0]
                        val = lvaldesc2D[desc_i]
                        d2Ddesc[desc] = val
                        desc_i = desc_i + 1
                    
                    for descMap in self.ldescMap:
                        if descMap == "MOLECULAR_WEIGHT":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["MolWt"]
                        elif descMap == "MolWeight":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["MolWt"]    
                        elif descMap == "JCHEM_ROTATABLE_BOND_COUNT":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["NumRotatableBonds"]
                        elif descMap == "JCHEM_POLAR_SURFACE_AREA":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["TPSA"]
                        elif descMap == "JCHEM_ATOM_COUNT":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["NumHeteroatoms"]
                        elif descMap == "ALOGPS_LOGP":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["MolLogP"]
                        elif descMap == "JCHEM_NUMBER_OF_RINGS":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["RingCount"]
                        elif descMap == "JCHEM_ACCEPTOR_COUNT":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["NumHAcceptors"]
                        elif descMap == "JCHEM_DONOR_COUNT":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["NumHDonors"]
                        elif descMap == "JCHEM_REFRACTIVITY":
                            self.dchemAdd["info"][id][descMap] = d2Ddesc["MolMR"]
                        else:
                            self.dchemAdd["info"][id][descMap] = "NA"



                    # SMILES 
                    self.dchemAdd["SMILESClass"][id]= {}
                    self.dchemAdd["SMILESClass"][id]["SMILES"] = smiles
                    self.dchemAdd["SMILESClass"][id]["inchikey"] = inch

                    if self.nameMap == "DrugMap":
                        self.dchemAdd["SMILESClass"][id]["DRUG_GROUPS"] = "add"
                    else:
                        self.dchemAdd["SMILESClass"][id]["GHS_category"] = "add"


                    for desc in self.ldescMap:
                        if desc in list(ddesc.keys()):
                            self.dchemAdd["info"][id][desc] = ddesc[desc]
                        elif desc in list(dinfo.keys()):
                            self.dchemAdd["info"][id][desc] = dinfo[desc]
                        else:
                            self.dchemAdd["info"][id][desc] = "NA"
                    
                    # neighbor
                    if lneighbor != [] and lneighbor != "Error":
                        lneighbormap = []
                        for n in lneighbor:
                            try:lneighbormap.append(self.map["inchikey"][n])
                            except: pass
                        self.dchemAdd["neighbor"][id] = lneighbormap

                    del llines[i]
                    imax = imax - 1
                    continue

                i = i + 1 


        if len(llines) == 1:
            self.inDB = 1
            return 

        else:
            filout = open(p1D2D, "w")
            filout.write("".join(llines))
            filout.close()

            # generate coords
            # remove coord in case of reload
            p1D2Dcoord = self.prout + "coord1D2D.csv"
            p3Dcoord = self.prout + "coord3D.csv"
            try: remove(p1D2Dcoord)
            except:pass
            try: remove(p3Dcoord)
            except:pass

            # run R script
            cmd = "%s/addonMap.R %s %s %s1D2Dscaling.csv %s3Dscaling.csv %sCP1D2D.csv %sCP3D.csv %s"%(path.abspath("./chemmaps/Rscripts"), p1D2D, p3D, self.pMap, self.pMap, self.pMap, self.pMap, self.prout)
            print(cmd)
            system(cmd)

            if path.exists(p1D2Dcoord) and path.exists(p3Dcoord):
                dcoords = loadMap1D2D3D(p1D2Dcoord, p3Dcoord)
                if dcoords == {}:
                    self.err = 1
                    self.inDB = 1
                    return "ERROR"
                ddesc1D2D = loadMatrixToDict(p1D2D)
                #desc3D = loadMatrixToDict(p3D)
                for ID in dcoords.keys():
                    self.dchemAdd["coord"][ID] = {}
                    self.dchemAdd["coord"][ID] = dcoords[ID]
                    cmdSQL = "UPDATE chemmap_coords_user SET dim1d2d = '{%s, %s}', dim3d = '{%s}', d3_cube='{%s, %s, %s}'  WHERE inchikey='%s' AND map_name = '%s';"%( dcoords[ID][0],dcoords[ID][1], dcoords[ID][2], dcoords[ID][0],dcoords[ID][1], dcoords[ID][2], ddesc1D2D[ID]["inchikey"],self.nameMap)
                    self.cDB.updateElement(cmdSQL)
                    

    def findneighbor(self, nbneighbor=20):

        if self.err == 1:
            return "ERROR"

        if self.inDB == 1:
            return

        if not "dchemAdd" in self.__dict__:
            print("ERROR -> generate first coordinate")
            self.err = 1
            return "ERROR"

        if not "neighbor" in list(self.dchemAdd.keys()):
            self.dchemAdd["neighbor"] = {}


        for ID in self.dchemAdd["coord"].keys():
            if ID in list(self.dchemAdd["neighbor"].keys()):
                continue
            else:
                
                # data search
                if self.nameMap == "DSSToxMap":
                    inch = self.dchemAdd["SMILESClass"][ID]["inchikey"]
                    cmdExtract = "Select dsstox_id from mvwchemmap_mapdsstox ORDER BY cube(d3_cube) <->  (select cube (d3_cube) from chemmap_coords_user \
                    where inchikey='%s' and map_name = 'DSSToxMap' limit (1)) limit (%s);"%(inch, 20)
                    lID = self.cDB.execCMD(cmdExtract)
                    if lID != "Error" or lID != []:
                        lID = [ID[0] for ID in lID]
                        self.dchemAdd["neighbor"][ID] = lID

                # compute on the fly
                else:
                    dcor1 = self.dchemAdd["coord"][ID]
                    ddist = {}
                    ddist[ID] = {}

                    for ID2 in self.map["coord"].keys():
                        dcor2 = self.map["coord"][ID2]
                        ddist[ID][ID2] = math.sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(dcor1, dcor2)]))

                    lID = [i[0] for i in sorted(ddist[ID].items(), key=lambda x: x[1])][:nbneighbor]
                    self.dchemAdd["neighbor"][ID] = lID

                # add in the user DB
                cmdSQL = "UPDATE chemmap_coords_user SET neighbors_dim3 = '{%s}' WHERE inchikey='%s' AND map_name = '%s';"%(",".join("\"" + ID + "\"" for ID in lID), self.dchemAdd["SMILESClass"][ID]["inchikey"], self.nameMap)
                self.cDB.updateElement(cmdSQL)





    def findinfoTable(self):

        if not "dchemAdd" in self.__dict__:
            print("ERROR -> generate first coordinate")
            return "ERROR"

        if self.inDB == 1:
            return

        # load Desc 2D
        d2Ddesc = loadMatrixInfoToDict(self.dchemAdd["p2D"])

        for IDadd in d2Ddesc.keys():
            if str(IDadd) in list(self.dchemAdd["info"].keys()):
                continue
            else:
                self.dchemAdd["info"][IDadd] = {}
                self.dchemAdd["SMILESClass"][IDadd] = {}

                #SMILES
                self.dchemAdd["SMILESClass"][IDadd]["SMILES"] = d2Ddesc[IDadd]["SMILES"]


                if self.nameMap == "DrugMap":
                    self.dchemAdd["SMILESClass"][IDadd]["DRUG_GROUPS"] = "add"
                    self.dchemAdd["SMILESClass"][IDadd]["inchikey"] = d2Ddesc[IDadd]["inchikey"]
                else:
                    self.dchemAdd["SMILESClass"][IDadd]["GHS_category"] = "add"
                    self.dchemAdd["SMILESClass"][IDadd]["inchikey"] = d2Ddesc[IDadd]["inchikey"]

                # info => fix prop with descriptor computed
                # add to DB HERE for info to put on map
                for desc in self.ldescMap:
                    if desc == "MOLECULAR_WEIGHT":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["MolWt"]
                    elif desc == "JCHEM_ROTATABLE_BOND_COUNT":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["NumRotatableBonds"]
                    elif desc == "JCHEM_POLAR_SURFACE_AREA":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["TPSA"]
                    elif desc == "JCHEM_ATOM_COUNT":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["NumHeteroatoms"]
                    elif desc == "ALOGPS_LOGP":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["MolLogP"]
                    elif desc == "JCHEM_NUMBER_OF_RINGS":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["RingCount"]
                    elif desc == "JCHEM_ACCEPTOR_COUNT":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["NumHAcceptors"]
                    elif desc == "JCHEM_DONOR_COUNT":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["NumHDonors"]
                    elif desc == "JCHEM_REFRACTIVITY":
                        self.dchemAdd["info"][IDadd][desc] = d2Ddesc[IDadd]["MolMR"]
                    else:
                        self.dchemAdd["info"][IDadd][desc] = "NA"

