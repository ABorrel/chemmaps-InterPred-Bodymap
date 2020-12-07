from django.contrib.staticfiles import finders
from os import listdir, path
from re import search
from .toolbox import loadMatrixToDict, loadToList, openGeneExp


def assaysMapping(lbody, foldExp):

    prmap = finders.find("bodymap/mapping/")
    ppreMap = prmap + "/preMapping.csv"
    lassays_mapped = loadToList(ppreMap)

    # reduce map
    dassays = {}
    for assays in lassays_mapped:
        if assays["type mapping"] == "gene target":
            for bodypart in lbody:
                if not bodypart in list(dassays.keys()):
                    dassays[bodypart] = []
                dassays[bodypart].append(assays)
            continue
        if assays["system"] in lbody:
            if not assays["system"] in list(dassays.keys()):
                dassays[assays["system"]] = []
            dassays[assays["system"]].append(assays)

    dout = {}
    dgene = {}
    for bodypart in dassays.keys():
        if not bodypart in list(dout.keys()):
            dout[bodypart] = {}
        
        for assays in dassays[bodypart]:
            name = assays["Assays"]
            if assays["type mapping"] != "gene target":
                organ = assays["organ"]
                
                if not organ in list(dout[bodypart].keys()):
                    dout[bodypart][organ] = {}
                dout[bodypart][organ][name] = {}
                dout[bodypart][organ][name]["gene"] = "NA"
                dout[bodypart][organ][name]["exp"] = 0.0
            else:
                gene = assays["gene"]
                if gene in list(dgene.keys()):
                    dgenetemp = dgene[gene]
                else:
                    pgene = prmap + "/geneExp/" + str(gene) + ".csv" 
                    if not path.exists(pgene):
                        continue
                    else:
                        dgenetemp = openGeneExp(pgene)
                        dgene[gene] = dgenetemp
                
                if not bodypart in list(dgenetemp.keys()):
                    continue
                for organ in dgenetemp[bodypart].keys():
                    if dgenetemp[bodypart][organ]["control"] == 0.0: 
                        exp = dgenetemp[bodypart][organ]["exp"]
                    else:
                        exp = dgenetemp[bodypart][organ]["exp"] / dgenetemp[bodypart][organ]["control"]
                    if exp >= foldExp:
                        if not organ in list(dout[bodypart].keys()):
                            dout[bodypart][organ] = {}
                        dout[bodypart][organ][name] = {}
                        dout[bodypart][organ][name]["gene"] = gene
                        dout[bodypart][organ][name]["exp"] = exp

    return dout