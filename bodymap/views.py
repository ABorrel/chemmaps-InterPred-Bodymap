from django.shortcuts import render
from random import randint
import json


from .forms import bodypartChoice
from .loadMapping import assaysMapping


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
        lBodypart = formBody.clean_run()
        dmap = assaysMapping(lBodypart, 2)
        doutbody = {}
        i = 1
        for bodypart in dmap.keys():
            doutbody[bodypart] = i
            i = i + 1
        dmapJS = json.dumps(dmap)


        return render(request, 'bodymap/tableResults.html', {"dmap": dmapJS, "dbody":doutbody, "Error": "0"})

    else:

        return render(request, 'bodymap/tableResults.html', {"Error": "1"})
    # add error mapping here
    #else:
    #    return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
    #                                                              "dSMILESOUT": cinput.dclean["OUT"],
    #                                                              "ddesc": cinput.ddesc,
    #                                                              "form_model": formModel, "Error": "1"})



