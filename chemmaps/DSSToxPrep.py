from . import toolbox
from .JSbuilder import DDESCDSSTOX
from .DBrequest import DBrequest
from .uploadMap import propToDict

from os import path
from math import sqrt
from copy import deepcopy
from re import search

from CompDesc import CompDesc

class DSSToxPrep:

    def __init__(self, input, ldesc, prout):

        self.input = input
        self.ldescMap = ldesc
        self.err = 0
        self.log = ""
        self.prout = prout
        self.cDB = DBrequest()
        self.cDB.verbose = 0

        lprop = self.cDB.extractColoumn("chem_descriptor_opera_name_new", "name")
        self.lallProp = [prop [0] for prop in lprop]

        lprop = self.cDB.extractColoumn("chem_toxexp_name", "name")
        self.lPropTox = [prop [0] for prop in lprop]

    def loadChemMapCenterChem(self, center_chem, center, nbChem):

        #center = 0
        #a = self.input # for control
        # control input type
        if not type(center_chem) == str:
            self.err = 1
            return

        # case of DTXID
        if search("DTXSID", center_chem):
            # check if include in the DB
            cmd_search = "SELECT dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1] FROM mvwchemmap_mapdsstox\
                WHERE dsstox_id = '%s'" %(center_chem)
            
            
            chem_center = self.cDB.execCMD(cmd_search)
            if chem_center == []:
                self.err = 1
                return 
            
            if center == 1:
                x = chem_center[0][3]
                y = chem_center[0][4]
                z = chem_center[0][5]
                inch = chem_center[0][2]
            

            cmdExtract = "SELECT dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value, prop_tox \
                FROM mvwchemmap_mapdsstox ORDER BY cube(d3_cube) <->  (SELECT cube(d3_cube) FROM mvwchemmap_mapdsstox \
                where dsstox_id='%s' limit (1)) limit (%s);"%(center_chem, nbChem)

        else:

            # need to check if it is in user table
            cmd_count = "SELECT COUNT(*) FROM chemical_description_user WHERE inchikey = '%s' AND map_name = 'dsstox'"%(center_chem)
            inUser = self.cDB.execCMD(cmd_count)[0][0]

            if inUser == 1:
                cmdExtract = "SELECT dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value, prop_tox \
                    FROM mvwchemmap_mapdsstox ORDER BY cube(d3_cube) <->  (SELECT cube (d3_cube) FROM chemical_description_user \
                    where inchikey='%s' AND map_name='dsstox' limit (1)) limit (%s);"%(center_chem, nbChem)

                if center == 1:
                    coords_center = self.cDB.execCMD("SELECT d3_cube FROM chemical_description_user WHERE inchikey = '%s' AND map_name = 'dsstox'"%(center_chem))
                    if coords_center == []:
                        self.err = 1
                        return
                    else:
                         coords_center = coords_center[0]
                    x = coords_center[0][0]
                    y = coords_center[0][1]
                    z = coords_center[0][2]

            else:
                # have to be a inch
                cmdExtract = "SELECT dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value, prop_tox \
                    FROM mvwchemmap_mapdsstox ORDER BY cube(d3_cube) <->  (SELECT cube (d3_cube) FROM mvwchemmap_mapdsstox \
                    where inchikey='%s' limit (1)) limit (%s);"%(center_chem, nbChem)

                if center == 1:
                    coords_center = self.cDB.execCMD("SELECT d3_cube FROM mvwchemmap_mapdsstox WHERE inchikey = '%s'"%(center_chem))
                    if coords_center == []:
                        self.err = 1
                        return
                    else:
                         coords_center = coords_center[0]
                    x = coords_center[0][0]
                    y = coords_center[0][1]
                    z = coords_center[0][2]

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

        i = 0
        imax = len(lchem)
        while i < imax:
            inch = lchem[i][2]
            smiles = lchem[i][1]
            dsstox = lchem[i][0]
            xadd = lchem[i][3]
            yadd = lchem[i][4]
            zadd = lchem[i][5]
            lneighbors = lchem[i][6]
            lprop = lchem[i][7]
            l_prop_tox = lchem[i][8]
            if l_prop_tox == None: l_prop_tox = ["NA" for toxname in self.lPropTox]
            

            if lprop == None or lneighbors == None:
                i = i + 1
                continue

            #coords
            if center == 1:
                self.coord[dsstox] = [float(xadd - x), float(yadd - y), float(zadd - z)]
            else:
                self.coord[dsstox] = [float(xadd), float(yadd), float(zadd)]
        
            # info

            self.dinfo[dsstox] = {}
            for descMap in self.ldescMap:
                if descMap in self.lallProp:
                    val = lprop[self.lallProp.index(descMap)]
                else:
                    val = l_prop_tox[self.lPropTox.index(descMap)]

                try: self.dinfo[dsstox][DDESCDSSTOX[descMap]] = round(float(val),1)
                except: self.dinfo[dsstox][DDESCDSSTOX[descMap]] = val

            #SMILES
            self.dSMILES[dsstox] = {}
            self.dSMILES[dsstox]["inchikey"] = inch
            self.dSMILES[dsstox]["SMILES"] = smiles
            self.dSMILES[dsstox]["GHS_category"] = str(l_prop_tox[self.lPropTox.index("GHS_category")])

            # neighbor
            self.dneighbor[dsstox] = lneighbors

            # dictionnary of comparison inch / dsstox
            dinch[inch] = dsstox
            i = i + 1 

        # Change name in the neighbor ===> need to do it with a sql request
        for chem_dtx in self.dneighbor.keys():
            inch = self.dSMILES[chem_dtx]["inchikey"]
            
            lneighbors = []
            for n in self.dneighbor[chem_dtx]:
                try: 
                    lneighbors.append(dinch[n])
                except: 
                    pass
            self.dneighbor[chem_dtx] = lneighbors

    def loadChemMapAddMap(self):
        
        nbChemAdd = len(list(self.input["coord"].keys()))
        nbChemInMap = 10000/nbChemAdd
        
        # case of only one chemical add => center view
        if nbChemAdd == 1:
            center_map = 1
        else:
            center_map =0


        for chem in self.input["SMILESClass"].keys():
            if chem in list(self.input["db_id"].keys()) and search("DTXSID", self.input["db_id"][chem]):
                dsstoxID = self.input["db_id"][chem]
                #ldsstoxAdd.append(dsstoxID)
                self.loadChemMapCenterChem(dsstoxID, center_map, nbChemInMap)
                
                try:self.coord[chem] = deepcopy(self.coord[dsstoxID])
                except:continue


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
                
                self.loadChemMapCenterChem(inch, center_map, nbChemInMap)

                if center_map == 1:
                    self.coord[chem] = [0,0,0]
                else:
                    self.coord[chem] = deepcopy(self.input["coord"][chem])
                self.dinfo[chem] = {}
                for desc in self.input["info"][chem]:
                    self.dinfo[chem][DDESCDSSTOX[desc]] = self.input["info"][chem][desc]
                self.dneighbor[chem] = deepcopy(self.input["neighbor"][chem])
                self.dSMILES[chem] = {}
                self.dSMILES[chem]["SMILES"] = deepcopy(self.input["SMILESClass"][chem]["SMILES"])
                self.dSMILES[chem]["inchikey"] = deepcopy(self.input["SMILESClass"][chem]["inchikey"])
                self.dSMILES[chem]["GHS_category"] = "add"


