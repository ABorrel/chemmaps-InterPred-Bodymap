function InfoChemical(dchem){
    var sizeCanvas = resizeCanvas();
    var options = { width: sizeCanvas, height: sizeCanvas };
    var smilesDrawer = new SmilesDrawer.Drawer(options);

    CompoundID.innerHTML = ID;
    
    if (map == 'pfas' || map == 'dsstox' || map == 'tox21') {
        document.getElementById('CompoundID').href =
            'https://comptox.epa.gov/dashboard/chemical/details/' + ID;
    } else if (map == 'drugbank') {
        document.getElementById('CompoundID').href = 'https://www.drugbank.ca/drugs/' + ID;
    }

    // case of DSStoxMap and PFASmap -> GHS
    if (map == 'pfas' || map == 'dsstox' || map == 'tox21') {
        GHS.innerHTML = dSMILESClass[ID]['GHS_category'];
    } else if (map == 'drugbank') {
        Group.innerHTML = dSMILESClass[ID]['DRUG_GROUPS'];
    }

    var ldesc = Object.keys(dinfo[ID]);
    var lboxes = [box1, box2, box3, box4, box5];
    for (var i in ldesc) {
        if (desctype[ldesc[i]] == 'str') {
            if (dinfo[ID][ldesc[i]].length > 50) {
                lboxes[i].innerHTML = dinfo[ID][ldesc[i]].substring(0, 60) + '...';
            } else {
                lboxes[i].innerHTML = dinfo[ID][ldesc[i]];
            }
        } else if (desctype[ldesc[i]] == 'class') {
            lboxes[i].innerHTML = dinfo[ID][ldesc[i]];
        } else if (desctype[ldesc[i]] == 'range') {
            lboxes[i].innerHTML = round(dinfo[ID][ldesc[i]], 2);
        }
    }
    SmilesDrawer.parse(dSMILESClass[ID]['SMILES'], function(tree) {
        // Draw to the canvas
        smilesDrawer.draw(tree, 'Compoundpng2', 'dark', false);
    });

    for (var j = 0; j < lpointload.length; j++) {
        if (lpointload[j] != intersect) {
            lpointload[j].material.color.set(lpointload[j].col);
        }
    }
    lpointload.pop();
    lpointload.push(intersect);
    intersect.material.color.set(0xff0000);
}