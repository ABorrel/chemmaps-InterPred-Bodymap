from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from re import fullmatch

from .forms import UploadChemList, uploadList
from .features import feature_by_key
from .mapdata import dsstox_column, full_column, ids_column, user_overrides
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

FEATURE_ROOT = {
    "drugbank": "/chemmaps/DrugMap3D/feature/",
    "dsstox": "/chemmaps/DSSToxMap3D/feature/",
    "tox21": "/chemmaps/Tox21Map3D/feature/",
    "pfas": "/chemmaps/PFASMap3D/feature/",
}


def _order_key(map_name, center):
    return "%s:%s" % (map_name, center or "")


def _remember_ids(request, map_name, center, ids):
    orders = dict(request.session.get("chemmaps_ids") or {})
    orders[_order_key(map_name, center)] = [str(item) for item in ids]
    request.session["chemmaps_ids"] = orders


def _feature_fields(map_name, center, ids, ondemand):
    from .features import catalog_for, class_label
    if not ondemand:
        return {
            "ondemand": False,
            "catalog": [],
            "class_label": "",
            "feature_root": "",
            "chem_ids": [str(item) for item in (ids or [])],
        }
    return {
        "ondemand": True,
        "catalog": catalog_for(map_name),
        "class_label": class_label(map_name),
        "feature_root": FEATURE_ROOT[map_name],
        "chem_ids": [str(item) for item in ids],
        "center_map": center or "",
    }


def _render_catalog_map(request, map_name, dcoord, dneighbor, dsmiles, center):
    ids = [str(item) for item in dcoord.keys()]
    _remember_ids(request, map_name, center, ids)
    context = {
        "dcoord": dcoord,
        "dinfo": {},
        "dneighbor": dneighbor,
        "dSMILESClass": dsmiles,
        "ldesc": [],
        "map": map_name,
        "assay": "",
        "center_map": center or "",
    }
    context.update(_feature_fields(map_name, center, ids, True))
    return render(request, "chemmaps/Map3D.html", context)


def _open_catalog_map(request, map_name, center=""):
    if map_name == "dsstox":
        build = DSSToxPrep(center, [], "")
        loaded = build.loadChemMapCenterChem(center, center=1, nbChem=10000)
        if build.err == 1 or not loaded or not loaded[0]:
            return None
        dcoord, _dinfo, dsmiles, dneighbor = loaded
    else:
        build = JSbuilder(map_name, [])
        build.loadMap()
        generated = build.generateJS()
        dcoord = generated["coord"]
        dneighbor = generated["neighbor"]
        dsmiles = generated["SMILESClass"]
        if not dcoord:
            return None
    return _render_catalog_map(request, map_name, dcoord, dneighbor, dsmiles, center)


def map_feature(request, map, key):
    if feature_by_key(map, key) is None:
        raise Http404
    center = request.GET.get("center", "") or ""
    if center and not fullmatch(r"DTXSID\d+", center):
        raise Http404
    order = (request.session.get("chemmaps_ids") or {}).get(_order_key(map, center))
    if not order:
        raise Http404
    if map == "dsstox" and center:
        column = dsstox_column(center, key)
    elif map == "dsstox":
        column = ids_column(map, key, order)
    else:
        column = full_column(map, key)
    overrides = user_overrides(toolbox.session_dir(request), key)
    values = [overrides.get(chem_id, column.get(chem_id, "NA")) for chem_id in order]
    return JsonResponse({"values": values})


def launchMap(request, map, *args, **kwargs):

    # load assays from map Tox21
    if map == "tox21":
        cloadAssays = loadAssays()
        d_assays = cloadAssays.assays_to_dict()
    else:
        d_assays = {}

    if request.method == "GET" and request.path.rstrip("/").endswith("Map3D"):
        center = ""
        if map == "dsstox":
            center = request.GET.get("center", "") or ""
            if not fullmatch(r"DTXSID\d+", center):
                return render(request, "chemmaps/launchMap.html", {
                    "form_smiles": UploadChemList(),
                    "from_upload": uploadList(),
                    "ErrorDSSTox": "1",
                    "map": map,
                    "dassays": d_assays,
                })
        opened = _open_catalog_map(request, map, center)
        if opened is None:
            return render(request, "chemmaps/launchMap.html", {
                "form_smiles": UploadChemList(),
                "from_upload": uploadList(),
                "ErrorDSSTox": "1" if map == "dsstox" else "0",
                "map": map,
                "dassays": d_assays,
            })
        return opened

    if request.method == 'GET':
        form_smiles = UploadChemList()
        formUpload = uploadList()
    else:
        form_smiles = UploadChemList(request.POST)
        formUpload = uploadList(request.POST, request.FILES)

    launch_context = {
        "form_smiles": form_smiles,
        "from_upload": formUpload,
        "map": map,
        "dassays": d_assays,
    }

    # If data is valid, proceeds to create a new post and redirect the user
    if form_smiles.is_valid() == True:

        content = form_smiles.cleaned_data["content"]
        content = content.replace("\r", "")
        content = content.split("\n")
        content = list(dict.fromkeys(content))
        if len(content) > 200:
            reponse = render(request, 'chemmaps/launchMap.html', dict(launch_context, ErrorLine="1"))
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
                reponse = render(request, 'chemmaps/launchMap.html', dict(launch_context, ErrorFile="1"))
            else:
                cinput = uploadSMILES(lsmiles, prsession)
                cinput.prepListSMILES()
                reponse = render(request, 'chemmaps/smilesprocess.html', {"dSMILESIN": cinput.dclean["IN"],
                                                                    "ERRORSmiles": str(cinput.err),
                                                                    "dSMILESOUT": cinput.dclean["OUT"], "map": map})
        except (OSError, UnicodeDecodeError, ValueError):
            reponse = render(request, "chemmaps/launchMap.html", dict(launch_context, ErrorFile="1"))
    else:
        reponse = render(request, "chemmaps/launchMap.html", launch_context)
    return reponse

