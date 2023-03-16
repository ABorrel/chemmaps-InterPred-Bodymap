function defineColumnDef(din) {
    
    var columnDefs = [];
    for (var assay in din){
        for(var prop in din[assay]){
            if(prop == "assay"){
                columnDefs.push({
                    headerName: prop.charAt(0).toUpperCase() + prop.slice(1).replace("_", " "),
                    field: prop,
                    sortable: true,
                    filter: true,
                    width: 450,
                    resizable: true,
                    lockVisible: true,
                    cellRenderer: function(params) {
                        let keyData = params.data.assay;
                        let newLink = `<a href= /chemmaps/tox21/${keyData} target="_blank">${keyData}</a>`;
                        return newLink;
                    },
                });
            }else if (prop == "gene"){
                columnDefs.push({
                    headerName: prop.charAt(0).toUpperCase() + prop.slice(1).replace("_", " "),
                    field: prop,
                    sortable: true,
                    filter: true,
                    width: 350,
                    resizable: true,
                    lockVisible: true,
                    cellRenderer: function(params) {
                        let keyData = params.data.gene;
                        if (keyData != null){
                            let newLink = `<a href= /chemmaps/tox21/target=${keyData} target="_blank">${keyData}</a>`;
                            return newLink;
                        };
                    },
                });
            }else if (prop == "invitro_assay_format"){
                columnDefs.push({
                    headerName: "Cell line",
                    field: prop,
                    sortable: true,
                    filter: true,
                    width: 250,
                    resizable: true,
                    lockVisible: true,
                });            
            }else if (prop == "mechanistic_target"){
                columnDefs.push({
                    headerName: prop.charAt(0).toUpperCase() + prop.slice(1).replace("_", " "),
                    field: prop,
                    sortable: true,
                    filter: true,
                    width: 250,
                    resizable: true,
                    lockVisible: true,
                });             
            
            }else{
                columnDefs.push({
                    headerName: prop.charAt(0).toUpperCase() + prop.slice(1).replace("_", " "),
                    field: prop,
                    sortable: true,
                    filter: true,
                    resizable: true,
                    lockVisible: true,
                });
            }
            
        };
        break;
    };
    return columnDefs;
}

function numberParser(params) {
    var newValue = params.newValue;
    var valueAsNumber;
    if (newValue === null || newValue === undefined || newValue === '') {
        valueAsNumber = null;
    } else {
        valueAsNumber = parseFloat(params.newValue);
    }
    return valueAsNumber;
}

function defineGridOption(din) {
    var gridOptions = {
        columnDefs: defineColumnDef(din),
        //rowSelection: 'multiple',
        rowData: defineRawData(din),

        //showToolPanel: true,
        //toolPanelSuppressRowGroups: true,
        //toolPanelSuppressValues: true,
        //toolPanelSuppressPivots: true,
        //toolPanelSuppressPivotMode: true
        //enableRangeSelection: true
    };
    return gridOptions;
}

function defineRawData(din) {
    var rowData = [];
    for (var assay in din) {
  
        rowData.push(din[assay]);
    };
    return rowData;
}
