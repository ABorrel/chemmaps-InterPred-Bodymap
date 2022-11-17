function createpanel() {
    var panel = new dat.GUI({ size: 12, left: 20 });
    var folder1 = panel.addFolder('Hide Chemicals');
    // folder 2 -> real time update function of information selected by user
    var folder2 = panel.addFolder('Colors by');
    var lchem = Object.keys(dSMILESClass);
    //console.log(lchem);
    //console.log(dinfo);
    var lonMap = Object.keys(dinfo[lchem[1]]);
    //console.log(lonMap);
    var settings = {};

    if (map == 'drugbank') {
        var settingsDefault = {
            'Draw structures': false,
            'Approved drugs': true,
            'In development drugs': true,
            'Withdrawn drugs': true,
            'Added chemicals': true,
            'Draw structures': false,
            Axes: false,
            'Set a pivot point': function() {
                SetPivot();
            },
            'Reset view': function() {
                controls.reset();
            },
            'Reset map': function() {
                location.reload();
            },
            Help: function() {
                Help();
            },
            "Save map view": function() {
                Screenshot();
            },
        };
        var spfunction = {
            desc: 'Drug group',
            changeColor: function() {
                colorbyType(this.desc);
            },
        };
        var outfunction = spfunction.changeColor.bind(spfunction);
        settings['Drug group'] = outfunction;
    }else if (map == 'pfas' || map == 'dsstox' || map == 'tox21') {
        var settingsDefault = {
            'Classified': true,
            'No classified': true,
            'Draw structures': false,
            'Added chemicals': true,
            Axes: false,
            'Set a pivot point': function() {
                SetPivot();
            },
            'Reset view': function() {
                controls.reset();
            },
            'Reset map': function() {
                location.reload();
            },
            Help: function() {
                Help();
            },
            'Save map view': function() {
                Screenshot();
            },
        };
    
        var spfunction = {
            desc: 'GHS category',
            changeColor: function() {
                colorbyType(this.desc);
            },
        };
        var outfunction = spfunction.changeColor.bind(spfunction);
        settings['GHS category'] = outfunction;
    }else if (map == 'Tox21Assay' ||  map == 'Tox21Target' || map == 'Tox21MostActive') {
        var settingsDefault = {
            'Conclusive': true,
            'Inconclusive': true,
            'Draw structures': false,
            Axes: false,
            'Set a pivot point': function() {
                SetPivot();
            },
            'Reset view': function() {
                controls.reset();
            },
            'Reset map': function() {
                location.reload();
            },
            Help: function() {
                Help();
            },
        };
    
        var spfunction = {
            desc: 'GHS category',
            changeColor: function() {
                colorbyType(this.desc);
            },
        };
        var outfunction = spfunction.changeColor.bind(spfunction);
        settings['GHS category'] = outfunction;

        var spfunction2 = {
            desc: 'Assay outcome',
            changeColor: function() {
                colorbyType(this.desc);
            },
        };
        var outfunction = spfunction.changeColor.bind(spfunction2);
        settings['Assay outcome'] = outfunction;
    }
    // check other parameters
    for (var i in lonMap) {
        var desc = lonMap[i];
        //console.log(desctype[lonMap[i]]);
        if (desctype[lonMap[i]] == 'range') {
            // use to create specific function by descriptors
            var spfunction = {
                desc: desc,
                changeColor: function() {
                    colorbyRange(this.desc);
                },
            };
            var outfunction = spfunction.changeColor.bind(spfunction);
            settings[desc] = outfunction;
        } else if (
            desctype[lonMap[i]] == 'class' &&
            lonMap[i] != 'Drug group' &&
            lonMap[i] != 'EPA category'
        ) {
            // use to create specific function by descriptors
            var spfunction = {
                desc: desc,
                changeColor: function() {
                    colorbyType(this.desc);
                },
            };
            var outfunction = spfunction.changeColor.bind(spfunction);
            settings[desc] = outfunction;
        }
    }
    //console.log(settings);
    // panel selection
    if (map == 'drugbank') {
        folder1.add(settingsDefault, 'Approved drugs').onChange(viewDBapproved);
        folder1.add(settingsDefault, 'In development drugs').onChange(viewDBindev);
        folder1.add(settingsDefault, 'Withdrawn drugs').onChange(viewDBwithdraw);
        folder1.add(settingsDefault, 'Added chemicals').onChange(viewAdded);
        folder1.add(settingsDefault, 'Draw structures').onChange(drawChemicals);
    } else if (map == 'pfas' || map == 'dsstox' || map == 'tox21') {
        folder1.add(settingsDefault, 'Classified').onChange(viewClassified);
        folder1.add(settingsDefault, 'No classified').onChange(viewNoClassified);
        folder1.add(settingsDefault, 'Added chemicals').onChange(viewAdded);
        folder1.add(settingsDefault, 'Draw structures').onChange(drawChemicals);
    }else if(map == "Tox21Assay" || map == 'Tox21Target' || map == 'Tox21MostActive'){
        folder1.add(settingsDefault, 'Conclusive').onChange(viewClassified);
        folder1.add(settingsDefault, 'Inconclusive').onChange(viewNoClassified);
        folder1.add(settingsDefault, 'Draw structures').onChange(drawChemicals);
    }
    // panel specific descriptor
    var lsetcolor = Object.keys(settings);
    for (var i in lsetcolor) {
        folder2.add(settings, lsetcolor[i]);
    }
    // default
    panel.add(settingsDefault, 'Axes').onChange(viewAxes);
    panel.add(settingsDefault, 'Set a pivot point');
    panel.add(settingsDefault, 'Reset view');
    panel.add(settingsDefault, 'Reset map');
    panel.add(settingsDefault, 'Help');
    panel.add(settingsDefault, 'Save map view');
    return panel;
}
// functions to select chemicals
function viewDBapproved(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['approved'].length; i++) {
            scene.remove(dpoints['approved'][i]);
        }
        dpoints['approved'] = []
    } else {
        posPointIndividuallyDrugMap("approved");
    }
}

