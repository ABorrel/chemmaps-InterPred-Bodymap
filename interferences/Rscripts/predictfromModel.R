#!/usr/bin/env Rscript
library (randomForest)



################
#     MAIN     #
################
args <- commandArgs(TRUE)
pdesc2D = args[1]
pdescOPERA = args[2]
pmodel = args[3]
pout = args[4]


#pdesc2D = "./interferences/temp/376251/2D.csv"
#pdescOPERA = "./interferences/temp/376251/OPERA.csv"
#pmodel = "./interferences/static/interferences/models/AUTOFLUORESCENCE_BLUE/model7.Rdata"
#pout = "./interferences/temp/376251/temp.txt"


load(pmodel)
model = outmodel$model

# open 2D
din2D = read.csv(pdesc2D, sep = "\t", header = TRUE)
rownames(din2D) = din2D[,1]
# del SMILES colunm
din2D =din2D[,-which(colnames(din2D) == "SMILES")]

#open OPERA
dinOPERA = read.csv(pdescOPERA, sep = "\t", header = TRUE)
rownames(dinOPERA) = dinOPERA[,1]

lchem = intersect(rownames(din2D), rownames(dinOPERA))
ddesc = cbind(din2D[lchem,], dinOPERA[lchem,])
ddesc = ddesc[,-1]

#print(ddesc)
lpred = predict(model, ddesc)
dout = cbind(lchem, lpred)

colnames(dout) = c("ID", "pred")
rownames(dout) = rownames(dout)

write.csv(dout, pout)
