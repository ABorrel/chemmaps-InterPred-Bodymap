// Zoom-adaptive local screen-space separation for overlapping map points.

var LOCAL_RADIUS_PX = 300;
var MIN_GAP_PX = 28;
var MAX_ITERATIONS = 10;
var LERP_FACTOR = 0.25;
var UPDATE_THROTTLE_MS = 16;
var MAX_FOREGROUND_POINTS = 50;
var SPREAD_EPS = 0.001;
var GRID_CELL_PX = 40;
// Only spread points near the camera depth of the closest visible point in view.
var NEAR_DEPTH_FRACTION = 0.12;
// Spread only when zoomed in near the maximum (closest fraction of the zoom range).
var MIN_ZOOM_FRACTION = 0.08;
var SPREAD_RANGE_FRACTION = 0.12;

var pointSpreadState = {
    camera: null,
    controls: null,
    renderer: null,
    allPoints: [],
    refDistance: 0,
    minZoomDistance: 0,
    spreadStartDistance: 0,
    lastUpdateTime: 0,
    needsRepulsion: true,
    lastSpread: 0,
    spreadTargets: {},
};

var _tmpVec = new THREE.Vector3();

function collectPointsFromDpoints(dpoints) {
    var points = [];
    for (var typeKey in dpoints) {
        if (!dpoints.hasOwnProperty(typeKey)) {
            continue;
        }
        for (var i = 0; i < dpoints[typeKey].length; i++) {
            points.push(dpoints[typeKey][i]);
        }
    }
    return points;
}

function ensureBasePosition(point) {
    if (point.userData.basePosition) {
        return;
    }
    var pos = point.geometry.attributes.position;
    point.userData.basePosition = new THREE.Vector3(
        pos.getX(0),
        pos.getY(0),
        pos.getZ(0)
    );
    point.userData.pickRadius = point.material.size;
    point.userData.displayPosition = point.userData.basePosition.clone();
}

function initPointSpread(options) {
    pointSpreadState.camera = options.camera;
    pointSpreadState.controls = options.controls;
    pointSpreadState.renderer = options.renderer;
    pointSpreadState.allPoints = collectPointsFromDpoints(options.dpoints);
    pointSpreadState.refDistance = options.camera.position.distanceTo(options.controls.target);
    pointSpreadState.minZoomDistance = Math.max(
        options.controls.minDistance || 0,
        pointSpreadState.refDistance * MIN_ZOOM_FRACTION
    );
    pointSpreadState.spreadStartDistance =
        pointSpreadState.minZoomDistance +
        (pointSpreadState.refDistance - pointSpreadState.minZoomDistance) * SPREAD_RANGE_FRACTION;
    pointSpreadState.spreadTargets = {};

    for (var i = 0; i < pointSpreadState.allPoints.length; i++) {
        ensureBasePosition(pointSpreadState.allPoints[i]);
    }

    options.controls.addEventListener('change', function() {
        pointSpreadState.needsRepulsion = true;
    });
}

function computeSpreadFactor() {
    var camera = pointSpreadState.camera;
    var controls = pointSpreadState.controls;
    if (!camera || !controls || pointSpreadState.refDistance <= 0) {
        return 0;
    }
    var dist = camera.position.distanceTo(controls.target);
    if (dist >= pointSpreadState.spreadStartDistance) {
        return 0;
    }
    var nearDist = pointSpreadState.minZoomDistance;
    var startDist = pointSpreadState.spreadStartDistance;
    if (startDist <= nearDist) {
        return dist <= nearDist ? 1 : 0;
    }
    return Math.min(1, (startDist - dist) / (startDist - nearDist));
}

function projectToScreen(worldPos, camera, renderer) {
    _tmpVec.copy(worldPos).project(camera);
    var width = renderer.domElement.clientWidth;
    var height = renderer.domElement.clientHeight;
    return {
        x: (_tmpVec.x * 0.5 + 0.5) * width,
        y: (-_tmpVec.y * 0.5 + 0.5) * height,
        z: _tmpVec.z,
    };
}

function getScreenRadius(point, worldPos, camera, renderer) {
    var materialSize = point.material.size;
    var screen = projectToScreen(worldPos, camera, renderer);
    var worldOffset = screenDeltaToWorld(materialSize, 0, worldPos, camera, renderer);
    var screen2 = projectToScreen(worldPos.clone().add(worldOffset), camera, renderer);
    var pixelDiameter = Math.sqrt(
        Math.pow(screen2.x - screen.x, 2) + Math.pow(screen2.y - screen.y, 2)
    );
    return Math.max(pixelDiameter * 0.5, 4);
}

