from .descriptor import prep, descriptor
from .toolbox import loadMatrixToDict, createFolder
from os import path, remove


class formatSMILES:

    def __init__(self, content, prout):

        self.prout = prout

        self.input = content
        self.err = 0

        if type(self.input) == dict:
            doutIN = {}
            doutOUT = {}
            for k in self.input.keys():
                doutIN[int(k)] = self.input[k]["SMI_IN"]
                doutOUT[int(k)] = {}
                doutOUT[int(k)]["SMILES"] = self.input[k]["SMI_CLEAN"]
                if doutOUT[int(k)]["SMILES"] == "0":
                    doutOUT[int(k)]["file"] = "interferences/img/checkNo.png"
                else:
                    doutOUT[int(k)]["file"] = "interferences/img/checkOK.png"

            self.dclean = {"IN":doutIN, "OUT":doutOUT}


    def prepListSMILES(self):

        lSMILES = self.input
        lSMILES = list(filter(lambda a: a != "", lSMILES))
        nbSIMLES = len(lSMILES)

        if nbSIMLES == 0:
            self.err = 1
            return

        else:
            doutIN = {}
            doutOUT = {}
            i = 1
            for SMILES in lSMILES:
                doutIN[i] = {}
                doutOUT[i] = {}
                doutIN[i] = SMILES
                chemical = prep.prep(SMILES, self.prout)
                chemical.clean()
                if chemical.err == 0:
                    doutOUT[i]["SMILES"] = chemical.smiclean
                    doutOUT[i]["file"] = "interferences/img/checkOK.png"
                else:
                    doutOUT[i]["SMILES"] = 0
                    doutOUT[i]["file"] = "interferences/img/checkNo.png"
                i = i + 1

            # see to pass process
            pfilout = self.prout + "smiClean.csv"
            filout = open(pfilout, "w")
            filout.write("ID\tSMI_IN\tSMI_CLEAN\n")
            for k in doutIN.keys():
                filout.write("%i\t%s\t%s\n"%(k,doutIN[k].strip(), doutOUT[k]["SMILES"]))
            filout.close()

        # control if some SMILES are valid
        self.err = 1
        for i in doutOUT.keys():
            if doutOUT[i]["SMILES"] != 0:
                self.err = 0
                break

        self.dclean = {"IN":doutIN, "OUT":doutOUT}


    def computeDesc(self):

        if not "dclean" in self.__dict__:
            self.err = 1
            return

        pfilout2D = self.prout + "2D.csv"
        pfiloutOpera = self.prout + "OPERA.csv"
        prOPERA = createFolder(self.prout + "OPERA/", 1)

        # control if exist
        if path.exists(pfilout2D) and path.exists(pfiloutOpera) and path.getsize(pfilout2D) > 100 and path.getsize(pfiloutOpera) > 100:
            dout = {}
            d2D = loadMatrixToDict(pfilout2D)

            for k in self.dclean["IN"].keys():
                dout[k] = {}
                SMICLEAN = self.dclean["OUT"][k]["SMILES"]
                if SMICLEAN == "0":
                    dout[k]["Descriptor"] = "Error"
                    dout[k]["desc"] = "interferences/img/checkNo.png"
                    dout[k]["desc"] = "interferences/img/checkNo.png"
                    continue
                else:
                    chemical = prep.prep(SMICLEAN, self.prout)
                    chemical.clean(SMICLEAN)
                    chemical.generateInchiKey()
                    dout[k]["Descriptor"] = "OK"

                    # have to check the database here !!!!
                    if str(k) in d2D.keys():
                        dout[k]["desc"] = "interferences/img/checkOK.png"
                    else:
                        dout[k]["desc"] = "interferences/img/checkNo.png"

            dopera = loadMatrixToDict(pfiloutOpera)


        else:
            psdfOPERA = prOPERA + "/mols.sdf"
            dout = {}

            # 2D descriptors can loop on chemical
            l2D = descriptor.getLdesc("1D2D")
            filout2D = open(pfilout2D, "w")
            filout2D.write("ID\tSMILES\t" + "\t".join(l2D) + "\n")

            for k in self.dclean["IN"].keys():
                dout[k] = {}
                SMICLEAN = self.dclean["OUT"][k]["SMILES"]
                if SMICLEAN == "0":
                    dout[k]["Descriptor"] = "Error"
                    dout[k]["desc"] = "interferences/img/checkNo.png"
                    dout[k]["desc"] = "interferences/img/checkNo.png"
                    continue
                else:
                    # chemical preparation
                    chemical = prep.prep(SMICLEAN, self.prout)
                    chemical.clean(SMICLEAN)
                    chemical.generateInchiKey()

                    #ompute descriptor
                    chemdesc = descriptor.Descriptor(SMICLEAN, self.prout + chemical.inchikey)
                    try:
                        chemdesc.computeAll2D()
                        chemdesc.writeMatrix("2D")
                    except:
                        chemdesc.err = 1


                    # have to check case of error
                    if chemdesc.err == 0:
                        chemdesc.writeSDF(psdfOPERA, k)
                        dout[k]["Descriptor"] = "OK"
                        dout[k]["desc"] = "interferences/img/checkOK.png"
                        filout2D.write("%i\t%s\t%s\n"%(k, SMICLEAN, "\t".join([str(chemdesc.all2D[d]) for d in l2D])))
                        # run png generation
                    else:
                        dout[k]["desc"] = "interferences/img/checkNo.png"
                        dout[k]["Descriptor"] = "ERROR"
            filout2D.close()


            # run OPERA
            dopera = descriptor.computeOperaDesc(psdfOPERA, self.prout)


        # check error
        self.err = 1
        for k in dout.keys():
            if dout[k]["Descriptor"] == "OK":
                if str(k) in list(dopera.keys()):
                    self.err = 0
                    break

        if self.err == 1:
            remove(pfilout2D)
            remove(pfiloutOpera)

        self.ddesc = dout
        return [pfilout2D, pfiloutOpera]
