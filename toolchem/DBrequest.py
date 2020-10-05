from django_server import DB



class DBrequest:
    def __init__(self, verbose):
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