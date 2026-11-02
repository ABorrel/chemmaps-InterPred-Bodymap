from .DBrequest import DBrequest
from .mapdata import class_text, geometry_rows

DDESCDRUGMAP = {"JCHEM_ROTATABLE_BOND_COUNT":"Rotable bond", "JCHEM_POLAR_SURFACE_AREA": "Polar surface",
               "MOLECULAR_WEIGHT": "Molecular weight", "JCHEM_PHYSIOLOGICAL_CHARGE": "Physio charge",
               "JCHEM_RULE_OF_FIVE": "Rule of five", "JCHEM_VEBER_RULE": "Veber rule", "FORMULA": "Formula",
               "JCHEM_GHOSE_FILTER": "Ghose filter","GENERIC_NAME": "Generic name",
               "JCHEM_TRADITIONAL_IUPAC":"IUPAC", "ALOGPS_SOLUBILITY": "Solubility",
               "JCHEM_MDDR_LIKE_RULE": "MDDR rule", "PRODUCTS": "Product",
               "ALOGPS_LOGP": "ALogP", "JCHEM_PKA_STRONGEST_BASIC": "Pka Basic",
               "JCHEM_NUMBER_OF_RINGS": "Number of rings", "JCHEM_PKA": "PKA",
               "JCHEM_ACCEPTOR_COUNT": "Acceptor count", "JCHEM_PKA_STRONGEST_ACIDIC": "Pka acidic",
               "EXACT_MASS": "Exact mass", "JCHEM_DONOR_COUNT": "Donor count", "INTERNATIONAL_BRANDS": "Brands",
               "JCHEM_AVERAGE_POLARIZABILITY": "Polarizability","JCHEM_BIOAVAILABILITY": "Bioavailability",
               "DATABASE_NAME": "Database", "JCHEM_REFRACTIVITY": "Refractivity", "JCHEM_LOGP": "LogP",
               "JCHEM_FORMAL_CHARGE": "Formal charge", "SALTS": "Salt", "JCHEM_ATOM_COUNT": "Atom count", "SMILES":"SMILES"}

DDESCDSSTOX = {"EPA_category": "EPA category", "LD50_mgkg": "LD50 (mg/kg)",
               "CATMoS_VT_pred": "Acute Tox (very toxic)", "CATMoS_NT_pred": "Acute Tox (no toxic)",
               "CATMoS_EPA_pred": "Acute Tox (EPA)", "CATMoS_GHS_pred": "Acute Tox (GHS)",
               "CATMoS_LD50_pred": "Acute Tox (LD50)", "CERAPP_Ago_pred": "Estrogen Receptor activity (Agonist)",
               "CERAPP_Bind_pred": "Estrogen Receptor activity (binding)", "Clint_pred": "Hepatic clearance",
               "CoMPARA_Anta_pred": "Androgen Receptor Activity (Antogonist)",
               "CoMPARA_Bind_pred": "Androgen Receptor Activity (binding)",
               "FUB_pred": "Plasma fraction unbound", "LogHL_pred": "Henry’s Law constant (atm-mol3/mole)",
               "LogKM_pred": "KM (biotransformation rate)", "LogKOA_pred": "Log Octanol/air partition coefficient",
               "LogKoc_pred": "Log Soil adsorption coefficient (L/Kg)",
               "LogBCF_pred": "Log Fish bioconcentration factor",
               "LogD55_pred": "LogD", "LogP_pred": "LogP", "MP_pred": "Melting Point (C)", "pKa_a_pred": "Pka acid",
               "pKa_b_pred": "Pka basic", "ReadyBiodeg_pred": "Biodegradability", "RT_pred": "HPLC retention time",
               "LogVP_pred": "Log vapor pressure (mmHg)", "LogWS_pred": "Log Water solubility", "MolWeight": "MW",
               "LogOH_pred": "Log Atmospheric constant (cm3/molsec)",
               "BioDeg_LogHalfLife_pred": "Biodegradation half-life",
               "BP_pred": "Boiling Point", "nbLipinskiFailures": "Lipinski Failures",
               "GHS_category": "GHS category",}

def propToDict(ldbprop, ldesc):
    dout = {}
    idx = {desc: i for i, desc in enumerate(ldesc)}
    for chem in ldbprop:
        DB_ID = str(chem[0])
        dout[DB_ID] = {}
        rowvals = chem[1]
        for desc in ldesc:
            i = idx[desc]
            try:
                dout[DB_ID][desc] = round(float(rowvals[i]), 1)
            except (ValueError, TypeError, IndexError):
                dout[DB_ID][desc] = rowvals[i]
    return dout


def coordToDict(lcoord):

    dout = {}
    for chem in lcoord:
        inchikey = str(chem[0])
        dout[inchikey] = [chem[1][0], chem[1][1], chem[2][0]]
    return dout

def NeighborToDict(lneighbors):

    dout = {}
    for chem in lneighbors:
        inchikey = str(chem[0])
        dout[inchikey] = chem[1]
    return dout



class loadingMap:
    def __init__(self, map, lprop):
        self.map = map
        self.DB = DBrequest()
        self.DB.verbose = 0
        self.lprop = lprop


    def loadMap(self):
        dout = {}
        dout["coord"] = {}
        dout["info"] = {}
        dout["neighbor"] = {}
        dout["SMILESClass"] = {}
        dout["inchikey"] = {}

        if self.map not in ("drugbank", "pfas", "tox21"):
            return dout

        lchem = geometry_rows(self.map)
        if not lchem:
            return dout

        dinch = {}
        class_field = "DRUG_GROUPS" if self.map == "drugbank" else "GHS_category"

        for chem in lchem:
            if len(chem) < 8 or chem[3] is None or chem[4] is None or chem[5] is None:
                continue
            inch = chem[2]
            smiles = chem[1]
            db_id = chem[0]
            lneighbors = chem[6]

            dout["coord"][db_id] = [float(chem[3]), float(chem[4]), float(chem[5])]
            dout["SMILESClass"][db_id] = {
                "inchikey": inch,
                "SMILES": smiles,
                class_field: class_text(chem[7]),
            }
            dout["neighbor"][db_id] = lneighbors if lneighbors is not None else []
            dinch[inch] = db_id

        for chem in dout["neighbor"].keys():
            lneighbors_out = []
            for n in dout["neighbor"][chem]:
                try:
                    lneighbors_out.append(dinch[n])
                except KeyError:
                    pass
            dout["neighbor"][chem] = lneighbors_out

        dout["inchikey"] = dinch
        return dout
