//position points on the map

var drawMode = "objects";
var cloudRoot = "";
var chemicalRoot = "";
var cloudPoints = {classified: null, noclassified: null};
var showClassified = true;
var showPlain = true;
var cloudById = {};
var addedIds = [];
var cloudHighlight = null;
var structurePoint = null;
var cloudFrameDistance = 1;
var cloudFullRadius = 1;
var pointerDirty = false;
var detailToken = 0;
var chemicalRequests = {};

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
            }else if(Assaycat.search("QC omit") !== -1){
                var colorhexa = dcol['QC omit'];
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

function circleSprite() {
    var canvas = document.createElement("canvas");
    canvas.width = 32;
    canvas.height = 32;
    var ctx = canvas.getContext("2d");
    ctx.beginPath();
    ctx.arc(16, 16, 15, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    return new THREE.CanvasTexture(canvas);
}

function makeCloud(positions, colors, ids, sprite, size) {
    var geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));
    var material = new THREE.PointsMaterial({
        size: size,
        map: sprite,
        alphaTest: 0.1,
        transparent: true,
        vertexColors: true,
        sizeAttenuation: false,
    });
    var cloud = new THREE.Points(geometry, material);
    cloud.userData.ids = ids;
    scene.add(cloud);
    return cloud;
}

function posPointCloud(payload) {
    var classifiedPos = [];
    var classifiedCol = [];
    var classifiedIds = [];
    var plainPos = [];
    var plainCol = [];
    var plainIds = [];
    var color = new THREE.Color();
    cloudById = {};
    for (var i = 0; i < payload.ids.length; i++) {
        var id = payload.ids[i];
        var x = payload.x[i];
        var y = payload.y[i];
        var z = payload.z[i];
        if (!(id in dcoords)) {
            dcoords[id] = [x, y, z];
        }
        var ghs = payload.ghs[i] == null || payload.ghs[i] === "" ? "NA" : String(payload.ghs[i]);
        if (!dSMILESClass[id]) {
            dSMILESClass[id] = {GHS_category: ghs, SMILES: "", inchikey: ""};
        } else if (!dSMILESClass[id].GHS_category) {
            dSMILESClass[id].GHS_category = ghs;
        }
        var hex = dcolGHS[ghs];
        if (hex == null) {
            hex = dcolGHS["NA"];
        }
        color.setHex(hex);
        var bucketPos = ghs === "NA" ? plainPos : classifiedPos;
        var bucketCol = ghs === "NA" ? plainCol : classifiedCol;
        var bucketIds = ghs === "NA" ? plainIds : classifiedIds;
        bucketPos.push(x * fact, y * fact, z * fact);
        bucketCol.push(color.r, color.g, color.b);
        bucketIds.push(id);
    }
    var dot = circleSprite();
    if (classifiedIds.length) {
        cloudPoints.classified = makeCloud(
            classifiedPos, classifiedCol, classifiedIds, dot, 8
        );
        cloudPoints.classified.visible = showClassified;
        for (var c = 0; c < classifiedIds.length; c++) {
            cloudById[classifiedIds[c]] = {object: cloudPoints.classified, index: c};
        }
    }
    if (plainIds.length) {
        cloudPoints.noclassified = makeCloud(
            plainPos, plainCol, plainIds, dot, 7
        );
        cloudPoints.noclassified.visible = showPlain;
        for (var n = 0; n < plainIds.length; n++) {
            cloudById[plainIds[n]] = {object: cloudPoints.noclassified, index: n};
        }
    }
    chemIds = payload.ids.slice();
    var extra = 0;
    for (var a = 0; a < addedIds.length; a++) {
        if (!cloudById[addedIds[a]]) {
            extra++;
        }
    }
    nbchem.textContent = String(payload.ids.length + extra);
}

function placeAdded() {
    for (var i = 0; i < addedIds.length; i++) {
        var id = addedIds[i];
        if (!dcoords[id]) {
            continue;
        }
        var point = posPoint(dcoords[id], id, 0xffffff, dsprite.add, dsize.add, fact, scene);
        dpoints.add.push(point);
    }
}

