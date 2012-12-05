var alldata;
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// var formatPercent = d3.format(".0%");

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .2);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    // .tickFormat(formatPercent);

var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")

var path = d3.geo.path();

var m = [40, 40, 40, 40],
    w = 960 - m[1] - m[3],
    h = 240 - m[0] - m[2],
    parse = d3.time.format("%Y-%m-%d").parse;
var tx = d3.time.scale().range([0, w])
    ty = d3.scale.linear().range([h, 0]),
    txAxis = d3.svg.axis().scale(tx).tickSize(-h).tickSubdivide(true).tickFormat(d3.time.format("%m/%e")),
    tyAxis = d3.svg.axis().scale(ty).ticks(6).orient("right");

var tarea = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return tx(d.date); })
    .y0(h)
    .y1(function(d) { return ty(d.count); });

var tline = d3.svg.line()
    .interpolate("monotone")
    .x(function(d) { return tx(d.date); })
    .y(function(d) { return ty(d.count); });

var tsvg = d3.select("#time-series")
            .append("svg:svg")
            .attr("width", w + m[1] + m[3])
            .attr("height", h + m[0] + m[2])
            .append("svg:g")
            .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

var tareapath = tsvg.append("svg:path")
        .attr("class", "area")

var txaxispath = tsvg.append("svg:g")
            .attr("class", "tx axis")


var tyaxispath = tsvg.append("svg:g")
            .attr("class", "ty axis")

var tlinepath = tsvg.append("svg:path")
            .attr("class", "line")
            .attr("clip-path", "url(#clip)")


var ttextanchor = tsvg.append("svg:text")
                .attr("x", w - 6)
                .attr("y", h - 6)
                .attr("text-anchor", "end")

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
    var promoterlocation = $('#search').val().split(',');
    d3.json("getcity?city=" + promoterlocation[0] + "&state=" + promoterlocation[1].replace(/\s+/g, ''), function(json) {
        console.log(json)

        var data =[];
            for (var i = 0; i < json.length ; i++) {
                console.log(json[i])
                var banddetails ={};
                banddetails["bandname"] = json[i].band
                banddetails["count"] = json[i].count
                banddetails['pct'] = json[i].pct
                banddetails["times"] = json[i].times
                data.push(banddetails);
            }

        console.log(data)
        x.domain(data.map(function(d) { return d.bandname; }));
        y.domain([0, d3.max(data, function(d) { return d.count; })]);

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
                .attr("y", function(d) { return y(d.count); })
                .attr("height", function(d) { return height - y(d.count); })
                .on('mouseover',function(d) {gettime(d, this)})
                .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
                .on('mouseout',  function(d) {
                        d3.select(this).attr('class', 'bar')
                        return tooltip.style("visibility", "hidden");
                    })

    });
});
function gettime(d, self) {
    times = d.times
    d3.select(self).attr('class', 'bar highlight')
    times.forEach(function(d) {
            d.date = parse(d[0])
            d.count = d[2]
            d.pct = d[1]
        })

    tx.domain([times[0].date, times[times.length - 1].date]);
    ty.domain([0, d3.max(times, function(d) { return d.count; })]).nice();
    
    

    tsvg.append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", w)
        .attr("height", h);


    

    tareapath.attr("d", tarea(times));

    txaxispath.attr("transform", "translate(0," + h + ")")
        .call(txAxis);

  // Add the y-axis.
    tyaxispath.attr("transform", "translate(" + w + ",0)")
        .call(tyAxis);

  // Add the line path.
        
    tlinepath.attr("d", tline(times));

  // Add a small label for the symbol name.
    ttextanchor.text("Talks");
        

    tsvg.selectAll(".dot").remove('circle')
    tsvg.selectAll(".dot")
        .data(times)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 3.5)
        .attr("cx", function(d) { console.log(d); return tx(d.date); })
        .attr("cy", function(d) { return ty(d.count); })
        .on("mouseover", function(d){showtime(d, this)})
        .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})   
        .on("mouseout", function(d){
                    tooltip.style("visibility", "hidden")
                    d3.select(this).attr('r', 4)
                })
    return tooltip.style("visibility", "visible")
        .style("color","#990000")
        .style("background","#CCFFCC")
        .style("border-radius","3px")
        .text("Tweet Percentage: " + Number(d.pct.toFixed(2)) + "%")
        
}

function showtime(d, self) {
    d3.select(self).attr('r', 8)
    cd = d[0]
    tooltext = "Tweet Percentage: " + Number(d[2].toFixed(2)) + "%"
    return tooltip.style("visibility", "visible")
        .style("color","#990000")
        .style("background","#CCFFCC")
        .style("border-radius","3px")
        .text(tooltext);
}