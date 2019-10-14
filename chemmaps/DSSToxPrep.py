from . import toolbox
from .JSbuilder import DDESCDSSTOX
from .DBrequest import DBrequest

from os import path
from math import sqrt
from copy import deepcopy

import sys
sys.path.insert(0, path.abspath('./../MD/'))
from MD import Chemical


class DSSToxPrep:
    def __init__(self, input, prout):

        self.input = input
        self.err = 0
        self.log = ""
        self.prout = prout
        self.cDB = DBrequest()
        self.cDB.verbose = 0
        #self.pcentroid = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/MapCentroid.csv"
        #self.pmap = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/mapChem.csv"
        #self.prStaticMaps = "/home/aborrel/django_server/django_server/chemmaps/static/chemmaps/map/DSSToxMap/"


    def loadChemMapbyID(self):

        # control input type
        if not type(self.input) == str:
            print("Check input type")
            self.err = 1
            return

        dout = {}

        # prep chem -> transform in inchikey
        cchem = Chemical.Chemical(self.input, self.prout)
        cchem.prepChem()
        inch = cchem.generateInchiKey()
        self.centerChem = inch

        # find inch in the table
        # extract 10,000 close chemical

        lcoords = self.cDB.extractColoumn("dsstox_coords", "dim1d2d[1],dim1d2d[2],dim3d[1]", "WHERE inchikey='%s'"%(inch))
        dout[inch] = lcoords[0]
        x = dout[inch][0]
        y = dout[inch][1]
        z = dout[inch][2]
        
        if x < 3 and x >- 3 or y < 3 and y >- 3 or z < 3 and z >- 3:
            rang_val = 0.025
        else:
            rang_val = 1
        
        sum_chem = 0
        while sum_chem < 10000:
            cmdSQLCount = "select count(*) from chemmap_coords where map_name = 'dsstox' and dim1d2d[1] < %s \
                            + (select dim1d2d[1] from dsstox_coords where inchikey = '%s') \
                            and dim1d2d[1] >  (select dim1d2d[1] from dsstox_coords where inchikey = '%s') - %s \
                            UNION \
                            select count(*) from chemmap_coords where  map_name= 'dsstox' and dim1d2d[2] < %s + \
                            (select dim1d2d[2] from dsstox_coords where inchikey = '%s') \
                            and dim1d2d[2] >  (select dim1d2d[2] from dsstox_coords where inchikey = '%s') - %s \
                            UNION \
                            select count(*) from chemmap_coords where  map_name= 'dsstox' and dim3d[1] < %s + \
                            (select dim3d[1] from dsstox_coords where inchikey = '%s') \
                            and dim3d[1] >  (select dim3d[1] from dsstox_coords where inchikey = '%s') - %s" %(rang_val, inch, inch, rang_val, rang_val, inch, 
                            inch, rang_val, rang_val, inch, inch, rang_val)
            self.cDB.verbose = 1
            lcount = self.cDB.execCMD(cmdSQLCount)
            sum_chem = lcount[0][0] + lcount[1][0] + lcount[2][0]
            print(sum_chem)
            rang_val = rang_val + rang_val
        #print(sum_chem)

        dddd
        

        # load chem for map
        dchemMap = {}
        x = mapx - 1
        while x <= mapx +1:
            lchemInMap = self.cDB.extractColoumn("dsstox_coords", "inchikey, dim1d2d[1],dim1d2d[2],dim3d[1]", "WHERE mapx=%s"%(x))
            for chemInMap in lchemInMap:
                dchemMap[chemInMap[0]] = [chemInMap[1], chemInMap[2], chemInMap[3]] 
                #lchemMap.append(chemInMap[0])
            x = x +1

        y = mapy - 1
        while y <= mapy + 1:
            lchemInMap = self.cDB.extractColoumn("dsstox_coords", "inchikey, dim1d2d[1],dim1d2d[2],dim3d[1]", "WHERE mapy=%s"%(y))
            for chemInMap in lchemInMap:
                dchemMap[chemInMap[0]] = [chemInMap[1], chemInMap[2], chemInMap[3]] 
            y = y + 1
        
        z = mapz - 1
        while z <= mapz + 1:
            lchemInMap = self.cDB.extractColoumn("dsstox_coords", "inchikey, dim1d2d[1],dim1d2d[2],dim3d[1]", "WHERE mapz=%s"%(z))
            for chemInMap in lchemInMap:
                dchemMap[chemInMap[0]] = [chemInMap[1], chemInMap[2], chemInMap[3]] 
            z = z + 1

        self.dchemMap = dchemMap
        #self.centerChem = [float(dchemMap[self.input]["DIM1"]), float(dchemMap[self.input]["DIM2"]), float(dchemMap[self.input]["DIM3"])]


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
            self.err = 1
            return

        lcoordcenter = [self.dchemMap[self.centerChem][0], self.dchemMap[self.centerChem][1], self.dchemMap[self.centerChem][2]]

        ddist = {}
        for chemID in self.dchemMap.keys():
            ddist[chemID] = sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(self.dchemMap[chemID], lcoordcenter)]))


        lID = [i[0] for i in sorted(ddist.items(), key=lambda x: x[1])][:nbchemical]


        dout = {}
        for ID in lID:
            if center == 1:
                dout[ID] = [self.dchemMap[ID][0] - self.dchemMap[self.centerChem][0], self.dchemMap[ID][1] - self.dchemMap[self.centerChem][1], self.dchemMap[ID][2] - self.dchemMap[self.centerChem][2]]
            else:
                dout[ID] = [float(self.dchemMap[ID][0]), float(self.dchemMap[ID][1]), float(self.dchemMap[ID][2])]
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

