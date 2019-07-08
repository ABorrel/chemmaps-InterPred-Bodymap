from . import toolbox
from .JSbuilder import DDESCDSSTOX

from os import path
from math import sqrt
from copy import deepcopy


class DSSToxPrep:

    def __init__(self, input):

        self.input = input
        self.err = 0
        self.log = ""
        self.pcentroid = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/MapCentroid.csv"
        self.pmap = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/mapChem.csv"
        self.prStaticMaps = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/"


    def loadChemMapbyID(self):

        # control input type
        if not type(self.input) == str:
            print("Check input type")
            self.err = 1
            return


        fmap = open(self.pmap, "r")
        l = fmap.readline()

        map = 0
        while l != "":

            ll = l.strip().split("\t")
            if ll[0] == self.input:
                map = int(ll[1])
                break
            l = fmap.readline()

        fmap.close()

        if map == 0:
            self.err = 1
            return



        else:
            dchemMap = {}
            dchemMap.update(toolbox.loadMap1D2D3D(self.prStaticMaps + str(map)))

            lIDmap = [map]
            # load map -1 and map +1
            if path.exists(self.prStaticMaps + str(map - 1) + "_map1D2D.csv"):
                dchemMap.update(toolbox.loadMap1D2D3D(self.prStaticMaps + str(map-1)))
                lIDmap.append(map-1)

            if path.exists(self.prStaticMaps + str(map + 1) + "_map1D2D.csv"):
                dchemMap.update(toolbox.loadMap1D2D3D(self.prStaticMaps + str(map + 1)))
                lIDmap.append(map+1)

            self.dchemMap = dchemMap
            self.lmap = lIDmap
            self.centerChem = [float(dchemMap[self.input]["DIM1"]), float(dchemMap[self.input]["DIM2"]), float(dchemMap[self.input]["DIM3"])]


    def loadChemMapbySession(self):

        if not path.exists(self.input):
            print("Check input type")
            return

        # load coord
        lIDmap = []
        dcentroid = toolbox.loadMatrixToDict(self.pcentroid)
        dcoordUpload = toolbox.loadMap1D2D3D(self.input)
        for chemID in dcoordUpload.keys():
            dcoorCenter = [float(dcoordUpload[chemID]["DIM1"]), float(dcoordUpload[chemID]["DIM2"]), float(dcoordUpload[chemID]["DIM3"])]

            ddist = {}
            for map in dcentroid.keys():
                dcoordCentroid = [float(dcentroid[map]["X"]), float(dcentroid[map]["Y"]), float(dcentroid[map]["Z"])]
                ddist[map] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(dcoorCenter, dcoordCentroid)]))

            lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:3]
            #print(lID)
            for ID in lID:
                if not ID in lIDmap:
                    lIDmap.append(ID)


        dchemMap = {}
        for IDmap in lIDmap:
            dchemMap.update(toolbox.loadMap1D2D3D(self.prStaticMaps + str(IDmap)))


        self.lmap = lIDmap
        self.dchemMap = dchemMap
        self.dcenterChem = dcoordUpload


    def refineChemMapOnSeveralChem(self, nbchemical):

        if not "dchemMap" in self.__dict__:
            print("Load initial Map")
            return

        nbchembycenter = int(nbchemical / len(self.dcenterChem.keys()))
        dout = {}

        for chemid in self.dcenterChem:
            lcoordcenter = [float(self.dcenterChem[chemid]["DIM1"]), float(self.dcenterChem[chemid]["DIM2"]), float(self.dcenterChem[chemid]["DIM3"])]

            ddist = {}
            for chemID in self.dchemMap.keys():
                lcoordID = [float(self.dchemMap[chemID]["DIM1"]), float(self.dchemMap[chemID]["DIM2"]), float(self.dchemMap[chemID]["DIM3"])]
                ddist[chemID] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(lcoordID, lcoordcenter)]))
            lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:nbchembycenter]

            for ID in lID:
                dout[ID] = [float(deepcopy(self.dchemMap[ID]["DIM1"])), float(deepcopy(self.dchemMap[ID]["DIM2"])), float(deepcopy(self.dchemMap[ID]["DIM3"]))]
                del self.dchemMap[ID]


        self.coord = dout



    def refineChemMap(self, center, nbchemical):

        if not "dchemMap" in self.__dict__:
            print("Load initial Map")
            return

        lcoordcenter = [self.centerChem[0], self.centerChem[1], self.centerChem[2]]

        ddist = {}
        for chemID in self.dchemMap.keys():
            lcoordID = [float(self.dchemMap[chemID]["DIM1"]), float(self.dchemMap[chemID]["DIM2"]), float(self.dchemMap[chemID]["DIM3"])]
            ddist[chemID] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(lcoordID, lcoordcenter)]))


        lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:nbchemical]


        dout = {}
        for ID in lID:
            if center == 1:
                dout[ID] = [float(self.dchemMap[ID]["DIM1"]) - self.centerChem[0], float(self.dchemMap[ID]["DIM2"]) - self.centerChem[1], float(self.dchemMap[ID]["DIM3"])- self.centerChem[2]]
            else:
                dout[ID] = [float(self.dchemMap[ID]["DIM1"]), float(self.dchemMap[ID]["DIM2"]), float(self.dchemMap[ID]["DIM3"])]

        self.coord = dout


    def loadInfo(self, ldesc):

        self.ldesc = ldesc

        dinfoout = {}
        dSMILESout = {}

        for IDmap in self.lmap:
            pinfoMap = self.prStaticMaps + str(IDmap) + "_TableProp.csv"
            dinfoMap = toolbox.loadMatrixInfoToDict(pinfoMap)


            for IDchem in self.coord.keys():
                if IDchem in dinfoMap.keys():
                    dinfoout[IDchem] = {}
                    dSMILESout[IDchem] = {}
                    for desc in ldesc:
                        dinfoout[IDchem][DDESCDSSTOX[desc]] = dinfoMap[IDchem][desc]
                        dSMILESout[IDchem]["inchikey"] = dinfoMap[IDchem]["inchikey"]
                        dSMILESout[IDchem]["GHS_category"] = dinfoMap[IDchem]["GHS_category"]
                        dSMILESout[IDchem]["SMILES"] = dinfoMap[IDchem]["SMILES"]


        self.dinfo = dinfoout
        self.dSMILES = dSMILESout


    def loadNeighbor(self):

        dneighborout = {}

        for IDmap in self.lmap:
            pneighborMap = self.prStaticMaps + str(IDmap) + "_TableNeighbors.csv"
            dneighborMap = toolbox.loadMatrixToDict(pneighborMap)

            for IDchem in self.coord.keys():
                if IDchem in dneighborMap.keys():
                    dneighborout[IDchem] = dneighborMap[IDchem]["Neighbors"].split(" ")

        self.dneighbor = dneighborout



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

