from django import forms



class bodypartChoice(forms.Form):

    CHOICES = (("Cardiovascular_System","Cardiovascular System"),
               ("Digestive_System", "Digestive System"),
               ("Endocrine_System", "Endocrine System"),
               ("Immune_System", "Immune System"),
               ("Musculoskeletal_System", "Musculoskeletal System"),
               ("Nervous_System", "Nervous System"),
               ("Exocrine_System", "Exocrine System"),
               ("Integumentary_System", "Integumentary System"),
               ("Olfactory_System", "Olfactory System"),
               ("Respiratory_System", "Respiratory System"),
               ("Urogenital_System", "Urogenital System"),
               ("Visual_System", "Visual System"))

    bodypart = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
                       "class": "column-checkbox"}), required=True)


    def clean_run(self):
        if len(self.cleaned_data['bodypart']) == 0:
            return "ERROR"
        return self.cleaned_data['bodypart']