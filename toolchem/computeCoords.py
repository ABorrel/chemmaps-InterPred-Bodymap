from os import system, path
from copy import deepcopy
from . import DBrequest
from django_server import toolbox

class computeCoords:

    def __init__(self, map_name, pr_session):
        self.map_name = map_name
        self.p_staticMap = path.abspath("./static/chemmaps/map/" + self.map_name + "/") + "/"
        self.error = []
        self.notice = []
        self.pr_session = pr_session
        self.cDBresquest = DBrequest.DBrequest()


    def computeCoordForOnlyNewChem(self):

        self.cDBresquest.openConnection()
        # extract desc table from DB
        l_ddescs = self.cDBresquest.loadDescTables("chemical_description_user", self.map_name, "AND desc_1d2d is not null AND desc_3d is not null AND d3_cube is null")
        if l_ddescs == [{}, {}]:
            self.cDBresquest.closeConnection()
            self.error = ["No chemical to update"]
            return 1
        p_desc1D2D = toolbox.writeDescFromDict(l_ddescs[0], self.pr_session + "1D2D.csv")
        p_desc1D3D = toolbox.writeDescFromDict(l_ddescs[1], self.pr_session + "3D.csv")
        self.cDBresquest.closeConnection()

        # run R script
        cmd = "%s/addonMap.R %s %s %s1D2Dscaling.csv %s3Dscaling.csv %sCP1D2D.csv %sCP3D.csv %s"%(path.abspath(path.dirname(__file__) + "/Rscripts"), p_desc1D2D, p_desc1D3D, self.p_staticMap, self.p_staticMap, self.p_staticMap, self.p_staticMap, self.pr_session)
        system(cmd)

        p_coords1D2D = self.pr_session + "coord1D2D.csv"
        p_coords3D = self.pr_session + "coord3D.csv"

        d_coords1D2D = toolbox.loadMatrixToDict(p_coords1D2D, sep = ",")
        d_coords3D = toolbox.loadMatrixToDict(p_coords3D, sep = ",")

        # add to DB
        self.cDBresquest.openConnection()
        l_inch = list(d_coords1D2D.keys())
        for inch in l_inch:
            cmd = "UPDATE chemical_description_user SET dim1d2d = '{%s}', dim3d = '{%s}', d3_cube='{%s, %s, %s}'  WHERE inchikey='%s' AND map_name = '%s';" %(",".join([str(d_coords1D2D[inch]["DIM%i"%(i)]) for i in range(1,11)]), ",".join([str(d_coords3D[inch]["DIM3-%i"%(i)]) for i in range(1,11)]), d_coords1D2D[inch]["DIM1"],d_coords1D2D[inch]["DIM2"], d_coords3D[inch]["DIM3-1"], inch, self.map_name)
            self.cDBresquest.DB.updateElement(cmd)
        self.cDBresquest.closeConnection()

        self.notice.append("New coordinated have been computed")


    def computeForAllCoordForMap(self):

        self.cDBresquest.openConnection()
        # extract desc table user from DB
        l_ddesc_users = self.cDBresquest.loadDescTables("chemical_description_user", self.map_name, "AND desc_1d2d is not null AND desc_3d is not null")
        if l_ddesc_users == [{}, {}]:
            self.cDBresquest.closeConnection()
            self.error = ["No chemical to update"]
            return 1

        # extract from the main table
        l_ddesc_db = self.cDBresquest.loadDescTables("chemical_description", self.map_name, "AND desc_1d2d is not null AND desc_3d is not null")

        # combine desc
        l_ddesc_1D2D = deepcopy(l_ddesc_users[0])
        l_ddesc_3D = deepcopy(l_ddesc_users[1])

        l_ddesc_1D2D.update(deepcopy(l_ddesc_db[0]))
        l_ddesc_3D.update(deepcopy(l_ddesc_db[1])) 

        p_desc1D2D = toolbox.writeDescFromDict(l_ddesc_1D2D, self.pr_session + "1D2D.csv")
        p_desc1D3D = toolbox.writeDescFromDict(l_ddesc_3D, self.pr_session + "3D.csv")

        # run R script
        cmd = "%s/generateMapFile.R %s %s %s"%(path.abspath("./chemmaps/Rscripts"), p_desc1D2D, p_desc1D3D, self.pr_session)
        system(cmd)

        p_coords1D2D = self.pr_session + "coord1D2D.csv"
        p_coords3D = self.pr_session + "coord3D.csv"

        d_coords1D2D = toolbox.loadMatrixToDict(p_coords1D2D, sep = ",")
        d_coords3D = toolbox.loadMatrixToDict(p_coords3D, sep = ",")


        # l_inch users 
        l_inch_users = list(l_ddesc_users[0].keys())
        l_inch_db = list(l_ddesc_db[0].keys())

        # reopen connection

        # Update user entry 
        for inch in l_inch_users:
            cmd = "UPDATE chemical_description_user SET dim1d2d = '{%s}', dim3d = '{%s}', d3_cube='{%s, %s, %s}'  WHERE inchikey='%s' AND map_name = '%s';" %(",".join([str(d_coords1D2D[inch]["DIM%i"%(i)]) for i in range(1,11)]), ",".join([str(d_coords3D[inch]["DIM3-%i"%(i)]) for i in range(1,11)]), d_coords1D2D[inch]["DIM1"],d_coords1D2D[inch]["DIM2"], d_coords3D[inch]["DIM3-1"], inch, self.map_name)
            self.cDBresquest.DB.updateElement(cmd)
        

        # create entry in user with coords to update DB
        for inch in l_inch_db:
            cmd = "INSERT INTO chemical_description_user(inchikey, dim1d2d, dim3d, d3_cube, map_name, status) VALUES('%s', '{%s}', '{%s}', '{%s, %s, %s}', '%s', 'coords') ;" %(inch, ",".join([str(d_coords1D2D[inch]["DIM%i"%(i)]) for i in range(1,11)]), ",".join([str(d_coords3D[inch]["DIM3-%i"%(i)]) for i in range(1,11)]), d_coords1D2D[inch]["DIM1"],d_coords1D2D[inch]["DIM2"], d_coords3D[inch]["DIM3-1"], self.map_name)
            self.cDBresquest.DB.addElementCMD(cmd)

        self.cDBresquest.closeConnection()
        self.notice.append("New coordinated have been computed")
