var compareBands;
$('#generateChart').on('click', function (e) {

    reset_chart();
    alert($('#search').val());


    d3.json("chart.json", function (error, json) {

        var margin = {
            top: 40,
            right: 40,
            bottom: 20,
            left: 40
        },
        width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;

        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .6);

        var y = d3.scale.linear()
            .range([height, 0]);

        var ys = d3.scale.linear()
            .range([height, 0]);

        var yg = d3.scale.linear()
            .range([height, 0]);

        var color = d3.scale.ordinal()
            .range(["#6b486b", "#d0743c" ]);

         var legendcolor = d3.scale.ordinal()
            .range(["#d0743c", "#6b486b"]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .tickSize(1)
            .tickPadding(2)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".2s"));;

        var yAxiss = d3.svg.axis()
            .scale(ys)
            .orient("left")
            .tickFormat(d3.format(".2s"));

        var yAxisg = d3.svg.axis()
            .scale(yg)
            .orient("left")
            .tickFormat(d3.format(".2s"));

        var svg = d3.select("#chart").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var arr1 = [];
        var arr2 = [];
        var bandTypes = ["Listening","Talking"]
        compareBands = json; //for future use
        for (band in json) {
            d1 = {};
            d2 = {};
            d1.x = band
            d1.y = json[band][0]; //Listening
            d1.y0 = 0;
            d2.x = band
            d2.y = json[band][1];
            d2.y0 = json[band][0];
            arr1.push(d1);
            arr2.push(d2);
          };


            var layers = [arr1, arr2];

            var n = 2 // no. of bands compared
            var  yGroupMax = d3.max(layers, function (layer) {
                    return d3.max(layer, function (d) {
                        return d.y;
                    });
                }),
                yStackMax = d3.max(layers, function (layer) {
                    return d3.max(layer, function (d) {
                        return d.y0 + d.y;
                    });
                });


            x.domain(Object.keys(compareBands));
            y.domain([0, yStackMax]);
            ys.domain([0, yStackMax]);
            yg.domain([0, yGroupMax]);


            var tooltip = d3.select("#chart")
                .append("div")
            // .attr("class", "tooltip");
            .style("position", "absolute")
                .style("z-index", "10")
                .style("visibility", "hidden")

            var layer = svg.selectAll(".layer")
                .data(layers)
                .enter().append("g")
                .attr("class", "layer")
                .style("fill", function (d, i) {
                return color(i);
            });

            var rect = layer.selectAll("rect")
                .data(function (d) {
                return d;
            })
                .enter().append("rect")
                .attr("x", function (d) {
                return x(d.x);
            })
                .attr("y", height)
                .attr("width", 20)
                .attr("height", 0)
                .on("mouseover", function (d) {
                onhover(d)
            })
                .on("mousemove", function () {
                return tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px");
            })
                .on("mouseout", function () {
                return tooltip.style("visibility", "hidden");
            });

            rect.transition()
                .delay(function (d, i) {
                return i * 10;
            })
                .attr("y", function (d) {
                return y(d.y0 + d.y);
            })
                .attr("height", function (d) {
                return y(d.y0) - y(d.y0 + d.y);
            });


            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 6)
                .attr("dy", ".71em")
                .style("text-anchor", "end")
                .text("Tweets");

            var legend = svg.selectAll(".legend")
                .data(bandTypes)
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function (d, i) {
                return "translate(0," + i * 20 + ")";
            });

            legend.append("rect")
                .attr("x", width - 18)
                .attr("width", 18)
                .attr("height", 18)
                .style("fill", legendcolor);

            legend.append("text")
                .attr("x", width - 24)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "end")
                .text(function (d) {
                return d;
            });


            function onhover(d) {

                var tooltext = "Band Name=" + d.x + "; Talking=" +  compareBands[d.x][0] +";Listening="+compareBands[d.x][1] ;
                
                tooltip.style("visibility", "visible")
                    .style("color", "#990000")
                    .style("background", "#CCFFCC")
                    .style("border-radius", "3px")
                    .text(tooltext);
                generateTime1(d.x);
                generateTime2(d.x);
            };


            d3.selectAll("input").on("change", function change() {
                if (this.value === "grouped") transitionGrouped();
                else transitionStacked();
            });

            function transitionGrouped() {
                y.domain([0, yGroupMax]);

                rect.transition()
                    .duration(500)
                    .delay(function (d, i) {
                    return i * 10;
                })
                    .attr("x", function (d, i, j) {
                    return x(d.x) + x.rangeBand() / n * j;
                })
                    .attr("width", 20)
                    .transition()
                    .attr("y", function (d) {
                    return y(d.y);
                })
                    .attr("height", function (d) {
                    return height - y(d.y);
                });

                var trans = svg.transition().duration(500),
                    delay = function (d, i) {
                        return i * 50;
                    };

                trans.select(".y.axis")
                    .call(yAxisg)
                    .selectAll("g")
                    .delay(delay);
            }

            function transitionStacked() {
                y.domain([0, yStackMax]);

                rect.transition()
                    .duration(500)
                    .delay(function (d, i) {
                    return i * 10;
                })
                    .attr("y", function (d) {
                    return y(d.y0 + d.y);
                })
                    .attr("height", function (d) {
                    return y(d.y0) - y(d.y0 + d.y);
                })
                    .transition()
                    .attr("x", function (d) {
                    return x(d.x);
                })
                    .attr("width", 20);

                var trans = svg.transition().duration(500),
                    delay = function (d, i) {
                        return i * 50;
                    };

                trans.select(".y.axis")
                    .call(yAxiss)
                    .selectAll("g")
                    .delay(delay);

            }
        });
  });

