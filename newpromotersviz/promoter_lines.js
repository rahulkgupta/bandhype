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
};

function reset_time(){
  $('#timeseries1').empty();
};

//Time Line for both the type of bands
function generateTime1(searchband){
    reset_time();
    // alert("calling timeseries function")

    
var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y%m%d").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.ordinal()
    .range(["#6b486b", "#d0743c" ])
    .domain(["Listening", "Talking" ]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.tweets); });

var svg = d3.select("#timeseries1").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var tooltip = d3.select("#timeseries1")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden")

d3.json("timeline.json", function(error,json) {
        error = true;
         var banddata;

          for (band in json){
          if (band === searchband){
            banddata = json[band];
            error = false;
          }
         } 

         if (error==true){
          // alert("No data for "+searchband);
          return;
         }

   var data =[];
      for (day in banddata){
        d={};
        d["date"] = day
        d["Listening"] = banddata[day][0].toString();
        d["Talking"] = banddata[day][1].toString();
        data.push(d);
      }

  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });

  var bands = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, tweets: +d[name]};
      })
    };
  });

 x.domain(data.map(function(d) { return d.date; }));
  y.domain([
    d3.min(bands, function(c) { return d3.min(c.values, function(v) { return v.tweets; }); }),
    d3.max(bands, function(c) { return d3.max(c.values, function(v) { return v.tweets; }); })
  ]);

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

  var band = svg.selectAll(".band")
      .data(bands)
    .enter().append("g")
      .attr("class", "band");

  band.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); })
       .on("mouseover", function(d){gettime(d)})
      .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
      .attr("height", function(d) { return height - y(d.tweets); });

  band.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.tweets) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });

  function gettime(d){

          var tooltext = d.name;
          tooltip.style("visibility", "visible")
                  .style("color","#990000")
                  // .style("background","#990000")
                  .style("border-radius","3px")
                  .text(tooltext);

        };
});

};
