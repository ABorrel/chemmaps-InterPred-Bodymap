#!/usr/bin/env Rscript


factorACP = function (coor_point, vector_arrows){

	factor = 1
	orgin = vector_arrows
	while (max (vector_arrows[,1]) < max (coor_point[,1]) && max (vector_arrows[,2]) < max (coor_point[,2]) && min (vector_arrows[,1]) > min (coor_point[,1]) && min (vector_arrows[,2]) > min (coor_point[,2]) ){
		factor = factor + 1
		vector_arrows[,1] = vector_arrows[,1] + orgin[,1]
		vector_arrows[,2] = vector_arrows[,2] + orgin[,2]

	}
	return (factor-1)

}

openData = function (pfilin, valcor, prout, vexclude){
	
  	desc = read.csv (pfilin, header = TRUE, sep = "\t")
  	print(dim(desc))
	
  	# remove chemical with only NA
  	desc = delete.na(desc, as.integer(0.8*dim(desc)[2]))
  	print(dim(desc))

 	# remove col not well computed
  	desc = t(delete.na(t(desc), as.integer(0.8*dim(desc)[1])))
  	print(dim(desc))
  	#print(desc[2,])

  	# deleted line with NA
  	#rownames (desc) = seq (1, dim(desc)[1])
  	desc = na.omit(desc)
  	#print (dim(desc))
  	cexclude = desc[,vexclude]
  	desc = desc[,-vexclude]
  
 	print(dim(desc))
  
	# dell when sd = 0
	sd_desc = apply (desc[,1:(dim(desc)[2])], 2, sd)

	
	#print ("--------")
	sd_0 = which (sd_desc == 0)
	

	#print ("------------")
	#print (mode(sd_0))
	#print (length (sd_0))
	#print ("------------")
	if ( !is.integer0(sd_0)){
		#print (as.factor (sd_0))
		#desc = desc[,-sd_0]
		desc=subset(desc,select=-sd_0)
		#cexclude = subset(cexclude,select=-sd_0)
		#print(dim(desc_new))
	}
	desc = apply(desc,2,as.double)
	
  print(dim(desc))
	print(valcor)
	#print(head(desc))
	if (valcor != 0){
		out_elimcor = elimcor_sansY (desc, valcor)
		descriptor = out_elimcor$possetap

		#MDSElimcor (desc, out_elimcor, paste (prout, "MDSDesc_", valcor, sep = ""), "corr")
		descriptor = colnames (desc) [descriptor]
		desc = desc[,descriptor]
	}
	print(dim(desc))
  desc = cbind(cexclude, desc)
	return (list((desc),colnames (desc)))
}


#remove SD = 0
delSDnull = function(desc){
  
  sd_desc = apply (desc[,1:(dim(desc)[2])], 2, sd)
  sd_0 = which (sd_desc == 0)
  
  if ( !is.integer0(sd_0)){
    desc=subset(desc,select=-sd_0)
  }
  descout = apply(desc,2,as.double)
  rownames(descout) = rownames(desc)
  return(descout) 
}


delete.na = function(DF, n=0) {
  #print(which(rowSums(is.na(DF)) <= n))
  DF = DF[which(rowSums(is.na(DF)) <= n),]
  return(DF)
}

is.integer0 <- function(x)
{
  is.integer(x) && length(x) == 0L
}


elimcor_sansY<-function(X,s=0.95)
{
  #X matrice contenant les variables à grouper
  #Y vecteur contenant les groupes à prédire
  #s valeur seuil de corrélation
  #print (rownames(X))
  correl=cor(as.matrix(X))
  stop=F
  possetap=1:ncol(X)
  groupes=as.list(1:ncol(X))
  
  while (stop==F)
  {
    ##regroupement des var pour lesquelles |corr|>0.95
    gplist<-list(NULL)
    possglob=1:ncol(correl)
    for (i in 1:(ncol(correl)))
    {
      poss=possglob[-i]
      gplist[[i]]=c(i,poss[which(abs(correl[i,poss])>s)])
    }
    ##on trie les groupes du plus gros au plus petit
    gplisteff=unlist(lapply(gplist,length))
    if (any(gplisteff>1))
    {
      gplistfin=gplist[gplisteff>1]
      gplistuniq=unlist(gplist[gplisteff==1])
      gpsel=NULL
      ##on sélectionne dans chaque groupe une variable au hasard
      for (i in 1:length(gplistfin))
      {
        selloc=min(gplistfin[[i]])
        gploc=groupes[[possetap[selloc]]]
        for (j in 1:length(gplistfin[[i]]))
        {
          gploc=c(gploc,groupes[[possetap[gplistfin[[i]][j]]]])				    }
        groupes[[possetap[selloc]]]=unique(gploc)
        gpsel=c(gpsel,selloc)
      }
      possetap=possetap[c(gplistuniq,unique(gpsel))]
      correl=cor(X[,possetap])
    }
    else stop=T	
  }
  #groupeseff=unlist(lapply(groupes,length))
  #groupes=groupes[groupeseff>1]
  return(list(possetap=possetap,groupes=groupes))
}