function viewDBindev(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['indev'].length; i++) {
            scene.remove(dpoints['indev'][i]);
        }
        dpoints['indev'] = []
    } else {
        posPointIndividuallyDrugMap("indev");
    }
}

function viewDBwithdraw(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['withdraw'].length; i++) {
            scene.remove(dpoints['withdraw'][i]);
        }
        dpoints['withdraw'] = []
    } else {
        posPointIndividuallyDrugMap("withdraw");
    }
}

function viewAdded(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['add'].length; i++) {
            scene.remove(dpoints['add'][i]);
        }
        dpoints['add'] = []
    } else {
        if(map == "drugbank"){
            posPointIndividuallyDrugMap("add");
        }else{
            posPointIndividuallyDSSTox("add")
        }
    }
}

function viewNoClassified(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['noclassified'].length; i++) {
            scene.remove(dpoints['noclassified'][i]);
        }
        dpoints['noclassified'] = []
    } else {
        posPointIndividuallyDSSTox('noclassified')
    }
}

function viewClassified(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['classified'].length; i++) {
            scene.remove(dpoints['classified'][i]);
        }
        dpoints['classified'] = []
    } else {
        posPointIndividuallyDSSTox('classified')
    }
}



function updateCanvas(){

    // only do if less that 50 chemicals
    
    var sizeCanvas = resizeCanvas();
    var options = { width: sizeCanvas, height: sizeCanvas };
    var smilesDrawer = new SmilesDrawer.Drawer(options);

    let i_canvas = 0; // i not in loop to avoid duplicate with ktype
    for (ktype in dpoints) {
        for (var i_draw = 0; i_draw < dpoints[ktype].length; i_draw++) {
            let id_canvas = "canvas_" + i_canvas;
            i_canvas = i_canvas + 1;
            
            SmilesDrawer.parse(dSMILESClass[dpoints[ktype][i_draw].name]['SMILES'], function(tree) {
                // Draw to the canvas
                smilesDrawer.draw(tree, id_canvas, 'dark', false, width=400, height=400);
            });
        } 
    }   

}


