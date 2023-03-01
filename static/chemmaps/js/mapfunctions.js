//position points on the map

function posPoint(lcoord, name, colorhexa, sprite, size, fact, scene) {
    var textureLoader = new THREE.TextureLoader();

    var position = new Float32Array(3);
    var sizes = new Float32Array(1);
    position[0] = parseFloat(lcoord[0] * fact);
    position[1] = parseFloat(lcoord[1] * fact);
    position[2] = parseFloat(lcoord[2] * fact);
    // manage geometry
    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(position, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    // have to fix for the rayscatting
    geometry.computeBoundingSphere();
    geometry.boundingSphere.radius = size;
    var material = new THREE.PointsMaterial({
        size: size,
        map: sprite,
        alphaTest: 0.1,
        color: colorhexa,
        transparent: true,
    });
    var particule = new THREE.Points(geometry, material);
    particule.name = name;
    particule.col = colorhexa;
    scene.add(particule);
    return particule;
}

function posPointIndividuallyDrugMap(repos) {
    //console.log(color);
    // textures and material
    for (var i in dcoords) {
        var position = new Float32Array(3);
        position[0] = parseFloat(dcoords[i][0] * fact);
        position[1] = parseFloat(dcoords[i][1] * fact);
        position[2] = parseFloat(dcoords[i][2] * fact);
        if (dSMILESClass[i]['DRUG_GROUPS'].search('approved') !== -1) {
            var typeDrug = 'approved';
        } else if (dSMILESClass[i]['DRUG_GROUPS'].search('withdraw') !== -1) {
            var typeDrug = 'withdraw';
        } else if (dSMILESClass[i]['DRUG_GROUPS'].search('add') !== -1) {
            var typeDrug = 'add';
        } else {
            var typeDrug = 'indev';
        }
        if(repos != "all" && repos != typeDrug){
            continue;
        }
        var size = dsize[typeDrug];
        var colorhexa = dcol[typeDrug];
        var sprite = dsprite[typeDrug];
        // manage geometry
        var geometry = new THREE.BufferGeometry();
        geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( position, 3 ) );
        geometry.size = new THREE.BufferAttribute(size, 1);
        // have to fix for the rayscatting
        geometry.computeBoundingSphere();
        geometry.boundingSphere.radius = size;
        var material = new THREE.PointsMaterial({
            size: size,
            map: sprite,
            alphaTest: 0.1,
            color: colorhexa,
            transparent: true,
        });
        var particule = new THREE.Points(geometry, material);
        particule.name = i;
        particule.col = colorhexa;
        dpoints[typeDrug].push(particule);
        scene.add(particule);
    }
}

function posPointIndividuallyDSSTox(repos) {
    for (var i in dcoords) {
        var position = new Float32Array(3);
        position[0] = parseFloat(dcoords[i][0] * fact);
        position[1] = parseFloat(dcoords[i][1] * fact);
        position[2] = parseFloat(dcoords[i][2] * fact);

        if (map=="Tox21Assay" || map == 'Tox21Target' || map == 'Tox21MostActive'){
            var Assaycat = dSMILESClass[i]['Assay Outcome'];
            if (Assaycat.search("inconclusive") !== -1) {
                var colorhexa = dcol['inconclusive'];
                var typechem = 'noclassified';
                var size = dsize[typechem];
            } else if(Assaycat.search("inactive") !== -1) {
                var typechem = 'classified';
                var colorhexa = dcol['inactive'];
                var size = dsize[typechem];
            }else if (Assaycat.search("Not tested") !== -1) {
                    var colorhexa = dcol['inconclusive'];
                    var typechem = 'noclassified';
                    var size = dsize[typechem];
            }else{
                var typechem = 'classified';
                var colorhexa =  dcol['active'];
                var size = dsize[typechem];
            }
            var sprite = dsprite[typechem];
            
            if(repos != "all" && repos != typechem){
                continue;
            }

            // manage geometry
            var geometry = new THREE.BufferGeometry();
            geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( position, 3 ) );
            geometry.size = new THREE.BufferAttribute(size, 1);
            
            // have to fix for the rayscatting
            geometry.computeBoundingSphere();
            geometry.boundingSphere.radius = size;
            var material = new THREE.PointsMaterial({
                size: size,
                map: sprite,
                alphaTest: 0.1,
                color: colorhexa,
                transparent: true,
            });
            var particule = new THREE.Points(geometry, material);
            particule.name = i;
            particule.col = colorhexa;
            dpoints[typechem].push(particule);
            scene.add(particule);

        }else{
            var GHScat = dSMILESClass[i]['GHS_category'];
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
    
            if(repos != "all" && repos != typechem){
                continue;
            }

            // manage geometry
            var geometry = new THREE.BufferGeometry();
            geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( position, 3 ) );
            geometry.size = new THREE.BufferAttribute(size, 1);
            // have to fix for the rayscatting
            geometry.computeBoundingSphere();
            geometry.boundingSphere.radius = size;
            var material = new THREE.PointsMaterial({
                size: size,
                map: sprite,
                alphaTest: 0.1,
                color: colorhexa,
                transparent: true,
            });
            var particule = new THREE.Points(geometry, material);
            particule.name = i;
            particule.col = colorhexa;
            dpoints[typechem].push(particule);
            scene.add(particule);
        }
    }
}

