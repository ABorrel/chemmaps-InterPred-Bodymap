from django.shortcuts import render
import json
from django.http import HttpResponse, Http404
from os import path, makedirs, remove, listdir, system
from shutil import rmtree
from random import randint

from . import DBrequest
from . import uploadChem
from . import computeDesc
from . import computeOPERA
from . import computeCoords
from . import computeInterPred
from . import chemOverlap
from . import countChem
from . import updateFromFiles
from . import pushAllUpdate
from .forms import updateForm 
from django_server import toolbox


# Create your views here
def push(request):
    
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
    d_DB["coordinate_update"] = cDBrequest.countChemCoordsUpdate()


    # update information from the DB
    cDBrequest.closeConnection()

    return render(request, 'toolchem/push.html', {"d_chem_json":d_DB, "notice":[]})

def index(request):

    # form update
    formUpdate = updateForm()
    cCount = countChem.countChem()
    dcount = cCount.indexCount()
    return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":[], "notice":[]})

def upload_chem(request):

    # open file with
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/")

    # count for index page
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    formUpdate = updateForm(request.POST, request.FILES)
    if request.method == 'POST':
        formout = formUpdate.clean()
        
        map_chem = formUpdate.data["form_map"]
        
        pfileserver = prsession + "uploadFileChem.txt"
        with open(pfileserver, 'wb+') as destination:
            for chunk in formUpdate.files["form_chem"].chunks():
                destination.write(chunk)
        destination.close()

        if formout == "update":
            if map_chem == "---":
                l_error = ["Please choose a map"]
                formUpdate = updateForm()
                return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":l_error})

            #if formUpdate.is_valid() == True:
            cChem = uploadChem.uploadChem(pfileserver, map_chem, prsession)
            cChem.prepChem()
            if cChem.err != []:
                formUpdate = updateForm()
                return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error": cChem.err, "notice":cChem.notice})

            else:
                cChem.pushChemicals()
                formUpdate = updateForm()
                return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "notice":cChem.notice, "dcount":dcount, "error":[]})
        
        else:
            
            cOverlap = chemOverlap.chemOverlap(pfileserver, map_chem, prsession)
            cOverlap.runCheck("dsstox_id")
            cOverlap.prepOutput()

            nb_topush = len(cOverlap.l_topush)
            nb_included = len(cOverlap.l_included)
            nb_noincluded = len(cOverlap.l_noincluded)

            return render(request, 'toolchem/overlap.html', {"nb_included": nb_included, "nb_noincluded": nb_noincluded, "nb_topush":nb_topush, "map": map_chem, "nbChemDescForMap": cOverlap.nbChemDescForMap})

def compute_desc(request):
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/", clean=1)
    cCompDesc = computeDesc.computeDesc(prsession)
    cCompDesc.runDesc()
    
    # count for index page
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    formUpdate = updateForm()
    return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "notice":cCompDesc.notice, "dcount":dcount, "error":cCompDesc.error})

def checkAlreadyComputedDesc(request):
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/")
    cCompDesc = computeDesc.computeDesc(prsession)
    cCompDesc.CheckDescriptorFromMainTable()
    
    # count for index page
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    formUpdate = updateForm()
    return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "notice":cCompDesc.notice, "dcount":dcount, "error":cCompDesc.error})

def compute_opera(request):
    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/OPERA/", clean=1)

    cCompOPERA = computeOPERA.computeOPERA(prsession)
    cCompOPERA.runOPERA()

    # count for index page
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    formUpdate = updateForm()
    return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "notice":cCompOPERA.notice, "dcount":dcount, "error":cCompOPERA.error})

def compute_interference(request):

    prsession = toolbox.createFolder(path.abspath("./temp") + "/update/InterPred/", clean=1)

    # count for index page
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    cCompInterpred = computeInterPred.computeInterPred(prsession)
    if cCompInterpred.prepInterpred() != 1:
        cCompInterpred.predictInterPred()
        cCompInterpred.pushInterPred()

    # clean folder
    rmtree(prsession)
    
    formUpdate = updateForm()
    return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "notice":cCompInterpred.notice,"dcount":dcount, "error":cCompInterpred.error})

def compute_coords(request):

    pr_session = path.abspath("./temp") + "/update/"

    # generate the return information
    # form update
    formUpdate = updateForm()
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    formUpdate = updateForm(request.POST, request.FILES)
    if request.method == 'POST':
        formout = formUpdate.clean()

    map_chem = formUpdate.data["form_map"]
    if map_chem == "---":
        l_error = ["Please choose a map"]
        return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":l_error, "notice":[]})
    else:
        pr_session = pr_session + map_chem + "/"
        toolbox.createFolder(pr_session, clean=1, txt=0)
        if formUpdate.data["specific"] == "Recompute the all map coordinates":
            c_coords = computeCoords.computeCoords(map_chem, pr_session)
            c_coords.computeForAllCoordForMap()
        else:
            c_coords = computeCoords.computeCoords(map_chem, pr_session)
            c_coords.computeCoordForOnlyNewChem()

        return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":c_coords.error, "notice":c_coords.notice})

def upload_datafiles(request):

    a = str(randint(0, 1000000))# define a random number for folder in update to avoid overlap
    #pr_session = toolbox.createFolder(path.abspath("./temp") + "update/coords-" + a + "/")
    pr_session = path.abspath("./temp") + "/update/"

    # generate the return information
    # form update
    cCount = countChem.countChem()
    dcount = cCount.indexCount()

    formUpdate = updateForm(request.POST, request.FILES)
    if request.method == 'POST':
        formout = formUpdate.clean()

    map_chem = formUpdate.data["form_map"]
    if map_chem == "---":
        formUpdate = updateForm()
        l_error = ["Please choose a map"]
        return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":l_error, "notice":[]})
    else:

        c_updateFromFile = updateFromFiles.updateFromFiles(formUpdate, pr_session)
        c_updateFromFile.checkFilesIn()

        return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":c_updateFromFile.error, "notice":c_updateFromFile.notice}) 

def download(request, name):

    name_session = request.session.get("name_session")
    prSession = toolbox.createFolder(path.abspath("./temp") + "/update/")
    file_path = prSession + name + ".csv"
    if path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + path.basename(file_path)
            return response
    raise Http404

def upload_assayfile(request):

    return HttpResponse("Wait for assay format from Agnes")

def clearuserchem(request):

    # open connrection to server
    cDBrequest = DBrequest.DBrequest(verbose=0)
    cDBrequest.openConnection()
    cmd_chemical_users = "DELETE FROM chemicals_user WHERE status = 'user'"
    cDBrequest.DB.updateElement(cmd_chemical_users)
    cmd_chemical_description_users = "DELETE FROM chemical_description_user WHERE status = 'user'"
    cDBrequest.DB.updateElement(cmd_chemical_description_users)

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
    d_DB["coordinate_update"] = cDBrequest.countChemCoordsUpdate()


    # update information from the DB
    cDBrequest.closeConnection()

    return render(request, 'toolchem/push.html', {"d_chem_json":d_DB, "notice":["User enties removed"]})

def pushUpdate(request):

    pr_session = path.abspath("./temp") + "/update/"
    cpush = pushAllUpdate.pushAllUpdate(pr_session)
    cpush.pushAll()

    # form update
    formUpdate = updateForm()
    cCount = countChem.countChem()
    dcount = cCount.indexCount()
    return render(request, 'toolchem/index.html', {"formUpdate":formUpdate, "dcount":dcount, "error":cpush.error, "notice":cpush.notice})
