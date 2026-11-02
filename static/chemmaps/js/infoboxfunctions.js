//have to be fix and generalized
function updateInfoBox(intersect) {
    var sizeCanvas = resizeCanvas();
    var options = { width: sizeCanvas, height: sizeCanvas };
    var smilesDrawer = new SmilesDrawer.Drawer(options);

    CompoundID.textContent = ID == null ? "" : String(ID);
    var dssToxMap = map == 'pfas' || map == 'dsstox' || map == 'tox21' || map == 'Tox21Assay' || map == 'Tox21Target' || map == 'Tox21MostActive';
    if (dssToxMap && /^DTXSID\d+$/.test(ID)) {
        document.getElementById('CompoundID').href =
            'https://comptox.epa.gov/dashboard/chemical/details/' + ID;

        document.getElementById('LinkDSSTOX').href = "DSSTox/" + ID;

    } else if (map == 'drugbank' && /^DB\d+$/.test(ID)) {
        document.getElementById('CompoundID').href = 'https://www.drugbank.ca/drugs/' + ID;
    }

    


    // case of DSStoxMap and PFASmap -> GHS
    if (map == 'pfas' || map == 'dsstox' || map == 'tox21' || map == 'Tox21Assay' || map == 'Tox21Target' || map == 'Tox21MostActive') {
        GHS.textContent = dSMILESClass[ID]['GHS_category'] == null ? "" : String(dSMILESClass[ID]['GHS_category']);
    } else if (map == 'drugbank') {
        Group.textContent = dSMILESClass[ID]['DRUG_GROUPS'] == null ? "" : String(dSMILESClass[ID]['DRUG_GROUPS']);
    }

    var lboxes = [box1, box2, box3, box4, box5];
    for (let i = 0; i < 5; i++) {
        var raw = dinfo[ID][ldesc[i]];
        var shown;
        if (desctype[ldesc[i]] == 'str') {
            shown = raw == null ? "" : String(raw);
            if (shown.length > 50) {
                shown = shown.substring(0, 60) + '...';
            }
        } else if (desctype[ldesc[i]] == 'range') {
            shown = raw == "NA" || raw == null ? "NA" : round(raw, 2).toString();
        } else {
            shown = raw == null ? "" : String(raw);
        }
        lboxes[i].textContent = shown;
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
//for png in infobox
function resizeCanvas() {
    var con = document.getElementById('pngcompound');
    return Math.max(con.offsetWidth, con.offsetHeight);
}
