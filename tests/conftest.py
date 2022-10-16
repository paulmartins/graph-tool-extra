import pytest
from graph_tool import all as gt


@pytest.fixture
def wiki_suurballe():
    """
    Create the graph used in the Wikipedia Suurballe Algorithm's page
    https://en.wikipedia.org/wiki/Suurballe%27s_algorithm
    """

    # Define graph
    g = gt.Graph(directed=False)
    g.vp.xy = g.new_vp("vector<float>")
    g.vp.name = g.new_vp("string")
    g.ep.weight = g.new_ep("int")

    # Add vertices
    g.add_vertex(6)
    g.vp.name[0] = "A"
    g.vp.xy[0] = [-2, -1]
    g.vp.name[1] = "B"
    g.vp.xy[1] = [0, -2]
    g.vp.name[2] = "C"
    g.vp.xy[2] = [-2, 1]
    g.vp.name[3] = "D"
    g.vp.xy[3] = [0, 2]
    g.vp.name[4] = "E"
    g.vp.xy[4] = [2, -1]
    g.vp.name[5] = "F"
    g.vp.xy[5] = [2, 1]

    # Add edges
    edge_list = []
    edge_list.append([1, 0, 1])
    edge_list.append([0, 2, 2])
    edge_list.append([1, 3, 1])
    edge_list.append([1, 4, 2])
    edge_list.append([2, 3, 2])
    edge_list.append([3, 5, 1])
    edge_list.append([4, 5, 2])
    g.add_edge_list(edge_list, eprops=[g.ep.weight])

    return g
