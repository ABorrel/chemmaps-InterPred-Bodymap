from os import listdir, system, remove, path
from numpy import mean, std

from .toolbox import loadMatrixToDict, formatModelName


PMODEL = path.abspath("./static/interferences/models") + "/"


class Predict:
    def __init__(self, lmodels, prSession):

        self.lmodels = lmodels
        self.pdes2D = prSession + "2D.csv"
        self.pOpera = prSession + "OPERA.csv"
        self.prSession = prSession
        self.err = 0


    def predictAll(self):


        dout = {}
        for name_model in self.lmodels:
            dout[name_model] = {}
            prmodel = PMODEL + name_model + "/"
            lRmodels = listdir(prmodel)
            for Rmodel in lRmodels:
                presult = self.prSession + "temp.txt"
                self.predictRmodel(prmodel + Rmodel, presult)
                dout[name_model][Rmodel.split(".")[0]] = loadMatrixToDict(presult, sep = ",")
                if path.exists(self.prSession + "temp.txt"):
                    remove(self.prSession + "temp.txt")
        self.resultPred = dout


    def predictRmodel(self, pmodel, pout):

        pRpredict = path.abspath("./interferences/Rscripts") + "/predictfromModel.R"
        cmd = "%s %s %s %s %s" % (pRpredict, self.pdes2D, self.pOpera, pmodel, pout)
        print(cmd)
        system(cmd)


    def processResult(self):

        if not "resultPred" in self.__dict__:
            #print("Compute prediction")
            self.err = 1
            return "ERROR"

        #print(self.resultPred)

        dresult = {}
        pprect = self.prSession + "predict.csv"

        for modelInt in self.resultPred.keys():
            for modelPart in self.resultPred[modelInt].keys():
                for chemIn in self.resultPred[modelInt][modelPart].keys():
                    chemID = self.resultPred[modelInt][modelPart][chemIn]["ID"]
                    if not chemID in dresult.keys():
                        dresult[chemID] = {}
                    if not modelInt in dresult[chemID].keys():
                        dresult[chemID][modelInt] = []
                    dresult[chemID][modelInt].append(float(self.resultPred[modelInt][modelPart][chemIn]["pred"]))

        # add SMILES
        d2D = loadMatrixToDict(self.pdes2D)
        for chem in dresult.keys():
            for model in dresult[chem].keys():
                M = mean(dresult[chem][model])
                SD = std(dresult[chem][model])
                dresult[chem][model] = {}
                dresult[chem][model]["M"] = round(M, ndigits=2)
                dresult[chem][model]["SD"] = round(SD, ndigits=2)
            dresult[chem]["SMILES"] = d2D[chem]["SMILES"]





        fpred = open(pprect, "w")
        fpred.write("ID\tSMILES\t%s\n"%("\t".join(["M-" + str(formatModelName(i)) + "\tSD-" + str(formatModelName(i)) for i in self.lmodels])))
        for chem in dresult.keys():
            fpred.write("%s\t%s\t%s\n"%(chem, dresult[chem]["SMILES"], "\t".join([str(dresult[chem][i]["M"]) + "\t" +
                                                     str(dresult[chem][i]["SD"])
                                                     for i in self.lmodels])))
            for model in self.lmodels:
                dresult[chem][formatModelName(model)] = dresult[chem][model]
                del dresult[chem][model]

        fpred.close()





        return dresult
