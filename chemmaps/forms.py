from django import forms

class UploadChemList(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "textSMILES"}), error_messages={'required': ''})



class uploadList(forms.Form):
    docfile = forms.FileField()




class descDrugMapChoice(forms.Form):

    CHOICES = (("PRODUCTS", "Product"),("FORMULA", "Formula"),("DATABASE_NAME", "Database"),
               ("GENERIC_NAME", "Generic name"), ("JCHEM_TRADITIONAL_IUPAC","IUPAC"),
               ("INTERNATIONAL_BRANDS", "Brands"),
               ("JCHEM_RULE_OF_FIVE", "Rule of five"), ("JCHEM_VEBER_RULE", "Veber rule"),
               ("JCHEM_MDDR_LIKE_RULE", "MDDR rule"), ("JCHEM_GHOSE_FILTER", "Ghose filter"),
               ("JCHEM_ROTATABLE_BOND_COUNT","Rotable bond"), ("JCHEM_POLAR_SURFACE_AREA", "Polar surface"),
               ("MOLECULAR_WEIGHT", "Molecular weight"), ("JCHEM_PHYSIOLOGICAL_CHARGE", "Physio charge"),
               ("ALOGPS_SOLUBILITY", "ALOG solubility"),("JCHEM_PKA_STRONGEST_BASIC", "Pka Basic"),
               ("JCHEM_PKA_STRONGEST_ACIDIC", "Pka acidic"), ("JCHEM_PKA", "PKA"),
               ("ALOGPS_LOGP", "ALOG LogP"),
               ("JCHEM_NUMBER_OF_RINGS", "Number of rings"),
               ("JCHEM_ACCEPTOR_COUNT", "Acceptor count"),
               ("EXACT_MASS", "Exact mass"), ("JCHEM_DONOR_COUNT", "Donor count"),
               ("JCHEM_AVERAGE_POLARIZABILITY", "Polarizability"),("JCHEM_BIOAVAILABILITY", "Bioavailability"),
               ("JCHEM_REFRACTIVITY", "Refractivity"), ("JCHEM_LOGP", "LogP"),
               ("JCHEM_FORMAL_CHARGE", "Formal charge"), ("SALTS", "Salt"), ("JCHEM_ATOM_COUNT", "Atom count"))


    desc = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple(attrs={
                       "class": "column-checkbox"}), initial= ["MOLECULAR_WEIGHT", "FORMULA", "GENERIC_NAME",
                                                               "ALOGPS_LOGP", "JCHEM_RULE_OF_FIVE"], required=True)

    def clean_desc(self):
        if len(self.cleaned_data['desc']) > 5:
            return "ERROR"
        return self.cleaned_data['desc']




class descDSSToxMapChoice(forms.Form):

        CHOICESDESC = (("EPA_category", "EPA category"), ("LD50_mgkg", "LD50 (mg/kg)"),
                       ("CATMoS_VT_pred", "Acute Tox (very toxic)"), ("CATMoS_NT_pred", "Acute Tox (no toxic)"),
                       ("CATMoS_EPA_pred", "Acute Tox (EPA)"), ("CATMoS_GHS_pred", "Acute Tox (GHS)"),
                       ("CATMoS_LD50_pred", "Acute Tox (LD50)"), ("CERAPP_Ago_pred", "Estrogen Receptor activity (Agonist)"),
                       ("CERAPP_Bind_pred", "Estrogen Receptor activity (binding)"), ("Clint_pred", "Hepatic clearance"),
                       ("CoMPARA_Anta_pred", "Androgen Receptor Activity (Antogonist)"),
                       ("CoMPARA_Bind_pred", "Androgen Receptor Activity (binding)"), ("FUB_pred", "Plasma fraction unbound"),
                       ("LogHL_pred", "Henry’s Law constant (atm-mol3/mole)"), ("LogKM_pred", "KM (biotransformation rate)"),
                       ("LogKOA_pred", "Log Octanol/air partition coefficient"),
                       ("LogKoc_pred", "Log Soil adsorption coefficient (L/Kg)"), ("LogBCF_pred", "Log Fish bioconcentration factor"),
                       ("LogD55_pred", "LogD"), ("LogP_pred", "LogP"), ("MP_pred", "Melting Point (C)"), ("pKa_a_pred", "Pka acid"),
                       ("pKa_b_pred", "Pka basic"), ("ReadyBiodeg_pred", "Biodegradability"),
                       ("RT_pred", "HPLC retention time"), ("LogVP_pred", "Log vapor pressure (mmHg)"),
                       ("LogWS_pred", "Log Water solubility"),
                       ("LogOH_pred", "Log Atmospheric constant (cm3/molsec)"),
                       ("BioDeg_LogHalfLife_pred", "Biodegradation half-life"), ("BP_pred", "Boiling Point"),
                       ("MolWeight", "MW"),
                       ("nbLipinskiFailures", "Lipinski Failures"))




        desc = forms.MultipleChoiceField(choices=CHOICESDESC, widget=forms.CheckboxSelectMultiple(attrs={
            "class": "column-checkbox"}), initial=["nbLipinskiFailures", "CoMPARA_Bind_pred", "CERAPP_Bind_pred", "MolWeight",
                                                   "LogP_pred"], required=True)

        chem = forms.CharField(label="", error_messages={'required': ''}, required=True)



        def clean_desc(self):
            if len(self.cleaned_data['desc']) > 5:
                return "ERROR"
            return self.cleaned_data['desc']


