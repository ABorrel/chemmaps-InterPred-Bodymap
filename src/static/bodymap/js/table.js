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

////////////////////////////////////////////////////////
////////////////////////////////////////////////////////

function defineColumnAssays(din) {
    var columnDefs = [
        {
            headerName: 'Assays',
            children: [
                {
                    headerName: 'Name',
                    field: 'name',
                    sortable: true,
                    filter: true,
                    resizable: true,
                    width: 300,
                    lockVisible: true
                },
                {
                    headerName: 'Organ',
                    field: 'organ',
                    sortable: false,
                    filter: true,
                    resizable: true,
                    width: 150
                },
                {
                    headerName: 'Suborgan',
                    field: 'subbody',
                    sortable: false,
                    filter: true,
                    resizable: true,
                    width: 300
                }
            ]
        }
    ];

    columnDefs.push({
        headerName: "Expression",
        children: [
            {
                headerName: "Gene",
                field: "gene",
                width: 110,
                sortable: true,
                filter: true,
                resizable: true,
            },
            {
                headerName: 'Expression relative',
                field: "exp",
                width: 150,
                sortable: true,
                filter: true,
                resizable: true,
                valueParser: numberParser,
                cellClassRules: {
                    'rag-green': 'x < 5',
                    'rag-yellow': 'x >= 5 && x < 10',
                    'rag-orange': 'x >= 10 && x < 20',
                    'rag-red': 'x >= 20'}
            }
        ]
    });
    return columnDefs;
}




function defineGridAssays(din) {

    var gridOptions = {
        columnDefs: defineColumnAssays(din),
        //rowSelection: 'multiple',
        rowData: defineRowAssays(din)

                //showToolPanel: true,
                //toolPanelSuppressRowGroups: true,
                //toolPanelSuppressValues: true,
                //toolPanelSuppressPivots: true,
                //toolPanelSuppressPivotMode: true
                //enableRangeSelection: true
    };
    return gridOptions;
}

function defineRowAssays(din) {
    var rowData = [];
    for (var organ in din) {
        for (var suborgan in din[organ]) {
            for (var assay in din[organ][suborgan]) {
                var add = {name: assay};
                add['organ'] = organ;
                add['subbody'] = suborgan;
                add['gene'] = din[organ][suborgan][assay]["gene"];
                add['exp'] = din[organ][suborgan][assay]["exp"];
                rowData.push(add);
            }
            ;
        }
        ;
    }
    ;
    return rowData;
}


////////////////////////////////////////
////////////////////////////////////////


function defineColumnChem(din) {
    var columnDefs = [
        {
            headerName: 'Assays',
            children: [
                {
                    headerName: 'Name',
                    field: 'name',
                    sortable: true,
                    filter: true,
                    resizable: true,
                    width: 300,
                    lockVisible: true
                },
                {
                    headerName: 'System',
                    field: 'organ',
                    sortable: true,
                    filter: true,
                    resizable: true,
                    width: 150
                },
                {
                    headerName: 'Organ',
                    field: 'subbody',
                    sortable: true,
                    filter: true,
                    resizable: true,
                    width: 300
                },
                {
                    headerName: 'Gene',
                    field: 'gene',
                    sortable: false,
                    filter: true,
                    resizable: true,
                    width: 300
                },
                {
                    headerName: 'Tissue expression threshold',
                    field: "exp",
                    width: 150,
                    sortable: true,
                    filter: true,
                    resizable: true,
                    valueParser: numberParser,
                    cellClassRules: {
                        'rag-red': 'x < 5',
                        'rag-orange': 'x >= 5 && x < 10',
                        'rag-yellow': 'x >= 10 && x < 25',
                        'rag-green': 'x >= 25'}
                }
            ]
        }
    ];

    columnDefs.push({
        headerName: "Activity",
        children: [
            {
                headerName: 'AC50',
                field: "AC50",
                width: 150,
                sortable: true,
                filter: true,
                resizable: true,
                valueParser: numberParser,
                cellClassRules: {
                    'rag-red': 'x < 1',
                    'rag-orange': 'x >= 1 && x < 10',
                    'rag-yellow': 'x >= 10 && x < 100',
                    'rag-green': 'x >= 100'}
            }
        ]
    });
    return columnDefs;
}




function defineGridChem(din) {

    var gridOptions = {
        columnDefs: defineColumnChem(din),
        //rowSelection: 'multiple',
        rowData: defineRowChem(din)

                //showToolPanel: true,
                //toolPanelSuppressRowGroups: true,
                //toolPanelSuppressValues: true,
                //toolPanelSuppressPivots: true,
                //toolPanelSuppressPivotMode: true
                //enableRangeSelection: true
    };
    return gridOptions;
}

function defineRowChem(din) {
    var rowData = [];
    for (var assay in din) {
        for (var organ in din[assay]) {
            for (var suborgan in din[assay][organ]) {
                if(din[assay][organ][suborgan]["gene"][0] != "NA"){
                    if(din[assay][organ][suborgan]["exp"][0] < 2.0){
                        continue;
                    }
                    ;
                    var add = {name: assay};
                    add['organ'] = organ;
                    add['subbody'] = suborgan;
                    add['gene'] = din[assay][organ][suborgan]["gene"][0];
                    add['exp'] = din[assay][organ][suborgan]["exp"][0];
                    add['AC50'] = din[assay][organ][suborgan]["AC50"];
                    rowData.push(add);
                }else{
                    var add = {name: assay};
                    add['organ'] = organ;
                    add['subbody'] = suborgan;
                    add['AC50'] = din[assay][organ][suborgan]["AC50"];
                    rowData.push(add);
                }
                ;
            }
            ;
        }
        ;
    }
    ;
    return rowData;
}




