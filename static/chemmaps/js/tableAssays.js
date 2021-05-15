function defineColumnDef(din) {
    
    var columnDefs = [];
    for (var assay in din){
        for(var prop in din[assay]){
            if(prop == "protocol_name"){
                columnDefs.push({
                    headerName: prop.charAt(0).toUpperCase() + prop.slice(1).replace("_", " "),
                    field: prop,
                    sortable: true,
                    filter: true,
                    width: 500,
                    resizable: true,
                    lockVisible: true,
                    cellRenderer: function(params) {
                        let keyData = params.data.protocol_name;
                        let newLink = `<a href= /chemmaps/tox21/${keyData} target="_blank">${keyData}</a>`;
                        return newLink;
                    },
                });
            }else if (prop == "assay_target"){
                columnDefs.push({
                    headerName: prop.charAt(0).toUpperCase() + prop.slice(1).replace("_", " "),
                    field: prop,
                    sortable: true,
                    filter: true,
                    width: 500,
                    resizable: true,
                    lockVisible: true,
                    cellRenderer: function(params) {
                        let keyData = params.data.assay_target;
                        if (keyData != null){
                            let newLink = `<a href= /chemmaps/tox21/target=${keyData} target="_blank">${keyData}</a>`;
                            return newLink;
                        };
                    },
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