def launchTox21AssayMap(request, assay):

    cloadAssays = loadTox21AssayMap(assay)
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayResults()

    dmap = cloadAssays.dmap
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    context = {"dcoord": dmap["coord"], "dinfo": dmap["info"], "dneighbor": dmap["neighbor"],
               "dSMILESClass": dmap["SMILESClass"],
               "ldesc": ldescJS, "map": "Tox21Assay", "assay": assay,
               "nb_active": cloadAssays.nb_active, "nb_tested": cloadAssays.nb_tested}
    context.update(_feature_fields("tox21", "", dmap["coord"].keys(), False))
    return render(request, 'chemmaps/Map3D.html', context)

def launchTox21TagetMap(request, target):


    cloadAssays = loadTox21AssayMap(target)
    cloadAssays.l_desc = ["MolWeight"] # put only MW to add count of active assays by chemicals
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayTargeted()

    dmap = cloadAssays.dmap
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    context = {"dcoord": dmap["coord"], "dinfo": dmap["info"], "dneighbor": dmap["neighbor"],
               "dSMILESClass": dmap["SMILESClass"],
               "ldesc": ldescJS, "map": "Tox21Target", "target": target, "assay": "",
               "nb_assays": cloadAssays.nb_assays}
    context.update(_feature_fields("tox21", "", dmap["coord"].keys(), False))
    return render(request, 'chemmaps/Map3D.html', context)

def launchTox21MostPotent(request):

    cloadAssays = loadTox21AssayMap("")
    cloadAssays.loadMapCoords()
    cloadAssays.loadAssayMostActive()

    dmap = cloadAssays.dmap
    ldescJS = list(dmap["info"][list(dmap["info"].keys())[0]].keys())

    context = {"dcoord": dmap["coord"], "dinfo": dmap["info"], "dneighbor": dmap["neighbor"],
               "dSMILESClass": dmap["SMILESClass"],
               "ldesc": ldescJS, "map": "Tox21MostActive", "target": "Most active", "assay": "",
               "nb_assays": cloadAssays.nb_assays}
    context.update(_feature_fields("tox21", "", dmap["coord"].keys(), False))
    return render(request, 'chemmaps/Map3D.html', context)

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

    if not fullmatch(r"DTXSID\d+", DTXSID or ""):
        return render(request, 'chemmaps/index.html', {"DTXSID": DTXSID})

    opened = _open_catalog_map(request, "dsstox", DTXSID)
    if opened is None:
        return render(request, 'chemmaps/index.html', {"DTXSID": DTXSID})
    return opened

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

    if map == "dsstox":
        build = JSbuilder(map, [], prsession)
        build.generateCoords(lfileDesc[0], lfileDesc[1])
        build.findinfoTable()
        build.findneighbor()

        cDSSTox = DSSToxPrep(build.dchemAdd, [], prsession)
        l_dict_out = cDSSTox.loadChemMapAddMap()
        if not l_dict_out:
            l_dict_out = [{}, {}, {}, {}]
        dcoord = l_dict_out[0]
        dneighbor = l_dict_out[3]
        dSMILESClass = l_dict_out[2]
    else:
        build = JSbuilder(map, [], prsession)
        build.loadMap()
        build.generateCoords(lfileDesc[0], lfileDesc[1])
        build.findinfoTable()
        build.findneighbor()

        dJS = build.generateJS()
        dcoord = dJS["coord"]
        dneighbor = dJS["neighbor"]
        dSMILESClass = dJS["SMILESClass"]

    return _render_catalog_map(request, map, dcoord, dneighbor, dSMILESClass, "")
