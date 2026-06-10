//have to be fix and generalized
var infoPanelInitialized = false;

function hideInfoPanel(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    var info = document.getElementById('info');
    var showTab = document.getElementById('infoShowTab');
    if (info) {
        info.classList.add('is-hidden');
    }
    if (showTab) {
        showTab.hidden = false;
    }
}

function showInfoPanel(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    var info = document.getElementById('info');
    var showTab = document.getElementById('infoShowTab');
    if (info) {
        info.classList.remove('is-hidden');
    }
    if (showTab) {
        showTab.hidden = true;
    }
    redrawInfoBoxSmiles();
}

function redrawInfoBoxSmiles() {
    var info = document.getElementById('info');
    if (!info || info.classList.contains('is-hidden')) {
        return;
    }
    if (typeof ID === 'undefined' || !ID || typeof dSMILESClass === 'undefined' || !dSMILESClass[ID]) {
        return;
    }
    var sizeCanvas = resizeCanvas();
    if (sizeCanvas <= 0) {
        return;
    }
    var options = { width: sizeCanvas, height: sizeCanvas };
    var smilesDrawer = new SmilesDrawer.Drawer(options);
    SmilesDrawer.parse(dSMILESClass[ID]['SMILES'], function(tree) {
        smilesDrawer.draw(tree, 'Compoundpng2', 'dark', false);
    });
}

function initInfoPanelDrag(chrome, panel) {
    chrome.addEventListener('mousedown', function(e) {
        if (e.target.closest('#infoHideBtn')) {
            return;
        }
        e.preventDefault();
        e.stopPropagation();

        if (typeof controls !== 'undefined' && controls) {
            controls.enabled = false;
        }

        var rect = panel.getBoundingClientRect();
        panel.style.right = 'auto';
        panel.style.bottom = 'auto';
        panel.style.left = rect.left + 'px';
        panel.style.top = rect.top + 'px';

        var startX = e.clientX;
        var startY = e.clientY;
        var startLeft = rect.left;
        var startTop = rect.top;

        function clampPosition(left, top) {
            var maxLeft = window.innerWidth - panel.offsetWidth - 4;
            var maxTop = window.innerHeight - panel.offsetHeight - 4;
            return {
                left: Math.min(maxLeft, Math.max(4, left)),
                top: Math.min(maxTop, Math.max(4, top)),
            };
        }

        function onMove(moveEvent) {
            moveEvent.preventDefault();
            moveEvent.stopPropagation();
            var pos = clampPosition(
                startLeft + (moveEvent.clientX - startX),
                startTop + (moveEvent.clientY - startY)
            );
            panel.style.left = pos.left + 'px';
            panel.style.top = pos.top + 'px';
        }

        function onUp(upEvent) {
            if (upEvent) {
                upEvent.preventDefault();
                upEvent.stopPropagation();
            }
            document.removeEventListener('mousemove', onMove, true);
            document.removeEventListener('mouseup', onUp, true);
            if (typeof controls !== 'undefined' && controls) {
                controls.enabled = true;
            }
        }

        document.addEventListener('mousemove', onMove, true);
        document.addEventListener('mouseup', onUp, true);
    });
}

function initInfoPanelResize(handle, panel) {
    handle.addEventListener('mousedown', function(e) {
        e.preventDefault();
        e.stopPropagation();

        if (typeof controls !== 'undefined' && controls) {
            controls.enabled = false;
        }

        var startX = e.clientX;
        var startY = e.clientY;
        var startW = panel.offsetWidth;
        var startH = panel.offsetHeight;
        var minW = 280;
        var minH = 140;
        var maxW = Math.min(window.innerWidth * 0.55, window.innerWidth - 24);
        var maxH = Math.min(window.innerHeight * 0.38, window.innerHeight - 80);

        function onMove(moveEvent) {
            moveEvent.preventDefault();
            moveEvent.stopPropagation();
            var newW = Math.min(maxW, Math.max(minW, startW + (moveEvent.clientX - startX)));
            var newH = Math.min(maxH, Math.max(minH, startH - (moveEvent.clientY - startY)));
            panel.style.width = newW + 'px';
            panel.style.height = newH + 'px';
        }

        function onUp(upEvent) {
            if (upEvent) {
                upEvent.preventDefault();
                upEvent.stopPropagation();
            }
            document.removeEventListener('mousemove', onMove, true);
            document.removeEventListener('mouseup', onUp, true);
            if (typeof controls !== 'undefined' && controls) {
                controls.enabled = true;
            }
            redrawInfoBoxSmiles();
        }

        document.addEventListener('mousemove', onMove, true);
        document.addEventListener('mouseup', onUp, true);
    });
}

