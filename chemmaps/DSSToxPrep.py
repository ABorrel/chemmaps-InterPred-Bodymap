from . import toolbox
from .JSbuilder import DDESCDSSTOX
from .DBrequest import DBrequest
from .uploadMap import propToDict

from os import path
from math import sqrt
from copy import deepcopy

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

        lprop = self.cDB.extractColoumn("dsstox_name_prop", "name")
        self.lallProp = [prop [0] for prop in lprop]
        #self.pcentroid = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/MapCentroid.csv"
        #self.pmap = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/mapChem.csv"
        #self.prStaticMaps = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/"





    def loadChemMapbyID(self, dsstoxIn, center, nbChem):

        # control input type
        if not type(dsstoxIn) == str:
            print("Check input type")
            self.err = 1
            return


        # check if include in the DB
        cmd_search = "Select dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1] from mvwchemmap_mapdsstox\
            where dsstox_id = '%s'" %(dsstoxIn)
        
        chem_center = self.cDB.execCMD(cmd_search)
        print(chem_center)
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

            if lprop == None:
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
            if lneighbors != None:
                self.dneighbor[dsstox] = lneighbors
            else:
                self.dneighbor[dsstox] = []

            # dictionnary of comparison inch / dsstox
            dinch[inch] = dsstox

        # Change name in the neighbor
        for chem in self.dneighbor.keys():
            lneighbors = []
            for n in self.dneighbor[chem]:
                try: lneighbors.append(dinch[n])
                except: pass
            self.dneighbor[chem] = lneighbors

    def loadChemMapAddMap(self):
        
        nbChemAdd = len(list(self.input["coord"].keys()))
        nbChemInMap = 10000/nbChemAdd
        for chem in self.input["SMILESClass"].keys():
            inch = self.input["SMILESClass"][chem]["inchikey"]
            cmdSQL = "Select dsstox_id from mvwchemmap_mapdsstox where inchikey='%s'"%(inch)
            dsstox = self.cDB.execCMD(cmdSQL)
            if dsstox != []:
                dsstox = dsstox[0][0]
                self.loadChemMapbyID(dsstox, 0, nbChemInMap)

                # update with added chemical
                self.coord[chem] = self.coord[dsstox]
                self.dinfo[chem] = self.dinfo[dsstox]
                self.dneighbor[chem] = self.dneighbor[dsstox]
                self.dSMILES[chem] = self.dSMILES[dsstox]
                self.dSMILES[chem]["GHS_category"] = "add"
        


    #def loadChemMapbySession(self):

    #    if not path.exists(self.input):
    #        print("Check input type")
    #        return

        # load coord
    #    lIDmap = []
    #    dcentroid = toolbox.loadMatrixToDict(self.pcentroid)
    #    dcoordUpload = toolbox.loadMap1D2D3D(self.input)
    #    for chemID in dcoordUpload.keys():
    #        dcoorCenter = [float(dcoordUpload[chemID]["DIM1"]), float(dcoordUpload[chemID]["DIM2"]), float(dcoordUpload[chemID]["DIM3"])]

    #        ddist = {}
    #        for map in dcentroid.keys():
    #            dcoordCentroid = [float(dcentroid[map]["X"]), float(dcentroid[map]["Y"]), float(dcentroid[map]["Z"])]
    #            ddist[map] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(dcoorCenter, dcoordCentroid)]))

    #        lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:3]
            #print(lID)
    #        for ID in lID:
    #            if not ID in lIDmap:
    #                lIDmap.append(ID)


    #    dchemMap = {}
    #    for IDmap in lIDmap:
    #        dchemMap.update(toolbox.loadMap1D2D3D(self.prStaticMaps + str(IDmap)))


    #    self.lmap = lIDmap
    #    self.dchemMap = dchemMap
    #    self.dcenterChem = dcoordUpload


    #def refineChemMapOnSeveralChem(self, nbchemical):

    #    if not "dchemMap" in self.__dict__:
    #        print("Load initial Map")
    #        return

    #    nbchembycenter = int(nbchemical / len(self.dcenterChem.keys()))
    #    dout = {}

    #    for chemid in self.dcenterChem:
    #        lcoordcenter = [float(self.dcenterChem[chemid]["DIM1"]), float(self.dcenterChem[chemid]["DIM2"]), float(self.dcenterChem[chemid]["DIM3"])]

    #        ddist = {}
    #        for chemID in self.dchemMap.keys():
    #            lcoordID = [float(self.dchemMap[chemID]["DIM1"]), float(self.dchemMap[chemID]["DIM2"]), float(self.dchemMap[chemID]["DIM3"])]
    #            ddist[chemID] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(lcoordID, lcoordcenter)]))
    #        lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:nbchembycenter]

    #        for ID in lID:
    #            dout[ID] = [float(deepcopy(self.dchemMap[ID]["DIM1"])), float(deepcopy(self.dchemMap[ID]["DIM2"])), float(deepcopy(self.dchemMap[ID]["DIM3"]))]
    #            del self.dchemMap[ID]


    #    self.coord = dout



    #def refineChemMap(self, center, nbchemical):

    #    if not "dchemMap" in self.__dict__:
    #        print("Load initial Map")
    #        self.err = 1
    #        return

    #    lcoordcenter = [self.dchemMap[self.centerChem][0], self.dchemMap[self.centerChem][1], self.dchemMap[self.centerChem][2]]

    #    ddist = {}
    #    for chemID in self.dchemMap.keys():
    #        ddist[chemID] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(self.dchemMap[chemID], lcoordcenter)]))


    #    lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:nbchemical]


    #    dout = {}
    #    for ID in lID:
    #        if center == 1:
    #            dout[ID] = [self.dchemMap[ID][0] - self.dchemMap[self.centerChem][0], self.dchemMap[ID][1] - self.dchemMap[self.centerChem][1], self.dchemMap[ID][2] - self.dchemMap[self.centerChem][2]]
    #        else:
    #            dout[ID] = [float(self.dchemMap[ID][0]), float(self.dchemMap[ID][1]), float(self.dchemMap[ID][2])]
    #    self.coord = dout




    #def loadInfo(self, ldesc):

    #    self.ldesc = ldesc

    #    dinfoout = {}
    #    dSMILESout = {}

    #    for IDmap in self.lmap:
    #        pinfoMap = self.prStaticMaps + str(IDmap) + "_TableProp.csv"
    #        dinfoMap = toolbox.loadMatrixInfoToDict(pinfoMap)


    #        for IDchem in self.coord.keys():
    #            if IDchem in dinfoMap.keys():
    #                dinfoout[IDchem] = {}
    #                dSMILESout[IDchem] = {}
    #                for desc in ldesc:
    #                    dinfoout[IDchem][DDESCDSSTOX[desc]] = dinfoMap[IDchem][desc]
    #                    dSMILESout[IDchem]["inchikey"] = dinfoMap[IDchem]["inchikey"]
    #                    dSMILESout[IDchem]["GHS_category"] = dinfoMap[IDchem]["GHS_category"]
    #                    dSMILESout[IDchem]["SMILES"] = dinfoMap[IDchem]["SMILES"]


    #    self.dinfo = dinfoout
    #    self.dSMILES = dSMILESout


    #def loadNeighbor(self):

    #    dneighborout = {}

    #    for IDmap in self.lmap:
    #        pneighborMap = self.prStaticMaps + str(IDmap) + "_TableNeighbors.csv"
    #        dneighborMap = toolbox.loadMatrixToDict(pneighborMap)

    #        for IDchem in self.coord.keys():
    #            if IDchem in dneighborMap.keys():
    #                dneighborout[IDchem] = dneighborMap[IDchem]["Neighbors"].split(" ")

    #    self.dneighbor = dneighborout



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

