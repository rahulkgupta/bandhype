var data; // loaded asynchronously

var path = d3.geo.path();

var svg = d3.select("#chart")
  .append("svg");

var counties = svg.append("g")
    .attr("id", "counties")
    .attr("class", "Blues");

var states = svg.append("g")
    .attr("id", "states");

d3.json("counties", function(json) {
  counties.selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("class", data ? quantize : null)
      .attr("d", path);
});

d3.json("states", function(json) {

  states.selectAll("path")
      .data(json.features)
    .enter().append("path")
      .attr("d", path);
});

d3.json("unemployment", function(json) {
  console.log(json)
  data = json;
  counties.selectAll("path")
      .attr("class", quantize);
});

function quantize(d) {
  return "q" + Math.min(8, ~~(data[d.id] * 9 / 12)) + "-9";
}
