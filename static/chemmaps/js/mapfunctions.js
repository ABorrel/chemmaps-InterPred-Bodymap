//position points on the map

function posCloud(din, dcolorRGB, size, scene) {
    var colors = new Float32Array(Object.keys(din).length * 3);
    var positions = new Float32Array(Object.keys(din).length * 3);
    var sizes = new Float32Array(Object.keys(din).length);
    var color = new THREE.Color();
    //console.log(color);

    //console.log(color);
    //console.log(din);
    var count = 0;
    for (var i in din) {
        console.log(i);
        positions[count * 3] = parseFloat(din[i][0] * 20);
        positions[count * 3 + 1] = parseFloat(din[i][1] * 20);
        positions[count * 3 + 2] = parseFloat(din[i][2] * 20);
        sizes[count] = size;
        color.setRGB(dcolorRGB['r'] / 250, dcolorRGB['g'] / 250, dcolorRGB['b'] / 250);
        //console.log(color.r);
        colors[count * 3] = color.r;
        colors[count * 3 + 1] = color.g;
        colors[count * 3 + 2] = color.b;
        count = count + 1;
    }
    // manage geometry
    var geometry = new THREE.BufferGeometry();
    geometry.addAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.addAttribute('size', new THREE.BufferAttribute(sizes, 1));
    geometry.computeBoundingSphere();
    // textures and material
    var textureLoader = new THREE.TextureLoader();
    var sprite = textureLoader.load('/static/chemmaps/img/aspirin.png');
    //en conssprite.repeat.set( 1, 1 );
    //		sprite.wrapS = sprite.wrapT = THREE.RepeatWrapping;
    //				sprite.format = THREE.RGBFormat;

    //make level of shpere
    //sprite.wrapS = THREE.RepeatWrapping;
    //sprite.wrapT = THREE.RepeatWrapping;
    //sprite.repeat.set( 4, 4 );

    var material;
    material = new THREE.PointsMaterial({
        size: size,
        map: sprite,
        alphaTest: 0.9,
        color: 0x888888,
        transparent: true,
    });
    //material.needsUpdate=true;

    // create point
    particules = new THREE.Points(geometry, material);
    scene.add(particules);
}

