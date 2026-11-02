from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from re import fullmatch

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
    return render(request, '500.html', status=500)

def index(request):
    toolbox.ensure_session(request)
    return render(request, 'chemmaps/index.html', {"DTXSID":""})

def launchHelp(request, map="all"):
    return render(request, 'chemmaps/help.html', {"map": map})

def download(request, name):
    if name not in toolbox.DOWNLOAD_NAMES:
        raise Http404
    prsession = toolbox.session_dir(request)
    file_path = path.realpath(prsession + name + ".csv")
    if path.commonpath([path.realpath(prsession), file_path]) != path.realpath(prsession):
        raise Http404
    if path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; filename="%s.csv"' % name
            return response
    raise Http404

def launchMap(request, map, *args, **kwargs):

    # load assays from map Tox21
    if map == "tox21":
        cloadAssays = loadAssays()
        d_assays = cloadAssays.assays_to_dict()
    else:
        d_assays = {}

    prsession = toolbox.session_dir(request)

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
            reponse = render(request, 'chemmaps/launchMap.html', {"form_info":formDesc, "form_smiles":form_smiles,
                                                           "from_upload": formUpload, "ErrorLine": "1", "map":map, "dassays":d_assays})
        else:
            prsession = toolbox.session_dir(request)
            toolbox.createFolder(prsession, 1)

            cinput = uploadSMILES(content, prsession)
            cinput.prepListSMILES()

            reponse = render(request, 'chemmaps/smilesprocess.html', {"dSMILESIN": cinput.dclean["IN"], "ERRORSmiles": str(cinput.err),
                                                                "dSMILESOUT": cinput.dclean["OUT"], "map":map})

    elif formUpload.is_valid() == True:

        prsession = toolbox.session_dir(request)
        toolbox.createFolder(prsession, 1)

        pfileserver = prsession + "upload.txt"
        with open(pfileserver, 'wb+') as destination:
            for chunk in formUpload.files["docfile"].chunks():
                destination.write(chunk)
        destination.close()

        try:
            with open(pfileserver, "r") as filin:
                content = filin.read()

            lsmiles = content.split("\n")
            lsmiles = list(dict.fromkeys(lsmiles))
            if len(lsmiles) > 200:
                reponse = render(request, 'chemmaps/launchMap.html', {"form_info": formDesc, "form_smiles": form_smiles,
                                                                   "from_upload": formUpload, "ErrorFile": "1",
                                                                   "map": map, "dassays":d_assays})
            else:
                cinput = uploadSMILES(lsmiles, prsession)
                cinput.prepListSMILES()
                reponse = render(request, 'chemmaps/smilesprocess.html', {"dSMILESIN": cinput.dclean["IN"],
                                                                    "ERRORSmiles": str(cinput.err),
                                                                    "dSMILESOUT": cinput.dclean["OUT"], "map": map})
        except (OSError, UnicodeDecodeError, ValueError):
            reponse = render(
                request,
                "chemmaps/launchMap.html",
                {
                    "form_info": formDesc,
                    "form_smiles": form_smiles,
                    "from_upload": formUpload,
                    "ErrorFile": "1",
                    "map": map,
                    "dassays": d_assays,
                },
            )

    elif formDesc.is_valid() == True:

        ldescMap = formDesc.cleaned_data["desc"]
        if map == "dsstox":
            chemIn = formDesc.cleaned_data['chem']
            if not fullmatch(r"DTXSID\d+", chemIn or ""):
                return render(request, 'chemmaps/launchMap.html', {"form_info": formDesc, "form_smiles": form_smiles,
                                                                "from_upload": formUpload, "Error": "0", "map": map,
                                                                "ErrorDSSTox":"1", "dassays":d_assays})
            build = DSSToxPrep(chemIn, ldescMap, prsession)
            l_dict_out = build.loadChemMapCenterChem(chemIn, center = 1, nbChem = 10000)

            if build.err == 1 or not l_dict_out:
                return render(request, 'chemmaps/launchMap.html', {"form_info": formDesc, "form_smiles": form_smiles,
                                                                "from_upload": formUpload, "Error": "0", "map": map,
                                                                "ErrorDSSTox":"1", "dassays":d_assays})
            dcoord = l_dict_out[0]
            dinfo = l_dict_out[1]
            dneighbor = l_dict_out[3]
            dSMILESClass = l_dict_out[2]
            ldescJS = list(dinfo[list(dinfo.keys())[0]].keys())
            center_chem = chemIn

        else:
            build = JSbuilder(map, list(ldescMap))
            build.loadMap()

            dJS = build.generateJS()
            dcoord = dJS["coord"]
            dinfo = dJS["info"]
            dneighbor = dJS["neighbor"]
            dSMILESClass = dJS["SMILESClass"]
            ldescJS = list(dinfo[list(dinfo.keys())[0]].keys())
            center_chem = ""

        reponse = render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                            "dSMILESClass":dSMILESClass,
                                                            "ldesc":ldescJS, "map":map, "assay":"" , "center_map":center_chem})
    else:
        reponse = render(request, 'chemmaps/launchMap.html', {"form_info":formDesc, "form_smiles":form_smiles,
                                                           "from_upload": formUpload,
                                                           "Error": "1" if "desc" in formDesc.errors else "0",
                                                           "map":map, "dassays":d_assays})
    return reponse