function resetPoint(){

    for (typechem in dpoints) {
        for (var i = 0; i < dpoints[typechem].length; i++) {
            var i_original = dpoints[typechem][i].name
            if (map=="Tox21Assay" || map == 'Tox21Target' || map == 'Tox21MostActive'){
                var Assaycat = dSMILESClass[i_original]['Assay Outcome'];
                if (Assaycat.search("inconclusive") !== -1) {
                    var colorhexa = dcol['inconclusive'];
                    var typechem = 'noclassified';
                    var size = dsize[typechem];
                } else if(Assaycat.search("inactive") !== -1) {
                    var typechem = 'classified';
                    var colorhexa = dcol['inactive'];
                    var size = dsize[typechem];
                }else if (Assaycat.search("Not tested") !== -1) {
                        var colorhexa = dcol['inconclusive'];
                        var typechem = 'noclassified';
                        var size = dsize[typechem];
                }else{
                    var typechem = 'classified';
                    var colorhexa =  dcol['active'];
                    var size = dsize[typechem];
                }
                var sprite = dsprite[typechem];
            }else if (map == "drugbank"){
                if (dSMILESClass[i_original]['DRUG_GROUPS'].search('approved') !== -1) {
                    var typechem = 'approved';
                } else if (dSMILESClass[i_original]['DRUG_GROUPS'].search('withdraw') !== -1) {
                    var typechem = 'withdraw';
                } else if (dSMILESClass[i_original]['DRUG_GROUPS'].search('add') !== -1) {
                    var typechem = 'add';
                } else {
                    var typechem = 'indev';
                }
                var size = dsize[typechem];
                var colorhexa = dcol[typechem];
                var sprite = dsprite[typechem];
            }else{
                var GHScat = dSMILESClass[i_original]['GHS_category'];
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
            }
            dpoints[typechem][i].material.map = sprite;
            dpoints[typechem][i].material.color.setHex(colorhexa);
            dpoints[typechem][i].material.size = size;
            dpoints[typechem][i].col = colorhexa;
            dpoints[typechem][i].material.map.needsUpdate = true;
            dpoints[typechem][i].material.size.needsUpdate = true;
        }
    }
}

// Build axes and text
function buildAxes(length, x, y, z) {
    var axes = new THREE.Object3D();
    axes.add(
        buildLine(new THREE.Vector3(0, 0, 0), new THREE.Vector3(length, 0, 0), 0xff0000, false, 0)
    ); //+X
    axes.add(
        buildLine(new THREE.Vector3(0, 0, 0), new THREE.Vector3(-length, 0, 0), 0xff0000, false, 0)
    ); //-X
    axes.add(
        buildLine(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, length, 0), 0x00ff00, true, 3)
    ); //+Y
    axes.add(
        buildLine(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, -length, 0), 0x00ff00, true, 3)
    ); //-Y
    axes.add(
        buildLine(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, length), 0xffff00, true, 1)
    ); //+Z
    axes.add(
        buildLine(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -length), 0xffff00, true, 1)
    ); //-Z
    axes.position.set(x, y, z);
    return axes;
}

function buildLine(src, dst, colorHex, dashed, dashedsize) {
    var geom = new THREE.BufferGeometry(),
        mat;
    
    if (dashed) {
        mat = new THREE.LineDashedMaterial({
            linewidth: 5,
            color: colorHex,
            dashSize: dashedsize,
            gapSize: dashedsize,
        });
    } else {
        mat = new THREE.LineBasicMaterial({ linewidth: 5, color: colorHex });
    }
    const points = [];
    points.push(src.clone());
    points.push(dst.clone());
    
    geom.setFromPoints(points);
    //geom.computeLineDistances(); // This one is SUPER important, otherwise dashed lines will appear as simple plain lines
    const line = new THREE.Line( geom, mat );
    
    var axis = new THREE.Line(geom, mat, THREE.LinePieces);
    return axis;
}

