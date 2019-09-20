from .toolbox import loadMatrixToDict
from .DBrequest import DBrequest

from os import path, remove
import sys
sys.path.insert(0, path.abspath('./../MD/'))
from MD import Chemical


class uploadSMILES:

    def __init__(self, content, prout):

        self.prout = prout
        self.cDB = DBrequest()
        self.cDB.verbose = 0
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
                chemical = Chemical.Chemical(SMILES, self.prout)
                chemical.prepChem()
                if chemical.err == 0:
                    doutOUT[i]["SMILES"] = chemical.smi
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

        dout = {}
        l2D = Chemical.getLdesc("1D2D")
        l3D = Chemical.getLdesc("3D")

        filout2D = open(pfilout2D, "w")
        filout3D = open(pfilout3D, "w")
        filout2D.write("ID\tSMILES\tinchikey\t" + "\t".join(l2D) + "\n")
        filout3D.write("ID\tSMILES\t" + "\t".join(l3D) + "\n")

        # load descriptor names here to avoid repeat
        ldesc1D2D = self.cDB.extractColoumn("desc_1d2d_name", "name")
        ldesc1D2D = [desc [0] for desc in ldesc1D2D]

        ldesc3D = self.cDB.extractColoumn("desc_3D_name", "name")
        ldesc3D = [desc [0] for desc in ldesc3D]


        for k in self.dclean["IN"].keys():
            dout[k] = {}
            SMICLEAN = self.dclean["OUT"][k]["SMILES"]
            if SMICLEAN == "0":
                dout[k]["Descriptor"] = "Error"
                dout[k]["desc"] = "chemmaps/img/checkNo.png"
                dout[k]["desc"] = "chemmaps/img/checkNo.png"
                continue
            else:
                # prep chemical 
                chemical = Chemical.Chemical(SMICLEAN, self.prout)
                chemical.prepChem()
                chemical.generateInchiKey()

                # check if chemical is in DB for 1D2D
                d1D2D = downloadDescFromDB(self.cDB, "1D2D", ldesc1D2D, chemical.inchikey)
                if d1D2D == {}:
                    chemical.computeAll2D()
                else:
                    # add upload here !!!!!!!!!!
                    chemical.all2D = d1D2D
                
                # for 3D
                d3D = downloadDescFromDB(self.cDB, "3D", ldesc3D, chemical.inchikey)
                if d3D == {}:
                    chemical.set3DChemical()
                    chemical.computeAll3D()
                else:
                    # add upload here !!!!!!!!!!
                    chemical.all3D = d3D
                #compute descriptor
                # have to check case of error

                if chemical.err == 0:
                    #print(chemdesc.all2D.keys())
                    dout[k]["Descriptor"] = "OK"
                    dout[k]["desc"] = "chemmaps/img/checkOK.png"
                    filout2D.write("%i\t%s\t%s\t%s\n"%(k, SMICLEAN, chemical.inchikey, "\t".join([str(chemical.all2D[d]) for d in l2D])))
                    filout3D.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(chemical.all3D[d]) for d in l3D])))
                    # run png generation
                    prPNG = path.abspath("./static/chemmaps/png") + "/"
                    chemical.computePNG(prPNG)
                else:
                    dout[k]["desc"] = "chemmaps/img/checkNo.png"
                    dout[k]["Descriptor"] = "Error"

        filout2D.close()
        filout3D.close()


        # check error at least one good put error to 0
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




def downloadDescFromDB(cDB, typedesc, ldesc, inchikey):

    cDB.verbose = 0
    if typedesc == "1D2D":
        lval = cDB.getRow("desc_1d2d", "inchikey='%s'"%(inchikey))
    elif typedesc == "3D":
        lval = cDB.getRow("desc_3d", "inchikey='%s'"%(inchikey))

    if lval == "Error" or lval == []:
        return {}
    else:
        dout = {}
        i = 0
        imax = len(ldesc)
        while i < imax:
            dout[ldesc[i]] = lval[0][1][i]
            i = i + 1

        return dout        