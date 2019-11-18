var dmappingBody = {};
dmappingBody["Uterus"] = [645, 520];
dmappingBody["Vagina"] = [645, 640];
dmappingBody["Urethra"] = [896, 630];
dmappingBody["Testes"] = [845, 650];
dmappingBody["Kidney"] = [280, 415];
dmappingBody["Prostate gland"] = [900, 560];
dmappingBody["Placenta"] = [1000,500];
dmappingBody["Ovary"] = [530, 530];
dmappingBody["Penis"] = [900, 675];
dmappingBody["Bladder"] = [240, 550];
dmappingBody["Mammary gland"] = [170, 320];
dmappingBody["Peritoneum"] = [270, 460];
dmappingBody["Colon"] = [170, 470];
dmappingBody["Tongue"] = [240, 160];
dmappingBody["Liver"] = [180, 360];
dmappingBody["Pancreas"] = [240, 400];
dmappingBody["Salivary gland"] = [240, 120];
dmappingBody["Small intestine"] = [220, 460];
dmappingBody["Stomach"] = [240, 350];
dmappingBody["Esophagus"] = [220, 200];
dmappingBody["Skeletal Muscle"] = [100, 240];
dmappingBody["Joint"] = [100, 420];
dmappingBody["Heart"] = [230, 300];
dmappingBody["Vascular"] = [220, 240];
dmappingBody["Nervous System"] = [210, 40];
dmappingBody["Pituitary gland"] = [210, 80];
dmappingBody["Adrenal gland"] = [350, 200];
dmappingBody["Adipose tissue"] = [320, 460];
dmappingBody["Thyroid"] = [750, 60];
dmappingBody["Immune System"] = [730, 150];
dmappingBody["Lung"] = [250, 270];
dmappingBody["Skin"] = [290, 120];
dmappingBody["Eye"] = [255, 75];





function calibratePosition(){
    var valAC50 =document.getElementById("cutAC50");
    console.log(valAC50); 
    var canvas = document.getElementById("bodymap");
    var ctx = canvas.getContext("2d");

    for(var i=0; i<1050; i=i+40){
        for(var j=0; j<700; j=j+40){
            ctx.font = "8px Arial";
            ctx.fillText(String(i) + "-" + String(j), i, j); 
        }
    }
}


function defineDictOrgan(dmap, valAC50, valExp){

    var dout = {};

    for(assay in dmap){
        for(system in dmap[assay]){
            for(organ in dmap[assay][system]){
                if(!(organ in dout)){
                    dout[organ] = "No";
                }
                if(dout[organ] == "Draw"){
                    continue;
                }

                if(dmap[assay][system][organ]["AC50"] <= valAC50){
                    if(dmap[assay][system][organ]["gene"][0] == "NA"){
                        dout[organ] = "Draw";
                    }else{
                        if (dmap[assay][system][organ]["exp"][0] >= valExp){
                            dout[organ] = "Draw";
                        }
                    }
                }
            }
        }
    }
    return dout;
}

function tellpos(p){
    var posX = p.offsetX - 25;
    var posY = p.offsetY - 25;
    var maxposX = p.offsetX + 25;
    var maxposY = p.offsetY + 25;

    while(posX <= maxposX){
        while(posY <= maxposY){
            try{
                org = dpos[posX][posY];
                if(org != undefined){
                    ctx.fillStyle = "#000000";
                    ctx.fillText(org, dmappingBody[org][0] + 10, dmappingBody[org][1] + 5); 
                    posX = posX + 50;
                    posY = posY + 50;
                }
            }catch{
            }
            
            posY = posY + 1;
        }
        posX = posX + 1;
    }
}       


function labelOrgan(){
    canvas.addEventListener("mousemove", tellpos, false);
}

function mapOnBody(dmap, valAC50, valExp){
    
    ctx.fillStyle = "#1ee844";

    var dorgan = defineDictOrgan(dmap, valAC50, valExp);
    //console.log(dmap);
    //console.log(valAC50);
    //console.log(valExp);
    var lorgani="";
    for(var organ in dorgan){
        if(dorgan[organ] == "Draw"){
            try {ctx.beginPath();
                ctx.arc(dmappingBody[organ][0], dmappingBody[organ][1], 10, 0, 2 * Math.PI);
                ctx.fill();
                lorgani = lorgani + organ + "; ";
            }catch{
                continue;
            }
        }else{
            try {ctx.beginPath();
            ctx.clearRect(dmappingBody[organ][0] - 10 - 1, dmappingBody[organ][1] - 10 - 1, 10 * 2 + 2, 10 * 2 + 2);
            ctx.closePath();
            }catch{
                continue;
            }
        }
    }

    console.log(lorgani);
    var outputOrgan = document.getElementById("organ_active");
    outputOrgan.innerHTML = lorgani;
}



function cutCircle (context, x, y, radius){
    context.globalCompositeOperation = 'destination-out'
    context.arc(x, y, radius, 0, Math.PI*2, true);
    context.fill();
}


function definePosDict(){
    var dout = {};
    for(org in dmappingBody){
        var x = dmappingBody[org][0];
        var y = dmappingBody[org][1];
        if (!(x in dout)){
            dout[x] = {}
        }
        dout[x][y] = org;
    };
    return(dout);
}