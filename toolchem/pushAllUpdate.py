from . import DBrequest
from django_server import toolbox
from os import path, rename, rmdir
from datetime import date
from shutil import copy2

today = date.today()
today = today.strftime("%d-%m-%Y")


class pushAllUpdate:
    def __init__(self, pr_session):
        self.cDB = DBrequest.DBrequest()
        self.cDB.DB.verbose = 0
        self.prsession = pr_session
        self.pr_static = path.abspath("./static/chemmaps/map") + "/"
        self.notice = []
        self.error = []


    def pushAll(self):

        self.pushChemicalUsers()
        self.pushChemicalDescription()
        self.recomputeNeighbors()
        self.pushNewStaticsAndCleanTable()
        self.cleanTables()

    def pushChemicalUsers(self):
        """Push in production table with chemicals and chemicals clean"""

        # extract list of chemicals in chemicals users
        self.cDB.openConnection()
        l_chem_user_DB = self.cDB.runCMD("SELECT smiles_origin, smiles_clean, inchikey, dsstox_id, drugbank_id, mol_clean, casn, name FROM chemicals_user WHERE status = 'update'")
        d_chem_user = {}
        for chem_user_db in l_chem_user_DB:
            if chem_user_db[3] != None:
                d_chem_user[chem_user_db[3]] = {}
                d_chem_user[chem_user_db[3]]["smiles_origin"] = chem_user_db[0]
                d_chem_user[chem_user_db[3]]["smiles_clean"] = chem_user_db[1]
                d_chem_user[chem_user_db[3]]["inchikey"] = chem_user_db[2]
                d_chem_user[chem_user_db[3]]["dsstox_id"] = chem_user_db[3]
                d_chem_user[chem_user_db[3]]["drugbank_id"] = chem_user_db[4]
                d_chem_user[chem_user_db[3]]["mol_clean"] = chem_user_db[5]
                d_chem_user[chem_user_db[3]]["casn"] = chem_user_db[6]
                d_chem_user[chem_user_db[3]]["name"] = chem_user_db[7]               

        l_chem_prod_DB = self.cDB.runCMD("SELECT dsstox_id FROM chemicals")
        l_chem_prod = []
        for chem_prod_db in l_chem_prod_DB:
            if chem_prod_db[0] != None:
                l_chem_prod.append(chem_prod_db[0])
        l_chem_prod.sort()


        for chem in d_chem_user.keys():
            in_main_db = toolbox.binary_search(l_chem_prod, chem)
            if in_main_db == -1:
                # create the entry
                id_DB = self.cDB.runCMD("SELECT MAX(id) from chemicals")
                id_DB = int(id_DB[0][0]) + 1

                cmd_sql = "INSERT INTO chemicals (id, smiles_origin, dsstox_id) VALUES('%s', '%s', '%s') ;" %(id_DB, d_chem_user[chem]["smiles_origin"], d_chem_user[chem]["dsstox_id"])
                self.cDB.DB.addElementCMD(cmd_sql)


            # update chemicals table
            l_cmd_update = []
            for k in d_chem_user[chem].keys():
                if d_chem_user[chem][k] != None and d_chem_user[chem][k] != "" and d_chem_user[chem][k] != "NA":
                    if k == "name":
                        l_cmd_update.append("%s='%s'"%(k, d_chem_user[chem][k].replace("'", "''")))
                
            cmd_sql = "UPDATE chemicals SET %s WHERE dsstox_id='%s'"%(",".join(l_cmd_update), chem)
            self.cDB.DB.updateElement(cmd_sql)

        self.cDB.closeConnection()

    def pushChemicalDescription(self):

        # extract list of chemicals in chemicals users
        self.cDB.openConnection()
        l_chem_user_DB = self.cDB.runCMD("SELECT source_id, inchikey, dim1d2d, dim3d, map_name, d3_cube, desc_1d2d, desc_3d, interference_prediction, desc_opera, status FROM chemical_description_user WHERE status != 'user'")
        self.cDB.closeConnection()

        d_chem_user = {}
        l_new_map = []
        for chem_user_db in l_chem_user_DB:
            if chem_user_db[1] != None and chem_user_db[1] != "":
                if chem_user_db[10] == "coords":
                    continue
                d_chem_user[chem_user_db[1]] = {}
                d_chem_user[chem_user_db[1]]["source_id"] = chem_user_db[0]
                d_chem_user[chem_user_db[1]]["inchikey"] = chem_user_db[1]
                d_chem_user[chem_user_db[1]]["dim1d2d"] = chem_user_db[2]
                d_chem_user[chem_user_db[1]]["dim3d"] = chem_user_db[3]
                d_chem_user[chem_user_db[1]]["map_name"] = chem_user_db[4]
                d_chem_user[chem_user_db[1]]["d3_cube"] = chem_user_db[5]
                d_chem_user[chem_user_db[1]]["desc_1d2d"] = chem_user_db[6]
                d_chem_user[chem_user_db[1]]["desc_3d"] = chem_user_db[7]               
                d_chem_user[chem_user_db[1]]["interference_prediction"] = chem_user_db[8]                  
                d_chem_user[chem_user_db[1]]["desc_opera"] = chem_user_db[9]  
                d_chem_user[chem_user_db[1]]["status"] = chem_user_db[10]
        
                # remove interference == NAN
                if chem_user_db[8] != None and chem_user_db[8] != [] and str(chem_user_db[8][0]) == "NaN":
                    d_chem_user[chem_user_db[1]]["interference_prediction"] = []
        

        self.cDB.openConnection()
        #self.cDB.DB.verbose = 1
        # update coords
        cmd_map = "SELECT DISTINCT map_name FROM chemical_description_user WHERE status='coords'"
        l_map_full_coords = self.cDB.runCMD(cmd_map)
        if l_map_full_coords != []:
            for map in l_map_full_coords:
                map_in = str(map[0])
                cmd_remove_neighbor = "UPDATE chemical_description SET neighbors_dim3 = null, neighbors_dimn = null WHERE map_name='%s';"%(map_in)
                self.cDB.DB.updateElement(cmd_remove_neighbor)

                cmd_update_coords = "UPDATE chemical_description SET dim1d2d = chemical_description_user.dim1d2d, "\
                    "dim3d = chemical_description_user.dim3d, d3_cube=chemical_description_user.d3_cube FROM chemical_description_user "\
                    "WHERE chemical_description.inchikey=chemical_description_user.inchikey AND chemical_description.map_name='%s' "\
                    "AND chemical_description_user.map_name='%s' AND chemical_description_user.status='coords'"%(map_in, map_in)
                self.cDB.DB.updateElement(cmd_update_coords)


        for inchikey in d_chem_user.keys():
            cmd_in_db = "SELECT COUNT(*) FROM chemical_description WHERE inchikey='%s' and map_name = '%s'"%(inchikey, d_chem_user[inchikey]["map_name"])
            in_db = int(self.cDB.runCMD(cmd_in_db)[0][0])
            if in_db == 0:
                # update DB
                id_DB = self.cDB.runCMD("SELECT MAX(id) FROM chemical_description;")
                id_DB = int(id_DB[0][0]) + 1
                cmd_sql = "INSERT INTO chemical_description (id, inchikey, map_name) VALUES('%s', '%s', '%s') ;" %(id_DB, d_chem_user[inchikey]["inchikey"], d_chem_user[inchikey]["map_name"])
                self.cDB.DB.addElementCMD(cmd_sql)

            l_cmd_update = []
            for k in d_chem_user[inchikey].keys():
                if k == "status":
                    continue
                if d_chem_user[inchikey][k] != None and d_chem_user[inchikey][k] != "" and d_chem_user[inchikey][k] != "NA" and d_chem_user[inchikey][k] != [] and k != "inchikey":
                    l_cmd_update.append("%s=chemical_description_user.%s"%(k, k))
            cmd_sql = "UPDATE chemical_description SET %s FROM chemical_description_user WHERE chemical_description.inchikey='%s' AND chemical_description_user.inchikey='%s '\
                'AND chemical_description.map_name='%s' AND chemical_description_user.map_name='%s' AND chemical_description_user.status != 'coords'"%(",".join(l_cmd_update), 
                 inchikey, inchikey, d_chem_user[inchikey]["map_name"], d_chem_user[inchikey]["map_name"])
            self.cDB.DB.updateElement(cmd_sql)
        self.cDB.closeConnection()

    def recomputeNeighbors(self, nb_neighbors=20):

       # extract chemical that need neighbor computation
        self.cDB.openConnection()
        l_chem_db = self.cDB.runCMD("SELECT id, inchikey, map_name FROM chemical_description WHERE neighbors_dim3 is null AND d3_cube is not null;")
        d_chem = {}
        for chem_db in l_chem_db:
            d_chem[chem_db[0]] = {}
            d_chem[chem_db[0]]["id"] = chem_db[0]
            d_chem[chem_db[0]]["inchikey"] = chem_db[1]
            d_chem[chem_db[0]]["map"] = chem_db[2]



        l_id = list(d_chem.keys())
        imax = len(l_id)
        i = 0

        while i < imax:
            cmdExtract = "SELECT inchikey FROM chemical_description WHERE map_name = '%s' ORDER BY cube(d3_cube) <->  (select cube (d3_cube) FROM chemical_description where id='%s' "\
                "AND map_name = '%s' limit (1))  limit (%s);"%(d_chem[l_id[i]]["map"], l_id[i], d_chem[l_id[i]]["map"], nb_neighbors + 1)
            lchem_neighbor = self.cDB.runCMD(cmdExtract)
            lchem_w = []
            for chem in lchem_neighbor:
                lchem_w.append(chem[0])
            w_neighbors = "{" + ",".join(["\"%s\"" % (str(chem_w)) for chem_w in lchem_w[1:]]) + "}" # remove the inchikey in the list
            cmd_update = "UPDATE chemical_description SET neighbors_dim3 = '%s' WHERE id='%s';" %(w_neighbors, l_id[i])
            self.cDB.DB.updateElement(cmd_update)     
            i = i + 1     
        self.cDB.closeConnection()

    def pushNewStaticsAndCleanTable(self):

        # select map for full update
        self.cDB.openConnection()
        cmd_map = "SELECT DISTINCT map_name FROM chemical_description_user WHERE status='coords'"
        
        l_map_full_coords = self.cDB.runCMD(cmd_map)
        if l_map_full_coords != []:
            l_map_to_update = [str(map[0]) for map in l_map_full_coords]
        else:
            return 

        
        for map_to_update in l_map_to_update:
            pr_update = self.prsession + map_to_update + "/"
            pr_static =  self.pr_static + map_to_update + "/"

            p_1D2D_scaling_updated = pr_update + "1D2Dscaling.csv"
            p_3D_scaling_updated = pr_update + "3Dscaling.csv"
            p_cp1D2D_updated = pr_update + "CP1D2D.csv"
            p_cp3D_updated = pr_update + "CP3D.csv"

            p_1D2D_scaling_old = pr_static +  "1D2Dscaling.csv"
            p_3D_scaling_old = pr_static + "3Dscaling.csv"
            p_cp1D2D_old = pr_static + "CP1D2D.csv"
            p_cp3D_old = pr_static + "CP3D.csv"



            if path.exists(p_1D2D_scaling_updated) and path.exists(p_3D_scaling_updated) and path.exists(p_cp1D2D_updated) and path.exists(p_cp3D_updated):

                # rename old file
                rename(p_1D2D_scaling_old, pr_static + "1D2Dscaling_" + today + ".csv")
                rename(p_3D_scaling_old, pr_static + "3Dscaling_" + today + ".csv")
                rename(p_cp1D2D_old, pr_static + "CP1D2D_" + today + ".csv")
                rename(p_cp3D_old, pr_static + "CP3D_" + today + ".csv")  

                # copy new file
                copy2(p_1D2D_scaling_updated, pr_static + "1D2Dscaling.csv")
                copy2(p_3D_scaling_updated, pr_static + "3Dscaling.csv")
                copy2(p_cp1D2D_updated, pr_static + "CP1D2D.csv")
                copy2(p_cp3D_updated, pr_static + "CP3D.csv")

                self.notice.append("%s CP and scaling files have been updates"%(map_to_update))

        self.cDB.closeConnection()

    def cleanTables(self):

        self.cDB.openConnection()

        # clean table chemicals
        nb_to_remove = self.cDB.runCMD("SELECT COUNT(*) FROM chemicals_user WHERE status != 'user'")[0][0]
        cmd_clean_chemical_user = "DELETE FROM chemicals_user WHERE status != 'user'"
        self.cDB.DB.updateElement(cmd_clean_chemical_user)
        self.notice.append("%s have been updated in the chemicals table"%(nb_to_remove))


        # clean table description
        nb_to_remove_description = self.cDB.runCMD("SELECT COUNT(*) FROM chemical_description_user WHERE status != 'user'")[0][0]
        cmd_clean_chemical_description_user = "DELETE FROM chemical_description_user WHERE status != 'user'"
        self.cDB.DB.updateElement(cmd_clean_chemical_description_user)
        self.notice.append("%s have been updated in the chemical_description table"%(nb_to_remove_description))

        self.cDB.closeConnection()

        # remove all update file
        if path.exists(self.prsession):
            toolbox.cleanFolder(self.prsession, txt=0)
            rmdir(self.prsession)
        self.notice.append("Update temporary files have been cleaned")

        