def launchTox21AssayMap(request, assay):

    cloadAssays = loadTox21AssayMap(assay)
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayResults()

    dmap = cloadAssays.dmap
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    return render(request, 'chemmaps/Map3D.html', {"dcoord": dmap["coord"], "dinfo": dmap["info"], "dneighbor": dmap["neighbor"],
                                                             "dSMILESClass": dmap["SMILESClass"],
                                                             "ldesc":ldescJS, "map":"Tox21Assay", "assay":assay, "nb_active": cloadAssays.nb_active, "nb_tested":  cloadAssays.nb_tested })

def launchTox21TagetMap(request, target):


    cloadAssays = loadTox21AssayMap(target)
    cloadAssays.l_desc = ["MolWeight"] # put only MW to add count of active assays by chemicals
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayTargeted()

    dmap = cloadAssays.dmap
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    return render(request, 'chemmaps/Map3D.html', {"dcoord": dmap["coord"], "dinfo": dmap["info"], "dneighbor": dmap["neighbor"],
                                                             "dSMILESClass": dmap["SMILESClass"],
                                                             "ldesc":ldescJS, "map":"Tox21Target", "target":target, "assay":"", "nb_assays": cloadAssays.nb_assays})

def launchTox21MostPotent(request):

    cloadAssays = loadTox21AssayMap("")
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayMostActive()

    dmap = cloadAssays.dmap
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    return render(request, 'chemmaps/Map3D.html', {"dcoord": dmap["coord"], "dinfo": dmap["info"], "dneighbor": dmap["neighbor"],
                                                             "dSMILESClass": dmap["SMILESClass"],
                                                             "ldesc":ldescJS, "map":"Tox21MostActive", "target":"Most active", "assay":"", "nb_assays": cloadAssays.nb_assays})

def browseChemicals(request):

    prsession = toolbox.createFolder(toolbox.session_dir(request))

    c_loadTox21Chem = loadBrowseTox21Chem()
    c_loadTox21Chem.loadAssaysAndChem()
    c_loadTox21Chem.writeTable(prsession)

    return render(request, 'chemmaps/chemicalBrowser.html', {
        "d_chem": c_loadTox21Chem.d_chem,
        "d_assays": c_loadTox21Chem.d_assays,
        "d_fail": c_loadTox21Chem.d_fail,
    })

