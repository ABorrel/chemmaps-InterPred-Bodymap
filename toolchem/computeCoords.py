from os import system, path
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
        l_ddescs = self.cDBresquest.loadDescTables("chemical_description_user", self.map_name)
        if l_ddescs == [{}, {}]:
            self.cDBresquest.closeConnection()
            self.error = ["No chemical to update"]
            return 1
        p_desc1D2D = toolbox.writeDescFromDict(l_ddescs[0], self.pr_session + "1D2D.csv")
        p_desc1D3D = toolbox.writeDescFromDict(l_ddescs[1], self.pr_session + "3D.csv")
        self.cDBresquest.closeConnection()

        # run R script
        cmd = "%s/addonMap.R %s %s %s1D2Dscaling.csv %s3Dscaling.csv %sCP1D2D.csv %sCP3D.csv %s"%(path.abspath("./chemmaps/Rscripts"), p_desc1D2D, p_desc1D3D, self.p_staticMap, self.p_staticMap, self.p_staticMap, self.p_staticMap, self.pr_session)
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
        return 0
    