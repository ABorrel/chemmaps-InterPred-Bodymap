from . import DBrequest
import CompDesc


class computeDesc:
    def __init__(self, pr_session):

        self.pr_session = pr_session

        self.cDB = DBrequest.DBrequest()
        self.cDB.openConnection()
        self.l_1D2D_desc = self.cDB.extract1D2DDesc()
        self.l_3D_desc = self.cDB.extract3DDesc()
        self.cDB.closeConnection()


    def loadChem(self):

        self.cDB.openConnection()
        # load all of the chemical
        cmd_sql = "SELECT source_id FROM chemical_description_user WHERE status='update' AND desc_1D2D is null"
        l_chem = self.cDB.runCMD(cmd_sql)

        for chem in l_chem:
            smiles = chem[0][0]
            cChem = CompDesc.CompDesc(smiles, self.pr_session)
            cChem.prepChem()
            cChem.computeAll2D()
            if cChem.err == 1:
                # change status 
                print("sss")
        print(l_chem)
        self.cDB.closeConnection()
        return 
    