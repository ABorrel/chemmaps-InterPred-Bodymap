from .DBrequest import DBrequest

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

        self.DB.connOpen()
        try:
            rows_all = self.DB.extractColoumn(
                "chem_descriptor_opera_name", "name", close_conn=False
            )
            self.lallProp = (
                [prop[0] for prop in rows_all]
                if isinstance(rows_all, list)
                else []
            )

            if map == "drugbank":
                rows_tox = self.DB.extractColoumn(
                    "chem_prop_drugbank_name", "name", close_conn=False
                )
            else:
                rows_tox = self.DB.extractColoumn(
                    "chem_toxexp_name", "name", close_conn=False
                )
            self.lPropTox = (
                [prop[0] for prop in rows_tox]
                if isinstance(rows_tox, list)
                else []
            )
        finally:
            self.DB.connClose()

        self._idx_all = {n: i for i, n in enumerate(self.lallProp)}
        self._idx_tox = {n: i for i, n in enumerate(self.lPropTox)}


    def loadMap(self):
        dout = {}
        dout["coord"] = {}
        dout["info"] = {}
        dout["neighbor"] = {}
        dout["SMILESClass"] = {}
        dout["inchikey"] = {}

        if self.map == "drugbank":
            lchem = self.DB.extractColoumn(
                "mvwchemmap_mapdrugbank",
                "drugbank_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value, prop_tox",
            )
        elif self.map == "pfas":
            lchem = self.DB.extractColoumn(
                "mvwchemmap_mappfas",
                "dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value, prop_tox",
            )
        elif self.map == "tox21":
            lchem = self.DB.extractColoumn(
                "mvwchemmap_maptox21",
                "dsstox_id, smiles_clean, inchikey, dim1d2d[1], dim1d2d[2], dim3d[1], neighbors_dim3, prop_value, prop_tox",
            )
        else:
            lchem = []

        if not isinstance(lchem, list):
            dout["inchikey"] = {}
            return dout

        dinch = {}
        ia = self._idx_all.get
        it = self._idx_tox.get

        for chem in lchem:
            if len(chem) < 9:
                continue
            inch = chem[2]
            smiles = chem[1]
            db_id = chem[0]
            xadd = chem[3]
            yadd = chem[4]
            zadd = chem[5]
            lneighbors = chem[6]
            lprop_row = chem[7]
            lprop_tox = chem[8]

            dout["coord"][db_id] = [float(xadd), float(yadd), float(zadd)]

            dout["info"][db_id] = {}
            for descMap in self.lprop:
                if self.map == "drugbank":
                    ia_i = ia(descMap)
                    it_i = it(descMap)
                    if ia_i is not None:
                        val = lprop_row[ia_i]
                    elif it_i is not None:
                        if lprop_tox is None:
                            val = "NA"
                        else:
                            val = lprop_tox[it_i]
                    else:
                        val = "NA"

                    if val == -9999 or val == "NaN":
                        val = "NA"
                    label = DDESCDRUGMAP.get(descMap)
                    if label is None:
                        continue
                    try:
                        dout["info"][db_id][label] = round(float(val), 1)
                    except (ValueError, TypeError):
                        dout["info"][db_id][label] = val
                else:
                    ia_i = ia(descMap)
                    it_i = it(descMap)
                    if ia_i is not None:
                        if lprop_row is None or lprop_row == []:
                            val = "NA"
                        else:
                            val = lprop_row[ia_i]
                    elif it_i is not None:
                        if lprop_tox is None:
                            val = "NA"
                        else:
                            val = lprop_tox[it_i]
                    else:
                        val = "NA"

                    if val == -9999 or val == "NaN":
                        val = "NA"
                    label = DDESCDSSTOX.get(descMap)
                    if label is None:
                        continue
                    try:
                        dout["info"][db_id][label] = round(float(val), 1)
                    except (ValueError, TypeError):
                        dout["info"][db_id][label] = val


            dout["SMILESClass"][db_id] = {}
            dout["SMILESClass"][db_id]["inchikey"] = inch
            dout["SMILESClass"][db_id]["SMILES"] = smiles


            if self.map == "drugbank":
                dg_i = it("DRUG_GROUPS")
                if lprop_tox is None or dg_i is None:
                    dout["SMILESClass"][db_id]["DRUG_GROUPS"] = "NA"
                else:
                    dout["SMILESClass"][db_id]["DRUG_GROUPS"] = lprop_tox[dg_i]
            else:
                gh_i = it("GHS_category")
                if lprop_tox is None or gh_i is None:
                    dout["SMILESClass"][db_id]["GHS_category"] = "NA"
                else:
                    dout["SMILESClass"][db_id]["GHS_category"] = lprop_tox[gh_i]


            dout["neighbor"][db_id] = lneighbors

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
