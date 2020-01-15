from django import forms
from .DBrequest import DBrequest


class bodypartChoice(forms.Form):

    CHOICES = (("Cardiovascular System","Cardiovascular System"),
               ("Digestive System", "Digestive System"),
               ("Endocrine System", "Endocrine System"),
               ("Immune System", "Immune System"),
               ("Musculoskeletal System", "Musculoskeletal System"),
               ("Nervous System", "Nervous System"),
               ("Exocrine System", "Exocrine System"),
               ("Integumentary System", "Integumentary System"),
               ("Olfactory System", "Olfactory System"),
               ("Respiratory System", "Respiratory System"),
               ("Urogenital System", "Urogenital System"),
               ("Visual System", "Visual System"))
            

    bodypart = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
                       "class": "column-checkbox"}), required=True)


    fold = forms.CharField(label="", error_messages={'required': ''}, required=True)

    def clean_run(self):
        if len(self.cleaned_data['bodypart']) == 0:
            return "ERROR"
        return [self.cleaned_data['bodypart'], self.cleaned_data['fold']]



class CASUpload(forms.Form):

    # extract list of available chemical from DB
    cDB = DBrequest(verbose=0)
    lname = cDB.execCMD("SELECT casn, name from chemicals where casn is not NULL ORDER BY name and map_name = 'Tox21Map'")
    lcas = cDB.execCMD("SELECT casn, casn from chemicals where casn is not NULL ORDER BY casn and map_name = 'Tox21Map'")
    

    #for CAS in lCAS:
    #    print(CAS)

    name = forms.CharField(label='name', widget=forms.Select(choices=lname))
    cas = forms.CharField(label='cas', widget=forms.Select(choices=lcas))
    #chem = forms.CharField(label="", error_messages={'required': ''}, required=True, )

    def clean_name(self):
        return str(self.data['name'])
    
    def clean_CAS(self):
        return str(self.data['cas'])




