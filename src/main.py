import time
import numpy as np
from graph_tool import all as gt
from python_max_flow import disjoint_paths


def show(g: gt.Graph, edge_pen_width: gt.EdgePropertyMap = None):
    """
    Small helper function to visualize a graph. Helpful for debugging
    """
    if "xy" in g.vp.keys():
        x, y = gt.ungroup_vector_property(g.vp.xy, [0, 1])
        y.fa *= -1
        y.fa -= y.fa.min()
        pos = gt.group_vector_property([x, y])
    else:
        pos = gt.sfdp_layout(g)

    if "name" in g.vp.keys():
        gt.graph_draw(g, pos=pos, vertex_text=g.vp.name, edge_pen_width=edge_pen_width)
    else:
        gt.graph_draw(g, pos=pos, vertex_text=g.vertex_index, edge_pen_width=edge_pen_width)


def main():
    X, Y = 1000, 1000
    source = 1384
    target = 869043

    g = gt.lattice([X, Y])
    x = g.new_vp("double", np.arange(g.num_vertices()) % X)                  
    y = g.new_vp("double", np.arange(g.num_vertices()) // X)
    g.vp.xy = gt.group_vector_property([x,y])
    
    # show(g)
    start = time.time()
    paths = disjoint_paths(g, source, target)
    print(f"Paths found in {time.time()-start}")
    print(paths)


if __name__ == "__main__":
    main()
