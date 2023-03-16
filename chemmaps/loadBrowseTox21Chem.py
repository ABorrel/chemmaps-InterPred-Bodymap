from django_server import DB

class loadBrowseTox21Chem:

    def __init__(self):
        self.c_DB = DB.DB()
    
    def loadAssaysAndChem(self):

        self.c_DB.connOpen()
        
        # load chemicals with lowest AC50
        l_chemDB = self.c_DB.execCMD("SELECT DISTINCT c.dsstox_id , c.name , c.casn FROM chts_invitrodb ch INNER JOIN chemicals c ON ch.dsstox_id = c.dsstox_id WHERE ch.dsstox_id is not null")
        d_chem = {}
        for chemDB in l_chemDB:
            dtxsid = chemDB[0]
            name = chemDB[1]
            casrn = chemDB[2]

            d_chem[dtxsid] = {}
            d_chem[dtxsid]["name"] = name
            d_chem[dtxsid]["casn"] = casrn

        self.d_chem = d_chem
        
        # load assay results 
        l_chemassayresults = self.c_DB.execCMD("SELECT dsstox_id, response, response_unit, assay, endpoint FROM chts_invitrodb")
        self.c_DB.connClose()

        d_assays = {}
        for chem in l_chemassayresults:
            dtxsid = chem[0]
            response = chem[1]
            #hitc = int(chem[1])
            #ac50 = chem[2]
            #if ac50 == None: ac50 = 0.0
            #else: ac50 = float(ac50)
            unit = chem[2]
            assay = chem[3]
            endpoint = chem[4]
        
            if dtxsid == None:
                continue

            if not dtxsid in list(d_assays.keys()):
                d_assays[dtxsid] = {}
                d_assays[dtxsid]["Most active assay"] = "None"
                d_assays[dtxsid]["Active assays"] = 0
                d_assays[dtxsid]["Inactive assays"] = 0
                d_assays[dtxsid]["Inconclusive assays"] = 0
                d_assays[dtxsid]["lowest_ac50"] = "NA"
                d_assays[dtxsid]["l_ac50"] = []
                d_assays[dtxsid]["l_assays"] = []


            if endpoint == "Call":
                if response == "Active":
                    d_assays[dtxsid]["Active assays"] = d_assays[dtxsid]["Active assays"] + 1
                elif response == "Inactive":
                    d_assays[dtxsid]["Inactive assays"] =  d_assays[dtxsid]["Inactive assays"] + 1 
                else:
                    d_assays[dtxsid]["Inconclusive assays"] =  d_assays[dtxsid]["Inconclusive assays"] + 1 
            elif endpoint == "ACC":
                try:response = float(response)
                except:pass
                if response == 0.0:
                    d_assays[dtxsid]["Inactive assays"] =  d_assays[dtxsid]["Inactive assays"] + 1 
                elif type(response) == float:
                    d_assays[dtxsid]["Active assays"] = d_assays[dtxsid]["Active assays"] + 1
                else:
                    d_assays[dtxsid]["Inconclusive assays"] =  d_assays[dtxsid]["Inconclusive assays"] + 1 
            elif endpoint == "AC50":
                try:response = float(response)
                except:pass
                if response == 0.0:
                    d_assays[dtxsid]["Inactive assays"] =  d_assays[dtxsid]["Inactive assays"] + 1 
                elif type(response) == float:
                    d_assays[dtxsid]["Active assays"] = d_assays[dtxsid]["Active assays"] + 1
                    d_assays[dtxsid]["l_ac50"].append(response)
                    d_assays[dtxsid]["l_assays"].append(assay)
                    # retrieve on the fly the lowest ac50
                    if d_assays[dtxsid]["lowest_ac50"] == "NA" or response < d_assays[dtxsid]["lowest_ac50"]:
                        d_assays[dtxsid]["Most active assay"] = assay
                        d_assays[dtxsid]["lowest_ac50"] = response
                else:
                    d_assays[dtxsid]["Inconclusive assays"] =  d_assays[dtxsid]["Inconclusive assays"] + 1 
            elif endpoint == "Top of curve":
                try:response = float(response)
                except:pass
                if response == 0.0:
                    d_assays[dtxsid]["Inactive assays"] =  d_assays[dtxsid]["Inactive assays"] + 1 
                elif type(response) == float:
                    d_assays[dtxsid]["Active assays"] = d_assays[dtxsid]["Active assays"] + 1
                else:
                    d_assays[dtxsid]["Inconclusive assays"] =  d_assays[dtxsid]["Inconclusive assays"] + 1 

        self.d_assays = d_assays
               
    def writeTable(self, pr_session):

        p_filout = pr_session + "lowestAC50.csv"
        filout = open(p_filout, "w")
        filout.write("DTXSID\tCASRN\tName\tNumber of active assay\tLowest AC50 (µM)\tAssay with the lowest AC50\n")
        for chem in self.d_chem:
            filout.write("%s\t%s\t%s\t"%(chem, self.d_chem[chem]["casn"], self.d_chem[chem]["name"]))
            if chem in list(self.d_assays.keys()):
                filout.write("%s\t%s\t%s\n"%(self.d_assays[chem]["Active assays"], self.d_assays[chem]["lowest_ac50"], self.d_assays[chem]["Most active assay"]))
            else:
                filout.write("\t\t\n")

    
