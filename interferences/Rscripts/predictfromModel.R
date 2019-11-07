#!/usr/bin/env Rscript
library (randomForest)
library (MASS)


# function to change the descriptor name => transition python 2 to 3
changeNameDesc1D2D = function(din){

    lold = c("nhyd", "nhal", "nhet", "nhev", "ncof", "ncocl", "ncobr", "ncoi", "ncarb", 
    "nphos", "nsulph", "noxy", "nnitro", "nring", "nrot", "ndonr", "naccr", "nsb", "ndb",
    "naro", "ntb", "nta", "PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "LogP", "LogP2", "MR",
    "W", "AW", "J", "diametert", "radiust", "petitjeant", "kappa1", "kappa2", "kappa3",
    "kappam1", "kappam2", "kappam3", "Sfinger1", "Sfinger2", "Sfinger3", "Sfinger4",
    "Sfinger5", "Sfinger6", "Sfinger7", "Sfinger8", "Sfinger9", "Sfinger10", "Sfinger11",
    "Sfinger12", "Sfinger13", "Sfinger14", "Sfinger15", "Sfinger16", "Sfinger17", 
    "Sfinger18", "Sfinger19", "Sfinger20", "Sfinger21", "Sfinger22", "Sfinger23", 
    "Sfinger24", "Sfinger25", "Sfinger26", "Sfinger27", "Sfinger28", "Sfinger29", 
    "Sfinger30", "Sfinger31", "Sfinger32", "Sfinger33", "Sfinger34", "Sfinger35",
    "Sfinger36", "Sfinger37", "Sfinger38", "Sfinger39", "Sfinger40", "Sfinger41", 
    "Sfinger42", "Sfinger43", "Sfinger44", "Sfinger45", "Sfinger46", "Sfinger47",
    "Sfinger48", "Sfinger49", "Sfinger50", "Sfinger51", "Sfinger52", "Sfinger53", 
    "Sfinger54", "Sfinger55", "Sfinger56", "Sfinger57", "Sfinger58", "Sfinger59", 
    "Sfinger60", "Sfinger61", "Sfinger62", "Sfinger63", "Sfinger64", "Sfinger65", 
    "Sfinger66", "Sfinger67", "Sfinger68", "Sfinger69", "Sfinger70", "Sfinger71", 
    "Sfinger72", "Sfinger73", "Sfinger74", "Sfinger75", "Sfinger76", "Sfinger77", 
    "Sfinger78", "Sfinger79", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", 
    "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", 
    "S22", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31", "S32", "S33", 
    "S34", "S35", "S36", "S37", "S38", "S39", "S40", "S41", "S42", "S43", "S44", "S45",
    "S46", "S47", "S48", "S49", "S50", "S51", "S52", "S53", "S54", "S55", "S56", "S57",
    "S58", "S59", "S60", "S61", "S62", "S63", "S64", "S65", "S66", "S67", "S68", "S69", 
    "S70", "S71", "S72", "S73", "S74", "S75", "S76", "S77", "S78", "S79", "ATSm1", "ATSm2", 
    "ATSm3", "ATSm4", "ATSm5", "ATSm6", "ATSm7", "ATSm8", "ATSv1", "ATSv2", "ATSv3", "ATSv4", 
    "ATSv5", "ATSv6", "ATSv7", "ATSv8", "ATSe1", "ATSe2", "ATSe3", "ATSe4", "ATSe5", "ATSe6", 
    "ATSe7", "ATSe8", "ATSp1", "ATSp2", "ATSp3", "ATSp4", "ATSp5", "ATSp6", "ATSp7", "ATSp8", 
    "Qass", "LabuteASA", "MTPSA", "slogPVSA0", "slogPVSA1", "slogPVSA2", "slogPVSA3",
    "slogPVSA4", "slogPVSA5", "slogPVSA6", "slogPVSA7", "slogPVSA8", "slogPVSA9", "slogPVSA10", 
    "slogPVSA11", "MRVSA0", "MRVSA1", "MRVSA2", "MRVSA3", "MRVSA4", "MRVSA5", "MRVSA6",
    "MRVSA7", "MRVSA8", "MRVSA9", "PEOEVSA0", "PEOEVSA1", "PEOEVSA2", "PEOEVSA3", 
    "PEOEVSA4", "PEOEVSA5", "PEOEVSA6", "PEOEVSA7", "PEOEVSA8", "PEOEVSA9", "PEOEVSA10",
    "PEOEVSA11", "PEOEVSA12", "PEOEVSA13", "VSAEstate0", "VSAEstate1", "VSAEstate2", 
    "VSAEstate3", "VSAEstate4", "VSAEstate5", "VSAEstate6", "VSAEstate7", "VSAEstate8", 
    "VSAEstate9")


    lnew = c("nH", "HalCount", "NumHeteroatoms", "HeavyAtomCount", "Fcount", "ClCount", "BrCount",
    "ICount", "CCount", "PCount", "SCount", "OCount", "NCount", "RingCount", "NumRotatableBonds",
    "NumHDonors", "NumHAcceptors", "SingleBoundCount", "DoubleBoundCount", "ArBoundCount",
    "TripleBoundCount", "NumAllatoms", "Path1Count", "Path2Count", "Path3Count", "Path4Count", 
    "Path5Count", "Path6Count", "MolLogP", "MolLogP2", "MolMR", "Weiner", "Mweiner", 
    "BalabanJ", "diameterPJ", "radiusPJ", "petitjean", "pkappa1", "pkappa2", "pkappa3", 
    "skappa1", "skappa2", "skappa3", "Cfrag1", "Cfrag2", "Cfrag3", "Cfrag4", "Cfrag5", 
    "Cfrag6", "Cfrag7", "Cfrag8", "Cfrag9", "Cfrag10", "Cfrag11", "Cfrag12", "Cfrag13", 
    "Cfrag14", "Cfrag15", "Cfrag16", "Cfrag17", "Cfrag18", "Cfrag19", "Cfrag20", "Cfrag21", 
    "Cfrag22", "Cfrag23", "Cfrag24", "Cfrag25", "Cfrag26", "Cfrag27", "Cfrag28", "Cfrag29", 
    "Cfrag30", "Cfrag31", "Cfrag32", "Cfrag33", "Cfrag34", "Cfrag35", "Cfrag36", "Cfrag37", 
    "Cfrag38", "Cfrag39", "Cfrag40", "Cfrag41", "Cfrag42", "Cfrag43", "Cfrag44", "Cfrag45", 
    "Cfrag46", "Cfrag47", "Cfrag48", "Cfrag49", "Cfrag50", "Cfrag51", "Cfrag52", "Cfrag53", 
    "Cfrag54", "Cfrag55", "Cfrag56", "Cfrag57", "Cfrag58", "Cfrag59", "Cfrag60", "Cfrag61", 
    "Cfrag62", "Cfrag63", "Cfrag64", "Cfrag65", "Cfrag66", "Cfrag67", "Cfrag68", "Cfrag69", 
    "Cfrag70", "Cfrag71", "Cfrag72", "Cfrag73", "Cfrag74", "Cfrag75", "Cfrag76", "Cfrag77", 
    "Cfrag78", "Cfrag79", "SEStatefrag1", "SEStatefrag2", "SEStatefrag3", "SEStatefrag4", 
    "SEStatefrag5", "SEStatefrag6", "SEStatefrag7", "SEStatefrag8", "SEStatefrag9", 
    "SEStatefrag10", "SEStatefrag11", "SEStatefrag12", "SEStatefrag13", "SEStatefrag14", 
    "SEStatefrag15", "SEStatefrag16", "SEStatefrag17", "SEStatefrag18", "SEStatefrag19",
    "SEStatefrag20", "SEStatefrag21", "SEStatefrag22", "SEStatefrag23", "SEStatefrag24", 
    "SEStatefrag25", "SEStatefrag26", "SEStatefrag27", "SEStatefrag28", "SEStatefrag29", 
    "SEStatefrag30", "SEStatefrag31", "SEStatefrag32", "SEStatefrag33", "SEStatefrag34", 
    "SEStatefrag35", "SEStatefrag36", "SEStatefrag37", "SEStatefrag38", "SEStatefrag39", 
    "SEStatefrag40", "SEStatefrag41", "SEStatefrag42", "SEStatefrag43", "SEStatefrag44", 
    "SEStatefrag45", "SEStatefrag46", "SEStatefrag47", "SEStatefrag48", "SEStatefrag49", 
    "SEStatefrag50", "SEStatefrag51", "SEStatefrag52", "SEStatefrag53", "SEStatefrag54",
    "SEStatefrag55", "SEStatefrag56", "SEStatefrag57", "SEStatefrag58", "SEStatefrag59", 
    "SEStatefrag60", "SEStatefrag61", "SEStatefrag62", "SEStatefrag63", "SEStatefrag64", 
    "SEStatefrag65", "SEStatefrag66", "SEStatefrag67", "SEStatefrag68", "SEStatefrag69", 
    "SEStatefrag70", "SEStatefrag71", "SEStatefrag72", "SEStatefrag73", "SEStatefrag74",
    "SEStatefrag75", "SEStatefrag76", "SEStatefrag77", "SEStatefrag78", "SEStatefrag79", 
    "MBAm1", "MBAm2", "MBAm3", "MBAm4", "MBAm5", "MBAm6", "MBAm7", "MBAm8", "MBAv1", 
    "MBAv2", "MBAv3", "MBAv4", "MBAv5", "MBAv6", "MBAv7", "MBAv8", "MBAe1", "MBAe2", 
    "MBAe3", "MBAe4", "MBAe5", "MBAe6", "MBAe7", "MBAe8", "MBAp1", "MBAp2", "MBAp3", 
    "MBAp4", "MBAp5", "MBAp6", "MBAp7", "MBAp8", "Qss", "LabuteASA", "TPSA", "SlogP_VSA1", 
    "SlogP_VSA2", "SlogP_VSA3", "SlogP_VSA4", "SlogP_VSA5", "SlogP_VSA6", "SlogP_VSA7", 
    "SlogP_VSA8", "SlogP_VSA9", "SlogP_VSA10", "SlogP_VSA11", "SlogP_VSA12", "SMR_VSA1", 
    "SMR_VSA2", "SMR_VSA3", "SMR_VSA4", "SMR_VSA5", "SMR_VSA6", "SMR_VSA7", "SMR_VSA8", 
    "SMR_VSA9", "SMR_VSA10", "PEOE_VSA1", "PEOE_VSA2", "PEOE_VSA3", "PEOE_VSA4", 
    "PEOE_VSA5", "PEOE_VSA6", "PEOE_VSA7", "PEOE_VSA8", "PEOE_VSA9", "PEOE_VSA10", 
    "PEOE_VSA11", "PEOE_VSA12", "PEOE_VSA13", "PEOE_VSA14", "VSA_EState1", "VSA_EState2", 
    "VSA_EState3", "VSA_EState4", "VSA_EState5", "VSA_EState6", "VSA_EState7", 
    "VSA_EState8", "VSA_EState9", "VSA_EState10")

    i = 1
    imax = length(lnew)
    while(i <= imax){
        colnames(din)[which(colnames(din) == lnew[i])] = lold[i]
        i = i + 1
    }
    
    return(din)
}


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
print (model)
# open 2D
din2D = read.csv(pdesc2D, sep = "\t", header = TRUE)
rownames(din2D) = din2D[,1]
# del SMILES colunm
din2D = din2D[,-which(colnames(din2D) == "SMILES")]
din2D = din2D[,-which(colnames(din2D) == "inchikey")]
din2D = changeNameDesc1D2D(din2D)
#print(colnames(din2D))


#open OPERA
dinOPERA = read.csv(pdescOPERA, sep = "\t", header = TRUE)
rownames(dinOPERA) = dinOPERA[,1]

lchem = intersect(rownames(din2D), rownames(dinOPERA))
ddesc = cbind(din2D[lchem,], dinOPERA[lchem,])
ddesc = ddesc[,-1]

lpred = predict(model, ddesc)
dout = cbind(lchem, lpred)



colnames(dout) = c("ID", "pred")
rownames(dout) = rownames(dout)

write.csv(dout, pout)
