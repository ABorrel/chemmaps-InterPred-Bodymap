from .toolbox import loadMatrixToDict, createFolder
from .DBrequest import DBrequest

from os import path, remove
from re import search
import sys

import CompDesc


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
                    doutOUT[int(k)]["file"] = "checkNo.png"
                else:
                    doutOUT[int(k)]["file"] = "checkOK.png"
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
                    smiles_clean = self.cDB.extractColoumn("chemicals", "smiles_clean, inchikey", "WHERE dsstox_id = '%s'"%(chem_input))
                elif search("^DB", chem_input):
                    smiles_clean = self.cDB.extractColoumn("chemicals", "smiles_clean, inchikey", "WHERE drugbank_id = '%s'"%(chem_input))
                
                # inspect the DB with SMILES from users
                if smiles_clean == [] or smiles_clean == "ERROR":
                    if not search(",", chem_input) and not search("'", chem_input) and not search("`", chem_input):
                        # search in chemical DB and chemical_user
                        smiles_clean = self.cDB.extractColoumn("chemicals", "smiles_clean, inchikey", "WHERE smiles_origin = '%s' or smiles_clean = '%s'" %(chem_input, chem_input))

                        if smiles_clean == [] or smiles_clean == "ERROR":
                            smiles_clean = self.cDB.extractColoumn("chemicals_user", "smiles_clean, inchikey", "WHERE smiles_origin = '%s' or smiles_clean = '%s'" %(chem_input, chem_input))

                # process the chemicals
                if smiles_clean == []  or smiles_clean == "ERROR":
                    chemical = CompDesc.CompDesc(chem_input, self.prout)
                    chemical.prepChem()
                    if chemical.err == 0:
                        smiles_clean = chemical.smi
                        inch = chemical.generateInchiKey()
                        # add in the DB
                        self.cDB.addElement("chemicals_user", ["smiles_origin", "smiles_clean", "inchikey", "status"], [chem_input, smiles_clean, inch, "user"])
                else:
                    inch = smiles_clean[0][1]
                    smiles_clean = smiles_clean[0][0]

                if smiles_clean != [] and smiles_clean != "ERROR" :
                    doutOUT[i]["SMILES"] = smiles_clean
                    doutOUT[i]["file"] = "checkOK.png"
                    doutOUT[i]["inchikey"] = inch
                else:
                    doutOUT[i]["SMILES"] = 0
                    doutOUT[i]["file"] = "checkNo.png"
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
        ldesc1D2D = self.cDB.extractColoumn("chem_descriptor_1d2d_name", "name")
        ldesc1D2D = [desc [0] for desc in ldesc1D2D]

        ldescOPERA = self.cDB.extractColoumn("chem_descriptor_opera_name_new", "name")
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
                dout[k]["desc"] = "checkNo.png"
                continue
            else:
                inch = self.input[str(k)]["INCH"]
                chemical = CompDesc.CompDesc(SMICLEAN, self.prout)
                chemical.prepChem()
                chemical.generateInchiKey()
                if chemical.err == 1:
                    dout[k]["Descriptor"] = "Error"
                    dout[k]["desc"] = "checkNo.png"
                    continue
                
                # check if chemical is in DB for 1D2D
                lval1D2D_OPERA = downloadDescFromDB(self.cDB, ldesc1D2D, ldescOPERA, inch)
                
                # case of error in computation
                if lval1D2D_OPERA == []:
                    dout[k]["desc"] = "checkNo.png"
                    dout[k]["Descriptor"] = "Error"
                    continue
                
                # case already computed
                elif lval1D2D_OPERA != [] and lval1D2D_OPERA != 0:
                    d_1D2D = lval1D2D_OPERA[0]
                    dopera = lval1D2D_OPERA[1]

                    valDesc1D2D = [d_1D2D[desc1D2D] for desc1D2D in ldesc1D2D]
                    valDesc1D2D = ['-9999' if desc == "NA" else desc for desc in valDesc1D2D]

                    valDescOPERA = [dopera[descOPERA] if descOPERA in list(dopera.keys()) else "NA"  for descOPERA in ldescOPERA]
                    valDescOPERA = ['-9999' if desc == "NA" or desc == "NaN" else desc for desc in valDescOPERA]
                    lval1D2D_OPERA = [valDesc1D2D, valDescOPERA]
                
                # compute 2D/opera descriptors
                elif lval1D2D_OPERA == 0:
                    chemical.computeAll2D()
                    if chemical.err == 1:
                        dout[k]["Descriptor"] = "Error"
                        dout[k]["desc"] = "checkNo.png"
                        self.cDB.addElement("chemical_description_user", ["inchikey", "source_id", "status"], [inch, SMICLEAN, "error"])
                        lval1D2D_OPERA = []
                    else:
                        #2D descriptor
                        valDesc1D2D = [chemical.all2D[desc1D2D] for desc1D2D in ldesc1D2D]
                        valDesc1D2D = ['-9999' if desc == "NA" else desc for desc in valDesc1D2D]
                        w1D2D = "{" + ",".join(["\"%s\"" % (desc) for desc in valDesc1D2D]) + "}"

                        # compute OPERA
                        chemical.computePADEL2DFPandCDK()
                        chemical.computeOperaDesc()

                        if chemical.err == 1:
                            dout[k]["desc"] = "checkNo.png"
                            dout[k]["Descriptor"] = "Error"
                            self.cDB.addElement("chemical_description_user", ["desc_1d2d", "inchikey", "source_id", "status"], [w1D2D, inch, SMICLEAN, "error"])
                            lval1D2D_OPERA = []
                        else:
                            dopera = loadMatrixToDict(chemical.pOPERA, sep = ',')
                            dopera = dopera[list(dopera.keys())[0]]

                            # opera
                            valDescOPERA = [dopera[descOPERA] if descOPERA in list(dopera.keys()) else "NA"  for descOPERA in ldescOPERA]
                            valDescOPERA = ['-9999' if desc == "NA" or desc == "NaN" else desc for desc in valDescOPERA]
                            wOPERA = "{" + ",".join(["\"%s\"" % (desc) for desc in valDescOPERA]) + "}"
                            
                            # add everything in user
                            self.cDB.addElement("chemical_description_user", ["desc_opera", "desc_1d2d", "inchikey", "source_id", "status"], [wOPERA, w1D2D, inch, SMICLEAN, "user"])
                            lval1D2D_OPERA = [valDesc1D2D, valDescOPERA]
                
                
                if lval1D2D_OPERA != []:
                    dout[k]["Descriptor"] = "OK"
                    dout[k]["desc"] = "checkOK.png"
                    filout2D.write("%i\t%s\t%s\t%s\n"%(k, SMICLEAN, inch, "\t".join([str(d) for d in lval1D2D_OPERA[0]])))
                    filoutOPERA.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(d) for d in lval1D2D_OPERA[1]])))
                
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

    cDB.verbose = 0

    # check if included in DB
    nb_mainDB = cDB.execCMD("SELECT COUNT(*) FROM chemical_description WHERE inchikey='%s'"%(inchikey))[0][0]
    if nb_mainDB > 0:
        lval1D2D = cDB.extractColoumn("chemical_description", "desc_1d2d","where inchikey='%s' limit(1)"%(inchikey))
        lvalOPERA = cDB.extractColoumn("chemical_description", "desc_opera", "where inchikey='%s' limit(1)"%(inchikey))
    
    else:
        nb_userDB = cDB.execCMD("SELECT COUNT(*) FROM chemical_description_user WHERE inchikey='%s' AND status != 'update'"%(inchikey))[0][0]
        if nb_userDB > 0:
            lval1D2D = cDB.extractColoumn("chemical_description_user", "desc_1d2d","where inchikey='%s' and status != 'update' limit(1)"%(inchikey))
            lvalOPERA = cDB.extractColoumn("chemical_description_user", "desc_opera", "where inchikey='%s' and status != 'update' limit(1)"%(inchikey))
        
        else:
            return 0

    if lval1D2D == "ERROR" or lval1D2D == [] or lvalOPERA == "ERROR" or lvalOPERA == [] or lvalOPERA == [(None)]:
        return []
        
    lval1D2D = lval1D2D[0][0]
    lvalOPERA = lvalOPERA[0][0]
    if lvalOPERA == None or lval1D2D == None:
        return []

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








