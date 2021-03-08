function tester(event) {

    let entry = event.target.getAttribute("entry");
    let visualized = event.target.getAttribute("visualized");
    let visualizationDiv = document.getElementById(`${entry}-vis`);

    if (visualizationDiv.style.display === "none") {

        if (visualized === "false") {
            let nodes = JSON.parse(event.target.getAttribute("nodes"));
            let links = JSON.parse(event.target.getAttribute("links"));

            let graph = {
                nodes: nodes,
                links: links
            };

            network_graph_render(graph, entry);
            event.target.setAttribute("visualized", true);
        }

        visualizationDiv.style.display = "block";
    } else {
        visualizationDiv.style.display = "none";
    }
}

let network_graph_render = function(graph, entry) {

    let width = 900;
    let height = 640;

    const color = d3.scaleOrdinal(d3.schemeCategory20);

    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));

    let svg = d3.select(`#${entry}-vis-graph`)
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height);
                    // .call(d3.zoom().on("zoom", function () {
                    //    svg.attr("transform", d3.event.transform)
                    // }));

    let link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(graph.links)
                    .enter()
                    .append("line")
                    .attr("stroke-width", function(d) { return d.stroke_width; })
                    .style("stroke", function() {
                        return "#000000";
                    });

    let node = svg.append("g")
                  .attr("class", "nodes")
                  .selectAll("g")
                  .data(graph.nodes)
                  .enter().append("g");

    let circles = node.append("circle")
                      .attr("r", 25)
                      .attr("fill", function(d) { return color(d.group); })
                      .call(d3.drag()
                          .on("start", dragstarted)
                          .on("drag", dragged)
                          .on("end", dragended));

    let lables = node.append("text")
          .text(function(d) {
            return d.id;
          })
          .attr('x', 20)
          .attr('y', 2);

    let namespaces = node.append("text")
          .text(function(d) {
            return d.group;
          })
          .attr('x', 20)
          .attr('y', 15);

    node.append("title")
          .text(function(d) { return d.id; });

    simulation
          .nodes(graph.nodes)
          .on("tick", ticked);

    simulation.force("link")
          .links(graph.links);

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("transform", function(d) {
              return "translate(" + d.x + "," + d.y + ")";
            })
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
};