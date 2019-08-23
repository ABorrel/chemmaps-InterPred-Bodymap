function defineColumnDef(din) {
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

function defineGridAssays(din) {

    var gridOptions = {
        columnDefs: defineColumnDef(din),
        //rowSelection: 'multiple',
        rowData: defineRowData(din)

                //showToolPanel: true,
                //toolPanelSuppressRowGroups: true,
                //toolPanelSuppressValues: true,
                //toolPanelSuppressPivots: true,
                //toolPanelSuppressPivotMode: true
                //enableRangeSelection: true
    };
    return gridOptions;
}

function defineRowData(din) {
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
