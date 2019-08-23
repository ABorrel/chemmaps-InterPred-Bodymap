from django import forms



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


    def clean_run(self):
        if len(self.cleaned_data['bodypart']) == 0:
            return "ERROR"
        return self.cleaned_data['bodypart']



class CASUpload(forms.Form):
    chem = forms.CharField(label="", error_messages={'required': ''}, required=True)

    def clean_chem(self):
        if len(self.cleaned_data['chem']) == "":
            return "ERROR"
        return self.cleaned_data['chem'].upper()
