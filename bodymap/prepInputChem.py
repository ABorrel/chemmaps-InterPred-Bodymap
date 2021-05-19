from os import path
import urllib.request
from re import search

from . import DBrequest


def prepChem(CASIN):

    cDB = DBrequest.DBrequest()
    l_chem = cDB.getRow("bodymap_chemsum", "casn='%s'"%(CASIN))[0]

    try:
        dcas = {}
        dcas["CAS"] = CASIN
        dcas["DSSTOX"] = l_chem[4]
        dcas["Name"] = l_chem[3]
        dcas["SMILES"] = l_chem[2]
        dcas["N-assay"] = l_chem[5]
        dcas["QC"] = l_chem[7]
        return dcas
    except:
        return 1
    
