//bubble.js

// Variables
var width = 800;
var height = 800;

// Select bubble chart
var chart = d3.select("#bubbleChart")
  .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("id", "primarysvg");

// Color scheme for bubbles based on positive/negative W-L balance
var color = d3.scaleOrdinal()
              .domain(["pos", "nego", "negh", "neut"])
              .range(["MediumSeaGreen ", "Orange" , "Peru", "LightSlateGrey"]);

// d3 pack for bubbles
var pack = d3.pack()
    .size([width, height])
    .padding(1.0);

// Default to weekday
changeDay('Weekday');

// Button to change weekday/weekend
$("label.dayBtn").click(function() {
  changeDay(this.id);
  });

// MainFunction to change from weekday to weekend/holiday
function changeDay(daytype){
  var csv_weday = "static/weday_result.csv";
  var scv_wehol = "static/wehol_result.csv";
  if (daytype === 'Weekday'){
    var dataSource = csv_weday;
  } else {
    var dataSource = scv_wehol;
  }

  // Load correct csv
  d3.csv(dataSource, function(d) {
    d.value = +d.g0;
    if (d.value) return d;

  }, function(error, classes) {
    if (error) throw error;

    // Create d3 hierarchy to store data
    var root = d3.hierarchy({children: classes})
        .sum(function(d) { return d.value; })
        .each(function(d) {
          if (d.data.value > 0.02){
            d.id = d.data.name;
            d.package = d.data.atype;
          } else {
            d.id = '';
            d.package = d.data.atype;
          }
        });

    // Select node within primary svg for each bubble
    var svg = d3.select("#primarysvg");

    var node = svg.selectAll(".node")
      .data(pack(root).leaves())
      .enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    // Make circles for bubbles
    node.append("circle")
        .attr("id", function(d) { return d.id; })
        .attr("r", function(d) { return d.r; })
        .style("fill", function(d) { return color(d.package); });

    node.append("clipPath")
        .attr("id", function(d) { return "clip-" + d.id; })
        .append("use")
        .attr("xlink:href", function(d) { return "#" + d.id; });

    node.append("text")
        .attr("clip-path", function(d) { return "url(#clip-" + d.id + ")"; })
        .style("font-size", "16px")
        .style('fill', 'white')
        .selectAll("tspan")
        .data(function(d) { return d.id.split(/(?=[A-Z\(][^A-Z])/g); })
        .enter().append("tspan")
        .attr("x", 0)
        .attr("y", function(d, i, nodes) { return 20 + (i - nodes.length / 2 - 0.5) * 16; })
        .text(function(d) { return d; });
  });
};