function frameCloud() {
    var box = new THREE.Box3();
    if (cloudPoints.classified) {
        box.expandByObject(cloudPoints.classified);
    }
    if (cloudPoints.noclassified) {
        box.expandByObject(cloudPoints.noclassified);
    }
    if (box.isEmpty()) {
        return;
    }
    var center = box.getCenter(new THREE.Vector3());
    var size = box.getSize(new THREE.Vector3());
    var radius = 0.5 * Math.sqrt(size.x * size.x + size.y * size.y + size.z * size.z);
    if (radius < 1) {
        radius = 1;
    }
    camera.fov = 60;
    camera.near = Math.max(radius / 1000, 0.1);
    camera.far = radius * 20;
    camera.updateProjectionMatrix();
    controls.target.copy(center);
    cloudFullRadius = radius;
    // Closer than a fit-all view, so neighboring chemicals sit apart on screen.
    // Point size stays in pixels. Attenuation would swell the chemicals nearest the camera.
    cloudFrameDistance = radius * 0.28;
    camera.position.set(center.x + radius * 0.06, center.y - radius * 0.08, center.z + cloudFrameDistance);
    if (cloudPoints.classified) {
        cloudPoints.classified.material.size = 8;
        cloudPoints.classified.material.needsUpdate = true;
    }
    if (cloudPoints.noclassified) {
        cloudPoints.noclassified.material.size = 7;
        cloudPoints.noclassified.material.needsUpdate = true;
    }
    controls.maxDistance = radius * 4;
    controls.update();
}

function clearCloudHighlight() {
    if (!cloudHighlight) {
        return;
    }
    var colors = cloudHighlight.object.geometry.getAttribute("color");
    colors.setXYZ(cloudHighlight.index, cloudHighlight.r, cloudHighlight.g, cloudHighlight.b);
    colors.needsUpdate = true;
    cloudHighlight = null;
}

function highlightCloudIndex(object, index) {
    if (cloudHighlight && cloudHighlight.object === object && cloudHighlight.index === index) {
        return;
    }
    clearCloudHighlight();
    var colors = object.geometry.getAttribute("color");
    cloudHighlight = {
        object: object,
        index: index,
        r: colors.getX(index),
        g: colors.getY(index),
        b: colors.getZ(index),
    };
    colors.setXYZ(index, 1, 0, 0);
    colors.needsUpdate = true;
}

function paintCloud(hexForId) {
    clearCloudHighlight();
    var color = new THREE.Color();
    var groups = [cloudPoints.classified, cloudPoints.noclassified];
    for (var g = 0; g < groups.length; g++) {
        var points = groups[g];
        if (!points) {
            continue;
        }
        var ids = points.userData.ids;
        var colors = points.geometry.getAttribute("color");
        for (var i = 0; i < ids.length; i++) {
            color.setHex(hexForId(ids[i]));
            colors.setXYZ(i, color.r, color.g, color.b);
        }
        colors.needsUpdate = true;
    }
    if (dpoints && dpoints.add) {
        for (var a = 0; a < dpoints.add.length; a++) {
            var hex = hexForId(dpoints.add[a].name);
            dpoints.add[a].col = hex;
            dpoints.add[a].material.color.setHex(dpoints.add[a].name === ID ? 0xff0000 : hex);
        }
    }
    if (ID && cloudById[ID]) {
        highlightCloudIndex(cloudById[ID].object, cloudById[ID].index);
    }
}

function ensureChemical(id) {
    if (!id) {
        return Promise.resolve(false);
    }
    var known = dSMILESClass[id];
    if (known && (known.detailLoaded || (known.SMILES && dneighbors[id]))) {
        return Promise.resolve(true);
    }
    if (chemicalRequests[id]) {
        return chemicalRequests[id];
    }
    var request = fetch(chemicalRoot + encodeURIComponent(id) + "/", {credentials: "same-origin"}).then(function(response) {
        if (!response.ok) {
            throw new Error("chemical");
        }
        return response.json();
    }).then(function(body) {
        if (!dSMILESClass[id]) {
            dSMILESClass[id] = {};
        }
        dSMILESClass[id].SMILES = body.smiles || "";
        dSMILESClass[id].inchikey = body.inchikey || "";
        if (body.ghs) {
            dSMILESClass[id].GHS_category = body.ghs;
        }
        dneighbors[id] = body.neighbors || [];
        dSMILESClass[id].detailLoaded = true;
        return true;
    }).catch(function() {
        return false;
    }).then(function(ok) {
        delete chemicalRequests[id];
        return ok;
    });
    chemicalRequests[id] = request;
    return request;
}

