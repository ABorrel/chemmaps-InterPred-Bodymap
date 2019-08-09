from os import path, makedirs, listdir, remove
from shutil import rmtree

def cleanFolder(prin):

    lfiles = listdir(prin)
    if len(lfiles) != 0:
        for filin in lfiles:
            if filin[-3:] != "txt": # keep descriptor in memory
                # problem with folder
                try:remove(prin + filin)
                except: rmtree(prin + filin)

    return prin


def createFolder(prin, clean=0, mode=""):

    if not path.exists(prin):
        if mode == "":
            makedirs(prin)
        else:
            makedirs(prin)


    if clean == 1:
        cleanFolder(prin)

    return prin



def loadMatrixToDict(pmatrixIn, sep ="\t"):

    filin = open(pmatrixIn, "r")
    llinesMat = filin.readlines()
    filin.close()

    dout = {}
    line0 = formatLine(llinesMat[0])
    line1 = formatLine(llinesMat[1])
    lheaders = line0.split(sep)
    lval1 = line1.split(sep)

    # case where R written
    if len(lheaders) == (len(lval1)-1):
        lheaders.append("val")

    i = 1
    imax = len(llinesMat)
    while i < imax:
        lineMat = formatLine(llinesMat[i])
        lvalues = lineMat.split(sep)
        kin = lvalues[0]
        dout[kin] = {}
        j = 0
        if len(lvalues) != len(lheaders):
            print(lineMat)
            print(llinesMat[i])
            print(lvalues)
            print("Error => nb element", i)
            print(len(lvalues))
            print(len(lheaders))

        jmax = len(lheaders)
        while j < jmax:
            dout[kin][lheaders[j]] = lvalues[j]
            j += 1
        i += 1

    return dout


def formatLine(linein):

    linein = linein.replace("\n", "")
    linenew = ""

    imax = len(linein)
    i = 0
    flagchar = 0
    while i < imax:
        if linein[i] == '"' and flagchar == 0:
            flagchar = 1
        elif linein[i] == '"' and flagchar == 1:
            flagchar = 0

        if flagchar == 1 and linein[i] == ",":
            linenew = linenew + " "
        else:
            linenew = linenew + linein[i]
        i += 1

    linenew = linenew.replace('\"', "")
    return linenew


def formatModelName(nameIn):

    lname = []
    lelem = nameIn.split("_")
    if lelem[0] == "AUTOFLUORESCENCE":
        lname.append("A")
    else:
        lname.append("Luciferace")

    for elem in lelem[1:]:
        if elem == "CELL":
            lname.append("Cell-based")
        elif elem == "FREE":
            lname.append("Cell-free")
        elif elem == "HEPG2":
            lname.append("HepG2")
        elif elem == "HEK293":
            lname.append("HEK293")
        else:
            lname.append(elem.capitalize())

    if len(lname) > 1:
        nameOut = list(" ".join(lname))
        nameOut[1] = "-"
        nameOut = "".join(nameOut)
    else:
        nameOut = lname[0]

    return nameOut