function reset_chart(){
  $('#chart').empty();
  $('#timeseries1').empty();
    $('#timeseries2').empty();

};

function reset_time(){
  $('#timeseries1').empty();
   $('#timeseries2').empty();
};
//Time Line for Band1
function generateTime1(bandname1){
    reset_time();

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 940 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;


    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], 1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")


    var svg = d3.select("#timeseries1").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json("timedata1.json", function(error,timejson1){

        error = true;
         alldata = timejson1;
         var banddata;

          for (band in timejson1){
          if (band === bandname1){
            banddata = timejson1[band];
            error = false;
          }
         } 

         if (error==true){
          // alert("No data for "+bandname1);
          return;
         }

        var data=[];   
        for (day in banddata) {
                var daydetails ={};
                daydetails["dayname"] = day
                daydetails["tweets"] = banddata[day];
                data.push(daydetails);
              };

    var tooltip = d3.select("#timeseries1")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden")

      x.domain(data.map(function(d) { 
          return d.dayname; 
      }));
     y.domain([0, d3.max(data, function(d) { return d.tweets;
       })]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".21em")
          .style("text-anchor", "end")
          .text("Total Tweets");

      svg.selectAll(".bar")
          .data(data)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("fill","#006D2C")
          .attr("x", function(d) { return x(d.dayname); })
          .attr("width", 10)
          .attr("y", function(d) { return y(d.tweets); })
          .on("mouseover", function(d){gettime(d)})
          .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
          .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
          .attr("height", function(d) { return height - y(d.tweets); });

      function gettime(d){
          var tooltext = "Date:"+d.dayname+"; Tweets:"+d.tweets;
          tooltip.style("visibility", "visible")
                  .style("color","#990000")
                  // .style("background","#990000")
                  .style("border-radius","3px")
                  .text(tooltext);


        };

    });
};

// time line for  band2
function generateTime2(bandname2){

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 940 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;


    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], 1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")


    var svg = d3.select("#timeseries2").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json("timedata2.json", function(error,timejson2){

        error = true;
         alldata = timejson2;
         var banddata;

          for (band in timejson2){
          if (band === bandname2){
            banddata = timejson2[band];
            error = false;
          }
         } 

         if (error==true){
          // alert("No data for "+bandname2);
          return;
         }

        var data=[];   
        for (day in banddata) {
                var daydetails ={};
                daydetails["dayname"] = day
                daydetails["tweets"] = banddata[day];
                data.push(daydetails);
              };

    var tooltip = d3.select("#timeseries1")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden")

      x.domain(data.map(function(d) { 
          return d.dayname; 
      }));
     y.domain([0, d3.max(data, function(d) { return d.tweets;
       })]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".21em")
          .style("text-anchor", "end")
          .text("Total Tweets");

      svg.selectAll(".bar")
          .data(data)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("fill","#006D2C")
          .attr("x", function(d) { return x(d.dayname); })
          .attr("width", 10)
          .attr("y", function(d) { return y(d.tweets); })
          .on("mouseover", function(d){gettime(d)})
          .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
          .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
          .attr("height", function(d) { return height - y(d.tweets); });

      function gettime(d){
          var tooltext = "Date:"+d.dayname+"; Tweets:"+d.tweets;
          tooltip.style("visibility", "visible")
                  .style("color","#990000")
                  // .style("background","#990000")
                  .style("border-radius","3px")
                  .text(tooltext);


        };

    });
};