function selectCloudId(id, object, index) {
    if (block != 0) {
        return;
    }
    var record = dSMILESClass[id];
    var known = record && (record.detailLoaded || (record.SMILES && dneighbors[id]));
    if (object && index != null) {
        highlightCloudIndex(object, index);
    }
    if (ID === id && (known || chemicalRequests[id])) {
        return;
    }
    ID = id;
    if (object && index != null) {
        highlightCloudIndex(object, index);
    }
    var coords = dcoords[id];
    if (coords) {
        coorblock.x = coords[0] * fact;
        coorblock.y = coords[1] * fact;
        coorblock.z = coords[2] * fact;
    }
    var token = ++detailToken;
    updateInfoBox(null);
    ensureChemical(id).then(function(ok) {
        if (token !== detailToken || ID !== id) {
            return;
        }
        if (ok || (dSMILESClass[id] && dSMILESClass[id].GHS_category)) {
            updateInfoBox(null);
        }
    });
}

function focusCloud(id) {
    var loc = cloudById[id];
    var coords = dcoords[id];
    if (!loc && !coords) {
        return;
    }
    if (coords) {
        var distance = cloudFullRadius * 0.12;
        controls.target.set(coords[0] * fact, coords[1] * fact, coords[2] * fact);
        camera.position.set(
            coords[0] * fact + distance * 0.2,
            coords[1] * fact - distance * 0.3,
            coords[2] * fact + distance
        );
        controls.update();
    }
    if (loc) {
        selectCloudId(id, loc.object, loc.index);
    }
}

function cloudThreshold() {
    var dist = camera.position.distanceTo(controls.target);
    var fov = (camera.fov || 60) * Math.PI / 180;
    var worldPerPixel = 2 * Math.tan(fov / 2) * dist / window.innerHeight;
    return worldPerPixel * 8;
}

function intersectCloud() {
    raycaster.params.Points.threshold = cloudThreshold();
    var hits = [];
    if (cloudPoints.classified && cloudPoints.classified.visible) {
        hits = hits.concat(raycaster.intersectObject(cloudPoints.classified, false));
    }
    if (cloudPoints.noclassified && cloudPoints.noclassified.visible) {
        hits = hits.concat(raycaster.intersectObject(cloudPoints.noclassified, false));
    }
    for (var typedrug in dpoints) {
        if (dpoints[typedrug].length) {
            hits = hits.concat(raycaster.intersectObjects(dpoints[typedrug], true));
        }
    }
    if (!hits.length || block != 0) {
        return;
    }
    hits.sort(function(a, b) {
        var rayA = a.distanceToRay == null ? a.distance : a.distanceToRay;
        var rayB = b.distanceToRay == null ? b.distance : b.distanceToRay;
        return rayA - rayB;
    });
    var hit = hits[0];
    if (hit.index != null && hit.object.userData && hit.object.userData.ids) {
        selectCloudId(hit.object.userData.ids[hit.index], hit.object, hit.index);
        return;
    }
    ID = hit.object.name;
    coorblock.x = hit.point.x;
    coorblock.y = hit.point.y;
    coorblock.z = hit.point.z;
    updateInfoBox(hit.object);
}

