function createpanel() {
    var panel = new dat.GUI({ size: 12, left: 20 });
    var folder1 = panel.addFolder('Hide Chemicals');
    // folder 2 -> real time update function of information selected by user
    var folder2 = panel.addFolder('Colors by');
    var lchem = Object.keys(dSMILESClass);
    //console.log(lchem);
    //console.log(dinfo);
    var lonMap = Object.keys(dinfo[lchem[1]]);
    console.log(lonMap);
    var settings = {};

    if (map == 'DrugMap') {
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
        };
        var spfunction = {
            desc: 'Drug group',
            changeColor: function() {
                colorbyType(this.desc);
            },
        };
        var outfunction = spfunction.changeColor.bind(spfunction);
        settings['Drug group'] = outfunction;
    } else if (map == 'PFASMap' || map == 'DSSToxMap' || map == 'Tox21Map') {
        var settingsDefault = {
            Classified: true,
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
        };
        var spfunction = {
            desc: 'GHS category',
            changeColor: function() {
                colorbyType(this.desc);
            },
        };
        var outfunction = spfunction.changeColor.bind(spfunction);
        settings['GHS category'] = outfunction;
    }
    // check other parameters
    for (var i in lonMap) {
        var desc = lonMap[i];
        console.log(desctype[lonMap[i]]);
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
    console.log(settings);
    // panel selection
    if (map == 'DrugMap') {
        folder1.add(settingsDefault, 'Approved drugs').onChange(viewDBapproved);
        folder1.add(settingsDefault, 'In development drugs').onChange(viewDBindev);
        folder1.add(settingsDefault, 'Withdrawn drugs').onChange(viewDBwithdraw);
        folder1.add(settingsDefault, 'Added chemicals').onChange(viewAdded);
        folder1.add(settingsDefault, 'Draw structures').onChange(drawChemicals);
    } else if (map == 'PFASMap' || map == 'DSSToxMap' || map == 'Tox21Map') {
        folder1.add(settingsDefault, 'Classified').onChange(viewClassified);
        folder1.add(settingsDefault, 'No classified').onChange(viewNoClassified);
        folder1.add(settingsDefault, 'Added chemicals').onChange(viewAdded);
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
    return panel;
}
// functions to select chemicals
function viewDBapproved(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['approved'].length; i++) {
            scene.remove(dpoints['approved'][i]);
        }
    } else {
        for (var i = 0; i < dpoints['approved'].length; i++) {
            scene.add(dpoints['approved'][i]);
        }
    }
}
function viewDBindev(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['indev'].length; i++) {
            scene.remove(dpoints['indev'][i]);
            dpoints['indev'][i].size = 1;
        }
    } else {
        for (var i = 0; i < dpoints['indev'].length; i++) {
            scene.add(dpoints['indev'][i]);
        }
    }
}
function viewDBwithdraw(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['withdraw'].length; i++) {
            scene.remove(dpoints['withdraw'][i]);
        }
    } else {
        for (var i = 0; i < dpoints['withdraw'].length; i++) {
            scene.add(dpoints['withdraw'][i]);
        }
    }
}
function viewAdded(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['add'].length; i++) {
            scene.remove(dpoints['add'][i]);
        }
    } else {
        for (var i = 0; i < dpoints['add'].length; i++) {
            scene.add(dpoints['add'][i]);
        }
    }
}
function viewNoClassified(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['noclassified'].length; i++) {
            scene.remove(dpoints['noclassified'][i]);
        }
    } else {
        for (var i = 0; i < dpoints['noclassified'].length; i++) {
            scene.add(dpoints['noclassified'][i]);
        }
    }
}
function viewClassified(visibility) {
    if (visibility == false) {
        for (var i = 0; i < dpoints['classified'].length; i++) {
            scene.remove(dpoints['classified'][i]);
            dpoints['classified'][i].size = 0.1;
        }
    } else {
        for (var i = 0; i < dpoints['classified'].length; i++) {
            scene.add(dpoints['classified'][i]);
        }
    }
}
// functions to draw chemical on map
function drawChemicals(visibility) {
    var textureLoader = new THREE.TextureLoader();
    if (visibility == true) {
        var numOfPoints = 0;
        scene.traverse(function(child) {
            if (child instanceof THREE.Points) numOfPoints++;
        });
        console.log(numOfPoints);
        if (numOfPoints > 50) {
            alert('Draw on the Map only less than 50 chemicals');
            return;
        }
        for (ktype in dpoints) {
            for (var i = 0; i < dpoints[ktype].length; i++) {
                // have to be rewrtie when png accessment will be fix
                var namepng = dSMILESClass[dpoints[ktype][i].name]['inchikey'];
                console.log(namepng);
                var ppng = 'chemmaps/png/' + namepng + '.png'
                console.log(ppng);
                var texture = textureLoader.load(ppng);
                dpoints[ktype][i].material.map = texture;
                dpoints[ktype][i].material.size = 15;
                dpoints[ktype][i].material.color.setHex(0xffffff);
                dpoints[ktype][i].col = 0xffffff;
                dpoints[ktype][i].material.map.needsUpdate = true;
                dpoints[ktype][i].material.size.needsUpdate = true;
            }
        }
    } else {
        if (map == 'PFASMap' || map == 'DSSToxMap' || map == 'Tox21Map') {
            for (ktype in dpoints) {
                for (var i = 0; i < dpoints[ktype].length; i++) {
                    var GHScat = dSMILESClass[dpoints[ktype][i].name]['GHS_category'];
                    if (GHScat == 'NA') {
                        var colorhexa = dcol['NA'];
                        var typechem = 'noclassified';
                    } else {
                        if (GHScat == 'add') {
                            var typechem = 'add';
                            var colorhexa = 0xffffff;
                        } else {
                            var typechem = 'classified';
                            var colorhexa = dcol[parseFloat(GHScat)];
                        }
                    }
                    var sprite = dsprite[typechem];
                    var size = dsize[typechem];

                    dpoints[ktype][i].material.map = sprite;
                    dpoints[ktype][i].material.color.setHex(colorhexa);
                    dpoints[ktype][i].material.size = size;
                    dpoints[ktype][i].col = colorhexa;
                    dpoints[ktype][i].material.map.needsUpdate = true;
                    dpoints[ktype][i].material.size.needsUpdate = true;
                }
            }
        }
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
    if (map == 'DrugMap') {
        window.open('DrugMapHelp');
    } else if (map == 'DSSToxMap') {
        window.open('DSSToxMap');
    } else if (map == 'PFASMap') {
        window.open('PFASMapHelp');
    } else if (map == 'Tox21Map') {
        window.open('Tox21MapHelp');
    }
}
// color
function colorbyType(descin) {
    console.log(descin);
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
                    dpoints[ktype][i].material.color.setHex(dcol["NA"]);
                    dpoints[ktype][i].col = dcol["NA"];
                }else{
                    dpoints[ktype][i].material.color.setHex(
                        dcol[dSMILESClass[dpoints[ktype][i].name]['GHS_category']]
                    );
                    dpoints[ktype][i].col = dcol[dSMILESClass[dpoints[ktype][i].name]['GHS_category']];
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
            lcol = ['#00ff00', '#c11212'];
        } else {
            var lcol = ['#c11212', '#ff5500', '#ffaa00', '#ffff00', '#aaff00'];
        }
        var dcoltemp = {};
        var i = 1;
        for (var i = 0; i < lval.length; i++) {
            dcoltemp[lval[i]] = lcol[i];
        }
        dcoltemp[''] = '#ffffff';
        dcoltemp['NA'] = '#ffffff';

        console.log(dcoltemp);
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
    var gradcol = generateColor('#061094', '#ffffff', nbcol);

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
                dpoints[ktype][i].material.color.setHex('#000000');
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
