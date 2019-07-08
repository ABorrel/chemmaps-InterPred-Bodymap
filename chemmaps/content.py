from .descriptor import prep, descriptor
from .toolbox import loadMatrixToDict
from os import path, remove


class uploadSMILES:

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
                    doutOUT[int(k)]["file"] = "chemmaps/img/checkNo.png"
                else:
                    doutOUT[int(k)]["file"] = "chemmaps/img/checkOK.png"

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
                    doutOUT[i]["file"] = "chemmaps/img/checkOK.png"
                else:
                    doutOUT[i]["SMILES"] = 0
                    doutOUT[i]["file"] = "chemmaps/img/checkNo.png"
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
        pfilout3D = self.prout + "3D.csv"

        # control if exist
        #if path.exists(pfilout3D) and path.exists(pfilout2D) and path.getsize(pfilout2D) > 5000 and path.getsize(pfilout3D) > 5000:
        #    dout = {}
        #    d2D = loadMatrixToDict(pfilout2D)

        #    for k in self.dclean["IN"].keys():
        #        dout[k] = {}
        #        SMICLEAN = self.dclean["OUT"][k]["SMILES"]
        #        if SMICLEAN == "0":
        #            dout[k]["Descriptor"] = "Error"
        #            dout[k]["desc"] = "chemmaps/img/checkNo.png"
        #            dout[k]["desc"] = "chemmaps/img/checkNo.png"
        #            continue
        #        else:
        #            chemical = prep.prep(SMICLEAN, self.prout)
        #            chemical.clean(SMICLEAN)
        #            chemical.generateInchiKey()
        #            dout[k]["Descriptor"] = "OK"

        #            # have to check the database here !!!!
        #            if str(k) in d2D.keys():
        #                dout[k]["desc"] = "chemmaps/img/checkOK.png"
        #            else:
        #                dout[k]["desc"] = "chemmaps/img/checkNo.png"
        #    return [pfilout2D, pfilout3D]

        if 2 == 1:
            return

        else:
            dout = {}

            l2D = descriptor.getLdesc("1D2D")
            l3D = descriptor.getLdesc("3D")

            filout2D = open(pfilout2D, "w")
            filout3D = open(pfilout3D, "w")
            filout2D.write("ID\tSMILES\t" + "\t".join(l2D) + "\n")
            filout3D.write("ID\tSMILES\t" + "\t".join(l3D) + "\n")

            for k in self.dclean["IN"].keys():
                dout[k] = {}
                SMICLEAN = self.dclean["OUT"][k]["SMILES"]
                if SMICLEAN == "0":
                    dout[k]["Descriptor"] = "Error"
                    dout[k]["desc"] = "chemmaps/img/checkNo.png"
                    dout[k]["desc"] = "chemmaps/img/checkNo.png"
                    continue
                else:
                    # chemical preparation
                    chemical = prep.prep(SMICLEAN, self.prout)
                    chemical.clean(SMICLEAN)
                    chemical.generateInchiKey()
                    chemical.generate3D()
                    chemical.parseSDFfor3DdescComputation()

                    #ompute descriptor
                    chemdesc = descriptor.Descriptor(SMICLEAN, self.prout + chemical.inchikey)
                    #try:
                    chemdesc.computeAll2D()
                    chemdesc.writeMatrix("2D")
                    #except:
                    chemdesc.err = 0 
                    try:
                        chemdesc.computeAll3D(chemical.lcoords)
                        chemdesc.writeMatrix("3D")
                    except:
                        chemdesc.err = 1


                    # have to check case of error
                    if chemdesc.err == 0:
                        #print(chemdesc.all2D.keys())
                        dout[k]["Descriptor"] = "OK"
                        dout[k]["desc"] = "chemmaps/img/checkOK.png"
                        filout2D.write("%i\t%s\t%s\n"%(k, SMICLEAN, "\t".join([str(chemdesc.all2D[d]) for d in l2D])))
                        filout3D.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(chemdesc.all3D[d]) for d in l3D])))
                        # run png generation
                        descriptor.computePNG(SMICLEAN, chemical.inchikey, self.prout)
                    else:
                        dout[k]["desc"] = "chemmaps/img/checkNo.png"
                        dout[k]["Descriptor"] = "Error"

            filout2D.close()
            filout3D.close()


        # check error
        self.err = 1
        for k in dout.keys():
            if dout[k]["Descriptor"] == "OK":
                self.err = 0
                break

        if self.err == 1:
            remove(pfilout3D)
            remove(pfilout2D)

        self.ddesc = dout
        return [pfilout2D, pfilout3D]




