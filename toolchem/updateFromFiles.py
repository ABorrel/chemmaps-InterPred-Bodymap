from django_server import DB, toolbox



class updateFromFiles:

    def __init__(self, c_form, pr_session):

        self.pr_session = pr_session
        self.c_form = c_form
        self.error = []
        self.notice = []
        self.cDB = DB.DB()

    def checkFilesIn(self):

        d_out = {}

        # chemicals prepared 
        if "form_chem_cleaned" in self.c_form.files:
            p_chem_cleaned = self.uploadFile(self.pr_session + "chem_cleaned", "form_chem_cleaned")
            l_chem_cleaned = toolbox.loadToList(p_chem_cleaned)
            l_header = list(l_chem_cleaned[0].keys())
            l_header.sort()
            l_control = ["smiles_origin", "smiles_cleaned","inchikey","dsstox_id","drugbank_id","casn","name"]
            l_control.sort()
            if l_control != l_header:
                self.error.append("Format of precomputed chemicals file not correct => no chemical loaded")
            else:
                d_out["form_chem_cleaned"]  = l_chem_cleaned
                self.notice.append("%i chemicals loaded from chemicals file precomputed"%(len(l_chem_cleaned)))

        # 2D descriptors
        if "form_desc2D" in self.c_form.files:
            p_chem_desc2D = self.uploadFile(self.pr_session + "chem_desc2D", "form_desc2D")
            l_chem_desc2D = toolbox.loadToList(p_chem_desc2D)
            l_header = list(l_chem_desc2D[0].keys())
            l_header.sort()
            l_control = self.cDB.extractColoumn() ##### extract descriptor list
            l_control = ["smiles_origin", "smiles_cleaned","inchikey","dsstox_id","drugbank_id","casn","name"]
            l_control.sort()
            if l_control != l_header:
                self.error.append("Format of precomputed chemicals file not correct => no chemical loaded")
            else:
                d_out["form_chem_cleaned"]  = l_chem_cleaned
                self.notice.append("%i chemicals loaded from chemicals file precomputed"%(len(l_chem_cleaned)))

        #3D descriptors
        if "form_chem_cleaned" in self.c_form.files:
            p_chem_clean = self.uploadFile(self.pr_session + "chem_cleaned", "form_chem_cleaned")
            l_chem_cleaned = toolbox.loadToList(p_chem_clean)
            l_header = list(l_chem_cleaned[0].keys())
            l_header.sort()
            l_control = ["smiles_origin", "smiles_cleaned","inchikey","dsstox_id","drugbank_id","casn","name"]
            l_control.sort()
            if l_control != l_header:
                self.error.append("Format of precomputed chemicals file not correct => no chemical loaded")
            else:
                d_out["form_chem_cleaned"]  = l_chem_cleaned
                self.notice.append("%i chemicals loaded from chemicals file precomputed"%(len(l_chem_cleaned)))
        

        return



    def uploadFile(self, p_filout, k_form):

        with open(p_filout, 'wb+') as destination:
            for chunk in self.c_form.files[k_form].chunks():
                destination.write(chunk)
        destination.close()

        return p_filout