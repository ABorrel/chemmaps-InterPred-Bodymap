from django.contrib.staticfiles import finders
from os import listdir
from re import search

from .toolbox import loadMatrixToDict

def assaysMapping(lbody, foldExp):

    prmap = finders.find("bodymap/mapping/assays_%s/"%(foldExp))
    lpmap = listdir(prmap)

    dout = {}
    for bodypart in lbody:
        if not bodypart in list(dout.keys()):
            dout[bodypart] = {}
        for pmap in lpmap:
            print(pmap)
            if search(bodypart, pmap):
                print("hhhh")
                subpart = pmap.split("-")[-1].split("_")[0]
                print(subpart)
                if not subpart in list(dout[bodypart].keys()):
                    dout[bodypart][subpart] = {}
                dassays = loadMatrixToDict(prmap + "/" + pmap)
                for assays in dassays.keys():
                    dout[bodypart][subpart][assays] = {}
                    dout[bodypart][subpart][assays]["gene"] = dassays[assays]["Genes"]
                    dout[bodypart][subpart][assays]["exp"] = float(dassays[assays]["Exp"])
    return dout