class descDSSToxChoice(forms.Form):
    CHOICESDESC = (("EPA_category", "EPA category"), ("LD50_mgkg", "LD50 (mg/kg)"),
                       ("CATMoS_VT_pred", "Acute Tox (very toxic)"), ("CATMoS_NT_pred", "Acute Tox (no toxic)"),
                       ("CATMoS_EPA_pred", "Acute Tox (EPA)"), ("CATMoS_GHS_pred", "Acute Tox (GHS)"),
                       ("CATMoS_LD50_pred", "Acute Tox (LD50)"), ("CERAPP_Ago_pred", "Estrogen Receptor activity (Agonist)"),
                       ("CERAPP_Bind_pred", "Estrogen Receptor activity (binding)"), ("Clint_pred", "Hepatic clearance"),
                       ("CoMPARA_Anta_pred", "Androgen Receptor Activity (Antogonist)"),
                       ("CoMPARA_Bind_pred", "Androgen Receptor Activity (binding)"), ("FUB_pred", "Plasma fraction unbound"),
                       ("LogHL_pred", "Henry’s Law constant (atm-mol3/mole)"), ("LogKM_pred", "KM (biotransformation rate)"),
                       ("LogKOA_pred", "Log Octanol/air partition coefficient"),
                       ("LogKoc_pred", "Log Soil adsorption coefficient (L/Kg)"), ("LogBCF_pred", "Log Fish bioconcentration factor"),
                       ("LogD55_pred", "LogD"), ("LogP_pred", "LogP"), ("MP_pred", "Melting Point (C)"), ("pKa_a_pred", "Pka acid"),
                       ("pKa_b_pred", "Pka basic"), ("ReadyBiodeg_pred", "Biodegradability"),
                       ("RT_pred", "HPLC retention time"), ("LogVP_pred", "Log vapor pressure (mmHg)"),
                       ("LogWS_pred", "Log Water solubility"),
                       ("LogOH_pred", "Log Atmospheric constant (cm3/molsec)"),
                       ("BioDeg_LogHalfLife_pred", "Biodegradation half-life"), ("BP_pred", "Boiling Point"),
                       ("MolWeight", "MW"),
                       ("nbLipinskiFailures", "Lipinski Failures"))


    desc = forms.MultipleChoiceField(choices=CHOICESDESC, widget=forms.CheckboxSelectMultiple(attrs={
        "class": "column-checkbox"}), initial=["nbLipinskiFailures", "CoMPARA_Bind_pred", "CERAPP_Bind_pred", "MolWeight",
                                               "LogP_pred"], required=True)


    def clean_desc(self):
        if len(self.cleaned_data['desc']) > 5:
            return "ERROR"
        return self.cleaned_data['desc']