function createText(scene, stext, x, y, z) {
    var loader = new THREE.FontLoader();
    var out = loader.load(
        'three.js-master/examples/fonts/helvetiker_regular.typeface.json',
        function(font) {
            var textGeometry = new THREE.TextGeometry(stext, {
                font: font,
                size: 1,
                height: 0.2,
                curveSegments: 10,
                bevelThickness: 0,
                bevelSize: 0,
                bevelEnabled: true,
            });
            var material = new THREE.MeshBasicMaterial({ color: 0x00ee34, overdraw: 0.9 });
            var mesh = new THREE.Mesh(textGeometry, material);
            mesh.position.x = x * 20;
            mesh.position.y = y * 20;
            mesh.position.z = z * 20;
            scene.add(mesh);
        }
    );
}

// render animation
function animate() {
    requestAnimationFrame(animate);
    render();
    //stats.update();
}

function render() {
    // for search positionning
    if (istepcamera < ncameraStep) {
        camera.position.x = camera.position.x + decart['x'];
        camera.position.y = camera.position.y + decart['y'];
        camera.position.z = camera.position.z + decart['z'];
        camera.updateProjectionMatrix();
        istepcamera++;
    } else {
        decart['x'] = 0;
        decart['y'] = 0;
        decart['z'] = 0;
    }
    controls.update();
    TWEEN.update();
    renderer.render(scene, camera);
}

function onMouseMove(event) {
    //console.log(event.preventDefault());
    mouse.x = event.clientX / window.innerWidth * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    intersectCompound();
}

function blockview(event) {
    if (controls.enabled == false) {
        controls.enabled = true;
        block = 0;
        blockflag.innerHTML = '';
    } else {
        controls.enabled = false;
        block = 1;
        blockflag.innerHTML = 'View blocked';
    }
}

function callbackFunc(response) {
    // do something with the response
    console.log(response);
}

// map function
function drawChemical() {
    document.getElementById('drawChemical');
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            if (ID == dpoints[ktype][i].name) {
                // duplicate texture from the compound2 info box
                const chemOnFly = document.getElementById("Compoundpng2");
                const texture = new THREE.CanvasTexture(chemOnFly);
                //console.log(texture);
                dpoints[ktype][i].material.map = texture;
                dpoints[ktype][i].material.size = 15;
                dpoints[ktype][i].material.color.setHex(0xffffff);
                dpoints[ktype][i].col = 0xffffff;
                dpoints[ktype][i].material.map.needsUpdate = true;
            }
        }
    }
}

function downloadNeighbor() {
    var element = document.createElement('a');
    var filname = ID + '.csv';
    var textin = 'ID\tSMILES\tinchikey\tGroup';

    var IDcenter = ID;
    //console.log(ID);
    
    var ldesc = Object.keys(dinfo[ID]);
    //console.log(ldesc);
    //console.log(dSMILESClass[ID]);
    // write header
    for (var idesc in ldesc) {
        textin = textin + '\t' + ldesc[idesc];
    }
    textin = textin + '\tdistance\n';
    textin = textin + createLineWriteForTable(IDcenter, IDcenter, ldesc);
    
    //console.log(dneighbors[IDcenter]);
    for (var p = 0; p < dneighbors[IDcenter].length; p++) {
        if(dneighbors[IDcenter][p] in dSMILESClass){
            textin = textin + createLineWriteForTable(dneighbors[IDcenter][p], IDcenter, ldesc);
        }
        ;
    }
    //console.log(textin);
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textin));
    element.setAttribute('download', filname);

    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);

}

function createLineWriteForTable(IDchem, IDcenter, ldesc) {
    
    var lineW =
        IDchem.toString() +
        '\t' +
        dSMILESClass[IDchem]['SMILES'] +
        '\t' +
        dSMILESClass[IDchem]['inchikey'] +
        '\t';
    
    if (map == 'drugbank') {
        lineW = lineW + dSMILESClass[IDchem]['DRUG_GROUPS'];
    } else {
        lineW = lineW + dSMILESClass[IDchem]['GHS_category'];
    }
    for (var idesc in ldesc) {
        lineW = lineW + '\t' + dinfo[IDchem][ldesc[idesc]].toString();
    }
    dist = computeEuclidian(IDchem, IDcenter); // add var?
    lineW = lineW + "\t" + dist.toString() + '\n';
    
    return lineW;
}

