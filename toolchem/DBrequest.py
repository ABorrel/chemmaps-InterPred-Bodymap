from django_server import DB



class DBrequest:
    def __init__(self, verbose):
        self.DB = DB.DB(verbose)

    def countChemicals(self):
        cmd = "SELECT COUNT(*) FROM chemicals"
        return self.DB.execCMD(cmd)

    def countCleanChemical(self):
        cmd = "SELECT COUNT(*) FROM chemicals WHERE smiles_clean != 'NA'"
        return self.DB.execCMD(cmd)

    def countDescFullChemical(self):
        cmd = "SELECT COUNT(*) FROM chemical_description WHERE desc_3d != '{}'"
        return self.DB.execCMD(cmd)

    def countChemOnDSSTOXMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_mapdsstox"
        return self.DB.execCMD(cmd)
    
    def countChemOnPFASMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_mappfas"
        return self.DB.execCMD(cmd)

    def countChemOnDrugMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_mapdrugbank"
        return self.DB.execCMD(cmd)

    def countChemOnTox21Map(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_maptox21"
        return self.DB.execCMD(cmd)

    def countChemInterPred(self):
        cmd = "SELECT COUNT(*) FROM chemical_description WHERE interference_prediction != '{}'"
        return self.DB.execCMD(cmd)
    
    def countChemBodyMap(self):
        cmd = "SELECT COUNT(*) FROM mvwchemmap_bodymapcase_name"
        return self.DB.execCMD(cmd)