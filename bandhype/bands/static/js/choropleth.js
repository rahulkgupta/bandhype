var data; // loaded asynchronously

var path = d3.geo.path();

var m = [40, 40, 40, 40],
    w = 960 - m[1] - m[3],
    h = 240 - m[0] - m[2],
    parse = d3.time.format("%Y-%m-%d").parse;

var x = d3.time.scale().range([0, w]),
    y = d3.scale.linear().range([h, 0]),
    xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true).tickFormat(d3.time.format("%m/%e")),
    yAxis = d3.svg.axis().scale(y).ticks(4).orient("right");

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
            .attr("transform", "translate(" + 20 + "," + m[0] + ")");

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


var svg = d3.select("#chart")
    .append("svg")
    .call(d3.behavior.zoom()
        .on("zoom", redraw))
    .append("svg:g");



var counties = svg.append("g")
    .attr("id", "counties")
    .attr("class", "Purples");

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

var currday = 0
var cd = "2012-11-14"
$('#search-btn').on('click', function(e){
    band = $("#search").val()
    d3.json("countrypop?query=" + band, function(json) {
        currday = 0
        cd = "2012-11-14"
        data = json
        console.log(json)
        counties.selectAll("path")
        .attr("class", quantize)
    });

    d3.json("timeband?query=" + band, function (json) {
        json.forEach(function(d) {
            d.date = parse(d[0])
            d.count = d[1]
            d.pct = d[2]

        })
        console.log(json[1])
        x.domain([json[0].date, json[json.length - 1].date]);
        y.domain([0, d3.max(json, function(d) { return d.count; })]).nice();
        

        tsvg.append("svg:clipPath")
            .attr("id", "clip")
            .append("svg:rect")
            .attr("width", w)
            .attr("height", h);

        areapath.attr("d", area(json));

        xaxispath.attr("transform", "translate(0," + h + ")")
            .call(xAxis);

  // Add the y-axis.
       yaxispath.attr("transform", "translate(" + w + ",0)")
            .call(yAxis);

  // Add the line path.
        
        linepath.attr("d", line(json));

  // Add a small label for the symbol name.
        textanchor.text("Talks");
        
        console.log(json)

        tsvg.selectAll(".dot").remove('circle')
        tsvg.selectAll(".dot")
            .data(json)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 4)
            .attr("cx", function(d) { console.log(d); return x(d.date); })
            .attr("cy", function(d) { return y(d.count); })
            .on("mouseover", function(d){changetime(d, this)})
            .on("mouseout", function(d){d3.select(this).attr('r', 4)})
                // .style("fill", function(d) { return color(d.species); });
    })
})

function redraw() {
    svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}

$('#change-btn').on('click', function(e){
    currday = 1
    cd = "2012-11-15"
    counties.selectAll("path")
    .attr("class", quantize);
});


function quantize(d) {
    var days = data[d.id]
    if (days) {
        for (var i = 0; i < days.length; i++) {
            if (days[i][0] == cd) {
                return "q" + Math.min(9, ~~(days[i][1]*10)) + "-9"; 
            }   
        }
    }
    return 'q0-9'
}

// Function when user clicks county in the map
function mapover(d){
    var days = data[d.id]
    var tooltext = ""
    if (days) {
        for (var i = 0; i < days.length; i++) {
            if (days[i][0] == cd) {
                tooltext = "County: "+d.properties.name+", Tweet Count: "+ days[i][2]
            }   
        }
    } else {
        tooltext = "County: "+d.properties.name+", Pct. of Tweets: 0%"
    }
    
    return tooltip.style("visibility", "visible")
        .style("color","#990000")
        .style("background","#CCFFCC")
        .style("border-radius","3px")
        .text(tooltext);
};

function changetime(d, self) {
    d3.select(self).attr('r', 8)
    cd = d[0]
    counties.selectAll("path")
    .attr("class", quantize);
}
