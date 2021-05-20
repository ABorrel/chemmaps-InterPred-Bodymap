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
            

    bodypart = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(), required=True)


    fold = forms.CharField(label="", error_messages={'required': ''}, required=True)

    def clean_run(self):
        if len(self.cleaned_data['bodypart']) == 0:
            return "ERROR"
        return [self.cleaned_data['bodypart'], self.cleaned_data['fold']]



class CASUpload(forms.Form):

    CHOICES = (("gene", "Gene expression cutoff based on median expression by gene for all organs"), ("organ", "Gene expression cutoff based on organ median expression for all genes"))

    # extract list of available chemical from DB
    cDB = DBrequest(verbose=0)
    lname = cDB.execCMD("SELECT DISTINCT casn, name from bodymap_chemsum WHERE name is not NULL ORDER BY name")
    lcas = cDB.execCMD("SELECT DISTINCT casn, casn from bodymap_chemsum WHERE casn is not NULL ORDER BY casn")

    lcas.insert(0, ("---", "---"))
    lname.insert(0, ("---", "---"))
    name = forms.CharField(label='name', widget=forms.Select(choices=lname))
    cas = forms.CharField(label='cas', widget=forms.Select(choices=lcas))
    #chem = forms.CharField(label="", error_messages={'required': ''}, required=True, )
    exp = forms.CharField(label='expression', widget=forms.RadioSelect(choices=CHOICES), initial="gene", required=True)



    def clean_upload(self):
        return [str(self.data['name']), str(self.data['cas']), str(self.data['exp'])]
    