// functions to draw chemical on map
function drawChemicals(visibility) {

    
    if (visibility == true) {
        var numOfPoints = 0;
        scene.traverse(function(child) {
            if (child instanceof THREE.Points) numOfPoints++;
        });
        if (numOfPoints > 50) {
            alert('Draw on the Map only less than 50 chemicals');
            return;
        }
        
        // need to reproduce loop
        updateCanvas();

        
        let i_canvas = 0; // i not in loop to avoid duplicate with ktype
        for (ktype in dpoints) {
            for (var i_draw = 0; i_draw < dpoints[ktype].length; i_draw++) {
                let id_canvas = "canvas_" + i_canvas;
                let chemOnFly = document.getElementById(id_canvas);
                i_canvas = i_canvas + 1;
                
                const texture = new THREE.CanvasTexture(chemOnFly);
                dpoints[ktype][i_draw].material.map = texture;
                dpoints[ktype][i_draw].material.size = 15;
                dpoints[ktype][i_draw].material.color.setHex(0xffffff);
                dpoints[ktype][i_draw].col = 0xffffff;
                dpoints[ktype][i_draw].material.map.needsUpdate = true;

            }
        }
    // need to reproduce loop
    } else {
        resetPoint();

    }
}
// functions to see manage the view
function viewAxes(visibility) {
    if (visibility == false) {
        scene.remove(axes);
    } else {
        scene.add(axes);
    }
}

function SetPivot() {
    if (!block) {
        alert(
            '!!! Please select and lock a star by the mouse double click before set a pivot point !!!'
        );
        return;
    }
    if (ID == null) {
        alert(
            '!!! Please select and lock a star by the mouse double click before set a pivot point !!!'
        );
        return;
    }
    controls.enabled = false;
    new TWEEN.Tween(controls.target)
        .to(
            {
                x: dcoords[ID][0] * fact,
                y: dcoords[ID][1] * fact,
                z: dcoords[ID][2] * fact,
            },
            2000
        )
        //.easing( TWEEN.Easing.Elastic.Out).start();
        .easing(TWEEN.Easing.Linear.None)
        .start();
    //controls.enabled = true;
}

function Help() {
    if (map == 'drugbank') {
        window.open('DrugMapHelp');
    } else if (map == 'dsstox') {
        window.open('DSSToxMap');
    } else if (map == 'pfas') {
        window.open('PFASMapHelp');
    } else if (map == 'tox21' || map == 'Tox21Assay' || map == 'Tox21Target' || map == 'Tox21MostActive') {
        window.open('Tox21MapHelp');
    }
}

function Screenshot() {
    var imgData, imgNode;

    try {
        var strMime = "image/jpeg";
        imgData = renderer.domElement.toDataURL(strMime);

        saveFile(imgData.replace(strMime, strDownloadMime), "test.jpg");

    } catch (e) {
        console.log(e);
        return;
    }
}

var saveFile = function (strData, filename) {
    var link = document.createElement('a');
    if (typeof link.download === 'string') {
        document.body.appendChild(link); //Firefox requires the link to be in the body
        link.download = filename;
        link.href = strData;
        link.click();
        document.body.removeChild(link); //remove the link when done
    } else {
        location.replace(uri);
    }
}

