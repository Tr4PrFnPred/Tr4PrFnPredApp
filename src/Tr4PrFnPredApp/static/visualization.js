function generate_network_graph(event) {

    let entry = event.target.getAttribute("entry");
    let visualized = event.target.getAttribute("visualized");
    let visualizationDiv = document.getElementById(`${entry}-vis`);

    if (visualizationDiv.style.display === "none") {

        if (visualized === "false") {
            let nodes = JSON.parse(event.target.getAttribute("nodes"));
            let links = JSON.parse(event.target.getAttribute("links"));
            let scatter = JSON.parse(event.target.getAttribute("scatter"));

            let graph = {
                nodes: nodes,
                links: links
            };

            network_graph_render(graph, entry);
            scatter_plot_render(scatter, entry);
            event.target.setAttribute("visualized", true);
        }

        visualizationDiv.style.display = "block";
    } else {
        visualizationDiv.style.display = "none";
    }
}

let scatter_plot_render = function(data, entry) {

    const entryName = entry.replace("/\s/g,", "");

    const trace1 = {
        x: Array.from({length: data.length}, (_, i) => i + 1),
        y: data.map(term => term.value),
        mode: 'markers',
        type: 'scatter',
        name: 'Team A',
        text: data.map(term => term.name),
        marker: { size: 12 }
    };

    const layout = {
          xaxis: {
            range: [ 1, data.length ]
          },
          yaxis: {
            range: [0, 1]
          },
          title:'One Versus All Graph'
    };

    Plotly.newPlot(`${entryName}-vis-scatter`, [trace1], layout);
};


let network_graph_render = function(graph, entry) {

    const width = 900;
    const height = 720;

    const entryName = entry.replace("/\s/g,", "");

    const color = d3.scaleOrdinal(d3.schemeCategory20);

    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(100))
        .force('charge', d3.forceManyBody().strength(-50))
        .force("center", d3.forceCenter(width / 2, height / 2));

    const svg = d3.select(`#${entryName}-vis-graph`)
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .call(d3.zoom().on("zoom", function () {
                       svg.attr("transform", d3.event.transform)
                    })).append("g");

    const link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(graph.links)
                    .enter()
                    .append("line")
                    .attr("stroke-width", function(d) { return d.stroke_width; })
                    .style("stroke", function() {
                        return "#000000";
                    });

    const node = svg.append("g")
                  .attr("class", "nodes")
                  .selectAll("g")
                  .data(graph.nodes)
                  .enter().append("g");

    const circles = node.append("circle")
                      .attr("r", 25)
                      .attr("fill", function(d) { return color(d.group); })
                      .call(d3.drag()
                          .on("start", dragstarted)
                          .on("drag", dragged)
                          .on("end", dragended));

    const lables = node.append("text")
          .text(function(d) {
            return d.id;
          })
          .attr('x', 25)
          .attr('y', 2);

    const namespaces = node.append("text")
          .text(function(d) {
            return d.group;
          })
          .attr('x', 25)
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