function posPoint(lcoord, name, colorhexa, sprite, size, fact, scene) {
    var textureLoader = new THREE.TextureLoader();
    //var sprite = textureLoader.load("/static/chemmaps/img/star.png");

    var position = new Float32Array(3);
    var sizes = new Float32Array(1);
    position[0] = parseFloat(lcoord[0] * fact);
    position[1] = parseFloat(lcoord[1] * fact);
    position[2] = parseFloat(lcoord[2] * fact);
    // manage geometry
    var geometry = new THREE.BufferGeometry();
    geometry.addAttribute('position', new THREE.BufferAttribute(position, 3));
    geometry.addAttribute('size', new THREE.BufferAttribute(sizes, 1));
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

function posMeshs(din, scene, color, rad) {
    var lmesh = [];
    // Texture
    var textureLoader = new THREE.TextureLoader();
    var texture = textureLoader.load('/static/chemmaps/img/disturb.jpg');
    for (var i in din) {
        var objectGeometry = new THREE.SphereGeometry(rad);
        var objectMaterial = new THREE.MeshLambertMaterial({ map: texture, color: color });
        var mesh = new THREE.Mesh(objectGeometry, objectMaterial);
        mesh.position.x = parseFloat(din[i][0] * 20);
        mesh.position.y = parseFloat(din[i][1] * 20);
        mesh.position.z = parseFloat(din[i][2] * 20);
        mesh.name = i;
        scene.add(mesh);
        lmesh.push(mesh);
    }
    return lmesh;
}

function posPointIndividuallyDrugMap() {
    //console.log(color);
    // textures and material
    var dout = { approved: [], withdraw: [], indev: [], add: [] };
    for (var i in dcoords) {
        var position = new Float32Array(3);
        var sizes = new Float32Array(1);
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
        var size = dsize[typeDrug];
        var colorhexa = dcol[typeDrug];
        var sprite = dsprite[typeDrug];
        // manage geometry
        var geometry = new THREE.BufferGeometry();
        geometry.addAttribute('position', new THREE.BufferAttribute(position, 3));
        geometry.addAttribute('size', new THREE.BufferAttribute(size, 1));
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
        dout[typeDrug].push(particule);
        scene.add(particule);
    }
    return dout;
}

function posPointIndividuallyDSSTox() {
    var dout = { classified: [], noclassified: [], add: [] };
    for (var i in dcoords) {
        var position = new Float32Array(3);
        var sizes = new Float32Array(1);
        position[0] = parseFloat(dcoords[i][0] * fact);
        position[1] = parseFloat(dcoords[i][1] * fact);
        position[2] = parseFloat(dcoords[i][2] * fact);
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

        // manage geometry
        var geometry = new THREE.BufferGeometry();
        geometry.addAttribute('position', new THREE.BufferAttribute(position, 3));
        geometry.addAttribute('size', new THREE.BufferAttribute(size, 1));
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
        dout[typechem].push(particule);
        scene.add(particule);
    }
    return dout;
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
    var geom = new THREE.Geometry(),
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
    geom.vertices.push(src.clone());
    geom.vertices.push(dst.clone());
    geom.computeLineDistances(); // This one is SUPER important, otherwise dashed lines will appear as simple plain lines
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

//light position ///not use
function posLights(xmax, ymax, zmax, scale, color) {
    var llights = [];
    for (var x = -xmax; x < xmax; x = x + scale) {
        for (var y = -ymax; y < ymax; y = y + scale) {
            for (var z = -zmax; z < zmax; z = z + scale) {
                var light = posLight(x, y, z, color);
                scene.add(light);
                llights.push(light);
            }
        }
    }
    return llights;
}

function posLight(x, y, z, color) {
    var light;
    var intensity = 100;
    var distance = 300;
    var decay = 2.0;
    var sphere = new THREE.SphereGeometry(0.1, 10, 8);
    light = new THREE.PointLight(color, intensity, distance, decay);
    light.add(new THREE.Mesh(sphere, new THREE.MeshBasicMaterial({ color: color })));
    light.position.x = x;
    light.position.y = y;
    light.position.z = z;
    return light;
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


//var fs = require('fs');



// map function
function drawChemical() {
    document.getElementById('drawChemical');
    var textureLoader = new THREE.TextureLoader();
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            if (ID == dpoints[ktype][i].name) {
                console.log(ktype)
                var namepng = dSMILESClass[dpoints[ktype][i].name]['inchikey'];
                ppng = "/static/chemmaps/png/" + namepng + '.png'
                //if(fs.exists(ppng) == true){
                    var texture = textureLoader.load(ppng);
                    dpoints[ktype][i].material.map = texture;
                    console.log('/static/chemmaps/png/' + namepng + '.png')
                    dpoints[ktype][i].material.size = 15;
                    dpoints[ktype][i].material.color.setHex(0xffffff);
                    dpoints[ktype][i].col = 0xffffff;
                    dpoints[ktype][i].material.map.needsUpdate = true;
                    dpoints[ktype][i].material.size.needsUpdate = true;
               // } else {
               //     console.log(ppng);
                //}
            }
        }
    }
}

function downloadNeighbor() {
    var element = document.createElement('a');
    var filname = ID + '.csv';
    var textin = 'ID\tSMILES\tinchikey\tGroup';

    var IDcenter = dneighbors[ID][0];
    
    var ldesc = Object.keys(dinfo[ID]);
    // write header
    for (var idesc in ldesc) {
        textin = textin + '\t' + ldesc[idesc];
    }
    textin = textin + '\tdistance\n';
    //textin = textin + createLineWriteForTable(ID, ldesc);
    
    for (var i = 0; i < dneighbors[ID].length; i++) {
        textin = textin + createLineWriteForTable(dneighbors[ID][i], IDcenter, ldesc);
    }
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textin));
    element.setAttribute('download', filname);

    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function createLineWriteForTable(IDchem, IDcenter, ldesc) {
    var lineW =
        IDchem +
        '\t' +
        dSMILESClass[IDchem]['SMILES'] +
        '\t' +
        dSMILESClass[IDchem]['inchikey'] +
        '\t';
    if (map == 'DrugMap') {
        lineW = lineW + dSMILESClass[IDchem]['DRUG_GROUPS'];
    } else {
        lineW = lineW + dSMILESClass[IDchem]['GHS_category'];
    }
    for (var idesc in ldesc) {
        lineW = lineW + '\t' + dinfo[IDchem][ldesc[idesc]];
    }
    dist = computeEuclidian(IDchem, IDcenter); // add var?
    lineW = lineW + "\t" + dist + '\n';
    
    return lineW;
}

