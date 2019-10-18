from django.contrib.staticfiles import finders
from os import path


from .toolbox import loadMatrixToDict, loadToList, openGeneExp



class mapChem :
    def __init__(self, CASin, foldExp):
        self.CASin = CASin
        self.foldExp = foldExp
        self.pToxCast = finders.find("bodymap/mapping/chemicals/%s.csv"%(CASin))
        self.pmapBody = finders.find("bodymap/mapping/preMapping.csv")


    def mapChemToBody(self):

        dAC50 = loadMatrixToDict(self.pToxCast)
        prmap = finders.find("bodymap/mapping/")
        
        if not self.CASin in list(dAC50.keys()):
            return "Error"
        else:

            dout = {}
            dgene = {}
            dresultAssays = dAC50[self.CASin]
            del dresultAssays["CASRN"]
            lassays_mapped = loadToList(self.pmapBody)

            for assays in dresultAssays.keys():
                if dresultAssays[assays] != "NA" and dresultAssays[assays] != "1000000":
                    for assay_mapped in lassays_mapped:
                        if assay_mapped['Assays'] == assays:
                            if assay_mapped["type mapping"] != "gene target":
                                organ = assay_mapped["organ"]
                                system = assay_mapped["system"]
                                gene = assay_mapped["gene"]
                                
                                if not assays in list(dout.keys()):
                                    dout[assays] = {}
                                
                                if not system in list(dout[assays].keys()):
                                    dout[assays][system] = {}

                                if not organ in list(dout[assays][system].keys()):
                                    dout[assays][system][organ] = {}
                                    dout[assays][system][organ]["AC50"] = 100000.0
                                    dout[assays][system][organ]["gene"] = []
                                
                                if dout[assays][system][organ]["AC50"] > float(dresultAssays[assays]):
                                    dout[assays][system][organ]["AC50"] = float(dresultAssays[assays])
                                
                                if not gene in dout[assays][system][organ]["gene"]:
                                    dout[assays][system][organ]["gene"].append(gene)
                        
                            else:
                                gene = assay_mapped["gene"]
                                if gene in list(dgene.keys()):
                                    dgenetemp = dgene[gene]
                                else:
                                    pgene = prmap + "/geneExp/" + str(gene) + ".csv" 
                                    if not path.exists(pgene):
                                        continue
                                    else:
                                        dgenetemp = openGeneExp(pgene)
                                        dgene[gene] = dgenetemp

                                if not assays in list(dout.keys()):
                                        dout[assays] = {}

                                for system in dgenetemp.keys():
                                    if not system in list(dout[assays].keys()):
                                        dout[assays][system] = {}
                                    for organ in dgenetemp[system].keys():
                                    
                                        if dgenetemp[system][organ]["control"] == 0.0: 
                                            exp = dgenetemp[system][organ]["exp"]
                                        else:
                                            exp = dgenetemp[system][organ]["exp"] / dgenetemp[system][organ]["control"]
                                    
                                        if exp >= self.foldExp:
                                            if not organ in list(dout[assays][system].keys()):
                                                dout[assays][system][organ] = {}
                                                dout[assays][system][organ]["AC50"] = 100000.0
                                                dout[assays][system][organ]["gene"] = []

                                            if dout[assays][system][organ]["AC50"] > float(dresultAssays[assays]):
                                                dout[assays][system][organ]["AC50"] = float(dresultAssays[assays])
                                        
                                            if not gene in dout[assays][system][organ]["gene"]:
                                                dout[assays][system][organ]["gene"].append(gene)

            return dout

