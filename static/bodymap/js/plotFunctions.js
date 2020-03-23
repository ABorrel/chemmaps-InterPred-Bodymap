

function dotPlot(dmap){

    //console.log(dmap);
    //console.log("In plot");

    var lsystem = [];
    var llval = [];
    //var llassays = [];

    for(var assay in dmap){
        for(var system in dmap[assay]){
            if(lsystem.includes(system) == false){
                lsystem.push(system);
            }
        }
    }
    ;
    var llassays = Object.keys(dmap); 

    for (var j=0; j<llassays.length; j++){
      var lval = [];
      for (var i=0; i<lsystem.length; i++){
        if(Object.keys(dmap[llassays[j]]).includes(lsystem[i]) == true){
          var lvaltemp = [];
          for(var organ in dmap[llassays[j]][lsystem[i]]){

            //console.log(llassays[j]);
            //console.log(lsystem[i]);
            //console.log(organ);
            //console.log(dmap[llassays[j]][lsystem[i]][organ]["AC50"])
            var val = Math.log10(dmap[llassays[j]][lsystem[i]][organ]["AC50"]);
            //console.log(val);
            // add random fact in ac50
            //var r = Math.random()*0.01;
            //console.log(r);
            if(val != NaN){
              lvaltemp.push(val);
            }
            
            //lass.push(assay);
          }
          //console.log(lvaltemp);
          //var valMin = Math.min(lvaltemp);
          lval.push(Math.min(...lvaltemp));
          //console.log(lval);
        }else{
          lval.push(NaN);
        }  
      }
      ;
      llval.push(lval)
    }
    ;  
      
    //console.log(llassays);
    //console.log(llval);
    //console.log(lsystem);
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
              size: 9
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
          
          autotick: false,
          ticks: 'outside',
          tick0: 0,
          dtick: 0.50,
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
            size: 7,
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
        
        annotations: [
          {
            x: 1,
            y: 0.0,
            xref: 'paper',
            yref: 'paper',
            text: 'log10(AC50)',
            showarrow: false,
          }
        ]

      };


      Plotly.newPlot('dotplot', ltrace, layout, {showSendToCloud: true});

}
;