from django import forms

class UploadChemList(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "textSMILES"}), label="", error_messages={'required': ''})



class uploadList(forms.Form):
    docfile = forms.FileField()




class QSARModelChoice(forms.Form):

    CHOICES = (("LUCIFERASE","Luciferase"),
               ("AUTOFLUORESCENCE_ALL", "Autofluorescence All"),
               ("AUTOFLUORESCENCE_BLUE", "Autofluorescence Blue"),
               ("AUTOFLUORESCENCE_GREEN", "Autofluorescence Green"),
               ("AUTOFLUORESCENCE_RED", "Autofluorescence Red"),
               ("AUTOFLUORESCENCE_BLUE_HEPG2_CELL", "Autofluorescence Blue HEPG2 Cell Based"),
               ("AUTOFLUORESCENCE_BLUE_HEK293_CELL", "Autofluorescence Blue HEK293 Cell Based"),
               ("AUTOFLUORESCENCE_BLUE_HEPG2_FREE", "Autofluorescence Blue HepG2 Cell Free"),
               ("AUTOFLUORESCENCE_BLUE_HEK293_FREE", "Autofluorescence Blue HepG2 Cell Free"),
               ("AUTOFLUORESCENCE_GREEN_HEPG2_CELL", "Autofluorescence Green HEPG2 Cell Based"),
               ("AUTOFLUORESCENCE_GREEN_HEK293_CELL", "Autofluorescence Green HEK293 Cell Based"),
               ("AUTOFLUORESCENCE_GREEN_HEPG2_FREE", "Autofluorescence Green HepG2 Cell Free"),
               ("AUTOFLUORESCENCE_GREEN_HEK293_FREE", "Autofluorescence Green HepG2 Cell Free"),
               ("AUTOFLUORESCENCE_RED_HEPG2_CELL", "Autofluorescence Red HEPG2 Cell Based"),
               ("AUTOFLUORESCENCE_RED_HEK293_CELL", "Autofluorescence Red HEK293 Cell Based"),
               ("AUTOFLUORESCENCE_RED_HEPG2_FREE", "Autofluorescence Red HepG2 Cell Free"),
               ("AUTOFLUORESCENCE_RED_HEK293_FREE", "Autofluorescence Red HepG2 Cell Free"))

    modelQSAR = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
                       "class": "column-checkbox"}), required=True)

    def clean_desc(self):
        if len(self.cleaned_data['modelQSAR']) == 0:
            return "ERROR"
        return self.cleaned_data['modelQSAR']
