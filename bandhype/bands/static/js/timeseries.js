var m = [40, 40, 40, 40],
    w = 960 - m[1] - m[3],
    h = 240 - m[0] - m[2],
    parse = d3.time.format("%Y-%m-%d").parse;

var x = d3.time.scale().range([0, w]),
    y = d3.scale.linear().range([h, 0]),
    xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true).tickFormat(d3.time.format("%m/%e")),
    yAxis = d3.svg.axis().scale(y).ticks(4).orient("left");

var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y0(h)
    .y1(function(d) { return y(d.count); });

var line = d3.svg.line()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.count); });

var tsvg = d3.select("#time-series")
            .append("svg:svg")
            .attr("width", w + m[1] + m[3])
            .attr("height", h + m[0] + m[2])
            .append("svg:g")
            .attr("transform", "translate(" + (m[1] + 10) + "," + m[0] + ")");

var ttooltip = d3.select("body")
    .append("div")
    .attr("id", "ttooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")

var areapath = tsvg.append("svg:path")
        .attr("class", "area")

var xaxispath = tsvg.append("svg:g")
            .attr("class", "x axis")


var yaxispath = tsvg.append("svg:g")
            .attr("class", "y axis")

var linepath = tsvg.append("svg:path")
            .attr("class", "line")
            .attr("clip-path", "url(#clip)")


var textanchor = tsvg.append("svg:text")
                .attr("x", w - 6)
                .attr("y", h - 6)
                .attr("text-anchor", "end")


function changetime(d, self) {
    d3.select(self).attr('r', 8)
    if (!zoomed) {
        state_data = d.states
        states.selectAll("path")
            .attr("class", quantize);
    } else {        
        county_data = d.counties
        counties.selectAll("path")
            .attr("class", cquantize);
    }
    
    
    tooltext = "Tweet Percentage: " + Number((d[2]*100).toFixed(2)) + "%"
    return ttooltip.style("visibility", "visible")
        .text(tooltext);
}