// color
function colorbyType(descin) {
    //console.log(descin);
    if (descin == 'Drug group') {
        for (ktype in dpoints) {
            for (var i = 0; i < dpoints[ktype].length; i++) {
                dpoints[ktype][i].material.color.setHex(dcol[ktype]);
                dpoints[ktype][i].col = dcol[ktype];
                dpoints[ktype][i].material.map.needsUpdate = true;
            }
        }
    } else if (descin == 'GHS category') {
        for (ktype in dpoints) {
            for (var i = 0; i < dpoints[ktype].length; i++) {
                if (ktype == "add"){
                    dpoints[ktype][i].material.color.setHex(dcolGHS["NA"]);
                    dpoints[ktype][i].col = dcolGHS["NA"];
                }else{
                    dpoints[ktype][i].material.color.setHex(
                        dcolGHS[dSMILESClass[dpoints[ktype][i].name]['GHS_category']]
                    );
                    dpoints[ktype][i].col = dcolGHS[dSMILESClass[dpoints[ktype][i].name]['GHS_category']];
                }
                
                dpoints[ktype][i].material.map.needsUpdate = true;
            }
        }
    }else if (descin == 'Assay outcome'){
        for (ktype in dpoints) {
            for (var i = 0; i < dpoints[ktype].length; i++) {
                if (ktype == "add"){
                    dpoints[ktype][i].material.color.setHex(dcol["NA"]);
                    dpoints[ktype][i].col = dcol["NA"];
                }else{
                    if(dinfo[dpoints[ktype][i].name]["Assay Outcome"].search("inconclusive") !==- 1 || dinfo[dpoints[ktype][i].name]["Assay Outcome"].search("Not tested") !==- 1 || dinfo[dpoints[ktype][i].name]["Assay Outcome"].search("-") !==- 1){
                        dpoints[ktype][i].material.color.setHex(dcol["inconclusive"]);
                        dpoints[ktype][i].col = dcol["inconclusive"];
                    }else if(dinfo[dpoints[ktype][i].name]["Assay Outcome"].search("inactive") !==- 1){
                        dpoints[ktype][i].material.color.setHex(parseFloat(dcol["inactive"]));
                        dpoints[ktype][i].col = dcol["inactive"];
                    }else{
                        dpoints[ktype][i].material.color.setHex(parseFloat(dcol["active"]));
                        dpoints[ktype][i].col = dcol["active"];
                    }
                }
                dpoints[ktype][i].material.map.needsUpdate = true;
            }
        }
    } else {
        var lval = [];
        for (var chem in dinfo) {
            for (var desc in dinfo[chem]) {
                if (desc == descin) {
                    var val = dinfo[chem][desc];
                    if (lval.includes(val) == false && isNaN(val) == false) {
                        lval.push(val);
                    }
                }
            }
        }

        if (lval.length == 2) {
            lcol = ['#40B0A6', '#FEFE62'];
        } else {
            var lcol = ['#40B0A6', '#006CD1', '#E66100', '#D41159', '#FEFE62'];
        }
        var dcoltemp = {};
        var i = 1;
        for (var i = 0; i < lval.length; i++) {
            dcoltemp[lval[i]] = lcol[i];
        }
        dcoltemp[''] = '#ffffff';
        dcoltemp['NA'] = '#ffffff';

        for (ktype in dpoints) {
            for (var i = 0; i < dpoints[ktype].length; i++) {
                // black for NA
                var valtemp = dinfo[dpoints[ktype][i].name][descin];
                var coltemp = new THREE.Color(dcoltemp[valtemp]).getHex();
                dpoints[ktype][i].material.color.setHex(coltemp);
                dpoints[ktype][i].col = coltemp;
                dpoints[ktype][i].material.map.needsUpdate = true;
            }
        }
    }
}

function colorbyRange(descin) {
    var lval = [];
    for (var chem in dinfo) {
        for (var desc in dinfo[chem]) {
            if (desc == descin) {
                var val = parseFloat(dinfo[chem][desc]);
                if (descin == "AC50" && val == 0.0){
                    continue;
                }
                if (isNaN(val) == false) {
                    lval.push(parseFloat(dinfo[chem][desc]));
                }
            }
        }
    }
    var med = getMedian(lval);
    var minval = Math.min.apply(Math, lval);
    var maxval = Math.max.apply(Math, lval);

    var ecart = Math.min(med - minval, maxval - med);

    var gradval = range(med - ecart, med + ecart, ecart * 2 / nbcol);
    var gradcol = generateColor('#005AB5', '#FEFE62', nbcol);

    var dcol = {};
    for (var i = 0; i < gradval.length - 1; i++) {
        dcol[gradval[i]] = gradcol[i];
    }
    var flag = 0;
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            // black for NA
            var val = parseFloat(dinfo[dpoints[ktype][i].name][descin]);
            if (isNaN(val) == true) {
                coltemp = new THREE.Color('#000000').getHex();
                dpoints[ktype][i].material.color.setHex(coltemp);
                dpoints[ktype][i].col = coltemp;
                dpoints[ktype][i].material.map.needsUpdate = true;
                continue;
            }
            // case AC50
            if(descin == "AC50" && val == 0.0){
                coltemp = new THREE.Color('#000000').getHex();
                dpoints[ktype][i].material.color.setHex(coltemp);
                dpoints[ktype][i].col = coltemp;
                dpoints[ktype][i].material.map.needsUpdate = true;
                continue;
            }

            flag = 0;
            for (var vallimite in dcol) {
                vallimite = parseFloat(vallimite);
                if (val < vallimite) {
                    var coltemp = new THREE.Color(dcol[vallimite]).getHex();
                    dpoints[ktype][i].material.color.setHex(coltemp);
                    dpoints[ktype][i].col = coltemp;
                    dpoints[ktype][i].material.map.needsUpdate = true;
                    flag = 1;
                    break;
                }
            }
            if (flag == 0) {
                var coltemp = new THREE.Color('#061094').getHex();
                dpoints[ktype][i].material.color.setHex(coltemp);
                dpoints[ktype][i].col = coltemp;
                dpoints[ktype][i].material.map.needsUpdate = true;
            }
        }
    }
}