# case of automatic launch -> Comptox
def launchDSSToxMap(request, DTXSID):

    # fault Ldesc
    ldescMap = ["nbLipinskiFailures", "CoMPARA_Bind_pred", "CERAPP_Bind_pred", "MolWeight",
                                                   "LogP_pred"]

    if not fullmatch(r"DTXSID\d+", DTXSID or ""):
        return render(request, 'chemmaps/index.html', {"DTXSID": DTXSID})

    build = DSSToxPrep(DTXSID, ldescMap, "")
    l_dict_out = build.loadChemMapCenterChem(DTXSID, center = 1, nbChem = 10000)
    if build.err == 1 or not l_dict_out:
        return render(request, 'chemmaps/index.html', {"DTXSID":DTXSID})

    dinfo = l_dict_out[1]
    ldescJS = list(dinfo[list(dinfo.keys())[0]].keys())
    return render(request, 'chemmaps/Map3D.html', {
        "dcoord": l_dict_out[0], "dinfo": dinfo, "dneighbor": l_dict_out[3],
        "dSMILESClass": l_dict_out[2], "ldesc": ldescJS, "map": "dsstox",
        "center_map": DTXSID, "assay": "",
    })

@require_POST
def computeDescriptor(request, map):

    prsession = toolbox.session_dir(request)
    
    dSMI = toolbox.loadMatrixToDict(prsession + "smiClean.csv", sep="\t")

    cinput = uploadSMILES(dSMI, prsession)
    lfileDesc = cinput.computeDesc(map)

    if cinput.err == 1:
        return render(request, 'chemmaps/descriptor.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                            "ddesc":{}, "dSMILESOUT": cinput.dclean["OUT"],
                                                            "ErrorDesc": "1"})

    if "desc" not in request.POST:
        if map == "drugbank":
            formDesc = descDrugMapChoice()
        elif map == "pfas" or map == "tox21":
            formDesc = descDSSToxChoice()
        else:
            formDesc = descDSSToxMapChoice()
        return render(request, 'chemmaps/descriptor.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                            "dSMILESOUT": cinput.dclean["OUT"], "ddesc": cinput.ddesc,
                                                            "form_info": formDesc, "Error": "0"})

    if map == "drugbank":
        formDesc = descDrugMapChoice(request.POST)
    else:
        formDesc = descDSSToxChoice(request.POST)

    if formDesc.is_valid() != True:
        return render(request, 'chemmaps/descriptor.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                            "dSMILESOUT": cinput.dclean["OUT"], "ddesc": cinput.ddesc,
                                                            "form_info": formDesc,
                                                            "Error": "1" if "desc" in formDesc.errors else "0"})

    ldescMap = formDesc.cleaned_data["desc"]
    if map == "dsstox":
        build = JSbuilder(map, ldescMap, prsession)
        build.generateCoords(lfileDesc[0], lfileDesc[1])
        build.findinfoTable()
        build.findneighbor()

        cDSSTox = DSSToxPrep(build.dchemAdd, ldescMap, prsession)
        l_dict_out = cDSSTox.loadChemMapAddMap()
        dcoord = l_dict_out[0]
        dinfo = l_dict_out[1]
        dneighbor = l_dict_out[3]
        dSMILESClass = l_dict_out[2]
        ldesc = list(dinfo[list(dinfo.keys())[0]].keys())
    else:
        build = JSbuilder(map, ldescMap, prsession)
        build.loadMap()
        build.generateCoords(lfileDesc[0], lfileDesc[1])
        build.findinfoTable()
        build.findneighbor()

        dJS = build.generateJS()
        dcoord = dJS["coord"]
        dinfo = dJS["info"]
        dneighbor = dJS["neighbor"]
        dSMILESClass = dJS["SMILESClass"]
        ldesc = list(dinfo[list(dinfo.keys())[0]].keys())

    return render(request, 'chemmaps/Map3D.html', {"dcoord": dcoord, "dinfo": dinfo, "dneighbor": dneighbor,
                                                       "dSMILESClass": dSMILESClass, "ldesc": ldesc,
                                                        "map": map, "assay": ""})
