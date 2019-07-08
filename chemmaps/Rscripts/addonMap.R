#!/usr/bin/env Rscript



scaling = function(din, dscaling){
  
  ldesc = intersect(colnames(dscaling), colnames(din))
  print(dscaling)
  din = din[,ldesc]
  dscaling = dscaling[,ldesc]
  lcenter = as.double(dscaling[2,ldesc])
  lscale = as.double(dscaling[1,ldesc])  
  dout = scale(din, scale=lscale, center= lcenter)
  
  rownames(dout) = rownames(din)
  
  return(dout)
}


computeCoord = function(ddescScale, dCP, col3D){
  
  
  dCP = dCP[colnames(ddescScale), colnames(ddescScale)]
  dcoord = as.matrix(ddescScale)%*%as.matrix(dCP)
  
  if(dim(dcoord)[1] == 1){
    dcoordtemp = data.frame(t(dcoord[,c(1,2)]))
    if(col3D == 1){
      colnames(dcoordtemp) = c("DIM3", "DIM4")
    }else{
      colnames(dcoordtemp) = c("DIM1", "DIM2")
    }
    rownames(dcoordtemp) = rownames(dcoord)
    dcoord = dcoordtemp
    
  }else{
    dcoord = dcoord[,c(1,2)]
    if(col3D == 1){
      colnames(dcoord) = c("DIM3", "DIM4")
    }else{
      colnames(dcoord) = c("DIM1", "DIM2")
    }
  }
  
  return(dcoord)
}


################
#     MAIN     #
################

args <- commandArgs(TRUE)
p1D2D = args[1]
p3D = args[2]
p1D2Dscaling = args[3]
p3Dscaling = args[4]
p1D2DCP = args[5]
p3DCP = args[6]
prout = args[7]

d1D2D = read.csv(p1D2D, sep = "\t", header = TRUE, row.names = 1)
d3D = read.csv(p3D, sep = "\t", header = TRUE, row.names = 1)

d1D2Dscale = read.csv(p1D2Dscaling, sep = ",", row.names = 1)
d3Dscale = read.csv(p3Dscaling, sep = ",", row.names = 1)

d1D2DCP = read.csv(p1D2DCP, sep = ",", row.names = 1)
d3DCP = read.csv(p3DCP, sep = ",", row.names = 1)


# step1 scaling#
################
d1D2Dscale = scaling(d1D2D, d1D2Dscale)
d3Dscale = scaling(d3D, d3Dscale)

# step2 coord #
###############
dcoords1D2D = computeCoord(d1D2Dscale, d1D2DCP, col3D = 0)
write.csv(dcoords1D2D, paste(prout, "coord1D2D.csv", sep = ""))

dcoords3D = computeCoord(d3Dscale, d3DCP, col3D = 1)
write.csv(dcoords3D, paste(prout, "coord3D.csv", sep = ""))
