from django_server import DB



class DBrequest:
    def __init__(self, verbose = 0):
        self.DB = DB.DB(verbose)

    def openConnection(self):
        self.DB.connOpen()

    def closeConnection(self):
        self.DB.connClose()

    def countChemicals(self):
        cmd = "SELECT COUNT(*) FROM chemicals"
        return self.DB.execCMD(cmd)[0][0]

    def countCleanChemical(self):
        cmd = "SELECT COUNT(*) FROM chemicals WHERE smiles_clean != 'NA'"
        return self.DB.execCMD(cmd)[0][0]

    def countDescFullChemical(self):
        cmd = "SELECT COUNT(*) FROM chemical_description WHERE desc_3d != '{}'"
        return self.DB.execCMD(cmd)[0][0]

    def countChemOnDSSTOXMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_mapdsstox"
        return self.DB.execCMD(cmd)[0][0]
    
    def countChemOnPFASMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_mappfas"
        return self.DB.execCMD(cmd)[0][0]

    def countChemOnDrugMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_mapdrugbank"
        return self.DB.execCMD(cmd)[0][0]

    def countChemOnTox21Map(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_maptox21"
        return self.DB.execCMD(cmd)[0][0]

    def countChemInterPred(self):
        cmd = "SELECT COUNT(*) FROM chemical_description WHERE interference_prediction != '{}'"
        return self.DB.execCMD(cmd)[0][0]
    
    def countChemBodyMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_bodymapcase_name"
        return self.DB.execCMD(cmd)[0][0]

    def countChemUser(self):
        cmd = "SELECT COUNT(*) FROM chemicals_user WHERE status='user'"
        return self.DB.execCMD(cmd)[0][0]

    def countDescFullChemUser(self):
        cmd = "SELECT COUNT(*) FROM chemical_description_user WHERE status='user'"
        return self.DB.execCMD(cmd)[0][0]
    
    def countChemUpdate(self):
        cmd = "SELECT COUNT(*) FROM chemicals_user WHERE status='update'"
        return self.DB.execCMD(cmd)[0][0]

    def countDescFullChemUpdate(self):
        cmd = "SELECT COUNT(*) FROM chemical_description_user WHERE status='update'"
        return self.DB.execCMD(cmd)[0][0]

    def runCMD(self, cmd):
        return self.DB.execCMD(cmd)

    def countUpdateDescChemicals(self):
        cmd = "SELECT COUNT(*) FROM chemical_description_user WHERE status='update' AND desc_1d2d is null AND desc_3d is null"
        return self.DB.execCMD(cmd)[0][0]

    def countUpdateOPERAChemicals(self):
        cmd = "SELECT COUNT(*) FROM chemical_description_user WHERE status='update' AND desc_opera is null"
        return self.DB.execCMD(cmd)[0][0]

    def countUpdateInterpredChemicals(self):
        cmd = "SELECT COUNT(*) FROM chemical_description_user WHERE status='update' AND interference_prediction is null AND desc_opera is not null AND desc_1d2d is not null"
        return self.DB.execCMD(cmd)[0][0]

    def countUpdateChemicals(self):
        cmd = "SELECT COUNT(*) FROM chemicals_user WHERE status='update'"
        return self.DB.execCMD(cmd)[0][0]

    def checkIfChemicalIsReadyToPush(self, SMILES_in):
        cmd = "SELECT COUNT(*) FROM chemicals_user WHERE status='update' and smiles_origin='%s'"%(SMILES_in)
        return self.DB.execCMD(cmd)[0][0]

    def extract1D2DDesc(self):
        cmd = "SELECT name FROM chem_descriptor_1d2d_name ORDER BY id"
        return self.DB.execCMD(cmd)

    def extract3DDesc(self):
        cmd = "SELECT name FROM chem_descriptor_3d_name ORDER BY id"
        return self.DB.execCMD(cmd)

    def extractOPERADesc(self):
        cmd = "SELECT name FROM chem_descriptor_opera_name ORDER BY id"
        return self.DB.execCMD(cmd)

    def extractInterPredDesc(self):
        cmd = "SELECT name FROM chem_interference_prediction_name ORDER BY id"
        return self.DB.execCMD(cmd)

    def countUpdateForCoordinates(self, name_map):
        cmd = "SELECT COUNT(*) FROM chemical_description_user WHERE status='update' AND map_name='%s'"%(name_map)
        return self.DB.execCMD(cmd)