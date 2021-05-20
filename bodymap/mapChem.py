from django.contrib.staticfiles import finders
from os import path
from .toolbox import loadMatrixToDict, loadToList, openGeneExp
from .DBrequest import DBrequest




class mapChem :
    def __init__(self, CASin):
        self.CASin = CASin
        self.cDB = DBrequest()
        self.cDB.verbose = 0
           
    def loadFromDB(self, tableAssayMap, tableAC50, tableGene):

        dac50 = self.cDB.execCMD("SELECT assay, ac50 FROM %s WHERE casn='%s'"%(tableAC50, self.CASin))
        self.dac50 = dac50

        # load premap
        lassayMapped = self.cDB.execCMD("SELECT assay, gene, type_map, organ, system FROM %s"%(tableAssayMap))
        dassayMapped = {}
        for assayMapped in lassayMapped:
            assay = assayMapped[0]
            gene = assayMapped[1]
            typeMap =  assayMapped[2]
            organ = assayMapped[3]
            system = assayMapped[4]
            dassayMapped[assay] = {}
            dassayMapped[assay]["type"] = typeMap
            dassayMapped[assay]["gene"] = gene
            dassayMapped[assay]["organ"] = organ
            dassayMapped[assay]["system"] = system
        
        self.dassayMapped = dassayMapped
        self.tableGene = tableGene

    def mapChemToBody(self, expControl):

        if expControl == "organ":
            dExp = loadMatrixToDict("./static/bodymap/mapping/controlExpByOrgan.txt")

        dvia = {"Immune System": "Immune System", "Digestive System": "Liver", "Respiratory System": "Lung", "Digestive System":"Stomach"}
        dout = {}
        for lassaysAc50 in self.dac50:
            assay = lassaysAc50[0]
            ac50 = lassaysAc50[1]
            if not assay in list(self.dassayMapped.keys()):
                continue
            

            typeMap = self.dassayMapped[assay]["type"]
            if typeMap == "tissue":
                system = self.dassayMapped[assay]["system"]
                organ = self.dassayMapped[assay]["organ"]
                gene = "NA"
                
                if not assay in list(dout.keys()):
                    dout[assay] = {}

                if not system in list(dout[assay].keys()):
                    dout[assay][system] = {}

                if not organ in list(dout[assay][system].keys()):
                    dout[assay][system][organ] = {}
                    dout[assay][system][organ]["AC50"] = 100000.0
                    dout[assay][system][organ]["gene"] = []

                if dout[assay][system][organ]["AC50"] > float(ac50):
                    dout[assay][system][organ]["AC50"] = float(ac50)
                                
                if not gene in dout[assay][system][organ]["gene"]:
                    dout[assay][system][organ]["gene"].append(gene)

            elif typeMap == "viability":
                for system in dvia.keys():
                    organ = dvia[system]
                    gene = "NA"

                    if not assay in list(dout.keys()):
                        dout[assay] = {}

                    if not system in list(dout[assay].keys()):
                        dout[assay][system] = {}

                    if not organ in list(dout[assay][system].keys()):
                        dout[assay][system][organ] = {}
                        dout[assay][system][organ]["AC50"] = 100000.0
                        dout[assay][system][organ]["gene"] = []

                    if dout[assay][system][organ]["AC50"] > float(ac50):
                        dout[assay][system][organ]["AC50"] = float(ac50)
                                    
                    if not gene in dout[assay][system][organ]["gene"]:
                        dout[assay][system][organ]["gene"].append(gene)

            elif typeMap == "gene":
                gene = self.dassayMapped[assay]["gene"]
                llexp = self.cDB.execCMD("SELECT gene, system, organ, expression, control FROM %s WHERE gene='%s'"%(self.tableGene, self.dassayMapped[assay]["gene"]))
                
                for lexp in llexp:
                    system = lexp[1]
                    organ = lexp[2]
                    if expControl == "gene":# error gene
                        try: exp = float(lexp[3]) / float(lexp[4])
                        except: exp = 0.0
                    else: 
                        exp = float(lexp[3]) / float(dExp[organ]["control"])
                    if exp < 2.0:
                        continue
                   
                    if not assay in list(dout.keys()):
                        dout[assay] = {}
                    if not system in list(dout[assay].keys()):
                        dout[assay][system] = {}

                    if not organ in list(dout[assay][system].keys()):
                        dout[assay][system][organ] = {}
                        dout[assay][system][organ]["AC50"] = 100000.0
                        dout[assay][system][organ]["gene"] = []
                        dout[assay][system][organ]["exp"] = []

                        if dout[assay][system][organ]["AC50"] > float(ac50):
                            dout[assay][system][organ]["AC50"] = float(ac50)
                                        
                        if not gene in dout[assay][system][organ]["gene"]:
                            dout[assay][system][organ]["gene"].append(gene)
                            dout[assay][system][organ]["exp"].append(exp)

                                        
        return dout
