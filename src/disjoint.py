import graph_tool

# We import the C++ module (called libdisjoint.so)
import libdisjoint


# The function below is what will be used from Python, and dispatch to the the
# C++ module.

def edge_disjoint_paths(g, source, target, weight=None):
    if weight is None:
        weight = g.new_edge_property("float")
    
    source = int(source)
    target = int(target)

    return libdisjoint.edge_disjoint_paths(g._Graph__graph, source, target, weight._get_any())
