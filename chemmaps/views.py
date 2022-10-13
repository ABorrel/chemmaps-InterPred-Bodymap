from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import default_storage
from django.template import RequestContext
from random import randint
import json
from re import search

from .forms import UploadChemList, descDrugMapChoice, descDSSToxMapChoice, descDSSToxChoice, uploadList
from .content import uploadSMILES
from .JSbuilder import JSbuilder
from .DSSToxPrep import DSSToxPrep
from .loadAssays import loadAssays
from .loadTox21AssayMap import loadTox21AssayMap
from .loadBrowseTox21Chem import loadBrowseTox21Chem

from os import path

from chemmaps import toolbox


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request, *args, **argv):
    response = render(request,'500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def index(request):

    if not "name_session" in request.session.keys():
        a = randint(0, 1000000)
        request.session.get("name_session", a)
        request.session["name_session"] = a
    return render(request, 'chemmaps/index.html', {"DTXSID":""})

def launchHelp(request, map="all"):
    return render(request, 'chemmaps/help.html', {"map": map})

def download(request, name):

    name_session = request.session.get("name_session")
    prsession = path.abspath("./temp") + "/" + str(name_session) + "/"

    file_path = prsession + name + ".csv"
    if path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + path.basename(file_path)
            return response
    raise Http404

def launchMap(request, map):

    name_session = request.session.get("name_session")

    # load assays from map Tox21
    if map == "tox21":
        cloadAssays = loadAssays()
        d_assays = cloadAssays.DBtoDict("tox21_assays")
    else:
        d_assays = {}
    d_assays = json.dumps(d_assays)

    # open file with
    prsession = path.abspath("./temp") + "/" + str(name_session) + "/"

    # load forms
    if request.method == 'GET':
        form_smiles = UploadChemList()
        if map == "drugbank":
            formDesc = descDrugMapChoice()
        elif map == "pfas" or map == "tox21":
            formDesc = descDSSToxChoice()
        else:
            formDesc = descDSSToxMapChoice()
        formUpload = uploadList()
    else:
        form_smiles = UploadChemList(request.POST)
        if map == "drugbank":
            formDesc = descDrugMapChoice(request.POST)
        elif map == "pfas" or map == "tox21":
            formDesc = descDSSToxChoice(request.POST)
        else:
            formDesc = descDSSToxMapChoice(request.POST)
        formUpload = uploadList(request.POST, request.FILES)


    # If data is valid, proceeds to create a new post and redirect the user
    if form_smiles.is_valid() == True:

        content = form_smiles.cleaned_data["content"]
        content = content.replace("\r", "")
        content = content.split("\n")
        content = list(dict.fromkeys(content))
        if len(content) > 200:
            return render(request, 'chemmaps/launchMap.html', {"form_info":formDesc, "form_smiles":form_smiles,
                                                           "from_upload": formUpload, "ErrorLine": "1", "map":map, "dassays":d_assays})

        prsession = path.abspath("./temp") + "/" + str(name_session) + "/"
        toolbox.createFolder(prsession, 1)

        cinput = uploadSMILES(content, prsession)
        cinput.prepListSMILES()

        return render(request, 'chemmaps/smilesprocess.html', {"dSMILESIN": cinput.dclean["IN"], "ERRORSmiles": str(cinput.err),
                                                            "dSMILESOUT": cinput.dclean["OUT"], "map":map})


    elif formUpload.is_valid() == True:

        prsession = path.abspath("./temp") + "/" + str(name_session) + "/"
        toolbox.createFolder(prsession, 1)

        pfileserver = prsession + "upload.txt"
        with open(pfileserver, 'wb+') as destination:
            for chunk in formUpload.files["docfile"].chunks():
                destination.write(chunk)
        destination.close()

        filin = open(pfileserver, "r")
        try:
            content = filin.read()
            filin.close()

            lsmiles = content.split("\n")
            lsmiles = list(dict.fromkeys(lsmiles))
            if len(lsmiles) > 200:
                return render(request, 'chemmaps/launchMap.html', {"form_info": formDesc, "form_smiles": form_smiles,
                                                                   "from_upload": formUpload, "ErrorFile": "1",
                                                                   "map": map, "dassays":d_assays})
            cinput = uploadSMILES(lsmiles, prsession)
            cinput.prepListSMILES()

            return render(request, 'chemmaps/smilesprocess.html', {"dSMILESIN": cinput.dclean["IN"],
                                                                   "ERRORSmiles": str(cinput.err),
                                                                   "dSMILESOUT": cinput.dclean["OUT"], "map": map})

        except:
            filin.close()
            return render(request, 'chemmaps/launchMap.html', {"form_info": formDesc, "form_smiles": form_smiles,
                                                               "from_upload": formUpload, "ErrorFile": "1", "map": map, "dassays":d_assays})


    elif formDesc.is_valid() == True:

        ldescMap = formDesc.clean_desc()
        if ldescMap == "ERROR":
            return render(request, 'chemmaps/launchMap.html', {"form_info":formDesc, "form_smiles":form_smiles,
                                                           "from_upload": formUpload, "Error": "1", "map":map, "dassays":d_assays})

        if map == "dsstox":
            chemIn = formDesc.cleaned_data['chem']
            build = DSSToxPrep(chemIn, ldescMap, prsession)
            if not search("DTXSID", chemIn):
                build.err = 1
            else:
                build.loadChemMapCenterChem(chemIn, center = 1, nbChem = 10000)
            if build.err == 1:
                return render(request, 'chemmaps/launchMap.html', {"form_info": formDesc, "form_smiles": form_smiles,
                                                                   "from_upload": formUpload, "Error": "0", "map": map,
                                                                   "ErrorDSSTox":"1", "dassays":d_assays})
            dcoord = json.dumps(build.coord)
            dinfo = json.dumps(build.dinfo)
            dneighbor = json.dumps(build.dneighbor)
            dSMILESClass = json.dumps(build.dSMILES)
            ldescJS = list(build.dinfo[list(build.dinfo.keys())[0]].keys())
            center_chem = chemIn


        else:
            build = JSbuilder(map, list(ldescMap))
            build.loadMap()

            dJS = build.generateJS()
            #   format for JS
            dcoord = json.dumps(dJS["coord"])
            dinfo = json.dumps(dJS["info"])
            dneighbor = json.dumps(dJS["neighbor"])
            dSMILESClass = json.dumps(dJS["SMILESClass"])
            ldescJS = list(dJS["info"][list(dJS["info"].keys())[0]].keys())
            center_chem = ""

        mapJS = json.dumps(map)
        prSessionJS = json.dumps(prsession[1:])

        return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                             "dSMILESClass":dSMILESClass,
                                                             "ldesc":ldescJS, "map":map, "mapJS": mapJS,"prSessionJS":prSessionJS, "assay":"" , "center_map":center_chem})

    else:
        return render(request, 'chemmaps/launchMap.html', {"form_info":formDesc, "form_smiles":form_smiles,
                                                           "from_upload": formUpload, "Error": "0", "map":map, "dassays":d_assays})

