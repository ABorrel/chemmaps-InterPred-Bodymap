from django import forms



class updateForm(forms.Form):

    form_chem = forms.FileField(label='chemicals')

    form_chem_cleaned = forms.FileField(label='chemicals_cleaned')
    form_desc1D2D = forms.FileField(label='desc1D2D')
    form_desc3D = forms.FileField(label='desc3D')
    form_OPERA = forms.FileField(label='opera')
    form_coord1D2D = forms.FileField(label='coord1D2D')
    form_coord3D = forms.FileField(label='coord3D')

    l_maps = (("---", "---"),("tox21", "Tox21Map"),("drugbank", "DrugMap"),("pfas", "PFASMap"),
               ("dsstox", "DSSTOXMap"))

    form_map = forms.CharField(label='map', widget=forms.Select(choices=l_maps))




