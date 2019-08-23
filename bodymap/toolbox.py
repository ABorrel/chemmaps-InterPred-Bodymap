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


def createFolder(prin, clean=0):

    if not path.exists(prin):
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


