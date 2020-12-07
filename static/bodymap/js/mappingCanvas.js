var dmappingBody = {};
dmappingBody["Uterus"] = [400, 560];
dmappingBody["Placenta"] = [400, 550];
dmappingBody["Vagina"] = [400, 602];
dmappingBody["Urethra"] = [415, 600];
dmappingBody["Testes"] = [425, 625];
dmappingBody["Kidney"] = [440, 475];
dmappingBody["Prostate gland"] = [415, 595];
dmappingBody["Ovary"] = [370, 560];
dmappingBody["Penis"] = [415, 615];
dmappingBody["Bladder"] = [427, 585];
dmappingBody["Mammary gland"] = [355, 355];
dmappingBody["Peritoneum"] = [352, 322];
dmappingBody["Colon"] = [405, 615];
dmappingBody["Tongue"] = [403, 205];
dmappingBody["Liver"] = [360, 427];
dmappingBody["Pancreas"] = [395, 462];
dmappingBody["Salivary gland"] = [415, 214];
dmappingBody["Small intestine"] = [430, 520];
dmappingBody["Stomach"] = [430, 432];
dmappingBody["Esophagus"] = [408, 270];
dmappingBody["Skeletal Muscle"] = [465, 270];
dmappingBody["Joint"] = [345, 575];
dmappingBody["Heart"] = [410, 350];
dmappingBody["Vascular"] = [320, 385];
dmappingBody["Nervous System"] = [375, 160];
dmappingBody["Pituitary gland"] = [411, 145];
dmappingBody["Adrenal gland"] = [380, 463];
dmappingBody["Adipose tissue"] = [360, 460];
dmappingBody["Thyroid"] = [408, 250]
dmappingBody["Immune System"] = [440, 145];
dmappingBody["Lung"] = [446, 326];
dmappingBody["Skin"] = [345, 285];
dmappingBody["Eye"] = [386, 168];





function calibratePosition(){
    var valAC50 =document.getElementById("cutAC50");
    var canvas = document.getElementById("bodymap");
    var ctx = canvas.getContext("2d");

    for(var i=0; i<720; i=i+40){
        for(var j=0; j<825; j=j+40){
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
                    continue;
                }
                if(dout[organ] == "Draw-cyan"){
                    continue;
                }
                if(dmap[assay][system][organ]["AC50"] <= valAC50){
                    if(dmap[assay][system][organ]["gene"][0] == "NA"){
                        dout[organ] = "Draw-blue";
                    }else{
                        if (dmap[assay][system][organ]["exp"][0] >= valExp && dout[organ] == "Draw-blue"){
                            dout[organ] = "Draw-cyan";
                        }
                        else if (dmap[assay][system][organ]["exp"][0] >= valExp && dout[organ] != "Draw-blue"){
                            dout[organ] = "Draw-green";
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
    
    

    var dorgan = defineDictOrgan(dmap, valAC50, valExp);
    //console.log(dmap);
    //console.log(valAC50);
    //console.log(valExp);
    var lorgani="";
    ctx.drawImage(background,0,0);
    for(var organ in dorgan){
        if(dorgan[organ] == "Draw-green"){
            ctx.fillStyle = "#1ee844";
            try {ctx.beginPath();
                ctx.arc(dmappingBody[organ][0], dmappingBody[organ][1], 7, 0, 2 * Math.PI);
                ctx.fill();
                lorgani = lorgani + organ + "; ";
            }catch{
                continue;
            }
        }else if(dorgan[organ] == "Draw-blue"){
            ctx.fillStyle = "#282ab5";
            try {ctx.beginPath();
                ctx.arc(dmappingBody[organ][0], dmappingBody[organ][1], 7, 0, 2 * Math.PI);
                ctx.fill();
                lorgani = lorgani + organ + "; ";
            }catch{
                continue;
            }
        }else if(dorgan[organ] == "Draw-cyan"){
            ctx.fillStyle = "#2bfafa";
            try {ctx.beginPath();
                ctx.arc(dmappingBody[organ][0], dmappingBody[organ][1], 7, 0, 2 * Math.PI);
                ctx.fill();
                lorgani = lorgani + organ + "; ";
            }catch{
                continue;
            }
        }else{

        }
    }

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