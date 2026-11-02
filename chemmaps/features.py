"""Feature catalog for the chemical maps. Labels match the map panel types."""

DRUG_FEATURES = (
    ("PRODUCTS", "Product", "str"),
    ("FORMULA", "Formula", "str"),
    ("DATABASE_NAME", "Database", "str"),
    ("GENERIC_NAME", "Generic name", "str"),
    ("JCHEM_TRADITIONAL_IUPAC", "IUPAC", "str"),
    ("INTERNATIONAL_BRANDS", "Brands", "str"),
    ("JCHEM_RULE_OF_FIVE", "Rule of five", "class"),
    ("JCHEM_VEBER_RULE", "Veber rule", "class"),
    ("JCHEM_MDDR_LIKE_RULE", "MDDR rule", "class"),
    ("JCHEM_GHOSE_FILTER", "Ghose filter", "class"),
    ("JCHEM_ROTATABLE_BOND_COUNT", "Rotable bond", "range"),
    ("JCHEM_POLAR_SURFACE_AREA", "Polar surface", "range"),
    ("MOLECULAR_WEIGHT", "Molecular weight", "range"),
    ("JCHEM_PHYSIOLOGICAL_CHARGE", "Physio charge", "range"),
    ("ALOGPS_SOLUBILITY", "ALOG solubility", "range"),
    ("ALOGPS_LOGP", "ALogP", "range"),
    ("JCHEM_PKA_STRONGEST_BASIC", "Pka Basic", "range"),
    ("JCHEM_NUMBER_OF_RINGS", "Number of rings", "range"),
    ("JCHEM_PKA", "PKA", "range"),
    ("JCHEM_ACCEPTOR_COUNT", "Acceptor count", "range"),
    ("JCHEM_PKA_STRONGEST_ACIDIC", "Pka acidic", "range"),
    ("EXACT_MASS", "Exact mass", "range"),
    ("JCHEM_DONOR_COUNT", "Donor count", "range"),
    ("JCHEM_AVERAGE_POLARIZABILITY", "Polarizability", "range"),
    ("JCHEM_BIOAVAILABILITY", "Bioavailability", "class"),
    ("JCHEM_REFRACTIVITY", "Refractivity", "range"),
    ("JCHEM_LOGP", "LogP", "range"),
    ("JCHEM_FORMAL_CHARGE", "Formal charge", "range"),
    ("SALTS", "Salt", "str"),
    ("JCHEM_ATOM_COUNT", "Atom count", "range"),
)

DSSTOX_FEATURES = (
    ("EPA_category", "EPA category", "class"),
    ("LD50_mgkg", "LD50 (mg/kg)", "range"),
    ("CATMoS_VT_pred", "Acute Tox (very toxic)", "class"),
    ("CATMoS_NT_pred", "Acute Tox (no toxic)", "class"),
    ("CATMoS_EPA_pred", "Acute Tox (EPA)", "class"),
    ("CATMoS_GHS_pred", "Acute Tox (GHS)", "class"),
    ("CATMoS_LD50_pred", "Acute Tox (LD50)", "range"),
    ("CERAPP_Ago_pred", "Estrogen Receptor activity (Agonist)", "class"),
    ("CERAPP_Bind_pred", "Estrogen Receptor activity (binding)", "class"),
    ("Clint_pred", "Hepatic clearance", "range"),
    ("CoMPARA_Anta_pred", "Androgen Receptor Activity (Antogonist)", "class"),
    ("CoMPARA_Bind_pred", "Androgen Receptor Activity (binding)", "class"),
    ("FUB_pred", "Plasma fraction unbound", "range"),
    ("LogHL_pred", "Henry’s Law constant (atm-mol3/mole)", "range"),
    ("LogKM_pred", "KM (biotransformation rate)", "range"),
    ("LogKOA_pred", "Log Octanol/air partition coefficient", "range"),
    ("LogKoc_pred", "Log Soil adsorption coefficient (L/Kg)", "range"),
    ("LogBCF_pred", "Log Fish bioconcentration factor", "range"),
    ("LogD55_pred", "LogD", "range"),
    ("LogP_pred", "LogP", "range"),
    ("MP_pred", "Melting Point (C)", "range"),
    ("pKa_a_pred", "Pka acid", "range"),
    ("pKa_b_pred", "Pka basic", "range"),
    ("ReadyBiodeg_pred", "Biodegradability", "class"),
    ("RT_pred", "HPLC retention time", "range"),
    ("LogVP_pred", "Log vapor pressure (mmHg)", "range"),
    ("LogWS_pred", "Log Water solubility", "range"),
    ("MolWeight", "MW", "range"),
    ("LogOH_pred", "Log Atmospheric constant (cm3/molsec)", "range"),
    ("BioDeg_LogHalfLife_pred", "Biodegradation half-life", "range"),
    ("BP_pred", "Boiling Point", "range"),
    ("nbLipinskiFailures", "Lipinski Failures", "class"),
)

# RDKit columns in the session 2D file for chemicals the user added.
USER_DESCRIPTOR = {
    "MOLECULAR_WEIGHT": "MolWt",
    "MolWeight": "MolWt",
    "JCHEM_ROTATABLE_BOND_COUNT": "NumRotatableBonds",
    "JCHEM_POLAR_SURFACE_AREA": "TPSA",
    "JCHEM_ATOM_COUNT": "NumHeteroatoms",
    "ALOGPS_LOGP": "MolLogP",
    "JCHEM_NUMBER_OF_RINGS": "RingCount",
    "JCHEM_ACCEPTOR_COUNT": "NumHAcceptors",
    "JCHEM_DONOR_COUNT": "NumHDonors",
    "JCHEM_REFRACTIVITY": "MolMR",
}

_BY_MAP = {
    "drugbank": DRUG_FEATURES,
    "dsstox": DSSTOX_FEATURES,
    "tox21": DSSTOX_FEATURES,
    "pfas": DSSTOX_FEATURES,
}


def class_label(map_name):
    if map_name == "drugbank":
        return "Drug group"
    return "GHS category"


def catalog_for(map_name):
    rows = _BY_MAP.get(map_name, ())
    return [{"key": key, "label": label, "type": kind} for key, label, kind in rows]


def feature_by_key(map_name, key):
    for item in catalog_for(map_name):
        if item["key"] == key:
            return item
    return None
