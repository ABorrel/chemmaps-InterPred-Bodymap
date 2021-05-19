from django.shortcuts import render
from random import randint
import json


from .forms import bodypartChoice, CASUpload
from .loadMapping import assaysMapping
from .mapChem import mapChem
from .prepInputChem import prepChem


# Create your views here.
def index(request):

    if not "name_session" in request.session.keys():
        a = randint(0, 1000000)
        request.session.get("name_session", a)
        request.session["name_session"] = a
    return render(request, 'bodymap/index.html', {
    })

def help(request):
    return render(request, 'bodymap/help.html', {
    })


def mappingChemicalToBody(request):


    # form for bodypart
    if request.method == 'GET':
        formCAS = CASUpload()
        return render(request, 'bodymap/chemTobody.html', {"formCAS": formCAS, "Error": "0"})
    else:
        formCAS = CASUpload(request.POST)

    # run map with new chem
    formout = formCAS.clean_upload()
    CAS = formout[0]
    name = formout[1]
    exp_type = formout[2]

    if CAS == "---" and name == "---":
        return render(request, 'bodymap/chemTobody.html', {"formCAS": formCAS, "Error": "1"})
    elif CAS == "---" and name != "---":
        dchem = prepChem(name)
        CAS = name
    elif CAS != "---" and name == "---":
        dchem = prepChem(CAS)
    else:
        return render(request, 'bodymap/chemTobody.html',{"formCAS": formCAS, "Error": "1"})

    if dchem == 1:
        return render(request, 'bodymap/chemTobody.html',{"formCAS": formCAS, "Error": "1"})

    cmapChem = mapChem(CAS)
    cmapChem.loadFromDB("bodymap_assay_mapping_new", "bodymap_assay_ac50", "bodymap_genemap")
    dmap = cmapChem.mapChemToBody(exp_type)
    dmapJS = json.dumps(dmap)
    dchemJS = json.dumps(dchem)
    typeJS = json.dumps("chem")
    NassaysJS = json.dumps(int(dchem["N-assay"]))
    exp_typeJS = json.dumps(exp_type)

    if dchem["QC"] == "FAIL":
        Error_in = "2"
    else:
        Error_in = "0"
    
    return render(request, 'bodymap/ChemMapping.html', {"dmap": dmapJS, "Nassay":NassaysJS, "dchem": dchemJS, "Error": Error_in, "Type":"chem", "TypeJS":typeJS, "exp_type":exp_typeJS})



def mappingChemicalToBodyByCASRN(request, CAS):

    dchem = prepChem(CAS)
    exp_type = "gene"
    if dchem == 1:
        formCAS = CASUpload()
        return render(request, 'bodymap/chemTobody.html',{"formCAS": formCAS, "Error": "1"})

    cmapChem = mapChem(CAS)
    cmapChem.loadFromDB("bodymap_assay_mapping_new", "bodymap_assay_ac50", "bodymap_genemap")
    dmap = cmapChem.mapChemToBody(exp_type)
    dmapJS = json.dumps(dmap)
    dchemJS = json.dumps(dchem)
    typeJS = json.dumps("chem")
    NassaysJS = json.dumps(int(dchem["N-assay"]))
    exp_typeJS = json.dumps(exp_type)

    if dchem["QC"] == "FAIL":
        Error_in = "2"
    else:
        Error_in = "0"
    
    return render(request, 'bodymap/ChemMapping.html', {"dmap": dmapJS, "Nassay":NassaysJS, "dchem": dchemJS, "Error": Error_in, "Type":"chem", "TypeJS":typeJS, "exp_type":exp_typeJS})

