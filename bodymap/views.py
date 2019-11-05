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



def mappingAssaysBody(request):


    # form for bodypart
    if request.method == 'GET':
        formBody = bodypartChoice()
        return render(request, 'bodymap/assaysTobody.html', {"form_body": formBody, "Error": "0"})
    else:
        formBody = bodypartChoice(request.POST)


    # run map with new chem
    if formBody.is_valid() == True:
        lformout = formBody.clean_run()
        lBodypart = lformout[0]
        fold = lformout[1]
        dmap = assaysMapping(lBodypart, float(fold))
        dmapJS = json.dumps(dmap)
        typeJS = json.dumps("assays")

        return render(request, 'bodymap/tableResults.html', {"dmap": dmapJS, "Error": "0", "Type":"assays", "TypeJS":typeJS,})

    else:

        return render(request, 'bodymap/tableResults.html', {"Error": "1"})
    # add error mapping here
    #else:
    #    return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
    #                                                              "dSMILESOUT": cinput.dclean["OUT"],
    #                                                              "ddesc": cinput.ddesc,
    #                                                              "form_model": formModel, "Error": "1"})



def mappingChemicalToBody(request):


    # form for bodypart
    if request.method == 'GET':
        formCAS = CASUpload()
        return render(request, 'bodymap/chemTobody.html', {"formCAS": formCAS, "Error": "0"})
    else:
        formCAS = CASUpload(request.POST)


    # run map with new chem
    if formCAS.is_valid() == True:
        CAS = formCAS.clean_chem()
        CAS = "10190-99-5"
        dchem = prepChem(CAS)
        if dchem == 1:
            return render(request, 'bodymap/ChemMapping.html', {"Error": "1"})

        cmapChem = mapChem(CAS, 5)
        dmap = cmapChem.mapChemToBody()
        dmapJS = json.dumps(dmap)
        dchemJS = json.dumps(dchem)
        typeJS = json.dumps("chem")


        return render(request, 'bodymap/ChemMapping.html', {"dmap": dmapJS, "dchem": dchemJS, "Error": "0", "Type":"chem", "TypeJS":typeJS})

    else:

        return render(request, 'bodymap/ChemMapping.html', {"Error": "1"})
    # add error mapping here
    #else:
    #    return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
    #                                                              "dSMILESOUT": cinput.dclean["OUT"],
    #                                                              "ddesc": cinput.ddesc,
    #                                                              "form_model": formModel, "Error": "1"})
