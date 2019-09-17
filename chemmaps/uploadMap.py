from .DBrequest import DBrequest



class loadingMap:
    def __init__(self, map, lprop):
        self.map = map
        self.DB = DBrequest()
        self.DB.verbose = 0
        self.lprop = lprop

        # load order prop
        if map == "DrugMap":
            lprop = self.DB.extractColoumn("drugbank_name_prop", "name")
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

        lchem = self.DB.extractColoumn("drugbank_chemicals", "*")
        for chem in lchem:
            DB_id = chem[0]
            SMILES = chem[1]
            inchikey = chem[3]
            QSAR = chem[4]
            if QSAR == False:
                continue
            # info with prop from DB
            lval = self.DB.execCMD("SELECT prop_value FROM drugbank_prop WHERE drugbank_id='%s' ;"%(DB_id))
            dout["info"][DB_id] = {}
            for prop in self.lprop:
                dout["info"][DB_id][str(prop)] = lval[0][0][self.lallProp.index(prop)]
            
            # coords
            lcoord = self.DB.execCMD("SELECT * FROM drugbank_coords WHERE inchikey='%s' ;"%(inchikey))
            #print(lcoord)
            if lcoord == [] or lcoord == "Error":
                continue
            dout["coord"][DB_id] = {}
            dout["coord"][DB_id]["DIM1"] = lcoord[0][1][0]
            dout["coord"][DB_id]["DIM2"] = lcoord[0][1][1]
            dout["coord"][DB_id]["DIM3"] = lcoord[0][2][0]

            # neighbor
            dout["neighbor"][DB_id] = {}
            lenighbor = self.DB.execCMD("SELECT neighbors_dim3 FROM drugbank_neighbors WHERE inchikey='%s' ;"%(inchikey))
            dout["neighbor"][DB_id] = lenighbor

            # SMILES 
            dout["SMILESClass"][DB_id] = SMILES

        return dout


#cDB = DBrequest.DBrequest()
#lprop = cDB.extractColoumn("drugbank_name_prop", "name")
#print(str(lprop[0][0]))
#a = [prop [0] for prop in lprop]
#print(a)
