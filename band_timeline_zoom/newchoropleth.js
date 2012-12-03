var alldata;
    
//generates map for a particular date
function generateMap(date){

  var data; // loaded asynchronously
  var path = d3.geo.path();

  var svg = d3.select("#chart")
      .append("svg")
      .call(d3.behavior.zoom()
      .on("zoom", redraw))
      .append("svg:g");

    var counties = svg.append("g")
        .attr("id", "counties")
        .attr("class", "Greens");

    var states = svg.append("g")
        .attr("id", "states");

  var tooltip = d3.select("#chart")
    .append("div")
    // .attr("class", "tooltip");
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")

  d3.json("us-counties.json", function(json) {
    counties.selectAll("path")
        .data(json.features)
      .enter().append("path")
        .attr("class", data ? quantize : null)
        .on("mouseover", function(d){mapover(d)})
        .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
        .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
        .attr("d", path);
  });

  d3.json("us-states.json", function(json) {
    states.selectAll("path")
        .data(json.features)
      .enter().append("path")
        .attr("d", path);
  });

    data = alldata[date];
    counties.selectAll("path")
        .attr("class", quantize);


  function redraw() {
  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  }
  function quantize(d) {
    return "q" + Math.min(8, ~~(data[d.id] * 9 / 12)) + "-9";
  }

  // Function when user clicks county in the map
  function mapover(d){
    var tooltext = "County: "+d.properties.name+", No. of Tweets: "+ data[d.id]
    return tooltip.style("visibility", "visible")
                  .style("color","#990000")
                  .style("background","#CCFFCC")
                  .style("border-radius","3px")
                  .text(tooltext);
  };

};

function reset(){
  $('#chart').empty();
};

//generateChart calls server for a band name
$('#generateChart').on('click', function(e){
    reset();

    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 940 - margin.left - margin.right,
        height = 100 - margin.top - margin.bottom;


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

      $('#timeseries').empty();

    var svg = d3.select("#timeseries").append("svg:svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


      error = true;
      var bandname = $('#search').val();

     d3.json("unemployment.json", function(locationjson) {
        alert(bandname);

     alldata = locationjson;

     var data =[];
     var initialise ;
        for (day in alldata){
          var daydetails ={};
          daydetails["dayname"] = day

          //count the tweets for the day
          var tweet_num = 0;
          var datedata = alldata[day];
          for (fips in datedata){
            tweet_num += datedata[fips];
          }
          // alert(tweet_num)
          daydetails["tweets"] = tweet_num;
          data.push(daydetails);
          initialise = day;
        }

    generateMap(initialise);
    var tooltip = d3.select("#timeseries")
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
          .attr("width", 5)
          .attr("y", function(d) { return y(d.tweets); })
          .on("mouseover", function(d){gettime(d)})
          .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
          .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
          .attr("height", function(d) { return height - y(d.tweets); });

      function gettime(d){
          reset();
          var tooltext = d.dayname
          tooltip.style("visibility", "visible")
                  .style("color","#990000")
                  // .style("background","#990000")
                  .style("border-radius","3px")
                  .text(tooltext);

          generateMap(d.dayname);

        };

    });
});