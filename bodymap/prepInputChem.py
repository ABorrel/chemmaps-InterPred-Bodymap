from os import path
import urllib.request
from re import search

from django.db import connection


def prepChem(CASIN):

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM bodymap_chemsum WHERE casn=%s;",[CASIN])
        l_chem = cursor.fetchone()
    
    
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
    
