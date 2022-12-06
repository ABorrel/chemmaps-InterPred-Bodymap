function hex(c) {
    var s = "0123456789abcdef";
    var i = parseInt(c);
    if (i == 0 || isNaN(c))
        return "00";
    i = Math.round(Math.min(Math.max(0, i), 255));
    return s.charAt((i - i % 16) / 16) + s.charAt(i % 16);
}

/* Convert an RGB triplet to a hex string */
function convertToHex(rgb) {
    return hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
}


/* Remove '#' in color hex string */
function trim(s) {
    return (s.charAt(0) == '#') ? s.substring(1, 7) : s
}

/* Convert a hex string to an RGB triplet */
function convertToRGB(hex) {
    var color = [];
    color[0] = parseInt((trim(hex)).substring(0, 2), 16);
    color[1] = parseInt((trim(hex)).substring(2, 4), 16);
    color[2] = parseInt((trim(hex)).substring(4, 6), 16);
    return color;
}

function generateColor(colorStart, colorEnd, colorCount) {

    // The beginning of your gradient
    var start = convertToRGB(colorStart);

    // The end of your gradient
    var end = convertToRGB(colorEnd);

    // The number of colors to compute
    var len = colorCount;

    //Alpha blending amount
    var alpha = 0.0;
    var saida = [];
    for (i = 0; i < len; i++) {
        var c = [];
        alpha += (1.0 / len);
        c[0] = start[0] * alpha + (1 - alpha) * end[0];
        c[1] = start[1] * alpha + (1 - alpha) * end[1];
        c[2] = start[2] * alpha + (1 - alpha) * end[2];
        saida.push("#" + convertToHex(c));
    }
    return saida;
}



//toolbox
function range(h, c, b) {

    var i = [];
    var d, f, e;
    var a = b || 1;
    var g = false;
    if (!isNaN(h) && !isNaN(c)) {
        d = h;
        f = c;
    } else {
        if (isNaN(h) && isNaN(c)) {
            g = true;
            d = h.charCodeAt(0);
            f = c.charCodeAt(0);
        } else {
            d = (isNaN(h) ? 0 : h);
            f = (isNaN(c) ? 0 : c);
        }
    }
    e = ((d > f) ? false : true);
    if (e) {
        while (d <= f) {
            i.push(((g) ? String.fromCharCode(d) : d));
            d += a;
        }
    } else {
        while (d >= f) {
            i.push(((g) ? String.fromCharCode(d) : d));
            d -= a;
        }
    }
    return i;
}
;

function round(value, exp) {
    if (typeof exp === 'undefined' || +exp === 0)
        return Math.round(value);

    value = +value;
    exp = +exp;

    if (isNaN(value) || !(typeof exp === 'number' && exp % 1 === 0))
        return NaN;

    // Shift
    value = value.toString().split('e');
    value = Math.round(+(value[0] + 'e' + (value[1] ? (+value[1] + exp) : exp)));

    // Shift back
    value = value.toString().split('e');
    return +(value[0] + 'e' + (value[1] ? (+value[1] - exp) : -exp));
}
;

function getMedian(args) {
    if (!args.length) {
        return 0
    }
    ;
    var numbers = args.slice(0).sort((a, b) => a - b);
    var middle = Math.floor(numbers.length / 2);
    var isEven = numbers.length % 2 === 0;
    return isEven ? (numbers[middle] + numbers[middle - 1]) / 2 : numbers[middle];
}
;

function calculateEcart(camera, pos, nstep) {

// *30 because position initial include in the
    decart["x"] = ((pos[0]) - camera.position.x) / nstep;
    decart["y"] = ((pos[1]) - camera.position.y) / nstep;
    decart["z"] = ((pos[2]) - camera.position.z) / nstep;
}
;

function centroid(din) {
    var Sx = 0;
    var Sy = 0;
    var Sz = 0;
    var nPoints = 0;

    for (var i in din) {
        Sx = Sx + parseFloat(din[i][0] * fact);
        Sy = Sy + parseFloat(din[i][1] * fact);
        Sz = Sz + parseFloat(din[i][2] * fact);
        nPoints = nPoints + 1;
    }
    ;
    
    var centroid = new Float32Array(3);
    centroid[0] = Sx / nPoints;
    centroid[1] = Sy / nPoints;
    centroid[2] = Sz / nPoints;

    return(centroid);
}
;


function genRandonString(length) {
    var chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    var charLength = chars.length;
    var result = '';
    for ( var i = 0; i < length; i++ ) {
       result += chars.charAt(Math.floor(Math.random() * charLength));
    }
    return result;
 }