function screenDeltaToWorld(deltaX, deltaY, worldPos, camera, renderer) {
    var width = renderer.domElement.clientWidth;
    var height = renderer.domElement.clientHeight;
    var screen = projectToScreen(worldPos, camera, renderer);
    var ndc1 = new THREE.Vector3(
        (screen.x / width) * 2 - 1,
        -(screen.y / height) * 2 + 1,
        screen.z
    );
    var ndc2 = new THREE.Vector3(
        ((screen.x + deltaX) / width) * 2 - 1,
        -((screen.y + deltaY) / height) * 2 + 1,
        screen.z
    );
    var w1 = ndc1.unproject(camera);
    var w2 = ndc2.unproject(camera);
    return w2.sub(w1);
}

function writePointPosition(point, vec) {
    var attr = point.geometry.attributes.position;
    attr.setXYZ(0, vec.x, vec.y, vec.z);
    attr.needsUpdate = true;
    point.geometry.computeBoundingSphere();
    point.geometry.boundingSphere.radius = point.userData.pickRadius || point.material.size;
}

function getCameraDistance(worldPos, camera) {
    return camera.position.distanceTo(worldPos);
}

function getLocalCandidates(spread) {
    var camera = pointSpreadState.camera;
    var renderer = pointSpreadState.renderer;
    var centerX = renderer.domElement.clientWidth * 0.5;
    var centerY = renderer.domElement.clientHeight * 0.5;
    var radiusSq = LOCAL_RADIUS_PX * LOCAL_RADIUS_PX;
    var pool = [];
    var allPoints = pointSpreadState.allPoints;

    for (var i = 0; i < allPoints.length; i++) {
        var point = allPoints[i];
        if (!point.visible) {
            continue;
        }
        ensureBasePosition(point);
        var base = point.userData.basePosition;
        var screen = projectToScreen(base, camera, renderer);
        if (screen.z < -1 || screen.z > 1) {
            continue;
        }
        var dx = screen.x - centerX;
        var dy = screen.y - centerY;
        if (dx * dx + dy * dy > radiusSq) {
            continue;
        }
        pool.push({
            point: point,
            sx: screen.x,
            sy: screen.y,
            radius: getScreenRadius(point, base, camera, renderer),
            cameraDist: getCameraDistance(base, camera),
            ox: 0,
            oy: 0,
        });
    }

    if (pool.length === 0) {
        return [];
    }

    pool.sort(function(a, b) {
        return a.cameraDist - b.cameraDist;
    });

    var closestDist = pool[0].cameraDist;
    var depthLimit = closestDist * (1 + NEAR_DEPTH_FRACTION);
    depthLimit = Math.max(
        depthLimit,
        closestDist + pointSpreadState.refDistance * 0.01
    );

    var candidates = [];
    for (var j = 0; j < pool.length && candidates.length < MAX_FOREGROUND_POINTS; j++) {
        if (pool[j].cameraDist <= depthLimit) {
            candidates.push(pool[j]);
        }
    }

    return candidates;
}

function runRepulsion(candidates) {
    var cellSize = GRID_CELL_PX;
    var grid = {};

    function cellKey(x, y) {
        return Math.floor(x / cellSize) + ',' + Math.floor(y / cellSize);
    }

    function addToGrid(item, index) {
        var key = cellKey(item.sx + item.ox, item.sy + item.oy);
        if (!grid[key]) {
            grid[key] = [];
        }
        grid[key].push(index);
    }

    for (var iter = 0; iter < MAX_ITERATIONS; iter++) {
        grid = {};
        for (var i = 0; i < candidates.length; i++) {
            addToGrid(candidates[i], i);
        }

        for (i = 0; i < candidates.length; i++) {
            var a = candidates[i];
            var ax = a.sx + a.ox;
            var ay = a.sy + a.oy;
            var cx = Math.floor(ax / cellSize);
            var cy = Math.floor(ay / cellSize);

            for (var gx = cx - 1; gx <= cx + 1; gx++) {
                for (var gy = cy - 1; gy <= cy + 1; gy++) {
                    var bucket = grid[gx + ',' + gy];
                    if (!bucket) {
                        continue;
                    }
                    for (var b = 0; b < bucket.length; b++) {
                        var j = bucket[b];
                        if (j <= i) {
                            continue;
                        }
                        var c = candidates[j];
                        var dx = ax - (c.sx + c.ox);
                        var dy = ay - (c.sy + c.oy);
                        var distSq = dx * dx + dy * dy;
                        var minDist = a.radius + c.radius + MIN_GAP_PX;
                        if (distSq >= minDist * minDist) {
                            continue;
                        }
                        var dist = Math.sqrt(distSq);
                        if (dist < 0.001) {
                            dist = 0.001;
                            dx = 1;
                            dy = 0;
                        }
                        var push = (minDist - dist) * 0.5;
                        var nx = dx / dist;
                        var ny = dy / dist;
                        a.ox += nx * push;
                        a.oy += ny * push;
                        c.ox -= nx * push;
                        c.oy -= ny * push;
                    }
                }
            }
        }
    }
}

