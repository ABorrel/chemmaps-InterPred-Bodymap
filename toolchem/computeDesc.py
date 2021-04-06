from . import DBrequest
import CompDesc
from random import shuffle

class computeDesc:
    def __init__(self, pr_session):

        self.pr_session = pr_session
        self.cDB = DBrequest.DBrequest()
        self.cDB.openConnection()
        self.l_1D2D_desc = self.cDB.extract1D2DDesc()
        self.l_3D_desc = self.cDB.extract3DDesc()
        self.cDB.closeConnection()

        self.error = []
        self.notice = []

    def CheckDescriptorFromMainTable(self):
        self.cDB.openConnection()
        # load all of the chemical
        cmd_sql = "SELECT inchikey FROM chemical_description_user WHERE status='update' AND desc_1d2d is null OR desc_3d is null OR desc_opera is null OR interference_prediction is null"
        
        l_chem = self.cDB.runCMD(cmd_sql)
        shuffle(l_chem)

        if len(l_chem) == 0:
            self.notice.append("No chemical ready to be processed")

        nb_computed = 0
        for inchikey in l_chem:
            # check if existing in the main DB
            cmd_search_main_table =  "SELECT desc_1d2d, desc_3d, desc_opera, interference_prediction FROM chemical_description WHERE inchikey='%s'"%(inchikey)
            l_desc = self.cDB.runCMD(cmd_search_main_table)

            if l_desc == [] or l_desc == "Error":
                continue
            
            cmd_update = "UPDATE chemical_description_user SET "
            l_w = []
            #2D descriptors
            if l_desc[0][0] != None:
                w2d = "{%s}"%(",".join([str(val) for val in l_desc[0][0]]))
                l_w.append("desc_1d2d = '%s'"%(w2d))
            else:
                w2d = ''
            
            # 3D descriptors
            if l_desc[0][1] != None:
                w3d = "{%s}"%(",".join([str(val) for val in l_desc[0][1]]))
                l_w.append("desc_3d = '%s'"%(w3d))
            else:
                w3d = ''

            # OPERA descriptors
            if l_desc[0][2] != None:
                wopera = "{%s}"%(",".join([str(val) for val in l_desc[0][2]]))
                l_w.append("desc_opera = '%s'"%(wopera))
            else:
                wopera = ''

            # interference descriptors
            if l_desc[0][3] != None:
                winterpred = "{%s}"%(",".join([str(val) for val in l_desc[0][3]]))
                l_w.append("interference_prediction = '%s'"%(winterpred))
            else:
                winterpred = ''

            # check if something to update
            if l_w != []:
                cmd_update = cmd_update +  ",".join(l_w) + " WHERE inchikey = '%s'"%(inchikey)
                self.cDB.DB.updateElement(cmd_update)
            
            if len(l_w) > 0: 
                cmd_update = "UPDATE chemical_description_user SET status = 'check' WHERE inchikey = '%s'"%(inchikey)
                self.cDB.DB.updateElement(cmd_update)
                self.error.append("%s: No everything computed"%(inchikey))

        self.cDB.closeConnection()

    def runDesc(self):

        self.cDB.openConnection()
        # load all of the chemical
        cmd_sql = "SELECT source_id FROM chemical_description_user WHERE status='update' AND desc_1d2d is null OR status='update' AND desc_3d is null"
        
        l_chem = self.cDB.runCMD(cmd_sql)

        if len(l_chem) == 0:
            self.notice.append("No chemical ready to be processed")

        nb_computed = 0
        for chem in l_chem:

            smiles = chem[0]
            cChem = CompDesc.CompDesc(smiles, self.pr_session)
            cChem.prepChem()
            cChem.generateInchiKey()

            # case of no QSAR ready structure
            if cChem.err == 1:
                cmd_update = "UPDATE chemical_description_user SET status = 'error' WHERE source_id = '%s'"%(smiles)
                self.cDB.DB.updateElement(cmd_update)
                self.error.append("%s: error QSAR ready computation"%(smiles))
                continue
            

            # descriptor 1D2D
            cChem.computeAll2D()
            if cChem.err == 1:
                # change status to error
                cmd_update = "UPDATE chemical_description_user SET status = 'error' WHERE source_id = '%s'"%(smiles)
                self.cDB.DB.updateElement(cmd_update)
                self.error.append("%s: error 1D2D computation"%(smiles))
            else:
                # organise desc 1D2D
                l_desc2D_upload = []
                for desc in self.l_1D2D_desc:
                    l_desc2D_upload.append(cChem.all2D[desc[0]])
                l_desc2D_upload = ['-9999' if desc == "NA" or desc == "NaN" else desc for desc in l_desc2D_upload]
                
                w2D = "{" + ",".join(["%s" % (descval) for descval in l_desc2D_upload]) + "}"
                cmd_update = "UPDATE chemical_description_user SET desc_1d2d = '%s' WHERE source_id = '%s'"%(w2D, smiles)
                self.cDB.DB.updateElement(cmd_update)


            # descriptor 3D
            cChem.set3DChemical()
            if cChem.err == 1:
                # change status to error
                cmd_update = "UPDATE chemical_description_user SET status = 'error' WHERE source_id = '%s'"%(smiles)
                self.cDB.DB.updateElement(cmd_update)
                self.error.append("%s: error 3D computation"%(smiles))       
            else:         
                cChem.computeAll3D()
            
                if cChem.err == 1:
                    # change status to error
                    cmd_update = "UPDATE chemical_description_user SET status = 'error' WHERE source_id = '%s'"%(smiles)
                    self.cDB.DB.updateElement(cmd_update)
                    self.error.append("%s: error 3D computation"%(smiles))
                
                else:
                    l_desc3D_upload = []
                    for desc3D in self.l_3D_desc:
                        l_desc3D_upload.append(cChem.all3D[desc3D[0]])
                    l_desc3D_upload = ['-9999' if desc == "NA" or desc == "NaN" else desc for desc in l_desc3D_upload]
                    w3D = "{" + ",".join(["%s" % (descval) for descval in l_desc3D_upload]) + "}"
                    cmd_update = "UPDATE chemical_description_user SET desc_3d = '%s' WHERE source_id = '%s'"%(w3D, smiles)
                    self.cDB.DB.updateElement(cmd_update)
                    nb_computed = nb_computed + 1

        if nb_computed > 0:
            self.notice.append("%i chemicals processed"%(nb_computed))
        self.cDB.closeConnection()
    