function initInfoPanel() {
    if (infoPanelInitialized) {
        return;
    }
    infoPanelInitialized = true;

    var hideBtn = document.getElementById('infoHideBtn');
    var showTab = document.getElementById('infoShowTab');
    var info = document.getElementById('info');
    var chrome = info ? info.querySelector('.info-chrome') : null;
    var resizeHandle = document.getElementById('infoResizeHandle');

    if (hideBtn) {
        hideBtn.addEventListener('click', hideInfoPanel);
    }
    if (showTab) {
        showTab.addEventListener('click', showInfoPanel);
    }
    if (chrome && info) {
        initInfoPanelDrag(chrome, info);
    }
    if (resizeHandle && info) {
        initInfoPanelResize(resizeHandle, info);
    }
}

function updateInfoBox(intersect) {
    var sizeCanvas = resizeCanvas();
    var options = { width: sizeCanvas, height: sizeCanvas };
    var smilesDrawer = new SmilesDrawer.Drawer(options);

    CompoundID.innerHTML = ID;
    if (map == 'pfas' || map == 'dsstox' || map == 'tox21'|| map == 'Tox21Assay' || map == 'Tox21Target' || map == 'Tox21MostActive') {
        document.getElementById('CompoundID').href =
            'https://comptox.epa.gov/dashboard/chemical/details/' + ID;

        document.getElementById('LinkDSSTOX').href = "DSSTox/" + ID;

    } else if (map == 'drugbank') {
        document.getElementById('CompoundID').href = 'https://www.drugbank.ca/drugs/' + ID;
    }

    


    // case of DSStoxMap and PFASmap -> GHS
    if (map == 'pfas' || map == 'dsstox' || map == 'tox21' || map == 'Tox21Assay' || map == 'Tox21Target' || map == 'Tox21MostActive') {
        GHS.innerHTML = dSMILESClass[ID]['GHS_category'];
    } else if (map == 'drugbank') {
        Group.innerHTML = dSMILESClass[ID]['DRUG_GROUPS'];
    }

    var lboxes = [box1, box2, box3, box4, box5];
    for (let i = 0; i < 5; i++) {
        if (desctype[ldesc[i]] == 'str') {
            if (dinfo[ID][ldesc[i]].length > 50) {
                lboxes[i].innerHTML = dinfo[ID][ldesc[i]].substring(0, 60) + '...';
            } else {
                lboxes[i].innerHTML = dinfo[ID][ldesc[i]].toString();
            }
        } else if (desctype[ldesc[i]] == 'class') {
            lboxes[i].innerHTML = dinfo[ID][ldesc[i]].toString();
        } else if (desctype[ldesc[i]] == 'range') {
            if(dinfo[ID][ldesc[i]] == "NA"){
                lboxes[i].innerHTML = "NA";
            }else{
                lboxes[i].innerHTML = round(dinfo[ID][ldesc[i]], 2).toString();
            }
        } else {
            lboxes[i].innerHTML = dinfo[ID][ldesc[i]].toString();
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
//for png in infobox
function resizeCanvas() {
    var con = document.getElementById('pngcompound');
    if (!con) {
        return 0;
    }
    return Math.max(con.offsetWidth, con.offsetHeight, 60);
}
