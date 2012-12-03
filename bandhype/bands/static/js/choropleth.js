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
var currday = "2012-11-14"
$('#search-btn').on('click', function(e){
    band = $("#search").val()
    d3.json("countrypop?query=" + band, function(json) {
        data = json
        console.log(json)
        counties.selectAll("path")
        .attr("class", quantize)
    });
})

function redraw() {
    svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}

$('#change-btn').on('click', function(e){
    currday = "2012-11-15"
    counties.selectAll("path")
    .attr("class", quantize);
});


function quantize(d) {
    var days = data[d.id]
    if (days)
        if (days[currday]) {
            console.log(days[currday]);
            return "q" + Math.min(9, ~~(days[currday][0] * 8)) + "-9";    
        }
            
    return 'q0-9'
}

// Function when user clicks county in the map
function mapover(d){
    var days = data[d.id]
    var tooltext = ""
    if (days) {
        if (days[currday]) {
            console.log(days[currday]);
            tooltext = "County: "+d.properties.name+", Pct. of Tweets: "+ days[currday][0] *100 + "%"
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
