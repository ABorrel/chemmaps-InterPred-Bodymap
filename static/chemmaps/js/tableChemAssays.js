function defineColumnDef() {
    
    var columnDefs = [];
    
    columnDefs.push({
        headerName: "DTXSID",
        field: "dtxid",
        sortable: true,
        filter: true,
        width: 170,
        resizable: true,
        lockVisible: true,
        cellClass: "grid-cell-left",
        cellRenderer: function(params) {
            let keyData = params.data.dtxid;
            let newLink = `<a href= https://comptox.epa.gov/dashboard/chemical/invitrodb/${keyData} target="_blank">${keyData}</a>`;
            return newLink;
        },
    });

    columnDefs.push({
        headerName: "CASRN",
        field: "casrn",
        sortable: true,
        filter: true,
        width: 150,
        resizable: true,
        lockVisible: true,
        cellClass: "grid-cell-left",
    });

    columnDefs.push({
        headerName: "Name",
        field: "name",
        sortable: true,
        filter: true,
        width: 250,
        resizable: true,
        lockVisible: true,
        cellClass: "grid-cell-left",
    });

    columnDefs.push({
        headerName: "Number of active assays",
        field: "nb_active",
        sortable: true,
        filter: true,
        width: 280,
        resizable: true,
        lockVisible: true,
        cellClass: "grid-cell-left",
    });

    columnDefs.push({
        headerName: "Lowest AC50 (µM)",
        field: "lowest_ac50",
        sortable: true,
        filter: true,
        width: 250,
        resizable: true,
        lockVisible: true,
        cellClass: "grid-cell-left",
    });

    columnDefs.push({
        headerName: "Assay with the lowest AC50",
        field: "lowest_active_assay",
        sortable: true,
        filter: true,
        width: 350,
        resizable: true,
        lockVisible: true,
        cellClass: "grid-cell-left",
        cellRenderer: function(params) {
            let keyData = params.data.lowest_active_assay;
            let newLink = `<a href= /chemmaps/tox21/${keyData} target="_blank">${keyData}</a>`;
            return newLink;
        },
    });
    return columnDefs;
}


function defineGridOption(d_chem, d_assays) {
    var gridOptions = {
        columnDefs: defineColumnDef(),
        //rowSelection: 'multiple',
        rowData: defineRawData(d_chem, d_assays),
        //rowData:[{"dtxid":"test", "casrn":"test", "name_chem":"test", "lowest_ac50":"test", "most_active_assay":"test"}],
        //showToolPanel: true,
        //toolPanelSuppressRowGroups: true,
        //toolPanelSuppressValues: true,
        //toolPanelSuppressPivots: true,
        //toolPanelSuppressPivotMode: true
        //enableRangeSelection: true
    };
    return gridOptions;
}

function defineRawData(d_chem, d_assays) {
    var rowData = [];
    for (var chem in d_chem) {
        if(chem in d_assays){
            rowData.push({"dtxid":chem, "casrn":d_chem[chem]["casn"], "name":d_chem[chem]["name"], "nb_active":d_assays[chem]["Active assays"] , "lowest_ac50":d_assays[chem]["lowest_ac50"], "lowest_active_assay":d_assays[chem]["Most active assay"]});
        }else{
            rowData.push({"dtxid":chem, "casrn":d_chem[chem]["casn"], "name":d_chem[chem]["name"], "nb_active":0 , "lowest_ac50":"NA", "lowest_active_assay":""});
        };
    };
    return rowData;
}
