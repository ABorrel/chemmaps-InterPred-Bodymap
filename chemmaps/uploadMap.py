from .DBrequest import DBrequest





def propToDict(ldbprop, ldesc):
    dout = {}
    for chem in ldbprop:
        DB_ID = str(chem[0])
        dout[DB_ID] = {}
        for desc in ldesc:
            dout[DB_ID][desc] = chem[1][ldesc.index(desc)]
    return dout


def coordToDict(lcoord):

    dout = {}
    for chem in lcoord:
        inchikey = str(chem[0])
        dout[inchikey] = [chem[1][0], chem[1][1], chem[2][0]]

    return dout

def NeighborToDict(lneighbors):

    dout = {}
    for chem in lneighbors:
        inchikey = str(chem[2])
        dout[inchikey] = chem[0]

    return dout



class loadingMap:
    def __init__(self, map, lprop):
        self.map = map
        self.DB = DBrequest()
        self.DB.verbose = 0
        self.lprop = lprop
        print("ssss",self.lprop)

        # load order prop
        if map == "DrugMap":
            lprop = self.DB.extractColoumn("drugbank_name_prop", "name")
            print(lprop)
            #self.lallProp = lprop
            self.lallProp = [prop [0] for prop in lprop]
            
            # to del after test 
            if lprop == []:
                self.lprop = self.lallProp

    def loadMap(self):
        dout = {}
        dout["coord"] = {}
        dout["info"] = {}
        dout["neighbor"] = {}
        dout["SMILESClass"] = {}
        #self.DB.verbose = 1
        lchem = self.DB.extractColoumn("drugbank_chemicals", "*")
        lcoord = self.DB.extractColoumn("drugbank_coords", "*")
        dcoord = coordToDict(lcoord)
        linfo = self.DB.extractColoumn("drugbank_prop", "*")
        dinfo = propToDict(linfo, self.lallProp)
        lneighbor = self.DB.extractColoumn("drugbank_neighbors", "*")
        dneighbor = NeighborToDict(lneighbor)


        for chem in lchem:
            DB_id = chem[0]
            SMILES = chem[1]
            inchikey = chem[3]
            QSAR = chem[4]
            if QSAR == False:
                continue
            # info with prop from DB
            dout["info"][DB_id] = {}
            for prop in self.lprop:
                dout["info"][DB_id][str(prop)] = dinfo[DB_id][str(prop)]

            # coords
            if not inchikey in list(dcoord.keys()):
                continue
            else:
                dout["coord"][DB_id] = {}
                dout["coord"][DB_id]["DIM1"] = dcoord[inchikey][0]
                dout["coord"][DB_id]["DIM2"] = dcoord[inchikey][1]
                dout["coord"][DB_id]["DIM3"] = dcoord[inchikey][2]

            # neighbor
            dout["neighbor"][DB_id] = {}
            dout["neighbor"][DB_id] = dneighbor[inchikey]

            # SMILES 
            dout["SMILESClass"][DB_id] = {}
            dout["SMILESClass"][DB_id]["SMILES"] = SMILES
            dout["SMILESClass"][DB_id]["DRUG_GROUPS"] = dinfo[DB_id]["DRUG_GROUPS"]
            dout["SMILESClass"][DB_id]["inchikey"] = inchikey


        return dout











#cDB = DBrequest.DBrequest()
#lprop = cDB.extractColoumn("drugbank_name_prop", "name")
#print(str(lprop[0][0]))
#a = [prop [0] for prop in lprop]
#print(a)
