function defineColumnDef(din) {
    var columnDefs = [
        {
            headerName: 'Chemicals',
            children: [
                {
                    headerName: 'ID',
                    field: 'id',
                    sortable: true,
                    filter: true,
                    resizable: true,
                    width: 55,
                    lockVisible: true,
                },
                {
                    headerName: 'SMILES',
                    field: 'smiles',
                    sortable: false,
                    filter: true,
                    resizable: true,
                },
            ],
        },
    ];
    for (var chem in din) {
        for (var model in din[chem]) {
            if (model != 'SMILES' && model != 'inTox21') {
                columnDefs.push({
                    headerName: model,
                    children: [
                        {
                            headerName: 'M-' + model,
                            field: 'M-' + model,
                            width: 110,
                            sortable: true,
                            filter: true,
                            resizable: true,
                            valueParser: numberParser,
                            cellClassRules: {
                                'rag-green': 'x < 0.25',
                                'rag-yellow': 'x >= 0.25 && x < 0.50',
                                'rag-orange': 'x >= 0.50 && x < 0.75',
                                'rag-red': 'x >= 0.75',
                            },
                        },
                        {
                            headerName: 'SD-' + model,
                            field: 'SD-' + model,
                            width: 70,
                            sortable: true,
                            filter: true,
                            resizable: true,
                            valueParser: numberParser,
                            //cellClassRules: {
                            //    'rag-green': 'x < 0.05',
                            //    'rag-yellow': 'x >= 0.05 && x < 0.1',
                            //    'rag-orange': 'x >= 0.1 && x < 0.15',
                            //    'rag-red': 'x >= 0.2'}
                        },
                    ],
                });
            }
        }
        break;
    }

    columnDefs.push({
        headerName: 'Tox21 library',
        children: [
            {
                headerName: 'Included',
                field: 'Included',
                width: 110,
                sortable: true,
                filter: true,
                resizable: true,
                valueParser: numberParser,
            },
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
    for (var chem in din) {
        var add = { id: chem };
        add['smiles'] = din[chem]['SMILES'];
        for (var model in din[chem]) {
            if (model != 'SMILES' && model != 'inTox21') {
                //console.log(model);
                //console.log(din[chem][model]['M']);
                //console.log(model);
                add['M-' + model] = din[chem][model]['M'];
                add['SD-' + model] = din[chem][model]['SD'];
            }
        }
        add['Included'] = din[chem]['inTox21'];
        rowData.push(add);
    }
    return rowData;
}
