from django import forms
from . import DBrequest



class updateForm(forms.Form):

    # file forms
    form_chem = forms.FileField(label='chemicals')
    form_chem_cleaned = forms.FileField(label='chemicals_cleaned')
    form_desc1D2D = forms.FileField(label='desc1D2D')
    form_desc3D = forms.FileField(label='desc3D')
    form_OPERA = forms.FileField(label='opera')
    form_coord1D2D = forms.FileField(label='coord1D2D')
    form_coord3D = forms.FileField(label='coord3D')

    # choose the map
    l_maps = (("---", "---"),("tox21", "Tox21Map"),("drugbank", "DrugMap"),("pfas", "PFASMap"),
               ("dsstox", "DSSTOXMap"))
    form_map = forms.CharField(label='map', widget=forms.Select(choices=l_maps))

    # extract from DB chemicals to process
    cDB = DBrequest.DBrequest()
    cDB.openConnection()
    nb_update_chem = cDB.countUpdateChemicals()
    nb_update_desc = cDB.countUpdateDescChemicals()
    nb_update_OPERA = cDB.countUpdateOPERAChemicals()
    nb_update_interpred = cDB.countUpdateInterpredChemicals()

    # count 
    nb_update_dsstoxmap = cDB.countUpdateForCoordinates("dsstox")[0][0]
    nb_update_drugmap = cDB.countUpdateForCoordinates("drugbank")[0][0]
    nb_update_pfasmap = cDB.countUpdateForCoordinates("pfas")[0][0]
    nb_update_tox21map = cDB.countUpdateForCoordinates("tox21")[0][0]

    cDB.closeConnection()


    def clean(self):

        if 'overlap' in self.data:
            return "overlap"
        return "update"
