from django.conf import settings
from . import DBrequest
from django_server import toolbox

from os import listdir, system
from numpy import std, average


class computeInterPred:
    def __init__(self, pr_session):
        self.pr_session = pr_session
        self.notice = []
        self.error = []
        self.pr_models = settings.STATICFILES_DIRS[0] + "/interferences/models/"
        self.p_Rscript = settings.STATICFILES_DIRS[0] + "/interferences/predictfromModel.R"
        self.cDB = DBrequest.DBrequest()
        self.cDB.openConnection()
        self.l_OPERA = self.cDB.extractOPERADesc()
        self.l_1D2D_desc = self.cDB.extract1D2DDesc()
        self.l_interPredModels = self.cDB.extractInterPredDesc()
        self.cDB.closeConnection()

    def prepInterpred(self):

        # extract chemicals 
        self.cDB.openConnection()
        cmd_sql = "SELECT inchikey, desc_1d2d, desc_opera FROM chemical_description_user WHERE status != 'error' AND desc_opera is not null AND desc_1d2d is not null AND interference_prediction is null"
        l_dchem = self.cDB.runCMD(cmd_sql)
        self.cDB.closeConnection()

        if len(l_dchem) == 0:
            self.error.append("No chemical is ready to be computed")
            return 1

        p_desc1d2d = self.pr_session + "desc1d2d.csv"
        f_desc1d2d = open(p_desc1d2d, "w")
        f_desc1d2d.write("inchikey\t%s\n"%("\t".join([desc[0]for desc in self.l_1D2D_desc])))
        p_opera = self.pr_session + "opera.csv"
        f_opera = open(p_opera, "w")
        f_opera.write("inchikey\t%s\n"%("\t".join([desc[0]for desc in self.l_OPERA])))

        # define a table for 
        for dchem in l_dchem:
            inchikey = dchem[0]
            l_desc1D2D = dchem[1]
            l_opera =  dchem[2]
            f_desc1d2d.write("%s\t%s\n"%(inchikey, "\t".join([str(val) for val in l_desc1D2D])))
            f_opera.write("%s\t%s\n"%(inchikey, "\t".join([str(val) for val in l_opera])))
        f_opera.close()
        f_desc1d2d.close()

        self.p_1D2D = p_desc1d2d
        self.p_opera = p_opera


    def predictInterPred(self):

        i = 0
        l_InterPred_models = listdir(self.pr_models)
        nb_model = len(l_InterPred_models)
        d_pred = {}
        while i < nb_model:
            
            pr_model = self.pr_models + l_InterPred_models[i] + "/"
            l_submodel = listdir(pr_model)

            j = 0
            jmax = len(l_submodel)
            while j < jmax:
                p_submodel = self.pr_models + l_InterPred_models[i] + "/" + l_submodel[j]
                p_out = self.pr_session + "pred_%i.csv"%(j)
                cmd = "%s %s %s %s %s" % (self.p_Rscript, self.p_1D2D, self.p_opera, p_submodel, p_out)
                system(cmd)
                d_temp = toolbox.loadMatrixToDict(p_out, sep = ",")
                for chem in d_temp.keys():
                    if not chem in list(d_pred.keys()):
                        d_pred[chem] = {}
                    if not l_InterPred_models[i] in list(d_pred[chem].keys()):
                        d_pred[chem][l_InterPred_models[i]] = []
                    if d_temp[chem]["pred"] != "NA":
                        d_pred[chem][l_InterPred_models[i]].append(float(d_temp[chem]["pred"]))
                j = j + 1
            i = i + 1

        self.d_pred = d_pred

    def pushInterPred(self):

        # transform for DB
        self.cDB.openConnection()
        for chem in self.d_pred.keys():
            l_db = []
            for interPred in self.l_interPredModels:
                funct = interPred[0].split("_")[0]
                if funct == "SD":
                    model = interPred[0].replace("SD_", "")
                    l_db.append(std(self.d_pred[chem][model]))
                else:
                    model = interPred[0].replace("M_", "")
                    l_db.append(average(self.d_pred[chem][model]))
            
            wInterPred = "{" + ",".join(["%s" % (descInterPred) for descInterPred in l_db]) + "}"
            cmd_update = "UPDATE chemical_description_user SET interference_prediction = '%s' WHERE inchikey = '%s'"%(wInterPred, chem)
            self.cDB.DB.updateElement(cmd_update)
        self.cDB.closeConnection()

        self.notice.append("%i chemicals computed using InterPred models"%(len(list(self.d_pred.keys()))))

