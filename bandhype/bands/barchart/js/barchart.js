var alldata;
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// var formatPercent = d3.format(".0%");

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    // .tickFormat(formatPercent);


$('#promoter').on('click', function(e){

  // alert($('#search').val());
  $('#chart').empty();

  var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


  var json;
  error = true;
  var promoterlocation = $('#search').val();

     d3.json("bar.json", function(locationjson) {
     alldata = locationjson;


     for (loc in locationjson){
      if (loc === promoterlocation){
        json = locationjson[loc];
        error = false;
      }
     } 

     if (error==true){
      alert("Invalid Location");
      return;
     }


     var data =[];
        for (band in json){
           var banddetails ={};
          banddetails["bandname"] = band
          banddetails["tweets"] = json[band]
          data.push(banddetails);
        }

      x.domain(data.map(function(d) { return d.bandname; }));
      y.domain([0, d3.max(data, function(d) { return d.tweets; })]);

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
          .text("tweets");

      svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return x(d.bandname); })
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.tweets); })
          .attr("height", function(d) { return height - y(d.tweets); });

    });
});