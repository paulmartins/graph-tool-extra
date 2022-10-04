
import numpy as np
from graph_tool import GraphView, all as gt

PSEUDO_INF = 100_000_000


def disjoint_paths(g: gt.Graph, source: gt.Vertex, target: gt.Vertex):
    """
    Find paths from `source` to `target` vertices that do not share any edge
    using a max-flow problem. See the links below for some more documentation
    https://en.wikipedia.org/wiki/Maximum_flow_problem#Maximum_number_of_paths_from_s_to_t
    https://stackoverflow.com/questions/62619343/how-to-approach-coding-for-node-disjoint-path/62620125#62620125
    
    
    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be used
    source : :class:`~graph_tool.Vertex`
        Source vertex, start point of the disjoint paths
    target : :class:`~graph_tool.Vertex`
        Target vertex, end point of the disjoint paths

    Returns
    -------
    paths : List of edges in `g`
    """
    
    # Save the initial number of vertices before we split them into "in" and "out"
    n_vertices = g.num_vertices()

    # Add "out" vertices
    g.add_vertex(n_vertices)

    # Edge property to save capacity values
    capacity = g.new_edge_property("float")

    # Define in -> out edges
    # NOTE: the capacity of the edge from the source must be large enough
    # to cover for the meximum number of path, ideally to be set to infinity 
    # but this is not compatible with graph-tool functions used lated
    s_in = np.arange(n_vertices)
    t_out = np.arange(n_vertices, 2*n_vertices, 1)
    io_cap = np.ones(n_vertices)
    io_cap[source] = PSEUDO_INF
    in_out_edges = np.stack([s_in, t_out, io_cap], axis=-1)

    # Define out -> in edges
    normal_edges = g.get_edges()
    normal_edges[:,0] += n_vertices
    oi_cap = np.full_like(normal_edges[:,0], PSEUDO_INF)
    out_in_edges = np.stack([normal_edges[:,0], normal_edges[:,1], oi_cap], axis=-1)
    
    # Make sure we have a directed graph (required by max-flow problem later)
    # If not, we need to define out -> in edges in the other direction
    if not g.is_directed():
        g.set_directed(True)
        reversed_edges = g.get_edges()
        reversed_edges[:,1] += n_vertices
        out_in_edges = np.concatenate([
            out_in_edges, 
            np.stack([reversed_edges[:,1], reversed_edges[:,0], oi_cap], axis=-1)
        ])

    # Remove all the original in -> in edges (not needed if default capacity is 0?)
    # for edge in g.get_edges():
    #     g.remove_edge(g.edge(*edge))

    # Add all edges we defined above
    g.add_edge_list(np.concatenate([in_out_edges, out_in_edges]), eprops=[capacity])

    # Run max-flow and get the edge residual capacities
    # residual = gt.edmonds_karp_max_flow(g, source, target, capacity)
    # residual = gt.push_relabel_max_flow(g, source, target, capacity)
    residual = gt.boykov_kolmogorov_max_flow(g, source, target, capacity)

    # Retrive the actual flow 
    flow = g.new_edge_property("bool")
    flow.a = capacity.a - residual.a
    max_flow = sum(flow[e] for e in g.vertex(target).in_edges())
    print(f"Max flow = {max_flow} (= number of vertex disjoint paths)")

    # Criteria to keep an edge in the paths is positive flow
    to_keep = g.new_edge_property("bool")
    gt.map_property_values(flow, to_keep, lambda x: x > 0)
    gp = GraphView(g, efilt=to_keep)
    
    # Visualise paths
    # gt.graph_draw(
    #     g, 
    #     pos=gt.sfdp_layout(g), 
    #     edge_pen_width=gt.prop_to_size(flow, mi=0, ma=5, power=1),
    #     vertex_text=g.vertex_index
    # )

    # Find all the paths from source to target in the filtered graph
    # NOTE: one could also use all_shortest_paths
    edge_disjoint_paths = []
    for path in gt.all_paths(gp, source, target):
        edge_disjoint_paths.append([i for i in path if i < n_vertices])
    
    return edge_disjoint_paths