delnohomogeniousdistribution = function(din, cutoff = 80){
  dwork = apply(din,2,as.double)
  #print(dwork)
  
  countMax = dim(dwork)[1]*cutoff/100  
  
  i = 1
  imax = dim(dwork)[2]
  while(i <= imax){
    #print (i)
    #print (dwork[,i])
    qt = hist(dwork[,i], breaks = 10, plot = FALSE)$counts
    for (qtc in qt){
      if (qtc >= countMax){
        #dwork = dwork[,-i]
        #imax = imax - 1
        #i = i - 1
        break()
      }
    }
    i = i + 1
  }
    
  rownames(dwork) = rownames(din)
  return(dwork)
}


scaling = function(din){
  
  dinScale = scale(din)
  lscale = attr(dinScale, "scaled:scale")
  lcenter = attr(dinScale, "scaled:center")
  
  dforscaling = rbind(lscale, lcenter)
  rownames(dforscaling) = c("scale", "center")
  
  return(list(dinScale, dforscaling))
  
}


generatePCAcoords = function(dinScale){
  
  data.cor=cor(dinScale)
  data.eigen=eigen(data.cor)
  lambda = data.eigen$values
  var_cap = lambda/sum(lambda)*100
  cp = data.eigen$vectors
  rownames (cp) = colnames (dinScale)
  colnames (cp) = colnames (dinScale)
  data_plot = as.matrix(dinScale)%*%cp
  rownames(data_plot) = rownames(dinScale)
  
  return(list(data_plot, var_cap, cp))
}



prepMatrixDesc = function(pin, valcor, maxquantile, vexclude, homo){
  
  #### 1D2D matrix ####
  #####################
  din = openData(pin, valcor, "", vexclude)
  din_data = din[[1]]
  rownames(din_data) = din_data[,1]
  din_data = din_data[,-1] # remove name
  
  # remove not well distributed descriptors #
  ###########################################
  if(homo == 1){
    din_data = delnohomogeniousdistribution(din_data, maxquantile)
  }else{
    din_temp = apply(din_data,2,as.double)
    rownames(din_temp) = rownames(din_data)
    din_data = din_temp
  }
  din_data = na.omit(din_data)
  
  return(din_data)
  
}



################
#     MAIN     #
################

args <- commandArgs(TRUE)
p1D2D = args[1]
p3D = args[2]
prout = args[3]

# dsstoxmap
#p1D2D = "c://Users/aborr/research/sandbox/chemmaps_data-process/results/updateDSSTOX/coords/1D2D.csv"
#p3D = "c://Users/aborr/research/sandbox/chemmaps_data-process/results/updateDSSTOX/coords/3D.csv"
#prout = "c://Users/aborr/research/sandbox/chemmaps_data-process/results/updateDSSTOX/coords/proj_0.9-90/"
valcor = 0.9
maxquantile = 90


# drugmap
#p3D = "/home/borrela2/ChemMaps/data_analysis/drugBankAnalysis/Desc/3D.csv"
#p1D2D = "/home/borrela2/ChemMaps/data_analysis/drugBankAnalysis/Desc/1D2D.csv"
#valcor = 0.9
#maxquantile = 95
#prout = "/home/borrela2/ChemMaps/data_analysis/drugBankAnalysis/Desc/map/"

d1D2D = prepMatrixDesc(p1D2D, valcor, maxquantile, c(1), 1)
d3D = prepMatrixDesc(p3D, valcor, maxquantile, c(1), 1)

#################
# merge dataset #
#################

vcompound = rownames(d1D2D)
vcompound = intersect(vcompound,rownames(d3D))

d1D2D = d1D2D[vcompound,]
d3D = d3D[vcompound,]

d1D2D = delSDnull(d1D2D)
d3D = delSDnull(d3D)
#########################
#  generate coordinates #
#########################

# scaling
ld1D2Dscale = scaling(d1D2D)
ld3Dscale = scaling(d3D)

write.csv(ld1D2Dscale[[2]], file = paste(prout, "1D2Dscaling.csv", sep = ""))
write.csv(ld3Dscale[[2]], file = paste(prout, "3Dscaling.csv", sep = ""))

dscale1D2D = delSDnull(ld1D2Dscale[[1]])

# generate PCA -1D2D
lcoord = generatePCAcoords(dscale1D2D)
# write cp
write.csv(lcoord[[3]], file=paste(prout, "CP1D2D.csv", sep = ""))
# write coord
dcoord = lcoord[[1]]
colnames(dcoord) = paste("DIM", seq(1,dim(dcoord)[2]), sep = "")
write.csv(dcoord[,1:10], file=paste(prout, "coord1D2D.csv", sep = ""))#plot only 10 dimensions
write.csv(lcoord[[2]], file=paste(prout, "VarPlan1D2D.csv", sep = ""))

dscale3D = delSDnull(ld3Dscale[[1]])

# generate PCA -3D
lcoord = generatePCAcoords(dscale3D)
# write cp
write.csv(lcoord[[3]], file=paste(prout, "CP3D.csv", sep = ""))
# write coord
dcoord = lcoord[[1]]
colnames(dcoord) = paste("DIM3-", seq(1,dim(dcoord)[2]), sep = "")
write.csv(dcoord[,1:10], file=paste(prout, "coord3D.csv", sep = ""))
write.csv(lcoord[[2]], file=paste(prout, "VarPlan3D.csv", sep = ""))