def launchTox21AssayMap(request, assay):

    
    cloadAssays = loadTox21AssayMap(assay)
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayResults()

    dmap = cloadAssays.dmap

    #   format for JS
    dcoord = json.dumps(dmap["coord"])
    dinfo = json.dumps(dmap["info"])
    dneighbor = json.dumps(dmap["neighbor"])
    dSMILESClass = json.dumps(dmap["SMILESClass"])
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    mapJS = json.dumps("Tox21Assay")
    prSessionJS = json.dumps("")


    return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                             "dSMILESClass":dSMILESClass,
                                                             "ldesc":ldescJS, "map":"Tox21Assay", "mapJS": mapJS, "prSessionJS":prSessionJS, "assay":assay, "nb_active": cloadAssays.nb_active, "nb_tested":  cloadAssays.nb_tested })

def launchTox21TagetMap(request, target):


    cloadAssays = loadTox21AssayMap(target)
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayTargeted()

    dmap = cloadAssays.dmap

    #   format for JS
    dcoord = json.dumps(dmap["coord"])
    dinfo = json.dumps(dmap["info"])
    dneighbor = json.dumps(dmap["neighbor"])
    dSMILESClass = json.dumps(dmap["SMILESClass"])
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    mapJS = json.dumps("Tox21Assay")
    prSessionJS = json.dumps("")


    return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                             "dSMILESClass":dSMILESClass,
                                                             "ldesc":ldescJS, "map":"Tox21Target", "mapJS": mapJS, "prSessionJS":prSessionJS, "target":target, "assay":"", "nb_assays": cloadAssays.nb_assays})#, "nb_active": cloadAssays.nb_active, "nb_tested":  cloadAssays.nb_tested })

def launchTox21MostPotent(request):


    cloadAssays = loadTox21AssayMap("")
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayMostActive()

    dmap = cloadAssays.dmap

    #   format for JS
    dcoord = json.dumps(dmap["coord"])
    dinfo = json.dumps(dmap["info"])
    dneighbor = json.dumps(dmap["neighbor"])
    dSMILESClass = json.dumps(dmap["SMILESClass"])
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    mapJS = json.dumps("Tox21MostActive")
    prSessionJS = json.dumps("")


    return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                             "dSMILESClass":dSMILESClass,
                                                             "ldesc":ldescJS, "map":"Tox21Target", "mapJS": mapJS, "prSessionJS":prSessionJS, "target":"Most active", "assay":"", "nb_assays": cloadAssays.nb_assays})#, "nb_active": cloadAssays.nb_active, "nb_tested":  cloadAssays.nb_tested })

def browseChemicals(request):

    name_session = request.session.get("name_session")
    prsession = toolbox.createFolder(path.abspath("./temp") + "/" + str(name_session) + "/")
    
    c_loadTox21Chem = loadBrowseTox21Chem()
    c_loadTox21Chem.loadAssaysAndChem()
    c_loadTox21Chem.writeTable(prsession)

    d_chem_JS = json.dumps(c_loadTox21Chem.d_chem)
    d_assays_JS = json.dumps(c_loadTox21Chem.d_assays)


    return render(request, 'chemmaps/chemicalBrowser.html', {"d_chem":d_chem_JS, "d_assays":d_assays_JS})

