
from typing import List
import numpy as np
from graph_tool import GraphView, all as gt


def find_path(edges: np.ndarray, source: int, target: int) -> List[List[int]]:
    """
    Given a list of E edges as a numpy 2D array of dimension (E, 2), find the 
    path from source vertex to target vertex.
    This is used to get the shortest path from the results of the function
    :func:`~graph_tool.search.dijkstra_iterator` with the option `array=True`.

    Parameters
    ----------
    edges : :class:`numpy.ndarray`
        List of edges as 2D numpy array containing indices of source and target vertices
    source : int
        Index of the source vertex
    target : int
        Index of the target vertex
    
    Returns
    -------
    path : list of edges defined by [source, target] vertex indices
    """
    path = []
    last = target
    for edge in np.flip(edges, 0):
        if last == source:
            break
        if edge[1] == last:
            path.append(edge.tolist())
            last = edge[0]
    return path


def disjoint_paths(g: gt.Graph, source: gt.Vertex, target: gt.Vertex, weight: gt.EdgePropertyMap = None):
    """
    Find 2 paths from `source` to `target` vertices that do not share any edge
    using Suurballe's algorithm: https://en.wikipedia.org/wiki/Suurballe%27s_algorithm

    Parameters
    ----------
    g : :class:`~graph_tool.Graph`
        Graph to be used
    source : :class:`~graph_tool.Vertex`
        Source vertex, start point of the disjoint paths
    target : :class:`~graph_tool.Vertex`
        Target vertex, end point of the disjoint paths
    weight : :class:`~graph_tool.EdgePropertyMap` (optional, default: ``None``)
        Edge property map with weight values. If not specified, we'll assume all weights to be equal
    
    Returns
    -------
    paths : List of edges in `g`
    """

    if weight is None:
        weight = g.new_edge_property("float")

    # In case of an undirected graph, make sure we define separate edges for both directions.
    # This is because we will need to use different weights depending on the direction.
    if not g.is_directed():
        g.set_directed(True)
        reversed_edges = np.flip(g.get_edges(), axis=1)
        reversed_edges_list = [np.append(re, weight[g.edge(re[1], re[0])]).tolist() for re in reversed_edges]
        g.add_edge_list(reversed_edges_list, eprops=[weight])
    
    # Define extra properties required in the algorithm
    dist = g.new_vp("float")
    in_residual = g.new_ep("bool", val=1)
    in_final_path = g.new_ep("bool", val=0)

    # Find P1
    djikstra_edges_p1 = gt.dijkstra_iterator(g, weight, source, dist, array=True)
    p1 = find_path(djikstra_edges_p1, source, target)
    p1_reversed = np.flip(p1, axis=1).tolist()

    # Update weights and props
    for e in g.iter_edges():
        edge = g.edge(*e)
        weight[edge] += dist[e[0]] - dist[e[1]]
        if e in p1:
            in_residual[edge] = False
        if e in p1_reversed:
            weight[edge] = 0
    
    # Define residual graph
    gr = GraphView(g=g, efilt=in_residual)

    # Find P2, whichever is faster
    # --------------------------
    # Option 1:
    # vp2, ep2 = gt.shortest_path(g=gr, source=source, target=target, weights=gr.ep.weight)
    # p2 = [[int(e.source()), int(e.target())] for e in ep2]
    # --------------------------
    # Option 2:
    djikstra_edges_p2 = gt.dijkstra_iterator(gr, weight, source, array=True)
    p2 = find_path(djikstra_edges_p2, source, target)
    p2_reversed = np.flip(p2, axis=1).tolist()

    # Find the 2 disjoint paths
    for e in g.iter_edges():
        if e in p1 + p2:
            in_final_path[g.edge(*e)] = 1
        if e in p1_reversed + p2_reversed:
            in_final_path[g.edge(*e)] = 0
    
    # gp = GraphView(g=g, efilt=in_final_path)
    # show(gt.Graph(gp, prune=True))

    return in_final_path
