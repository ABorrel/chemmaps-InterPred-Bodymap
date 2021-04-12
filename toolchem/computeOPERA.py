from . import DBrequest
import CompDesc


class computeOPERA:
    def __init__(self, pr_session):

        self.pr_session = pr_session
        self.cDB = DBrequest.DBrequest()
        self.cDB.openConnection()
        self.l_OPERA = self.cDB.extractOPERADesc()
        self.cDB.closeConnection()
        self.notice = []
        self.error = []


    def runOPERA(self):

        self.cDB.openConnection()
        # load all of the chemical
        cmd_sql = "SELECT source_id FROM chemical_description_user WHERE status !='error' AND desc_opera is null"
        l_chem = self.cDB.runCMD(cmd_sql)

        if len(l_chem) == 0:
            self.notice.append("No chemical ready to be processed")

        nb_computed = 0
        for chem in l_chem:
            smiles = chem[0]
            cChem = CompDesc.CompDesc(smiles, self.pr_session)
            cChem.prepChem()
            if cChem.err == 0:
                # descriptor OPERA
                cChem.computePADEL2DFPandCDK()
                cChem.computeOperaDesc()


            if cChem.err == 1:
                # change status to error
                cmd_update = "UPDATE chemical_description_user SET status = 'error' WHERE source_id = '%s'"%(smiles)
                self.cDB.DB.updateElement(cmd_update)
                self.error.append("%s: error OPERA computation"%(smiles))

            else:
                nb_computed = nb_computed + 1
                # organise desc 1D2D
                l_descOPERA_upload = []
                for desc in self.l_OPERA:
                    l_descOPERA_upload.append(cChem.allOPERA[desc[0]])
                l_descOPERA_upload = ['-9999' if desc == "NA" or desc == "NaN" else desc for desc in l_descOPERA_upload]


                wOPERA = "{" + ",".join(["%s" % (descval) for descval in l_descOPERA_upload]) + "}"
                cmd_update = "UPDATE chemical_description_user SET desc_opera = '%s' WHERE source_id = '%s'"%(wOPERA, smiles)
                self.cDB.DB.updateElement(cmd_update)

        if nb_computed > 0:
            self.notice.append("%i chemicals processed"%(nb_computed))
        self.cDB.closeConnection()
    