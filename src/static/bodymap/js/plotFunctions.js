

function dotPlot(dmap){

    var lsystem = [];
    var llval = [];
    var llassays = [];

    for(var assay in dmap){
        for(var system in dmap[assay]){
            if(lsystem.includes(system) ==false){
                lsystem.push(system);
            }
        }
    }

    for (var i=0; i<lsystem.length; i++){
        var lval = [];
        var lass = []
        for (var assay in dmap){
            if (Object.keys(dmap[assay]).includes(lsystem[i]) == true){
                for(var organ in dmap[assay][lsystem[i]]){
                    var val = -Math.log10(dmap[assay][lsystem[i]][organ]["AC50"]);
                    lval.push(val);
                    lass.push(assay);
                }
            }
            llval.push(lval);
            llassays.push(lass);
            
        }
    }

    ltrace = []
    for (var i=0; i<llval.length; i++){
        var trace = {
            x: llval[i],
            y: lsystem,
            name: llassays[i],
            mode: 'markers',
            text: llassays[i],
            hoverinfo: 'text',
            marker: {
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
        title: dchem.CAS,
        
        
        xaxis: {
          showgrid: true,
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
          title: {
            text: "-log10(AC50)",
            standoff: 20
          },
          autotick: false,
          ticks: 'outside',
          tick0: 0,
          dtick: 0.25,
          ticklen: 8,
          tickwidth: 4,
          tickcolor: '#000'
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
          yanchor: 'top',
          xanchor: 'right'
        },
        showlegend: false,
        howerinfo:name,
        width: 600,
        height: 600,
        paper_bgcolor: 'rgb(255, 255, 255)',
        plot_bgcolor: 'rgb(255, 255, 255)',
        hovermode: 'closest',
        
      };


      Plotly.newPlot('dotplot', ltrace, layout, {showSendToCloud: true});

}
;