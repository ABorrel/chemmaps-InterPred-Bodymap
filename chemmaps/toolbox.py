def loadMatrixToDict(pmatrixIn, sep ="\t"):

    filin = open(pmatrixIn, "r", encoding="utf8", errors='ignore')
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
            #print(lineMat)
            #print(llinesMat[i])
            #print(lvalues)
            print("Error => nb element", i)
            #print(len(lvalues))
            #print(len(lheaders))

        jmax = len(lheaders)
        while j < jmax:
            dout[kin][lheaders[j]] = lvalues[j]
            j += 1
        i += 1

    return dout


from os import path, makedirs, listdir, remove
from shutil import rmtree

def cleanFolder(prin):

    lfiles = listdir(prin)
    if len(lfiles) != 0:
        for filin in lfiles:
            pdel = path.abspath(prin + filin)
            try:remove(pdel)
            except: rmtree(pdel)
    return prin


def createFolder(prin, clean=0):

    if not path.exists(prin):
        makedirs(prin)

    if clean == 1:
        cleanFolder(prin)

    return prin

def loadMatrixInfoToDict(pmatrixIn, sep ="\t", ldesc = []):

    filin = open(pmatrixIn, "r", encoding="utf8", errors='ignore')
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
            print("Error => nb element", i)

        jmax = len(lheaders)
        while j < jmax:
            if ldesc != []:
                if lheaders[j] in ldesc:
                    dout[kin][lheaders[j]] = lvalues[j]
            else:
                dout[kin][lheaders[j]] = lvalues[j]
            j += 1
        i += 1

    return dout



def loadMap1D2D3D(pMap):

    dout = {}
    
    pMap1D2D = pMap + "coord1D2D.csv"
    pMap3D = pMap + "coord3D.csv"

    if not path.exists(pMap1D2D) and not path.exists(pMap3D):
        print("Error in loading coord")

    fmap1D2D = open(pMap1D2D, "r")
    fmap3D = open(pMap3D, "r")

    # header
    line1D2D = fmap1D2D.readline()
    line3D = fmap3D.readline()
    # first line
    line1D2D = fmap1D2D.readline()
    line3D = fmap3D.readline()


    while line1D2D != "" and line3D != "":

        l1D2D = line1D2D.strip().split(",")
        l3D = line3D.strip().split(",")

        ID1D2D = l1D2D[0].replace("\"", "")
        ID3D = l3D[0].replace("\"", "")
        if ID1D2D == ID3D:
            dtemp = [float(l1D2D[1]), float(l1D2D[2]), float(l3D[1])]
            dout[ID1D2D] = dtemp

        line1D2D = fmap1D2D.readline()
        line3D = fmap3D.readline()

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




from rdkit import Chem
def convertSMILEStoINCHIKEY(SMILESin):
    molformat = Chem.MolFromSmiles(SMILESin)
    inchi = Chem.inchi.MolToInchi(molformat)
    inchikey = Chem.inchi.InchiToInchiKey(inchi)

    return inchikey


