from . import DBrequest


class countChem:

    def __init__(self):
        self.cDB = DBrequest.DBrequest()

    def indexCount(self):

        d_count = {}
        # extract from DB chemicals to process
        self.cDB.openConnection()
        d_count["nb_update_chem"] =  self.cDB.countUpdateChemicals()
        d_count['nb_update_desc'] =  self.cDB.countUpdateDescChemicals()
        d_count['nb_update_OPERA'] =  self.cDB.countUpdateOPERAChemicals()
        d_count['nb_update_interpred'] =  self.cDB.countUpdateInterpredChemicals()

        # count 
        d_count['nb_update_dsstoxmap'] =  self.cDB.countUpdateForCoordinates("dsstox")[0][0]
        d_count['nb_update_drugmap'] =  self.cDB.countUpdateForCoordinates("drugbank")[0][0]
        d_count['nb_update_pfasmap'] =  self.cDB.countUpdateForCoordinates("pfas")[0][0]
        d_count['nb_update_tox21map'] =  self.cDB.countUpdateForCoordinates("tox21")[0][0]

        self.cDB.closeConnection()

        return d_count