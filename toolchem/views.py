from django.shortcuts import render
from django.views.generic import TemplateView

from . import DBrequest

# Create your views here
def index(request):
    cDBrequest = DBrequest.DBrequest(verbose=0)

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



    # update information from the DB
    print(d_DB)
    d_DB_json = json.dumps(d_DB)


    # extract information from the DB

    return render(request, 'toolchem/index.html', {"dcount":d_DB_json})