from django.shortcuts import render
import json

from . import DBrequest

# Create your views here
def index(request):
    cDBrequest = DBrequest.DBrequest(verbose=0)

    # extract information from the DB
    d_DB = {}
    d_DB["All_chem"] = cDBrequest.countChemicals()[0][0]
    d_DB["All_chem_cleaned"] = cDBrequest.countCleanChemical()[0][0]
    d_DB["All_chem_desc"] = cDBrequest.countDescFullChemical()[0][0]
    d_DB["chemmaps_DSSTOXMap"] = cDBrequest.countChemOnDSSTOXMap()[0][0]
    d_DB["chemmaps_DrugMap"] = cDBrequest.countChemOnDrugMap()[0][0]
    d_DB["chemmaps_PFASMap"] = cDBrequest.countChemOnPFASMap()[0][0]
    d_DB["chemmaps_Tox21Map"] = cDBrequest.countChemOnTox21Map()[0][0]
    d_DB["interpred_chem"] = cDBrequest.countChemInterPred()[0][0]
    d_DB["bodymap_chem"] = cDBrequest.countChemBodyMap()[0][0]

    # update information from the DB


    return render(request, 'toolchem/index.html', {"d_chem_json":d_DB})