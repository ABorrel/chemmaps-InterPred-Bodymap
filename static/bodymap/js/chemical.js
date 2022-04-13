


function chemPanel(dchem) {
    var sizeCanvas = resizeCanvas();
    var options = { width: sizeCanvas, height: sizeCanvas, compactDrawing: false, terminalCarbons: true};
    var smilesDrawer = new SmilesDrawer.Drawer(options);

    QC.innerHTML = dchem.QC;
    document.getElementById('QC').href =
    'https://ice.ntp.niehs.nih.gov/DATASETDESCRIPTION';
    CASIDError.innerHTML = dchem.CAS;
    CASID.innerHTML = dchem.CAS;
    CASIDtop.innerHTML = dchem.CAS;
    ChemicalNametop.innerHTML = dchem.Name;
    document.getElementById('CASID').href =
            'https://comptox.epa.gov/dashboard/dsstoxdb/results?utf8=%E2%9C%93&search=' + dchem.CAS;
    
    document.getElementById('CASIDtop').href =
            'https://comptox.epa.gov/dashboard/dsstoxdb/results?utf8=%E2%9C%93&search=' + dchem.CAS

    DSSTOX.innerHTML = dchem.DSSTOX;
    document.getElementById('DSSTOX').href =
            'https://comptox.epa.gov/dashboard/chemical/details/' + dchem.DSSTOX;
    
    ChemicalName.innerHTML = dchem.Name;
    SMILES.innerHTML = dchem.SMILES;

    SmilesDrawer.parse(dchem.SMILES, function(tree) {
        // Draw to the canvas
        smilesDrawer.draw(tree, 'Compoundpng2', 'light', false);
    });

}



function resizeCanvas() {
    var con = document.getElementById('pngcompound');
    return Math.max(con.offsetWidth, con.offsetHeight);
}