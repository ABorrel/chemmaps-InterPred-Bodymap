from django_server import toolbox
from . import DBrequest
import CompDesc


class uploadChem:
    def __init__(self, p_fchem, map, pr_update):
        self.map = map
        self.p_fchem = p_fchem
        self.err = []
        self.notice = []
        self.pr_out = pr_update
        self.cDB = DBrequest.DBrequest()

    def prepChem(self):
        """Prep chemicals from upload and get ready for push update"""

        try:d_chem = toolbox.loadMatrixToDict(self.p_fchem)
        except:
            self.err.append("File is not a txt file format.")
            return 
        l_chemin = list(d_chem.keys())
        l_ks = list(d_chem[l_chemin[0]].keys())
        
        self.notice.append("%i chemicals uploaded"%(len(l_chemin)))

        #check file is properly formated
        if not "name" in l_ks and not "smiles_origin" in l_ks and not "dsstox_id" in l_ks and not "casn" in l_ks:
            self.err.append("Header of the file is not correct")
            return 
        else:
            self.cDB.openConnection()

            i = 0
            imax = len(l_chemin)
            while i < imax:
                # check is included in the main user table => do not check here if it is in the main chemical table 
                #in_db = self.cDB.checkIfChemicalIsReadyToPush(d_chem[l_chemin[i]]["smiles_origin"])
                #if in_db > 0:
                #    del d_chem[l_chemin[i]]
                #    l_chemin.pop(i)
                #    imax = imax - 1
                #    continue
                #else:
                    
                # format name for sql
                d_chem[l_chemin[i]]["name"] = d_chem[l_chemin[i]]["name"].replace("'", "''")
                # compute all of the entry for chemical table
                cChem = CompDesc.CompDesc(d_chem[l_chemin[i]]["smiles_origin"], self.pr_out)
                cChem.prepChem()

                #print(cChem.err)
                if cChem.err == 0:
                    smiles_clean = cChem.smi
                    d_chem[l_chemin[i]]["smiles_clean"] = smiles_clean
                    cChem.generateInchiKey()
                    #print(cChem.inchikey)
                    if cChem.err == 0:
                        d_chem[l_chemin[i]]["inchikey"] = cChem.inchikey
                    else:
                        d_chem[l_chemin[i]]["inchikey"] = ""
                            
                else: 
                    d_chem[l_chemin[i]]["smiles_clean"] = ""
                    d_chem[l_chemin[i]]["inchikey"] = ""
                i = i + 1
        self.cDB.closeConnection()

        self.d_chem = d_chem
        self.notice.append("%i chemicals pushed in DB"%(len(l_chemin)))

    
    def pushChemicals(self):

        if self.d_chem == {}:
            return 
        else:
            l_chemin = list(self.d_chem.keys())
            l_ks = list(self.d_chem[l_chemin[0]].keys())

            #self.cDB.openConnection()
            # insert into the main chemicals table
            cmdSQL = "INSERT INTO chemicals_user(%s, status) VALUES"%(",".join(l_ks))
            cmdSQL_desc = "INSERT INTO chemical_description_user(source_id, inchikey, map_name, status) VALUES"

            l_val = []
            l_val_desc = []
            self.cDB.openConnection()
            for chem in l_chemin:
                in_db = self.cDB.checkIfChemicalIsReadyToPush(self.d_chem[chem]["smiles_origin"])
                if in_db == 0:
                    l_val.append("(%s, \'update\')"%(",".join(["\'" + self.d_chem[chem][ks] + "\'" for ks in l_ks])))
                if self.d_chem[chem]["inchikey"] != "":
                    l_val_desc.append("('%s','%s','%s','update')"%(chem, self.d_chem[chem]["inchikey"], self.map))
                else:
                    l_val_desc.append("('%s','%s','%s','error')"%(chem, self.d_chem[chem]["inchikey"], self.map))
            

            # push in DB
            if l_val != []:
                cmdSQL = "%s%s"%(cmdSQL, ",".join(l_val))
                self.cDB.DB.addElementCMD(cmdSQL)
            
            if l_val_desc != []:
                cmdSQL_desc = "%s%s"%(cmdSQL_desc, ",".join(l_val_desc))
                self.cDB.DB.addElementCMD(cmdSQL_desc)

            self.cDB.closeConnection()
            
            
        