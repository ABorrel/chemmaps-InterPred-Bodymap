from django.shortcuts import render
from .forms import bodypartChoice
from random import randint

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

        # do something here

        #cPred = Predict(ldescMap, prsession)
        #cPred.predictAll()
        #dpred = cPred.processResult()
        ## print(dpred)
        #dpredJS = json.dumps(dpred)

        #return render(request, 'interferences/results.html', {"dpred": dpredJS})

    #else:
    #    return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
    #                                                              "dSMILESOUT": cinput.dclean["OUT"],
    #                                                              "ddesc": cinput.ddesc,
    #                                                              "form_model": formModel, "Error": "1"})



