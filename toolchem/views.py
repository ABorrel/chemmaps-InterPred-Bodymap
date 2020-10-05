from django.shortcuts import render
import json

from . import DBrequest

# Create your views here
def index(request):
    cDBrequest = DBrequest.DBrequest(verbose=0)
    cDBrequest.openConnection()
    # extract information from the DB
    d_DB = {}
    d_DB["All_chem"] = cDBrequest.countChemicals()
    d_DB["All_chem_cleaned"] = cDBrequest.countCleanChemical()
    d_DB["All_chem_desc"] = cDBrequest.countDescFullChemical()
    d_DB["chemmaps_DSSTOXMap"] = cDBrequest.countChemOnDSSTOXMap()
    d_DB["chemmaps_DrugMap"] = cDBrequest.countChemOnDrugMap()
    d_DB["chemmaps_PFASMap"] = cDBrequest.countChemOnPFASMap()
    d_DB["chemmaps_Tox21Map"] = cDBrequest.countChemOnTox21Map()
    d_DB["interpred_chem"] = cDBrequest.countChemInterPred()
    d_DB["bodymap_chem"] = cDBrequest.countChemBodyMap()

    # information from the users table
    d_DB["All_chem_user"] = cDBrequest.countChemUser()
    d_DB["All_chem_desc_user"] = cDBrequest.countDescFullChemUser()
    d_DB["All_chem_update"] = cDBrequest.countChemUpdate()
    d_DB["All_chem_desc_update"] = cDBrequest.countDescFullChemUpdate()


    # update information from the DB
    cDBrequest.closeConnection()

    return render(request, 'toolchem/index.html', {"d_chem_json":d_DB})