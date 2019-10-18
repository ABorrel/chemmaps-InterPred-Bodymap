




function dotPlot(dmap){

    var lsystem = [];
    var llval = [];

    console.log("ddd");

    for(var assay in dmap){
        for(var system in dmap[assay]){
            if(lsystem.includes(system) ==false){
                lsystem.push(system);
            }
        }
    }

    console.log(lsystem);
    for (var i=0; i<lsystem.length; i++){
        var lval = [];
        for (var assay in dmap){
            
            if (Object.keys(dmap[assay]).includes(lsystem[i]) == true){
                for(var organ in dmap[assay][lsystem[i]]){
                    console.log(organ)
                    var val = dmap[assay][lsystem[i]][organ]["AC50"];
                    lval.push(dmap[assay][lsystem[i]][organ]["AC50"]);
                }
            }
            llval.push(lval);
        }
    }

    ltrace = []
    for (var i=0; i<llval.length; i++){
        var trace = {
            x: llval[i],
            y: lsystem,
            mode: 'markers',
            marker: {
              color: 'rgba(204, 204, 204, 0.95)',
              line: {
                color: 'rgba(217, 217, 217, 1.0)',
                width: 1,
              },
              symbol: 'circle',
              size: 16
            }
        };
        ltrace.push(trace);
    }

    var layout = {
        title: 'AAAA',
        xaxis: {
          showgrid: false,
          showline: true,
          linecolor: 'rgb(102, 102, 102)',
          titlefont: {
            font: {
              color: 'rgb(204, 204, 204)'
            }
          },
          tickfont: {
            font: {
              color: 'rgb(102, 102, 102)'
            }
          },
          autotick: false,
          dtick: 10,
          ticks: 'outside',
          tickcolor: 'rgb(102, 102, 102)'
        },
        margin: {
          l: 140,
          r: 40,
          b: 50,
          t: 80
        },
        legend: {
          font: {
            size: 10,
          },
          yanchor: 'middle',
          xanchor: 'right'
        },
        width: 600,
        height: 600,
        paper_bgcolor: 'rgb(254, 247, 234)',
        plot_bgcolor: 'rgb(254, 247, 234)',
        hovermode: 'closest'
      };


      Plotly.newPlot('dotplot', ltrace, layout, {showSendToCloud: true});

}
;