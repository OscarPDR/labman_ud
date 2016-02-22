var gnodes;
var search_function = null;

function buildGraph(graph, options, container) {
    var width = options.container.width;
    var height = options.container.height;

    var transition_duration_in_ms = options.transition.duration;
    var transition_ease = options.transition.ease;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .gravity(0.5)
        .friction(0.5)
        .charge(-2500)
        .linkDistance(125)
        .size([width, height]);

    var svg = d3.select(container).append("svg")
        .attr("width", width)
        .attr("height", height);

    svg.style("cursor", "move");

    var g = svg.append("g");

    var min_zoom = 0.1;
    var max_zoom = 7;
    var zoom = d3.behavior.zoom().scaleExtent([min_zoom, max_zoom]);

    var my_nodes = null;

    function isRelatedNode(selected_node, other_node) {
        if (selected_node === other_node)
                return true;
        else
            return graph.links.some(function(_link) {
                return (_link.source === selected_node && _link.target === other_node) || (_link.source === other_node && _link.target === selected_node);
            });
    };

    function isConnectedBy(_link, _node) {
        return graph.nodes.some(function() {
            return (_link.source === _node) || (_link.target === _node);
        });
    };

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    my_nodes = graph.nodes;

    var link = g.selectAll(".link")
        .data(graph.links)
        .enter()
        .append("path")
        .attr("class", "link")
        .style("stroke-width", function(d) { return Math.sqrt(d.weight); })
        .on("mouseover", function(d) {
            setLinkFocus(d);
        })
        .on("mouseout", function(d) {
            svg.style("cursor", "move");

            link.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 1)
                .style("stroke", "#999");

            texts.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 0);

            node.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 1);

            labels.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 1);
        });

    gnodes = g.selectAll('g.gnode')
        .data(graph.nodes)
        .enter()
        .append('g')
        .classed('gnode', true);

    var glinks = g.selectAll('g.glink')
        .data(graph.links)
        .enter()
        .append('g')
        .classed('glink', true);

    search_function = function() {
        var s = $('#typea').val();

        my_nodes.forEach(function(d) {
            if (d.name == s) {
                setNodeFocus(d);
            }
        });
    };

    function setLinkFocus(d) {
        svg.style("cursor", "pointer");

        link.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return isActual(d, o) ? 1 : 0.1;
            })
            .style("stroke", "#2d2d2d");

        texts.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return isActual(d, o) ? 1 : 0;
            });

        node.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return isConnectedBy(d, o) ? 1 : 0.1;
            });

        labels.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return isConnectedBy(d, o) ? 1 : 0.1;
            });
    };

    function setNodeFocus(d) {
        svg.style("cursor", "pointer");

        link.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return o.source === d || o.target === d ? 1 : 0.1;
            });

        node.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return isRelatedNode(d, o) ? 1 : 0.1;
            });

        labels.transition()
            .duration(transition_duration_in_ms)
            .ease(transition_ease)
            .style("opacity", function(o) {
                return isRelatedNode(d, o) ? 1 : 0.1;
            })
            .style('font-weight', function(o) {
                return isActual(d, o) ? 'bold' : 'normal';
            })
            .style('font-size', function(o) {
                return isActual(d, o) ? '14px' : '12px';
            });
    };

    function isActual(a, b) {
        return a == b;
    };

    var node = gnodes.append("circle")
        .attr("class", "node")
        .attr("r", function(d) { return eigenvectorValue(d); })
        .style('stroke-width', 1.5)
        .style('stroke', 'white')
        .style("fill", function(d) { return color(d['modularity']); })
        .on("mouseover", function (d) {
            setNodeFocus(d);
        })
        .on("mouseout", function (d) {
            svg.style("cursor", "move");

            link.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 1);

            node.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 1);

            labels.transition()
                .duration(transition_duration_in_ms)
                .ease(transition_ease)
                .style("opacity", 1)
                .style('font-weight', 'normal')
                .style('font-size', '12px');
        })
        .call(force.drag);

    var labels = gnodes.append("text")
        .attr("class", "graph-label")
        .style("font-size", "12px")
        .text(function(d) { return d.name; });

    var texts = glinks.append("text")
        .attr("class", "tooltip-label")
        .style("opacity", 0)
        .text(function(d) { return "Share " + d.weight + " items"; });

    zoom.on("zoom", function() {
        g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    });

    node.on("dblclick.zoom", function(d) {
        d3.event.stopPropagation();

        var dcx = (width / 2 - d.x * zoom.scale());
        var dcy = (height / 2 - d.y * zoom.scale());
        zoom.translate([dcx, dcy]);

        g.attr("transform", "translate(" + dcx + "," + dcy + ")scale(" + zoom.scale() + ")");
    });

    svg.call(zoom);

    force.on("tick", function() {
        link.attr("d", linkArc);

        gnodes.attr("transform", function(d) {
            return 'translate(' + [d.x, d.y] + ')';
        });

        labels.attr("transform", function(d) {
            return 'translate(' + [16, 3] + ')';
        });

        texts.attr("transform", function(d) {
            var dx = (d.target.x + d.source.x) / 2;
            var dy = (d.target.y + d.source.y) / 2;

            return 'translate(' + [dx, dy] + ')';
        });

    })
    .start();
};

//  Helper functions
////////////////////////////////////////////////////////////////////////////////////////////////////

function betweennessValue(item) {
    return (item.betweenness * 35) + 5;
};

function closenessValue(item) {
    return (1 - item.closeness) * 25;
};

function degreeValue(item) {
    return item.degree * 2;
};

function eigenvectorValue(item) {
    return (item.eigenvector * 15) + 5;
};

function pagerankValue(item) {
    return item.pagerank * 300;
};

function linkArc(d) {
    var dx = d.target.x - d.source.x;
    var dy = d.target.y - d.source.y;
    var dr = Math.sqrt(dx * dx + dy * dy);

    return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
};
