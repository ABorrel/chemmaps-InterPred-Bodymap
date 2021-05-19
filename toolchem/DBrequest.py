from django_server import DB



class DBrequest:
    def __init__(self, verbose = 0):
        self.DB = DB.DB(verbose)

    def openConnection(self):
        self.DB.connOpen()

    def closeConnection(self):
        self.DB.connClose()

    def countChemicals(self):
        cmd = "SELECT COUNT(*) FROM %s.chemicals"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countCleanChemical(self):
        cmd = "SELECT COUNT(*) FROM %s.chemicals WHERE smiles_clean != 'NA'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countDescFullChemical(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description WHERE desc_3d != '{}'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countChemOnDSSTOXMap(self):
        cmd = "SELECT COUNT(*) FROM %s.mvwchemmap_mapdsstox"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]
    
    def countChemOnPFASMap(self):
        cmd = "SELECT COUNT(*) FROM %s.mvwchemmap_mappfas"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countChemOnDrugMap(self):
        cmd = "SELECT COUNT(*) FROM %s.mvwchemmap_mapdrugbank"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countChemOnTox21Map(self):
        cmd = "SELECT COUNT(*) FROM %s.mvwchemmap_maptox21"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countChemInterPred(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description WHERE interference_prediction != '{}'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]
    
    def countChemBodyMap(self):
        cmd = "SELECT COUNT(*) FROM %s.mvwchemmap_bodymapcase_name"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countChemUser(self):
        cmd = "SELECT COUNT(*) FROM %s.chemicals_user WHERE status='user'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countDescFullChemUser(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE status='user'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]
    
    def countChemUpdate(self):
        cmd = "SELECT COUNT(*) FROM %s.chemicals_user WHERE status='update'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countDescFullChemUpdate(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE status='update'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countChemCoordsUpdate(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE status='coords'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def runCMD(self, cmd):
        return self.DB.execCMD(cmd)

    def countUpdateDescChemicals(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE status='update' AND desc_1d2d is null AND desc_3d is null"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countUpdateOPERAChemicals(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE status='update' AND desc_opera is null"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countUpdateInterpredChemicals(self):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE status!='error' AND interference_prediction is null AND desc_opera is not null AND desc_1d2d is not null"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def countUpdateChemicals(self):
        cmd = "SELECT COUNT(*) FROM %s.chemicals_user WHERE status='update'"%(self.DB.schema)
        return self.DB.execCMD(cmd)[0][0]

    def checkIfChemicalIsReadyToPush(self, SMILES_in):
        cmd = "SELECT COUNT(*) FROM %s.chemicals_user WHERE status='update' and smiles_origin='%s'"%(self.DB.schema, SMILES_in)
        return self.DB.execCMD(cmd)[0][0]

    def extract1D2DDesc(self):
        cmd = "SELECT name FROM %s.chem_descriptor_1d2d_name ORDER BY id"%(self.DB.schema)
        return self.DB.execCMD(cmd)

    def extract3DDesc(self):
        cmd = "SELECT name FROM %s.chem_descriptor_3d_name ORDER BY id"%(self.DB.schema)
        return self.DB.execCMD(cmd)

    def extractOPERADesc(self):
        cmd = "SELECT name FROM %s.chem_descriptor_opera_name_new ORDER BY id"%(self.DB.schema)
        return self.DB.execCMD(cmd)

    def extractInterPredDesc(self):
        cmd = "SELECT name FROM %s.chem_interference_prediction_name ORDER BY id"%(self.DB.schema)
        return self.DB.execCMD(cmd)

    def countUpdateForCoordinates(self, name_map):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description_user WHERE map_name='%s' AND d3_cube is null AND status='update' OR status='check' AND map_name='%s' AND d3_cube is null"%(self.DB.schema, name_map, name_map)
        return self.DB.execCMD(cmd)
    
    def searchDTXID(self, dsstox_id):
        cmd = "SELECT COUNT(*) FROM %s.chemicals WHERE dsstox_id='%s'"%(self.DB.schema, dsstox_id)
        in_chemical = self.DB.execCMD(cmd)[0][0]
        if in_chemical == 0:
            cmd = "SELECT COUNT(*) FROM %s.chemicals_user WHERE dsstox_id='%s' AND status='update'"%(self.DB.schema, dsstox_id)
            return self.DB.execCMD(cmd)[0][0]
        else:
            return 1
    
    def searchInchikey(self, inchikey, map_chem):
        cmd = "SELECT COUNT(*) FROM %s.chemical_description WHERE inchikey='%s' AND map_name='%s'"%(self.DB.schema, inchikey, map_chem)
        return self.DB.execCMD(cmd)[0][0]
    
    def loadDescTables(self, name_table, map_name, condition):

        # load 1D2D
        d_desc1D2D = self.loadDesc1D2D(name_table, map_name, condition)
        if d_desc1D2D == {}:
            return [{}, {}]
        
        # load 3D
        d_desc3D = self.loadDesc3D(name_table, map_name, condition)

        return [d_desc1D2D, d_desc3D] 
    

    def loadDesc1D2D(self, name_table, map_name, condition):

        d_out = {}
        l_name_desc = self.extract1D2DDesc()

        cmd = "SELECT inchikey, desc_1d2d FROM %s.%s WHERE map_name = '%s' %s"%(self.DB.schema, name_table, map_name, condition)
        l_val = self.DB.execCMD(cmd)
        if l_val == []:
            return d_out

        for l_chemdesc in l_val:
            inch = l_chemdesc[0]
            l_desc = l_chemdesc[1]
            d_out[inch] = {}
            i = 0
            imax = len(l_desc)
            while i < imax:
                d_out[inch][l_name_desc[i][0]] = float(l_desc[i])
                i = i + 1
        return d_out
    

    def loadDesc3D(self, name_table, map_name, condition):

        d_out = {}
        l_name_desc = self.extract3DDesc()

        cmd = "SELECT inchikey, desc_3d FROM %s.%s WHERE map_name = '%s' %s"%(self.DB.schema, name_table, map_name, condition)
        l_val = self.DB.execCMD(cmd)

        for l_chemdesc in l_val:
            inch = l_chemdesc[0]
            l_desc = l_chemdesc[1]
            d_out[inch] = {}
            i = 0
            imax = len(l_desc)
            while i < imax:
                d_out[inch][l_name_desc[i][0]] = float(l_desc[i])
                i = i + 1
        return d_out