function connectCloudNeighbor(that) {
    if (!ID) {
        return;
    }
    ensureChemical(ID).then(function(ok) {
        if (!ok || ID == null) {
            return;
        }
        var lneighbor = Object.assign([], dneighbors[ID] || []);
        lneighbor = lneighbor.splice(0, that.value);
        if (ID in dlines) {
            for (var i = 0; i < dlines[ID].length; i++) {
                scene.remove(dlines[ID][i]);
            }
            dlines[ID] = [];
        }
        var origin = dcoords[ID];
        if (!origin) {
            return;
        }
        for (var n = 0; n < lneighbor.length; n++) {
            var neighbor = dcoords[lneighbor[n]];
            if (!neighbor) {
                continue;
            }
            var line = buildLine(
                new THREE.Vector3(origin[0] * fact, origin[1] * fact, origin[2] * fact),
                new THREE.Vector3(neighbor[0] * fact, neighbor[1] * fact, neighbor[2] * fact),
                0xff0000,
                false
            );
            scene.add(line);
            if (!(ID in dlines)) {
                dlines[ID] = [];
            }
            dlines[ID].push(line);
        }
    });
}

function neighborhoodCenter(id) {
    if (/^DTXSID\d+$/.test(id)) {
        return id;
    }
    var inchikey = dSMILESClass[id] && dSMILESClass[id].inchikey;
    if (inchikey) {
        return inchikey;
    }
    return id;
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
    if (pointerDirty) {
        pointerDirty = false;
        raycaster.setFromCamera(mouse, camera);
        intersectCompound();
    }
    renderer.render(scene, camera);
}

function onMouseMove(event) {
    //console.log(event.preventDefault());
    mouse.x = event.clientX / window.innerWidth * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    pointerDirty = true;
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
    if (drawMode === "cloud" && cloudById[ID] && dcoords[ID]) {
        var chemOnFly = document.getElementById("Compoundpng2");
        var texture = new THREE.CanvasTexture(chemOnFly);
        if (!structurePoint) {
            structurePoint = posPoint(dcoords[ID], ID, 0xffffff, texture, 15, fact, scene);
        } else {
            structurePoint.position.set(dcoords[ID][0] * fact, dcoords[ID][1] * fact, dcoords[ID][2] * fact);
            structurePoint.material.map = texture;
            structurePoint.material.map.needsUpdate = true;
            structurePoint.material.color.setHex(0xffffff);
        }
        return;
    }
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
    var detail = ID && dSMILESClass[ID];
    if (drawMode === "cloud" && ID && !(detail && (detail.detailLoaded || (detail.SMILES && dneighbors[ID])))) {
        ensureChemical(ID).then(function(ok) {
            if (ok) {
                downloadNeighbor();
            }
        });
        return;
    }
    var element = document.createElement('a');
    var filname = ID + '.csv';
    var textin = 'ID\tSMILES\tinchikey\tGroup';

    var IDcenter = ID;
    //console.log(ID);
    
    //var ldesc = Object.keys(dinfo[ID]);
    //console.log(ldesc);
    //console.log(dSMILESClass[ID]);
    // write header
    var exportLabels = cardFeatureLabels();
    for (var idesc in exportLabels) {
        textin = textin + '\t' + exportLabels[idesc];
    }
    textin = textin + '\tdistance\n';
    textin = textin + createLineWriteForTable(IDcenter, IDcenter, exportLabels);
    
    //console.log(dneighbors[IDcenter]);
    for (var p = 0; p < dneighbors[IDcenter].length; p++) {
        if(dneighbors[IDcenter][p] in dSMILESClass){
            textin = textin + createLineWriteForTable(dneighbors[IDcenter][p], IDcenter, exportLabels);
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
        var cell = dinfo[IDchem] && dinfo[IDchem][ldesc[idesc]] != null ? dinfo[IDchem][ldesc[idesc]] : "NA";
        lineW = lineW + '\t' + cell.toString();
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
    if (drawMode === "cloud") {
        intersectCloud();
        return;
    }
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
    if (drawMode === "cloud") {
        connectCloudNeighbor(that);
        return;
    }

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
    if (drawMode === "cloud") {
        if (!ID) {
            return;
        }
        window.location = "/chemmaps/DSSToxMap3D/?center=" + encodeURIComponent(neighborhoodCenter(ID)) + "&view=neighborhood";
        return;
    }
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
    if (drawMode === "cloud") {
        if (cloudById[thatUpper] || dcoords[thatUpper]) {
            focusCloud(thatUpper);
            return;
        }
        alert(that + ' is not a valide request\nReset the map and/or check your request\n\n');
        return;
    }
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
