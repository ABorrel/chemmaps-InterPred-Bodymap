from . import DBrequest
import CompDesc


class computeOPERA:
    def __init__(self, pr_session):

        self.pr_session = pr_session
        self.cDB = DBrequest.DBrequest()
        self.cDB.openConnection()
        self.l_OPERA = self.cDB.extractOPERADesc()
        self.cDB.closeConnection()


    def runOPERA(self):

        self.cDB.openConnection()
        # load all of the chemical
        cmd_sql = "SELECT source_id FROM chemical_description_user WHERE status='update' AND desc_opera is null"
        l_chem = self.cDB.runCMD(cmd_sql)

        for chem in l_chem:
            smiles = chem[0]
            cChem = CompDesc.CompDesc(smiles, self.pr_session)
            cChem.prepChem()
            
            # descriptor 1D2D
            cChem.computeOperaDesc()
            if cChem.err == 1:
                # change status to error
                cmd_update = "UPDATE chemical_description_user SET status = 'error' WHERE source_id = '%s'"%(smiles)
                self.cDB.runCMD(cmd_update)

            else:
                # organise desc 1D2D
                l_descOPERA_upload = []
                for desc in self.l_OPERA:
                    l_descOPERA_upload.append(float(cChem.allOPERA[desc[0]]))
                
                wOPERA = "{" + ",".join(["%s" % (descval) for descval in l_descOPERA_upload]) + "}"
                cmd_update = "UPDATE chemical_description_user SET desc_opera = '%s' WHERE source_id = '%s'"%(wOPERA, smiles)
                self.cDB.DB.updateElement(cmd_update)
        self.cDB.closeConnection()
    