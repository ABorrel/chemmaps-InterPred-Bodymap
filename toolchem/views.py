from django.shortcuts import render
import json
from django.http import HttpResponse
from os import path, makedirs, remove, listdir
from shutil import rmtree

from . import DBrequest
from . import uploadChem
from . import computeDesc
from . import computeOPERA
from . import computeInterPred
from .forms import updateForm 
from django_server import toolbox


# Create your views here
def index(request):
    
    # open connrection to server
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


def AdminForm(request):

    # form update
    formUpdate = updateForm()
    return render(request, 'toolchem/formtest.html', {"formUpdate":formUpdate, "error":[], "notice":[]})



def upload_chem(request):

    # open file with
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/")
    formUpdate = updateForm(request.POST, request.FILES)
    map_chem = formUpdate.data["form_map"]

    #if formUpdate.is_valid() == True:
    pfileserver = prsession + "uploadFileChem.txt"
    with open(pfileserver, 'wb+') as destination:
        for chunk in formUpdate.files["form_chem"].chunks():
            destination.write(chunk)
    destination.close()

    cChem = uploadChem.uploadChem(pfileserver, map_chem, prsession)
    cChem.prepChem()
    if cChem.err != []:
        formUpdate = updateForm()
        return render(request, 'toolchem/formtest.html', {"formUpdate":formUpdate, "error": cChem.err})

    else:
        cChem.pushChemicals()
        formUpdate = updateForm()
        return render(request, 'toolchem/formtest.html', {"formUpdate":formUpdate, "notice":cChem.notice, "error":[]})


def compute_desc(request):
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/")
    cCompDesc = computeDesc.computeDesc(prsession)
    cCompDesc.runDesc()
    

    formUpdate = updateForm()
    return render(request, 'toolchem/formtest.html', {"formUpdate":formUpdate, "notice":cCompDesc.notice, "error":cCompDesc.error})


def compute_opera(request):
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/")
    cCompOPERA = computeOPERA.computeOPERA(prsession)
    cCompOPERA.runOPERA()

    formUpdate = updateForm()
    return render(request, 'toolchem/formtest.html', {"formUpdate":formUpdate, "notice":cCompOPERA.notice, "error":cCompOPERA.error})


def compute_interference(request):
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/")
    cCompInterpred = computeInterPred.computeInterPred(prsession)
    cCompInterpred.runInterpred()

    formUpdate = updateForm()
    return render(request, 'toolchem/formtest.html', {"formUpdate":formUpdate, "notice":cCompInterpred.notice, "error":cCompInterpred.error})
