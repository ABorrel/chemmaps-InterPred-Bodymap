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

    renderFeatureRows();

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
function formatFeatureValue(label) {
    var raw = dinfo[ID] ? dinfo[ID][label] : null;
    if (desctype[label] == 'str') {
        var shown = raw == null ? "" : String(raw);
        if (shown.length > 50) {
            return shown.substring(0, 60) + '...';
        }
        return shown;
    }
    if (desctype[label] == 'range') {
        return raw == "NA" || raw == null ? "NA" : round(raw, 2).toString();
    }
    return raw == null ? "" : String(raw);
}

function renderFeatureRows() {
    var host = document.getElementById("feature-rows");
    if (!host || typeof ID === "undefined" || ID == null) {
        return;
    }
    host.textContent = "";
    var labels = cardFeatureLabels();
    for (var i = 0; i < labels.length; i++) {
        var label = labels[i];
        var line = document.createElement("div");
        var name = document.createElement("span");
        name.textContent = label + ": ";
        var value = document.createElement("span");
        value.textContent = formatFeatureValue(label);
        line.appendChild(name);
        line.appendChild(value);
        if (onDemand && pins.indexOf(label) !== -1) {
            var button = document.createElement("button");
            button.type = "button";
            button.textContent = "Remove";
            button.setAttribute("data-label", label);
            button.onclick = function() {
                removePin(this.getAttribute("data-label"));
            };
            line.appendChild(button);
        }
        host.appendChild(line);
    }
}

//for png in infobox
function resizeCanvas() {
    var con = document.getElementById('pngcompound');
    return Math.max(con.offsetWidth, con.offsetHeight);
}
