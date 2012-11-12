var data; // loaded asynchronously

var path = d3.geo.path();

var svg = d3.select("#chart")
    .append("svg");

var counties = svg.append("g")
    .attr("id", "counties")
    .attr("class", "Greens");

var states = svg.append("g")
     .attr("id", "states");


var tooltip = d3.select("body")
  .append("div")
  .style("position", "absolute")
  .style("z-index", "10")
  .style("visibility", "hidden")


d3.json("counties", function(json) {
     counties.selectAll("path")
          .data(json.features)
          .enter().append("path")
          .attr("class", data ? quantize : null)
          .on("mouseover", function(d){mapover(d)})
          .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
          .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
          .attr("d", path);
});

d3.json("states", function(json) {

     states.selectAll("path")
          .data(json.features)
          .enter().append("path")
          .attr("d", path);
});

d3.json("countrypop?query=justin bieber", function(json) {
     data = json;
     counties.selectAll("path")
          .attr("class", quantize);
});

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