function computeEuclidian(ID1, ID2){

    //console.log(ID1);
    //console.log(ID2);

    var x1 = dcoords[ID1][0];
    var y1 = dcoords[ID1][1];
    var z1 = dcoords[ID1][2];

    var x2 = dcoords[ID2][0];
    var y2 = dcoords[ID2][1];
    var z2 = dcoords[ID2][2];

    var dist = Math.sqrt(Math.pow((x2-x1),2) + Math.pow((y2-y1),2) + Math.pow((z2-z1),2))
    return dist;
}

// scale position in case of resize
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function intersectCompound() {
    for (var typedrug in dpoints) {
        var intersects = raycaster.intersectObjects(dpoints[typedrug], true);
        if (intersects.length >= 1) {
            break;
        }
    }
    if (intersects.length >= 1 && block == 0) {
        // take only the first element
        ID = intersects[0].object.name;
        coorblock['x'] = intersects[0].point.x;
        coorblock['y'] = intersects[0].point.y;
        coorblock['z'] = intersects[0].point.z;
        updateInfoBox(intersects[0].object);
    }
}

function connectNeighbor(that) {

    var lneighbor = Object.assign([], dneighbors[ID]);
    lneighbor = lneighbor.splice(0, that.value);
    // clean the connect
    if (ID in dlines) {
        for (var i = 0; i < dlines[ID].length; i++) {
            scene.remove(dlines[ID][i]);
        }
        dlines[ID] = [];
    }

    // find origin
    var flagID = 0;
    for (ktype in dpoints) {
        if(flagID == 1){
            break;
        }
        for (var i = 0; i < dpoints[ktype].length; i++) {
            var IDtemp = dpoints[ktype][i].name;
            if (IDtemp == ID){
                var Xor = dcoords[dpoints[ktype][i].name][0] * fact;
                var Yor = dcoords[dpoints[ktype][i].name][1] * fact;
                var Zor = dcoords[dpoints[ktype][i].name][2] * fact;
                flagID = 1;
                break;
            }
        }
    }

    // draw line
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            var IDtemp = dpoints[ktype][i].name;
            if (lneighbor.indexOf(IDtemp) != -1) {
                line = buildLine(
                    new THREE.Vector3(Xor, Yor, Zor),
                    new THREE.Vector3(
                        dcoords[dpoints[ktype][i].name][0] * fact,
                        dcoords[dpoints[ktype][i].name][1] * fact,
                        dcoords[dpoints[ktype][i].name][2] * fact
                    ),
                    0xff0000,
                    false
                );
                scene.add(line);
                if (!(ID in dlines)) {
                    dlines[ID] = [];
                }
                dlines[ID].push(line);
            }
        }
    }
}

