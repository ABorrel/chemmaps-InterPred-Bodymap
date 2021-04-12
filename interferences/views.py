from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from random import randint
from os import path
import json

from .forms import uploadList, UploadChemList, QSARModelChoice
from .toolbox import createFolder, loadMatrixToDict
from .content import formatSMILES
from .predictInterference import Predict



def index(request):
    if not "name_session" in request.session.keys():
        a = randint(0, 1000000)
        request.session.get("name_session", a)
        request.session["name_session"] = a

    return render(request, 'interferences/index.html', {
    })

def help(request):
    return render(request, 'interferences/help.html', {
    })

def uploadSMILES(request):

    name_session = request.session.get("name_session")

    if request.method == 'GET':
        form_smiles = UploadChemList()
    else:
        form_smiles = UploadChemList(request.POST)

    formUpload = uploadList(request.POST, request.FILES)


    # If data is valid, proceeds to create a new post and redirect the user
    if form_smiles.is_valid() == True:

        content = form_smiles.cleaned_data["content"]
        content = content.replace("\r", "")
        content = content.split("\n")
        content = list(dict.fromkeys(content))
        if len(content) > 120:
            return render(request, 'interferences/uploadSMILES.html', {"form_smiles":form_smiles,
                                                           "from_upload": formUpload, "ErrorLine": "1"})

        prSession = path.abspath("./temp") + "/" + str(name_session) + "/"
        createFolder(prSession, 1)

        cinput = formatSMILES(content, prSession)
        cinput.prepListSMILES()

        return render(request, 'interferences/cleanSMILES.html',
                          {"dSMILESIN": cinput.dclean["IN"], "ERRORSmiles": str(cinput.err),
                           "dSMILESOUT": cinput.dclean["OUT"]})


    elif formUpload.is_valid() == True:

        prSession = path.abspath("./temp") + "/" + str(name_session) + "/"
        createFolder(prSession, 1)

        pfileserver = prSession + "upload.txt"
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
            if len(lsmiles) > 100:
                return render(request, 'chemmaps/uploadSMILES.html', {"form_smiles":form_smiles,
                                                           "from_upload": formUpload, "ErrorFile": "1"})
            cinput = formatSMILES(lsmiles, prSession)
            cinput.prepListSMILES()

            return render(request, 'interferences/cleanSMILES.html',
                          {"dSMILESIN": cinput.dclean["IN"], "ERRORSmiles": str(cinput.err),
                           "dSMILESOUT": cinput.dclean["OUT"]})

        except:
            filin.close()
            return render(request, 'chemmaps/uploadSMILES.html', {"form_smiles":form_smiles,
                                                           "from_upload": formUpload, "ErrorFile": "1"})


    return render(request, 'interferences/uploadSMILES.html', {"form_smiles":form_smiles,
                                                           "from_upload": formUpload, "ErrorLine": "0"})

def computeDesc(request):

    name_session = request.session.get("name_session")

    # open file with
    prsession = path.abspath("./temp") + "/" + str(name_session) + "/"
    dSMI = loadMatrixToDict(prsession + "smiClean.csv", sep="\t")

    cinput = formatSMILES(dSMI, prsession)
    lfileDesc = cinput.computeDesc()

    if cinput.err == 1:
        return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                                  "ddesc": cinput.ddesc,
                                                                  "dSMILESOUT": cinput.dclean["OUT"],
                                                                  "ErrorDesc": "1"})
    # form for descriptors
    if request.method == 'GET':
        formModel = QSARModelChoice()
        return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                                  "dSMILESOUT": cinput.dclean["OUT"],
                                                                  "ddesc": cinput.ddesc,
                                                                  "form_model": formModel, "Error": "0"})
    else:
        formModel = QSARModelChoice(request.POST)

    # run map with new chem
    if formModel.is_valid() == True:
        ldescMap = formModel.clean_desc()
        inDB = ldescMap[1]
        ldescMap = ldescMap[0]

        cPred = Predict(ldescMap, inDB, prsession)
        cPred.predictAll()
        cPred.processResult()
        #print(dpred)
        dpredJS = json.dumps(cPred.dpred)

        return render(request, 'interferences/results.html', {"dpred":dpredJS})

    else:
        return render(request, 'interferences/computeDESC.html', {"map": map, "dSMILESIN": cinput.dclean["IN"],
                                                                 "dSMILESOUT": cinput.dclean["OUT"],
                                                                 "ddesc": cinput.ddesc,
                                                                 "form_model": formModel, "Error": "1"})

def download(request, name):

    name_session = request.session.get("name_session")
    prSession = path.abspath("./temp") + "/" + str(name_session) + "/"
    file_path = prSession + name + ".csv"
    if path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + path.basename(file_path)
            return response
    raise Http404