function recomputeSpreadTargets(spread) {
    var camera = pointSpreadState.camera;
    var renderer = pointSpreadState.renderer;
    var targets = {};
    var candidates = getLocalCandidates(spread);

    if (candidates.length > 1) {
        runRepulsion(candidates);
    }

    for (var i = 0; i < candidates.length; i++) {
        var item = candidates[i];
        if (Math.abs(item.ox) < 0.01 && Math.abs(item.oy) < 0.01) {
            continue;
        }
        var base = item.point.userData.basePosition;
        var worldOffset = screenDeltaToWorld(item.ox, item.oy, base, camera, renderer);
        targets[item.point.name] = worldOffset;
    }

    pointSpreadState.spreadTargets = targets;
}

function applySpreadPositions(spread) {
    var allPoints = pointSpreadState.allPoints;
    var targets = pointSpreadState.spreadTargets;

    for (var i = 0; i < allPoints.length; i++) {
        var point = allPoints[i];
        ensureBasePosition(point);
        var base = point.userData.basePosition;
        var target = base;
        if (spread > SPREAD_EPS && targets.hasOwnProperty(point.name)) {
            target = base.clone().add(targets[point.name].clone().multiplyScalar(spread));
        }
        if (!point.userData.displayPosition) {
            point.userData.displayPosition = base.clone();
        }
        point.userData.displayPosition.lerp(target, LERP_FACTOR);
        writePointPosition(point, point.userData.displayPosition);
    }
}

function resetAllToBase() {
    var allPoints = pointSpreadState.allPoints;
    pointSpreadState.spreadTargets = {};

    for (var i = 0; i < allPoints.length; i++) {
        var point = allPoints[i];
        ensureBasePosition(point);
        var base = point.userData.basePosition;
        if (!point.userData.displayPosition) {
            point.userData.displayPosition = base.clone();
        }
        point.userData.displayPosition.lerp(base, LERP_FACTOR);
        if (point.userData.displayPosition.distanceToSquared(base) < 0.0001) {
            point.userData.displayPosition.copy(base);
        }
        writePointPosition(point, point.userData.displayPosition);
    }
}

function updatePointSpread() {
    if (!pointSpreadState.camera || !pointSpreadState.renderer) {
        return;
    }

    if (typeof dpoints !== 'undefined') {
        pointSpreadState.allPoints = collectPointsFromDpoints(dpoints);
    }

    var spread = computeSpreadFactor();
    if (Math.abs(spread - pointSpreadState.lastSpread) > 0.03) {
        pointSpreadState.needsRepulsion = true;
    }
    pointSpreadState.lastSpread = spread;

    if (spread <= SPREAD_EPS) {
        resetAllToBase();
        return;
    }

    var now = performance.now();
    if (
        pointSpreadState.needsRepulsion &&
        now - pointSpreadState.lastUpdateTime >= UPDATE_THROTTLE_MS
    ) {
        recomputeSpreadTargets(spread);
        pointSpreadState.lastUpdateTime = now;
        pointSpreadState.needsRepulsion = false;
    } else if (
        now - pointSpreadState.lastUpdateTime >= UPDATE_THROTTLE_MS &&
        Object.keys(pointSpreadState.spreadTargets).length === 0
    ) {
        recomputeSpreadTargets(spread);
        pointSpreadState.lastUpdateTime = now;
    }

    applySpreadPositions(spread);
}

function scheduleSpreadUpdate() {
    pointSpreadState.needsRepulsion = true;
}
