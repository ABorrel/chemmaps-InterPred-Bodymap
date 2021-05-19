from .toolbox import loadMatrixToDict, createFolder
from .DBrequest import DBrequest

from os import path, remove
from re import search
from shutil import copy2
import sys
import CompDesc


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
                if doutOUT[int(k)]["SMILES"] == "0" or doutOUT[int(k)]["SMILES"] == "ERROR":
                    doutOUT[int(k)]["file"] = "img/checkNo.png"
                else:
                    doutOUT[int(k)]["file"] = "img/checkOK.png"
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
                    doutOUT[i]["file"] = "img/checkOK.png"
                    doutOUT[i]["inchikey"] = inch
                else:
                    doutOUT[i]["SMILES"] = 0
                    doutOUT[i]["file"] = "img/checkNo.png"
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


    def computeDesc(self, mapName):

        if not "dclean" in self.__dict__:
            self.err = 1
            return

        # creat file for downloading
        pfilout2D = self.prout + "2D.csv"
        pfilout3D = self.prout + "3D.csv"

        # load descriptor names here to avoid repeat
        ldesc1D2D = self.cDB.extractColoumn("chem_descriptor_1d2d_name", "name")
        ldesc1D2D = [desc [0] for desc in ldesc1D2D]

        ldesc3D = self.cDB.extractColoumn("chem_descriptor_3d_name", "name")
        ldesc3D = [desc [0] for desc in ldesc3D]

        dout = {} # for table in descriptor coloumn

        filout2D = open(pfilout2D, "w")
        filout3D = open(pfilout3D, "w")
        filout2D.write("ID\tSMILES\tinchikey\t" + "\t".join(ldesc1D2D) + "\n")
        filout3D.write("ID\tSMILES\t" + "\t".join(ldesc3D) + "\n")

        for k in self.dclean["IN"].keys():
            dout[k] = {}
            SMICLEAN = self.dclean["OUT"][k]["SMILES"]
            if SMICLEAN == "0":
                dout[k]["Descriptor"] = "Error"
                dout[k]["desc"] = "img/checkNo.png"
                dout[k]["desc"] = "img/checkNo.png"
            else:
                inch = self.input[str(k)]["INCH"]
                chemical = CompDesc.CompDesc(SMICLEAN, self.prout)
                chemical.prepChem()
                chemical.generateInchiKey()

                # check if chemical is in DB for 1D2D
                lval1D2D_3D = downloadDescFromDB(self.cDB, ldesc1D2D, ldesc3D, "global", inch)
                
                # check in the user chemical list
                if lval1D2D_3D == []:
                    lval1D2D_3D = downloadDescFromDB(self.cDB, ldesc1D2D, ldesc3D, "user", inch, mapName)

                    # compute desc in case of no where
                    if lval1D2D_3D == []:
                        chemical = CompDesc.CompDesc(SMICLEAN, self.prout)
                        chemical.prepChem()
                        chemical.generateInchiKey()
                        chemical.computeAll2D()
                        chemical.set3DChemical()
                        chemical.computeAll3D()

                        if chemical.err == 1:
                            dout[k]["desc"] = "img/checkNo.png"
                            dout[k]["Descriptor"] = "Error"
                            continue
                        else:
                            lval1D2D_3D = [chemical.all2D, chemical.all3D]

                            # add to DB
                            valDesc1D2D = [chemical.all2D[desc1D2D] for desc1D2D in ldesc1D2D]
                            valDesc1D2D = ['-9999' if desc == "NA" else desc for desc in valDesc1D2D]
                            w1D2D = "{" + ",".join(["\"%s\"" % (desc) for desc in valDesc1D2D]) + "}"

                            valDesc3D = [chemical.all3D[desc3D] for desc3D in ldesc3D]
                            valDesc3D = ['-9999' if desc == "NA" else desc for desc in valDesc3D]
                            w3D = "{" + ",".join(["\"%s\"" % (desc) for desc in valDesc3D]) + "}"
                            self.cDB.addElement("chemical_description_user", ["inchikey", "source_id", "map_name", "desc_1d2d", "desc_3d", "status"], [inch, SMICLEAN, mapName, w1D2D, w3D, "user"])
                
                if lval1D2D_3D != []:
                    dout[k]["Descriptor"] = "OK"
                    dout[k]["desc"] = "img/checkOK.png"
                    filout2D.write("%i\t%s\t%s\t%s\n"%(k, SMICLEAN, inch, "\t".join([str(lval1D2D_3D[0][d]) for d in ldesc1D2D])))
                    filout3D.write("%i\t%s\t%s\n" % (k, SMICLEAN, "\t".join([str(lval1D2D_3D[1][d]) for d in ldesc3D])))
                    # run png generation -- HERE CHANGE PNG FOLDER
                    prPNG = createFolder(path.abspath(self.prout + "/png") + "/")
                    p_png = chemical.computePNG(prPNG, bg="None")
                    if p_png != "ERROR: PNG Generation":
                        pr_static_png =  path.abspath("./static/chemmaps/png") + "/"
                        pr_static_png = createFolder(pr_static_png + chemical.inchikey[0:2] + "/" + chemical.inchikey[2:4] + "/")
                        print(pr_static_png)
                        copy2(p_png, pr_static_png + chemical.inchikey + ".png")
                
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




def downloadDescFromDB(cDB, ldesc1D2D, ldesc3D, table, inchikey, mapName=""):

    if table == "global":
        cDB.verbose = 0
        lval = cDB.extractColoumn("chemical_description", "desc_1d2d, desc_3d","where inchikey='%s' limit(1)"%(inchikey))
    else:
        lval = cDB.extractColoumn("chemical_description_user", "desc_1d2d, desc_3d","where inchikey='%s' and map_name='%s' limit(1)"%(inchikey, mapName))
    
    if lval == "Error" or lval == []:
        return []
        
    else:
        try:
            lval1D2D = lval[0][0]
            lval3D = lval[0][1]
        except:
            return []

    d1D2D = {}
    i = 0
    imax = len(ldesc1D2D)
    while i < imax:
        d1D2D[ldesc1D2D[i]] = lval1D2D[i]
        i = i + 1
        
    d3D = {}
    i = 0
    imax = len(ldesc3D)
    while i < imax:
        d3D[ldesc3D[i]] = lval3D[i]
        i = i + 1

    return [d1D2D, d3D]
