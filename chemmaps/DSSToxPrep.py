from . import toolbox
from .JSbuilder import DDESCDSSTOX
from .DBrequest import DBrequest
from .uploadMap import propToDict

from os import path
from math import sqrt
from copy import deepcopy
from re import search

import sys
sys.path.insert(0, path.abspath('./../MD/'))
from MD import Chemical


class DSSToxPrep:
    def __init__(self, input, ldesc, prout):

        self.input = input
        self.ldescMap = ldesc
        self.err = 0
        self.log = ""
        self.prout = prout
        self.cDB = DBrequest()
        self.cDB.verbose = 0

        lprop = self.cDB.extractColoumn("chem_prop_dsstox_name", "name")
        self.lallProp = [prop [0] for prop in lprop]



    def loadChemMapCenterChem(self, center_chem, center, nbChem):

        #a = self.input # for control
        # control input type
        if not type(center_chem) == str:
            #print("Check input type")
            self.err = 1
            return


        # case of DTXID
        if search("DTXSID", center_chem):
            # check if include in the DB
            cmd_search = "Select dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1] from mvwchemmap_mapdsstox\
                where dsstox_id = '%s'" %(center_chem)
            
            chem_center = self.cDB.execCMD(cmd_search)
            if chem_center == []:
                self.err = 1
                return 
            x = chem_center[0][3]
            y = chem_center[0][4]
            z = chem_center[0][5]
            inch = chem_center[0][2]
            

            cmdExtract = "Select dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value \
                from mvwchemmap_mapdsstox ORDER BY cube(d3_cube) <->  (select cube (d3_cube) from mvwchemmap_mapdsstox \
                    where inchikey='%s' limit (1)) limit (%s);"%(inch, nbChem)


        else:
            # have to be a inch
            cmdExtract = "Select dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value \
                from mvwchemmap_mapdsstox ORDER BY cube(d3_cube) <->  (select cube (d3_cube) from chemmap_coords_user \
                    where inchikey='%s' and map_name = 'DSSToxMap' limit (1)) limit (%s);"%(center_chem, nbChem)


        lchem = self.cDB.execCMD(cmdExtract)

        # format for JS dictionnary
        if not "coord" in self.__dict__:
            self.coord = {}
        
        if not "dinfo" in self.__dict__:
            self.dinfo = {}
        
        if not "dSMILES" in self.__dict__:
            self.dSMILES = {}

        if not "dneighbor" in self.__dict__:
            self.dneighbor = {}

        dinch = {}

        for chem in lchem:
            inch = chem[2]
            smiles = chem[1]
            dsstox = chem[0]
            xadd = chem[3]
            yadd = chem[4]
            zadd = chem[5]
            lneighbors = chem[6]
            lprop = chem[7]
            
            if lprop == None or lneighbors == None:
                continue

            #coords
            if center == 1:
                self.coord[dsstox] = [float(xadd - x), float(yadd - y), float(zadd - z)]
            else:
                self.coord[dsstox] = [float(xadd), float(yadd), float(zadd)]
        
            # info
            self.dinfo[dsstox] = {}
            for descMap in self.ldescMap:
                try: self.dinfo[dsstox][DDESCDSSTOX[descMap]] = round(float(lprop[self.lallProp.index(descMap)]),1)
                except: self.dinfo[dsstox][DDESCDSSTOX[descMap]] = lprop[self.lallProp.index(descMap)]

            #SMILES
            self.dSMILES[dsstox] = {}
            self.dSMILES[dsstox]["inchikey"] = inch
            self.dSMILES[dsstox]["SMILES"] = smiles
            self.dSMILES[dsstox]["GHS_category"] = lprop[self.lallProp.index("GHS_category")]

            # neighbor
            self.dneighbor[dsstox] = lneighbors

            # dictionnary of comparison inch / dsstox
            dinch[inch] = dsstox

        # Change name in the neighbor
        for chem in dinch.values():
            lneighbors = []
            if not chem in list(self.dneighbor.keys()):
                continue
            #a = self.dneighbor[chem] # for inspect error
            for n in self.dneighbor[chem]:
                try: 
                    lneighbors.append(dinch[n])
                except: 
                    pass
            self.dneighbor[chem] = lneighbors




    def loadChemMapAddMap(self):
        
        nbChemAdd = len(list(self.input["coord"].keys()))
        nbChemInMap = 10000/nbChemAdd

        #ldsstoxAdd = []
        #s = self.input

        for chem in self.input["SMILESClass"].keys():
            if chem in list(self.input["db_id"].keys()) and search("DTXSID", self.input["db_id"][chem]):
                dsstoxID = self.input["db_id"][chem]
                #ldsstoxAdd.append(dsstoxID)
                self.loadChemMapCenterChem(dsstoxID, 0, nbChemInMap)
                
                self.coord[chem] = deepcopy(self.coord[dsstoxID])
                self.dinfo[chem] = {}
                for desc in self.input["info"][chem]:
                    self.dinfo[chem][DDESCDSSTOX[desc]] = self.input["info"][chem][desc]
                self.dneighbor[chem] = deepcopy(self.dneighbor[dsstoxID])
                self.dSMILES[chem] = {}
                self.dSMILES[chem]["SMILES"] = deepcopy(self.input["SMILESClass"][chem]["SMILES"])
                self.dSMILES[chem]["inchikey"] = deepcopy(self.input["SMILESClass"][chem]["inchikey"])
                self.dSMILES[chem]["GHS_category"] = "add"

                 # dell already in DB
                del self.coord[dsstoxID]
                del self.dinfo[dsstoxID]
                del self.dneighbor[dsstoxID]
                del self.dSMILES[dsstoxID]

            else:
                inch = self.input["SMILESClass"][chem]["inchikey"]
                self.loadChemMapCenterChem(inch, 0, nbChemInMap)

                self.coord[chem] = deepcopy(self.input["coord"][chem])
                self.dinfo[chem] = {}
                for desc in self.input["info"][chem]:
                    self.dinfo[chem][DDESCDSSTOX[desc]] = self.input["info"][chem][desc]
                self.dneighbor[chem] = deepcopy(self.input["neighbor"][chem])
                self.dSMILES[chem] = {}
                self.dSMILES[chem]["SMILES"] = deepcopy(self.input["SMILESClass"][chem]["SMILES"])
                self.dSMILES[chem]["inchikey"] = deepcopy(self.input["SMILESClass"][chem]["inchikey"])
                self.dSMILES[chem]["GHS_category"] = "add"


    def addChem(self):


        if not "dcenterChem" in self.__dict__ or not "dneighbor" in self.__dict__ or not "dinfo" in self.__dict__ or not "dSMILES" in self.__dict__:
            print("ERROR - no chem uploaded")
            return

        # load descriptor 2D
        p2Dadd = self.input + "2D.csv"
        d2Dadd = toolbox.loadMatrixToDict(p2Dadd)


        for chemIDadd in self.dcenterChem.keys():
            self.coord[chemIDadd] = [float(self.dcenterChem[chemIDadd]["DIM1"]), float(self.dcenterChem[chemIDadd]["DIM2"]), float(self.dcenterChem[chemIDadd]["DIM3"])]

            SMILES = d2Dadd[chemIDadd]["SMILES"]
            inchikey = toolbox.convertSMILEStoINCHIKEY(SMILES)

            self.dSMILES[chemIDadd] = {}
            self.dSMILES[chemIDadd]["SMILES"] = SMILES
            self.dSMILES[chemIDadd]["inchikey"] = inchikey
            self.dSMILES[chemIDadd]["GHS_category"] = "add"

            #info
            self.dinfo[chemIDadd] = {}
            for desc in self.ldesc:
                if desc in d2Dadd[chemIDadd].keys():
                    self.dinfo[chemIDadd][DDESCDSSTOX[desc]] = d2Dadd[chemIDadd][desc]
                else:
                    self.dinfo[chemIDadd][DDESCDSSTOX[desc]] = "NA"


            #neighbor
            ddist = {}
            for chemID in self.coord.keys():
                lcoordID = [float(self.coord[chemID][0]), float(self.coord[chemID][1]),
                            float(self.coord[chemID][2])]
                ddist[chemID] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(lcoordID, self.coord[chemIDadd])]))

            lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:20]
            #print(lID)
            self.dneighbor[chemIDadd] = lID

