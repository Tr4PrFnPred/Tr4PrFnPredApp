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
    console.log(data);

      const xValue = d => d.name;
      const yValue = d => d.value;
      const yLabel = 'Score';
      const margin = { left: 150, right: 70, top: 20, bottom: 110 };

      const svg = d3.select(`#${entry}-vis-scatter`);
      const width = svg.attr('width');
      const height = svg.attr('height');
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const g = svg.append('g')
          .attr('transform', `translate(${margin.left},${margin.top})`);
      const xAxisG = g.append('g')
          .attr('transform', `translate(0, ${innerHeight})`);
      const yAxisG = g.append('g');

      /* X and Y Axis labels */
      xAxisG.append('text')
          .attr('class', 'axis-label')
          .attr('x', innerWidth / 2)
          .attr('y', 90);

      yAxisG.append('text')
          .attr('class', 'axis-label')
          .attr('x', -innerHeight / 2)
          .attr('y', -100)
          .attr('transform', `rotate(-90)`)
          .style('text-anchor', 'middle')
          .text(yLabel);
      /* X and Y Axis labels */

      /* X and Y Axis ticks */
      const xScale = d3.scalePoint();
      const yScale = d3.scaleLinear().domain([0, 1]);

      const xAxis = d3.axisBottom()
        .scale(xScale)
        .tickPadding(15)
        .tickSize(-innerHeight);

      const yTicks = 5;
      const yAxis = d3.axisLeft()
        .scale(yScale)
        .ticks(yTicks)
        .tickPadding(15)
        .tickSize(-innerWidth);

      /* X and Y Axis ticks */

      xScale
          .domain(data.map(d => d.name))
          .range([0, innerWidth]);

      yScale
          .domain(d3.extent(data, d => d.value))
          .range([innerHeight, 0])
          .nice(yTicks);

      g.selectAll('circle').data(data)
          .enter().append('circle')
            .attr('cx', d => xScale(xValue(d)))
            .attr('cy', d => yScale(yValue(d)))
            .attr('fill', 'blue')
            .attr('fill-opacity', 0.6)
            .attr('r', 8);

      xAxisG.call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65)");
      yAxisG.call(yAxis);
};


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
          .attr('x', 25)
          .attr('y', 2);

    let namespaces = node.append("text")
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