function computeEuclidian(ID1, ID2){

    var x1 = dcoords[ID1][0] * fact;
    var y1 = dcoords[ID1][1] * fact;
    var z1 = dcoords[ID1][2] * fact;

    var x2 = dcoords[ID2][0] * fact;
    var y2 = dcoords[ID2][1] * fact;
    var z2 = dcoords[ID2][2] * fact;

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
    console.log(lneighbor);
    lneighbor = lneighbor.splice(0, that.value);
    if (ID in dlines) {
        for (var i = 0; i < dlines[ID].length; i++) {
            scene.remove(dlines[ID][i]);
        }
        dlines[ID] = [];
    }
    for (ktype in dpoints) {
        for (var i = 0; i < dpoints[ktype].length; i++) {
            var IDtemp = dpoints[ktype][i].name;
            if (lneighbor.indexOf(IDtemp) != -1) {
                line = buildLine(
                    new THREE.Vector3(coorblock['x'], coorblock['y'], coorblock['z']),
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
                if (flag == 0) {
                    if (map == 'drugMap') {
                        if (dinfo[IDtemp]['Drug group'].search('NA') !== -1) {
                            var typeChem = 'approved';
                        } else if (dinfo[IDtemp]['Drug group'].search('withdraw') !== -1) {
                            var typeChem = 'withdraw';
                        } else if (dinfo[IDtemp]['Drug group'].search('User') !== -1) {
                            var typeChem = 'add';
                        } else {
                            var typeChem = 'indev';
                        }
                        var coloradd = dcol[typeChem];
                    } else if (map == 'DSSToxMap' || map == 'PFASMap' || map == 'Tox21Map') {
                        if (dSMILESClass[IDtemp]['GHS_category'] == 'NA') {
                            var typeChem = 'noclassified';
                        } else if (dSMILESClass[IDtemp]['GHS_category'] == 'User') {
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




// rewrite search function
//function searchID(that) {
//    var thatUpper = that.toUpperCase();
//    for (ktype in dpoints) {
//        for (var i = 0; i < dpoints[ktype].length; i++) {
//            if (thatUpper == dpoints[ktype][i].name) {
//                ID = thatUpper;
//                new TWEEN.Tween(controls.target)
//                    .to(
//                        {
//                            x: dcoords[ID][0] * fact,
//                            y: dcoords[ID][1] * fact,
//                            z: dcoords[ID][2] * fact,
//                        },
//                        500
//                    )
//                    //.easing( TWEEN.Easing.Elastic.Out).start();
//                    .easing(TWEEN.Easing.Linear.None)
//                   .start();
//                updateInfoBox(dpoints[ktype][i]);
//                return;
//            }
//        }
//    }
//    var thatlower = that.toLowerCase();
//    for (ktype in dpoints) {
//        for (var i = 0; i < dpoints[ktype].length; i++) {
//            var IDsearch = dpoints[ktype][i].name;
//            var genericlower = dinfo[IDsearch][1].toLowerCase();
//            if (
//                dinfo[IDsearch][5].search(thatlower) != -1 ||
//                genericlower.search(thatlower) != -1
//            ) {
//                ID = IDsearch;
//                new TWEEN.Tween(controls.target)
//                    .to(
//                        {
//                            x: dcoords[ID][0] * fact,
//                            y: dcoords[ID][1] * fact,
//                            z: dcoords[ID][2] * fact,
//                        },
//                        500
//                    )
//                    .easing(TWEEN.Easing.Linear.None)
//                    .start();
//                //    cameraCenterPoint();
//                updateInfoBox(dpoints[ktype][i]);
//                return;
//            }
//        }
//    }
//    alert(that + ' is not a valide request\nReset the map and/or check your request\n\n');
//}

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
