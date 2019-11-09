var dmappingBody = {};
dmappingBody["Uterus"] = [640, 520];
dmappingBody["Vagina"] = [640, 640];
dmappingBody["Urethra"] = [890, 640];
dmappingBody["Testes"] = [840, 650];
dmappingBody["Kidney"] = [280, 420];
dmappingBody["Prostate gland"] = [900, 560];
dmappingBody["Placenta"] = [1000,500];
dmappingBody["Ovary"] = [520, 530];
dmappingBody["Penis"] = [900, 670];
dmappingBody["Bladder"] = [220, 560];
dmappingBody[" Mammary gland"] = [160, 320];
dmappingBody["Peritoneum"] = [241, 460];
dmappingBody["Colon"] = [170, 460];
dmappingBody["Tongue"] = [260, 160];
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
dmappingBody["Nervous System"] = [220, 50];
dmappingBody["Pituitary gland"] = [220, 80];
dmappingBody["Adrenal gland"] = [350, 200];
dmappingBody["Adipose tissue"] = [320, 460];
dmappingBody["Thyroid"] = [750, 60];
dmappingBody["Immune System"] = [730, 150];
dmappingBody["Lung"] = [250, 270];
dmappingBody["Skin"] = [280, 120];
dmappingBody["Eye"] = [250, 65];




console.log(dmappingBody);

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


function defineDictOrgan(dmap,valAC50, valExp){

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



function mapOnBody(dmap, valAC50, valExp){
    var canvas = document.getElementById("bodymap");
    var ctx = canvas.getContext("2d");
    
    ctx.fillStyle = "#1ee844";

    var dorgan = defineDictOrgan(dmap, valAC50, valExp);
    console.log(dmap);
    console.log(valAC50);
    console.log(valExp);

    for(organ in dorgan){
        if(dorgan[organ] == "Draw"){
            ctx.beginPath();
            ctx.arc(dmappingBody[organ][0], dmappingBody[organ][1], 12, 0, 2 * Math.PI);
            ctx.fill();
        }else{
            ctx.beginPath();
            ctx.clearRect(dmappingBody[organ][0] - 20 - 1, dmappingBody[organ][1] - 20 - 1, 20 * 2 + 2, 20 * 2 + 2);
            ctx.closePath();
        }
    }
}

function cutCircle (context, x, y, radius){
    context.globalCompositeOperation = 'destination-out'
    context.arc(x, y, radius, 0, Math.PI*2, true);
    context.fill();
}