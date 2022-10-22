import numpy as np
from graph_tool import all as gt
from disjoint import vertex_disjoint_paths


class TestVertexDisjointPaths:
    X, Y, s, t = 10, 10, 23, 67
    g = gt.lattice([X, Y])

    def test_undirected(self):
        nv, ne = self.g.num_vertices(), self.g.num_edges()
        paths = vertex_disjoint_paths(self.g, self.s, self.t)
        # Check graph has not changed
        assert self.g.num_vertices() == nv
        assert self.g.num_edges() == ne
        # Check function works
        assert len(paths) == 4
        unique_v = [v for path in paths for v in path if v not in [self.s, self.t]]
        assert len(unique_v) == len(set(unique_v))
    
    def test_directed(self):
        self.g.set_directed(True)
        nv, ne = self.g.num_vertices(), self.g.num_edges()
        paths = vertex_disjoint_paths(self.g, self.s, self.t)
        # Check graph has not changed
        assert self.g.num_vertices() == nv
        assert self.g.num_edges() == ne
        # Check function works
        assert len(paths) == 2
        unique_v = [v for path in paths for v in path if v not in [self.s, self.t]]
        assert len(unique_v) == len(set(unique_v))