# case of automatic launch -> Comptox
def launchDSSToxMap(request, DTXSID):

    # fault Ldesc
    ldescMap = ["nbLipinskiFailures", "CoMPARA_Bind_pred", "CERAPP_Bind_pred", "MolWeight",
                                                   "LogP_pred"]

    build = DSSToxPrep(DTXSID, ldescMap, "")
    build.loadChemMapCenterChem(DTXSID, center = 1, nbChem = 10000)
    if build.err == 1:
        return render(request, 'chemmaps/index.html', {"DTXSID":DTXSID})

    else:
        dcoord = json.dumps(build.coord)
        dinfo = json.dumps(build.dinfo)
        dneighbor = json.dumps(build.dneighbor)
        dSMILESClass = json.dumps(build.dSMILES)
        ldescJS = list(build.dinfo[list(build.dinfo.keys())[0]].keys())

        mapJS = json.dumps("dsstox")
        prSessionJS = json.dumps("")

        return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor, "dSMILESClass":dSMILESClass, "ldesc":ldescJS, "map":"dsstox", "mapJS": mapJS,"prSessionJS":prSessionJS, "center_map":DTXSID, "assay":"" })

def computeDescriptor(request, map):


    name_session = request.session.get("name_session")
    #print(name_session)

    # open file with
    prsession = path.abspath("./temp") + "/" + str(name_session) + "/"
    
    dSMI = toolbox.loadMatrixToDict(prsession + "smiClean.csv", sep="\t")

    cinput = uploadSMILES(dSMI, prsession)
    lfileDesc = cinput.computeDesc(map)

    if cinput.err == 1:
        return render(request, 'chemmaps/descriptor.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                            "ddesc":{}, "dSMILESOUT": cinput.dclean["OUT"],
                                                            "ErrorDesc": "1"})

    # form for descriptors
    if request.method == 'GET':
        if map == "drugbank":
            formDesc = descDrugMapChoice()
        elif map == "pfas" or map == "tox21":
            formDesc = descDSSToxChoice()
        else:
            formDesc = descDSSToxMapChoice()
    else:
        if map == "drugbank":
            formDesc = descDrugMapChoice(request.POST)
        else:
            formDesc = descDSSToxChoice(request.POST)

    # run map with new chem
    if formDesc.is_valid() == True:
        ldescMap = formDesc.clean_desc()
        if ldescMap == "ERROR":
            return render(request, 'chemmaps/descriptor.html',{"map": map, "dSMILESIN":cinput.dclean["IN"],
                                                            "dSMILESOUT": cinput.dclean["OUT"], "ddesc":cinput.ddesc,
                                                            "form_info": formDesc, "Error": "1"})
        else:
            if map == "dsstox":
                build = JSbuilder(map, ldescMap, prsession)
                build.generateCoords(lfileDesc[0], lfileDesc[1])
                build.findinfoTable()
                build.findneighbor()

                cDSSTox = DSSToxPrep(build.dchemAdd, ldescMap, prsession)
                cDSSTox.loadChemMapAddMap()

                dcoord = json.dumps(cDSSTox.coord)
                dinfo = json.dumps(cDSSTox.dinfo)
                dneighbor = json.dumps(cDSSTox.dneighbor)
                dSMILESClass = json.dumps(cDSSTox.dSMILES)

                ldesc = list(cDSSTox.dinfo[list(cDSSTox.dinfo.keys())[0]].keys())


            else:

                build = JSbuilder(map, ldescMap, prsession)
                build.loadMap()
                # manage new chemical for the JS
                build.generateCoords(lfileDesc[0], lfileDesc[1])# from computed descriptors
                build.findinfoTable()
                build.findneighbor()

                dJS = build.generateJS()
                #   format for JS
                dcoord = json.dumps(dJS["coord"])
                dinfo = json.dumps(dJS["info"])
                dneighbor = json.dumps(dJS["neighbor"])
                dSMILESClass = json.dumps(dJS["SMILESClass"])
                ldesc = list(dJS["info"][list(dJS["info"].keys())[0]].keys())

            prSessionJS = json.dumps(prsession[1:])
            mapJS = json.dumps(map)

        
        print(len(list(dJS["coord"].keys())))
        print(len(list(dJS["info"].keys())))
        print(len(list(dJS["neighbor"].keys())))
        print(len(list(dJS["SMILESClass"].keys())))
        print(len(ldesc))
        return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                           "dSMILESClass": dSMILESClass, "ldesc": ldesc,
                                                            "map": map, "mapJS": mapJS, "prSessionJS":prSessionJS,
                                                            "assay":""})

    else:
        return render(request, 'chemmaps/descriptor.html', {"map": map, "dSMILESIN":cinput.dclean["IN"],
                                                            "dSMILESOUT": cinput.dclean["OUT"], "ddesc":cinput.ddesc,
                                                            "form_info": formDesc, "Error": "0"})




