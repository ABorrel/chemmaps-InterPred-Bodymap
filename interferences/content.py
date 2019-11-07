from .toolbox import loadMatrixToDict, createFolder
from .DBrequest import DBrequest

from os import path, remove
from re import search
import sys
sys.path.insert(0, path.abspath('./../MD/'))
from MD import Chemical



class formatSMILES:

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
                if doutOUT[int(k)]["SMILES"] == "0" or doutOUT[int(k)]["SMILES"] == "ERROR":
                    doutOUT[int(k)]["file"] = "interferences/img/checkNo.png"
                else:
                    doutOUT[int(k)]["file"] = "interferences/img/checkOK.png"
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
                
                # inspect the DB with SMILES from users
                if smiles_clean == [] or smiles_clean == "ERROR":
                    # search in chemical DB and chemical_user
                    smiles_clean = self.cDB.extractColoumn("chemmapchemicals", "smiles_clean, inchikey", "WHERE smiles_origin = '%s' or smiles_clean = '%s'" %(chem_input, chem_input))

                    if smiles_clean == [] or smiles_clean == "ERROR":
                        smiles_clean = self.cDB.extractColoumn("chemmapchemicals_user", "smiles_clean, inchikey", "WHERE smiles_origin = '%s' or smiles_clean = '%s'" %(chem_input, chem_input))

                # process the chemicals
                if smiles_clean == []  or smiles_clean == "ERROR":
                    chemical = Chemical.Chemical(chem_input, self.prout)
                    chemical.prepChem()
                    if chemical.err == 0:
                        smiles_clean = chemical.smi
                        inch = chemical.generateInchiKey()
                        # add in the DB
                        self.cDB.addElement("chemmapchemicals_user", ["smiles_origin", "smiles_clean", "inchikey"], [chem_input, smiles_clean, inch])
                else:
                    inch = smiles_clean[0][1]
                    smiles_clean = smiles_clean[0][0]

                if smiles_clean != [] and smiles_clean != "ERROR" :
                    doutOUT[i]["SMILES"] = smiles_clean
                    doutOUT[i]["file"] = "interferences/img/checkOK.png"
                    doutOUT[i]["inchikey"] = inch
                else:
                    doutOUT[i]["SMILES"] = 0
                    doutOUT[i]["file"] = "interferences/img/checkNo.png"
                    doutOUT[i]["inchikey"] = "ERROR"
                i = i + 1

            # see to pass process
            pfilout = self.prout + "smiClean.csv"
            filout = open(pfilout, "w")
            filout.write("ID\tSMI_IN\tSMI_CLEAN\tINCH\n")
            for k in doutIN.keys():
                filout.write("%i\t%s\t%s\t%s\n"%(k,doutIN[k].strip(), doutOUT[k]["SMILES"], doutOUT[k]["inchikey"]))
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
        pfiloutOPERA = self.prout + "OPERA.csv"

        # load descriptor names here to avoid repeat
        ldesc1D2D = self.cDB.extractColoumn("desc_1d2d_name", "name")
        ldesc1D2D = [desc [0] for desc in ldesc1D2D]

        ldescOPERA = self.cDB.extractColoumn("desc_opera_name", "name")
        ldescOPERA = [desc [0] for desc in ldescOPERA]

        dout = {} # for table in descriptor coloumn

        filout2D = open(pfilout2D, "w")
        filoutOPERA = open(pfiloutOPERA, "w")
        filout2D.write("ID\tSMILES\tinchikey\t" + "\t".join(ldesc1D2D) + "\n")
        filoutOPERA.write("ID\tSMILES\t" + "\t".join(ldescOPERA) + "\n")

        for k in self.dclean["IN"].keys():
            dout[k] = {}
            SMICLEAN = self.dclean["OUT"][k]["SMILES"]
            if SMICLEAN == "0":
                dout[k]["Descriptor"] = "Error"
                dout[k]["desc"] = "interferences/img/checkNo.png"
                dout[k]["desc"] = "interferences/img/checkNo.png"
            else:
                inch = self.input[str(k)]["INCH"]
                chemical = Chemical.Chemical(SMICLEAN, self.prout)
                chemical.prepChem()
                chemical.generateInchiKey()

                # check if chemical is in DB for 1D2D
                lval1D2D_OPERA = downloadDescFromDB(self.cDB, ldesc1D2D, ldescOPERA, inch)
                
                # check in the user chemical list
                if lval1D2D_OPERA == []:

                    # add here some user see in futur
                    ###lval1D2D_OPERA = downloadDescFromDB(self.cDB, ldesc1D2D, ldescOPERA, inch)

                    # compute desc in case of no where
                    if lval1D2D_OPERA == []:
                        chemical = Chemical.Chemical(SMICLEAN, self.prout)
                        chemical.prepChem()
                        chemical.generateInchiKey()
                        chemical.computeAll2D()

                        chemical.computeOperaDesc(path.abspath("./MD/doc/desc_fp.xml"))

                        if chemical.err == 1:
                            dout[k]["desc"] = "interferences/img/checkNo.png"
                            dout[k]["Descriptor"] = "Error"
                            continue
                        else:
                            dopera = loadMatrixToDict(chemical.pOPERA, sep = ',')
                            dopera = dopera[list(dopera.keys())[0]]
                            lval1D2D_OPERA = [chemical.all2D, dopera]

                            # add to DB
                            # find if it is on DB
                            out = self.cDB.execCMD("select count(*) from desc_1d2d where inchikey='%s'"%(inch))
                            out = [0][0]
                            if out == 0:
                                valDesc1D2D = [chemical.all2D[desc1D2D] for desc1D2D in ldesc1D2D]
                                valDesc1D2D = ['-9999' if desc == "NA" else desc for desc in valDesc1D2D]
                                w1D2D = "{" + ",".join(["\"%s\"" % (desc) for desc in valDesc1D2D]) + "}"
                                self.cDB.addElement("desc_1d2d", ["inchikey","desc_value"], [inch, w1D2D])


                            # in opera
                            out = self.cDB.execCMD("select count(*) from interference_chemicals where inchikey='%s'"%(inch))
                            out = [0][0]

                            if out == 0:
                                valDescOPERA = [dopera[descOPERA] for descOPERA in ldescOPERA]
                                valDescOPERA = ['-9999' if desc == "NA" or desc == "NaN" else desc for desc in valDescOPERA]
                                wOPERA = "{" + ",".join(["\"%s\"" % (desc) for desc in valDescOPERA]) + "}"
                                self.cDB.addElement("interference_chemicals", ["inchikey", "opera_desc"], [inch, wOPERA])
                
                if lval1D2D_OPERA != []:
                    dout[k]["Descriptor"] = "OK"
                    dout[k]["desc"] = "interferences/img/checkOK.png"
                    filout2D.write("%i\t%s\t%s\t%s\n"%(k, SMICLEAN, inch, "\t".join([str(lval1D2D_OPERA[0][d]) for d in ldesc1D2D])))
                    filoutOPERA.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(lval1D2D_OPERA[1][d]) for d in ldescOPERA])))
                
        filout2D.close()
        filoutOPERA.close()


        # check error at least one good put error to 0
        self.err = 1
        for k in dout.keys():
            if dout[k]["Descriptor"] == "OK":
                self.err = 0
                break

        if self.err == 1:
            remove(pfiloutOPERA)
            remove(pfilout2D)

        self.ddesc = dout
        return [pfilout2D, pfiloutOPERA]



def downloadDescFromDB(cDB, ldesc1D2D, ldescOPERA, inchikey):

    return []

    cDB.verbose = 0
    lval1D2D = cDB.extractColoumn("desc_1d2d", "desc_value","where inchikey='%s'"%(inchikey))
    lvalOPERA = cDB.extractColoumn("interference_prediction", "opera_desc", "where inchikey='%s'"%(inchikey))

    if lval1D2D == "Error" or lval1D2D == [] or lvalOPERA == "Error" or lvalOPERA == []:
        return []
        
    else:
        lval1D2D = lval1D2D[0][0]
        lvalOPERA = lvalOPERA[0][0]

    d1D2D = {}
    i = 0
    imax = len(ldesc1D2D)
    while i < imax:
        d1D2D[ldesc1D2D[i]] = lval1D2D[i]
        i = i + 1
        
    dOpera = {}
    i = 0
    imax = len(ldescOPERA)
    while i < imax:
        dOpera[ldescOPERA[i]] = lvalOPERA[i]
        i = i + 1

    return [d1D2D, dOpera]








