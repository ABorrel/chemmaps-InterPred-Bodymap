from django import forms



class updateForm(forms.Form):

    # file forms
    form_chem = forms.FileField(label='chemicals')
    form_chem_cleaned = forms.FileField(label='chemicals_cleaned', required=False)
    form_desc1D2D = forms.FileField(label='desc1D2D', required=False)
    form_desc3D = forms.FileField(label='desc3D', required=False)
    form_OPERA = forms.FileField(label='opera', required=False)
    form_coord1D2D = forms.FileField(label='coord1D2D', required=False)
    form_coord3D = forms.FileField(label='coord3D', required=False)
    form_assays = forms.FileField(label='assays', required=True)

    # choose the map
    l_maps = (("---", "---"),("tox21", "Tox21Map"),("drugbank", "DrugMap"),("pfas", "PFASMap"),
               ("dsstox", "DSSTOXMap"))
    form_map = forms.CharField(label='map', widget=forms.Select(choices=l_maps))


    def clean(self):

        if 'overlap' in self.data:
            return "overlap"
        elif 'all' in self.data:
            return "all"
        return "update"
