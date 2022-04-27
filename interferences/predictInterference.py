from os import listdir, system, remove, path
from numpy import mean, std
from re import search

from .DBrequest import DBrequest
from .toolbox import loadMatrixToDict, formatModelName


PMODEL = path.abspath("./static/interferences/models") + "/"


class Predict:
    def __init__(self, lmodels, noDB, prSession):

        self.lmodels = lmodels
        self.pdes2D = prSession + "2D.csv"
        self.pOpera = prSession + "OPERA.csv"
        self.prSession = prSession
        self.err = 0
        self.cDB = DBrequest()
        self.noDB = noDB
        self.cDB.verbose = 0

    def predictAll(self):

        # Load model
        lallmodel = self.cDB.extractColoumn("chem_interference_prediction_name", "name")
        lallmodel = [prop [0] for prop in lallmodel]
        self.allmodels = lallmodel
        
        dchem2D = loadMatrixToDict(self.pdes2D)
        lchem = list(dchem2D.keys())
        i = 0
        imax = len(lchem)
        dresult = {}
        while i < imax:
            inch = dchem2D[lchem[i]]["inchikey"]
            lpred = self.cDB.extractColoumn("chemical_description", "interference_prediction", "WHERE inchikey='%s' limit(1)"%(inch))
            

            if type(lpred) != list or lpred == []:
                 lpred = self.cDB.extractColoumn("chemical_description_user", "interference_prediction", "WHERE inchikey='%s' limit(1)"%(inch))
            
            if type(lpred) == list and lpred != []: 
                #lpred = self.cDB.extractColoumn("interference_chemicals", "interference_prediction", "WHERE inchikey='%s'"%(inch))
                lpred = lpred[0]
                if lpred[0] == None:
                    i = i + 1
                    continue
                lpred = lpred[0]
                dpred = {}
                j = 0
                jmax = len(lallmodel)
                while j < jmax:
                    dpred[lallmodel[j]] = lpred[j]
                    j = j + 1

                dresult[lchem[i]] = {}
                dresult[lchem[i]]["SMILES"] = dchem2D[lchem[i]]["SMILES"]
                for model in self.lmodels:
                    dresult[lchem[i]][model] = {}
                    dresult[lchem[i]][model]["M"] = round(dpred["M_" + model], ndigits=2)
                    dresult[lchem[i]][model]["SD"] = round(dpred["SD_" + model], ndigits=2)
                del lchem[i]
                imax = imax - 1
            
            else:
                # compute
                i = i + 1
        
        # prepare a new 2D desc file
        if len(lchem) == 0:
            self.dpred = dresult
            self.resultPred = {}
            return
        elif len(lchem) == len(list(dchem2D.keys())):
            pfnew2D = self.pdes2D
        elif len(lchem) != 0:
            ldesc = list(dchem2D[lchem[0]].keys())
            ldesc.remove("ID")
            ldesc.remove("SMILES")
            ldesc.remove("inchikey")
            pfnew2D = self.prSession + "2D_pred.csv"
            fnew2D = open(pfnew2D, "w")
            fnew2D.write("ID\tSMILES\tinchikey\t%s\n"%("\t".join(ldesc)))
            for chem in lchem:
                fnew2D.write("%s\t%s\t%s\t%s\n"%(dchem2D[chem]["ID"], dchem2D[chem]["SMILES"], dchem2D[chem]["inchikey"], "\t".join(str(dchem2D[chem][h]) for h in ldesc)))
            fnew2D.close()
        
        #Compute pred for all models
        dout = {}
        for model in lallmodel:
            if search("M_", model):
                name_model = model[2:]
                dout[name_model] = {}
                prmodel = PMODEL + name_model + "/"
                lRmodels = listdir(prmodel)
                for Rmodel in lRmodels:
                    presult = self.prSession + "temp.txt"
                    self.predictRmodel(prmodel + Rmodel, pfnew2D, self.pOpera, presult)
                    dout[name_model][Rmodel.split(".")[0]] = loadMatrixToDict(presult, sep = ",")
                    if path.exists(self.prSession + "temp.txt"):
                        remove(self.prSession + "temp.txt")
        self.resultPred = dout
        self.dpred = dresult
        self.pdes2D = pfnew2D

    def predictRmodel(self, pmodel, pdesc2D, pOPERA, pout):

        pRpredict = path.abspath("./interferences/Rscripts") + "/predictfromModel.R"
        cmd = "%s %s %s %s %s" % (pRpredict, pdesc2D, pOPERA, pmodel, pout)
        #print(cmd)
        system(cmd)
   
    def processResult(self):

        # pred result from DB
        if not "resultPred" in self.__dict__ and not "dpred" in self.__dict__:
            #print("Compute prediction")
            self.err = 1
            return "ERROR"

        if not "resultPred" in self.__dict__:
            if self.dpred == {}:
                self.err = 1
                return "ERROR"
            else:
                return self.dpred


        #print(self.resultPred)

        pprect = self.prSession + "predict.csv"
        for modelInt in self.resultPred.keys():
            for modelPart in self.resultPred[modelInt].keys():
                for chemIn in self.resultPred[modelInt][modelPart].keys():
                    chemID = self.resultPred[modelInt][modelPart][chemIn]["ID"]
                    if self.resultPred[modelInt][modelPart][chemIn]["pred"] == "NA":
                        continue
                    if not chemID in self.dpred.keys():
                        self.dpred[chemID] = {}
                    if not modelInt in self.dpred[chemID].keys():
                        self.dpred[chemID][modelInt] = []
                    self.dpred[chemID][modelInt].append(float(self.resultPred[modelInt][modelPart][chemIn]["pred"]))

        # add SMILES
        d2D = loadMatrixToDict(self.prSession + "2D.csv") #not self.pr2D because only included chem not in DB
        #a = self.dpred
        for chem in self.dpred.keys():
            flagDB = 0
            for model in self.dpred[chem].keys():
                if type (self.dpred[chem][model]) == dict or model == "SMILES":
                    flagDB = 1
                    break
                else:
                    #b = self.dpred[chem][model]
                    M = mean(self.dpred[chem][model])
                    SD = std(self.dpred[chem][model])
                    self.dpred[chem][model] = {}
                    self.dpred[chem][model]["M"] = round(M, ndigits=2)
                    self.dpred[chem][model]["SD"] = round(SD, ndigits=2)
            if flagDB == 0:
                self.dpred[chem]["SMILES"] = d2D[chem]["SMILES"]
                # push in DB
                wdb = []
                for kmodel in self.allmodels:
                    model = "_".join(kmodel.split("_")[1:])
                    valM = kmodel.split("_")[0]
                    wdb.append(str(self.dpred[chem][model][valM]))
                
                # choose the table
                out = self.cDB.execCMD("SELECT count(*) FROM chemical_description where inchikey='%s'"%(d2D[chem]["inchikey"]))
                if out == [(1,)]:
                    cmdSQL = "UPDATE chemical_description SET interference_prediction = '{%s}' WHERE inchikey='%s';"%(",".join(wdb), d2D[chem]["inchikey"])
                else:
                    if self.noDB == True:
                        cmdSQL = "DELETE FROM chemical_description_user WHERE inchikey='%s';"%(d2D[chem]["inchikey"])
                    else:
                        cmdSQL = "UPDATE chemical_description_user SET interference_prediction = '{%s}' WHERE inchikey='%s';"%(",".join(wdb), d2D[chem]["inchikey"])
                self.cDB.updateElement(cmdSQL)
                
        fpred = open(pprect, "w")
        fpred.write("ID\tSMILES\t%s\tinTox21\n"%("\t".join(["M-" + str(formatModelName(i)) + "\tSD-" + str(formatModelName(i)) for i in self.lmodels])))
        for chem in self.dpred.keys():

            # check if chemical is inside the tox21 chemical library
            cmd_sql = "SELECT COUNT(*) FROM chemical_description where map_name = 'tox21' and inchikey = '%s'"%(d2D[chem]["inchikey"])
            count = int(self.cDB.execCMD(cmd_sql)[0][0])
            if count > 0:
                self.dpred[chem]["inTox21"] = 1
            else:
                self.dpred[chem]["inTox21"] = 0 


            fpred.write("%s\t%s\t%s\t%s\n"%(chem, self.dpred[chem]["SMILES"], "\t".join([str(self.dpred[chem][i]["M"]) + "\t" +
                                                     str(self.dpred[chem][i]["SD"])
                                                     for i in self.lmodels]), self.dpred[chem]["inTox21"]))
            
            lmodel = list(self.dpred[chem].keys())
            lmodel.remove("SMILES")
            lmodel.remove("inTox21")
            for model in lmodel:
                if model in self.lmodels:
                    self.dpred[chem][formatModelName(model)] = {}
                    self.dpred[chem][formatModelName(model)]["M"] = float(self.dpred[chem][model]["M"])
                    self.dpred[chem][formatModelName(model)]["SD"] = float(self.dpred[chem][model]["SD"])
                del self.dpred[chem][model]
        fpred.close()
        self.dpred
