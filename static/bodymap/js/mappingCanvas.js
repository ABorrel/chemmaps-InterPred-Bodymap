var dmappingBody = {};
dmappingBody["Uterus"] = [100, 280, 410, 280];
dmappingBody["Vagina"] = [100, 280, 410, 280];
dmappingBody["Urethra"] = [100, 280, 410, 280];
dmappingBody["Testes"] = [100, 280, 410, 280];
dmappingBody["Kidney"] = [100, 280, 410, 280];
dmappingBody["Prostate gland"] = [100, 280, 410, 280];
dmappingBody["Placenta"] = [100, 280, 410, 280];
dmappingBody["Ovary"] = [100, 280, 410, 280];
dmappingBody["Penis"] = [100, 280, 410, 280];
dmappingBody["Bladder"] = [100, 280, 410, 280];
dmappingBody[" Mammary gland"] = [100, 280, 410, 280];
dmappingBody["Peritoneum"] = [100, 280, 410, 280];
dmappingBody["Colon"] = [100, 280, 410, 280];
dmappingBody["Tongue"] = [100, 280, 410, 280];
dmappingBody["Liver"] = [100, 280, 410, 280];
dmappingBody["Pancreas"] = [100, 280, 410, 280];
dmappingBody["Salivary gland"] = [100, 280, 410, 280];
dmappingBody["Small intestine"] = [100, 280, 410, 280];
dmappingBody["Stomach"] = [100, 280, 410, 280];
dmappingBody["Esophagus"] = [100, 280, 410, 280];
dmappingBody["Skeletal Muscle"] = [100, 280, 410, 280];
dmappingBody["Joint"] = [100, 280, 410, 280];
dmappingBody["Heart"] = [100, 280, 410, 280];
dmappingBody["Vascular"] = [100, 280, 410, 280];
dmappingBody["Nervous System"] = [100, 280, 410, 280];
dmappingBody["Pituitary gland"] = [100, 280, 410, 280];
dmappingBody["Adrenal gland"] = [100, 280, 410, 280];
dmappingBody["Adipose tissue"] = [100, 280, 410, 280];
dmappingBody["Thyroid"] = [100, 280, 410, 280];
dmappingBody["Adrenal gland"] = [100, 280, 410, 280];
dmappingBody["Immune System"] = [100, 280, 410, 280];
dmappingBody["Lung"] = [100, 280, 410, 280];
dmappingBody["Skin"] = [100, 280, 410, 280];
dmappingBody["Eye"] = [100, 280, 410, 280];


console.log(dmappingBody);

function calibratePosition(){
    var valAC50 =document.getElementById("cutAC50");
    console.log(valAC50); 
    var canvas = document.getElementById("bodymap");
    var ctx = canvas.getContext("2d");

    for(var i=0; i<660; i=i+40){
        for(var j=0; j<804; j=j+40){
            ctx.font = "8px Arial";
            ctx.fillText(String(i) + "-" + String(j), i, j); 
        }
    }
}


function mapbody(din, cutoffAC50){
    var canvas = document.getElementById("bodymap");
    var ctx = canvas.getContext("2d");
    
    ctx.fillStyle = "#1ee844";

    //console.log(dmappingBody);
    console.log(cutoffAC50);

    if(cutoffAC50 > 50){
        ctx.beginPath();
        ctx.arc(100, 75, 20, 0, 2 * Math.PI);
        ctx.fill();
    }else{
        ctx.beginPath();
        ctx.clearRect(100 - 20 - 1, 75 - 20 - 1, 20 * 2 + 2, 20 * 2 + 2);
        ctx.closePath();
    }

}

function cutCircle (context, x, y, radius){
    context.globalCompositeOperation = 'destination-out'
    context.arc(x, y, radius, 0, Math.PI*2, true);
    context.fill();
}