// see if it can be generalized for any map
function extractNeighbor(that) {
    var lneighbor = Object.assign([], dneighbors[ID]);
    lneighbor = lneighbor.splice(0, that.value);
    var count = 0; // equal 1 because keep center point

    for (ktype in dpoints) {
        var ltemp = []; // list remover
        for (var i = 0; i < dpoints[ktype].length; i++) {
            var IDtemp = dpoints[ktype][i].name;
            if (lneighbor.indexOf(IDtemp) == -1 && IDtemp != ID) {
                scene.remove(dpoints[ktype][i]);
            } else {
                ltemp.push(dpoints[ktype][i]);
                count++;
            }
        }
        dpoints[ktype] = ltemp;
    }
    // draw back compound no conserved
    if (count < that.value) {
        for (IDtemp in dcoords) {
            if (lneighbor.indexOf(IDtemp) != -1 && IDtemp != ID) {
                var flag = 0;
                for (ktype in dpoints) {
                    if (flag == 1) {
                        break;
                    }
                    for (var j = 0; j < dpoints[ktype].length; j++) {
                        if (dpoints[ktype][j].name == IDtemp) {
                            flag = 1;
                            break;
                        }
                    }
                }
                //console.log(dSMILESClass[IDtemp]['GHS_category']);
                //alert(map);
                if (flag == 0) {
                    if (map == 'drugbank') {
                        if (dSMILESClass[IDtemp]['DRUG_GROUPS'].search('approved') !== -1) {
                            var typeChem = 'approved';
                        } else if (dSMILESClass[IDtemp]['DRUG_GROUPS'].search('withdraw') !== -1) {
                            var typeChem = 'withdraw';
                        } else if (dSMILESClass[IDtemp]['DRUG_GROUPS'] == 'add') {
                            var typeChem = 'add';
                        } else {
                            var typeChem = 'indev';
                        }
                        var coloradd = dcol[typeChem];
                    
                    }else if (map == "Tox21Assay" || map == "Tox21Target" || map == 'Tox21MostActive'){

                        var Assaycat = dSMILESClass[IDtemp]['Assay Outcome'];
                        if (Assaycat.search("inconclusive") !== -1) {
                            var typeChem = 'noclassified';
                            var coloradd = dcol["inconclusive"]
                        } else if(Assaycat.search("inactive") !== -1) {
                            var typeChem = 'classified';
                            var coloradd = dcol["inactive"]
                        }else if (Assaycat.search("Not tested") !== -1) {
                            var typeChem = 'noclassified';
                            var coloradd = dcol["inconclusive"]
                        }else{
                            var typeChem = 'classified';
                            var coloradd = dcol["active"]
                        }
                    }else {
                        if (dSMILESClass[IDtemp]['GHS_category'] == 'NA') {
                            var typeChem = 'noclassified';
                        } else if (dSMILESClass[IDtemp]['GHS_category'] == 'add') {
                            var typeChem = 'add';
                        } else if (dSMILESClass[IDtemp]['GHS_category'] !== 'NA') {
                            var typeChem = 'classified';
                        }
                        var coloradd = dcol[dSMILESClass[IDtemp]['GHS_category']];
                    }
                    var point = posPoint(
                        dcoords[IDtemp],
                        IDtemp,
                        coloradd,
                        dsprite[typeChem],
                        dsize[typeChem],
                        fact,
                        scene
                    );
                    dpoints[typeChem].push(point);
                }
            }
        }
    }
    // lines from compound extracted
    for (line in dlines) {
        if (line != ID) {
            for (var i = 0; i < dlines[line].length; i++) {
                scene.remove(dlines[line][i]);
            }
        } else {
            if (dlines[line].length > that.value) {
                connectNeighbor(that);
            }
        }
    }
    updateCanvas(); // update smiles in the canvas
}

function cameraCenterPoint() {
    var lpos = [];
    var shift = 5;
    lpos.push(dcoords[ID][0] * fact);
    lpos.push(dcoords[ID][1] * fact);
    lpos.push(dcoords[ID][2] * fact);
    if (lpos[0] > 0) {
        lpos[0] = lpos[0] + shift;
    } else {
        lpos[0] = lpos[0] - shift;
    }
    if (lpos[1] > 0) {
        lpos[1] = lpos[1] + shift;
    } else {
        lpos[1] = lpos[1] - shift;
    }
    if (lpos[2] > 0) {
        lpos[2] = lpos[2] + shift;
    } else {
        lpos[2] = lpos[2] - shift;
    }
    calculateEcart(camera, lpos, ncameraStep);
    istepcamera = 0;
}

function searchID(that) {
    var thatUpper = that.toUpperCase();
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            if (thatUpper == dpoints[ktype][i].name) {
                ID = thatUpper;
                new TWEEN.Tween(controls.target)
                    .to(
                        {
                            x: dcoords[ID][0] * fact,
                            y: dcoords[ID][1] * fact,
                            z: dcoords[ID][2] * fact,
                        },
                        500
                    )
                    //.easing( TWEEN.Easing.Elastic.Out).start();
                    .easing(TWEEN.Easing.Linear.None)
                   .start();
                updateInfoBox(dpoints[ktype][i]);
                return;
            }
        }
    }

    alert(that + ' is not a valide request\nReset the map and/or check your request\n\n');
}

function searchIDtox(that) {
    var thatUpper = that.toUpperCase();
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            if (thatUpper == dpoints[ktype][i].name) {
                ID = thatUpper;
                controls.reset();
                cameraCenterPoint();
                updateInfoBox(dpoints[ktype][i]);
                return;
            }
        }
    }
    alert(
        that +
            ' is not a valide request\nReset the map and/or check your request\n\nFind your chemical https://comptox.epa.gov/dashboard/'
    );
}
