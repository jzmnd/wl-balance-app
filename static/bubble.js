//bubble.js

// Constants
var width = 700;
var height = 700;
var csv_weday = "static/data/weday_result.csv";
var csv_wehol = "static/data/wehol_result.csv";
var cutoff = 0.08;

// Defaults
var day = 'weday';
var cluster = 'cluster0';

// Color scheme for bubbles based on positive/negative W-L balance
var color = d3.scaleOrdinal()
  .domain(["pos", "nego", "negh", "neut"])
  .range(["MediumSeaGreen ", "Orange" , "Peru", "LightSlateGrey"]);

// Format for tooltip
var format = d3.format(".4f");

// Add svg for bubble chart and set id
d3.select("#bubbleChart")
  .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("id", "primarysvg");

// Button to change weekday/weekend
$("label.dayBtn")
  .click(function() {
    update(this.id, cluster);
    day = this.id;
  });

// Button to change cluster
$("label.clusterBtn")
  .click(function() {
    update(day, this.id);
    cluster = this.id;
  });

// Display initial chart
update(day, cluster);

// Update function
function update(daytyp, clutyp) {

  if (daytyp === 'weday') {
    var dataSource = csv_weday;
  } else {
    var dataSource = csv_wehol;
  }

  // Load correct csv
  d3.csv(dataSource, function(d) {
    d.value = +d['g' + clutyp.slice(7)];
    if (d.value) return d;
  },
  
  function(err, c) {
    if (err) throw err;

    // Create d3 hierarchy to store data
    var root = d3.hierarchy({children: c})
        .sum(function(d) { return d.value; })
        .sort()
        .each(function(d) {
          if (d.data.name) {
            d.id = d.data.name.replace(/[ \/]/g, "-").replace(/['\(\)]/g, "");
            d.dispname = d.data.name.trim();
            d.package = d.data.atype;
          }
        });

    // d3 Pack for bubbles
    var pack = d3.pack()
      .size([width, height])
      .padding(1.0);

    // Select primary svg
    var svg = d3.select("#primarysvg");

    // Select nodes, remove previous and add data
    var nodes = svg.selectAll(".node")
      .remove()
      .exit()
      .data(pack(root).leaves());

    // Node enter selection add group and transform positions
    var node = nodes.enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    // Make circles for bubbles with correct radius
    node.append("circle")
        .attr("id", function(d) { return d.id; })
        .attr("r", function(d) { return d.r; })
        .style("fill", function(d) { return color(d.package); });

    // Clip path to prevent text outside box
    node.append("clipPath")
        .attr("id", function(d) { return "clip-" + d.id; })
        .append("use")
          .attr("xlink:href", function(d) { return "#" + d.id; });

    // Add text from dispname if value is > cutoff
    node.append("text")
        .attr("clip-path", function(d) { return "url(#clip-" + d.id + ")"; })
        .selectAll("tspan")
        .data(function(d) {
          if (d.value > cutoff) {
            return d.dispname.split(/[ ](?=[A-Z\(][^A-Z])/g);
          } else {
            return "";
          }
        })
        .enter().append("tspan")
          .attr("x", 0)
          .attr("y", 5)
          .attr("dy", function(d, i, t) { return 14 * (i - (t.length - 1) / 2); })
          .text(function(d) { return d; });

    // Tooltips with title
    node.append("title")
      .text(function(d) { return d.dispname + "\n" + format(d.value); });

  });
};
