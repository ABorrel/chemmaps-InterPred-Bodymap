from django.contrib.staticfiles import finders

from .toolbox import loadMatrixToDict



class mapChem :
    def __init__(self, CASin, foldExp):
        self.CASin = CASin
        self.pToxCast = finders.find("bodymap/mapping/chemical/%s.csv"%(CASin))
        self.pmapBody = finders.find("bodymap/mapping/AssaysBody_%s.csv"%(foldExp))


    def mapChemToBody(self):

        dAC50 = loadMatrixToDict(self.pToxCast)
        if not self.CASin in list(dAC50.keys()):
            return "Error"

        else:
            dout = {}
            dresultAssays = dAC50[self.CASin]
            dbodymap = loadMatrixToDict(self.pmapBody)

            for assays in dresultAssays.keys():
                if dresultAssays[assays] != "NA" and dresultAssays[assays] != "1000000":
                    if assays in list(dbodymap.keys()):
                        dout[assays] = {}
                        lorgantissus = dbodymap[assays]["Body mapped"].split("_")
                        for organtissus in lorgantissus:
                            tissu = organtissus.split("-")[-1]
                            organ = organtissus.split("-")[0]

                            if not organ in list(dout[assays].keys()):
                                dout[assays][organ] = {}
                            if not tissu in list(dout[assays][organ].keys()):
                                dout[assays][organ][tissu] = {}
                            dout[assays][organ][tissu]["AC50"] = float(dresultAssays[assays])
                            dout[assays][organ][tissu]["gene"] = dbodymap[assays]["Gene"]
            return dout

