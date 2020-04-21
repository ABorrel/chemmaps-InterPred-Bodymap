from os import path
import urllib.request
from re import search



def prepChem(CASIN):

    pfchem = path.abspath("./static/bodymap/mapping/ChemSum")
    fchem = open(pfchem, "r")
    dcas = {}
    while dcas == {}:
        try : linestr = fchem.readline()
        except:
            break
        if search(CASIN, linestr):
            lelem = linestr.strip().split("\t")
            dcas["CAS"] = CASIN
            dcas["DSSTOX"] = lelem[1]
            dcas["Name"] = lelem[2]
            dcas["SMILES"] = lelem[3]
            dcas["N-assay"] = lelem[4]
    
    if dcas == {}:
        return 1
    else:
        return dcas
