#include <boost/python.hpp>
#include "graph_disjoint.hh"


void edge_disjoint_paths_bind(
    GraphInterface& gi,
    size_t source, 
    size_t target,
    boost::any weight
){
    typedef typename eprop_map_t<double>::type eprop_t;
    eprop_t w = boost::any_cast<eprop_t>(weight);

    gt_dispatch<>()
        ([&](auto& g){ suurballe_edge_disjoint(g, source, target, w.get_unchecked()); },
         all_graph_views())
        (gi.get_graph_view());
};

// The lines below setup a Python module called 'libdisjoint' that reflects the
// function 'edge_disjoint_paths_bind' above as 'edge_disjoint_paths' when 
// imported from Python.

BOOST_PYTHON_MODULE(libdisjoint)
{
    using namespace boost::python;
    def("edge_disjoint_paths", edge_disjoint_paths_bind);
}