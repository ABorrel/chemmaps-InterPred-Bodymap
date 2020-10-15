from django.conf import settings
from . import DBrequest
from django_server import toolbox
from random import randint

class computeInterPred:
    def __init__(self, pr_session):
        a = str(randint(0, 1000000))# define a random number for folder in update to avoid overlap
        self.pr_session = toolbox.createFolder(pr_session + a + "/")
        self.notice = []
        self.error = []
        self.pr_models = settings.STATICFILES_DIRS[0] + "/interferences/models/"
        self.p_Rscript = settings.STATICFILES_DIRS[0] + "/interferences/predictfromModel.R"
        self.cDB = DBrequest.DBrequest()
        self.cDB.openConnection()
        self.l_OPERA = self.cDB.extractOPERADesc()
        self.l_1D2D_desc = self.cDB.extract1D2DDesc()
        self.cDB.closeConnection()

    def runInterpred(self):

        # extract chemicals 
        self.cDB.openConnection()
        cmd_sql = "SELECT inchikey, desc_1d2d, desc_opera FROM chemical_description_user WHERE status='update' AND desc_opera is not null AND desc_1d2d is not null AND interference_prediction is null"
        l_dchem = self.cDB.runCMD(cmd_sql)
        self.cDB.closeConnection()

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

        


    
    def predictRmodel(self, pmodel, pdesc2D, pOPERA, pout):

        pRpredict = path.abspath("./interferences/Rscripts") + "/predictfromModel.R"
        cmd = "%s %s %s %s %s" % (pRpredict, pdesc2D, pOPERA, pmodel, pout)
        #print(cmd)
        system(cmd)