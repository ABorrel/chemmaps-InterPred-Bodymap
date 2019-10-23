from .toolbox import loadMatrixToDict
from .DBrequest import DBrequest

from os import path, remove
from re import search
import sys
sys.path.insert(0, path.abspath('./../MD/'))
from MD import Chemical


class uploadSMILES:

    def __init__(self, input, prout):

        self.prout = prout
        self.cDB = DBrequest()
        self.cDB.verbose = 0
        self.input = input
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

        lchem_input = self.input
        lchem_input = list(filter(lambda a: a != "", lchem_input))
        nbSIMLES = len(lchem_input)

        if nbSIMLES == 0:
            self.err = 1
            return

        else:
            doutIN = {}
            doutOUT = {}
            i = 1
            for chem_input in lchem_input:
                doutIN[i] = {}
                doutOUT[i] = {}
                doutIN[i] = chem_input
                smiles_clean = []
                inch = "Error"
                # Check if in DB => case it has a ID
                if search("DTXSID", chem_input):
                    smiles_clean = self.cDB.extractColoumn("chemmapchemicals", "smiles_clean, inchikey", "WHERE dsstox_id = '%s'"%(chem_input))
                elif search("^DB", chem_input):
                    smiles_clean = self.cDB.extractColoumn("chemmapchemicals", "smiles_clean, inchikey", "WHERE drugbank_id = '%s'"%(chem_input))
                
                if smiles_clean == []:
                    chemical = Chemical.Chemical(chem_input, self.prout)
                    chemical.prepChem()
                    if chemical.err == 0:
                        smiles_clean = chemical.smi
                        inch = chemical.generateInchiKey()
                else:
                    inch = smiles_clean[0][1]
                    smiles_clean = smiles_clean[0][0]

                if smiles_clean != []:
                    doutOUT[i]["SMILES"] = smiles_clean
                    doutOUT[i]["file"] = "chemmaps/img/checkOK.png"
                else:
                    doutOUT[i]["SMILES"] = 0
                    doutOUT[i]["file"] = "chemmaps/img/checkNo.png"
                i = i + 1

            # see to pass process
            pfilout = self.prout + "smiClean.csv"
            filout = open(pfilout, "w")
            filout.write("ID\tSMI_IN\tSMI_CLEAN\tINCH\n")
            for k in doutIN.keys():
                filout.write("%i\t%s\t%s\t%s\n"%(k,doutIN[k].strip(), doutOUT[k]["SMILES"], inch))
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

        # creat file for downloading
        pfilout2D = self.prout + "2D.csv"
        pfilout3D = self.prout + "3D.csv"

        # load descriptor names here to avoid repeat
        ldesc1D2D = self.cDB.extractColoumn("desc_1d2d_name", "name")
        ldesc1D2D = [desc [0] for desc in ldesc1D2D]

        ldesc3D = self.cDB.extractColoumn("desc_3D_name", "name")
        ldesc3D = [desc [0] for desc in ldesc3D]

        dout = {} # for table in descriptor coloumn

        filout2D = open(pfilout2D, "w")
        filout3D = open(pfilout3D, "w")
        filout2D.write("ID\tSMILES\tinchikey\t" + "\t".join(ldesc1D2D) + "\n")
        filout3D.write("ID\tSMILES\t" + "\t".join(ldesc3D) + "\n")

        a = self.input
        for k in self.dclean["IN"].keys():
            dout[k] = {}
            SMICLEAN = self.dclean["OUT"][k]["SMILES"]
            if SMICLEAN == "0":
                dout[k]["Descriptor"] = "Error"
                dout[k]["desc"] = "chemmaps/img/checkNo.png"
                dout[k]["desc"] = "chemmaps/img/checkNo.png"
            else:
                inch = self.input[str(k)]["INCH"]
                chemical = Chemical.Chemical(SMICLEAN, self.prout)
                chemical.prepChem()
                chemical.generateInchiKey()

                # check if chemical is in DB for 1D2D
                d1D2D = downloadDescFromDB(self.cDB, "1D2D", ldesc1D2D, inch)
                d3D = downloadDescFromDB(self.cDB, "3D", ldesc3D, inch)
                if d1D2D == {}:
                    chemical = Chemical.Chemical(SMICLEAN, self.prout)
                    chemical.prepChem()
                    chemical.generateInchiKey()
                    chemical.computeAll2D()
                    chemical.set3DChemical()
                    chemical.computeAll3D()
                
                    if chemical.err == 0:
                        #print(chemdesc.all2D.keys())
                        dout[k]["Descriptor"] = "OK"
                        dout[k]["desc"] = "chemmaps/img/checkOK.png"
                        filout2D.write("%i\t%s\t%s\t%s\n"%(k, SMICLEAN, chemical.inchikey, "\t".join([str(chemical.all2D[d]) for d in ldesc1D2D])))
                        filout3D.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(chemical.all3D[d]) for d in ldesc3D])))
                        # run png generation
                        prPNG = path.abspath("./static/chemmaps/png") + "/"
                        chemical.computePNG(prPNG)
                    else:
                        dout[k]["desc"] = "chemmaps/img/checkNo.png"
                        dout[k]["Descriptor"] = "Error"
                
                else:
                    dout[k]["Descriptor"] = "OK"
                    dout[k]["desc"] = "chemmaps/img/checkOK.png"
                    filout2D.write("%i\t%s\t%s\t%s\n"%(k, SMICLEAN, inch, "\t".join([str(d1D2D[d]) for d in ldesc1D2D])))
                    filout3D.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(d3D[d]) for d in ldesc3D])))
                       
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