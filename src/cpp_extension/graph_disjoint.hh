#include "graph_tool.hh"
#include <iostream>

using namespace graph_tool;
using namespace boost;
using namespace std;

// This template function takes a graph 'g' and a vertex property map 'core_map'
// where the core values will be stored. Their exact types are unspecified at
// this point.

template <typename Graph, typename WeightMap>
void suurballe_edge_disjoint(Graph& g, size_t source, size_t target, WeightMap weight)
{
    // The vertex index is an internal property map that every graph possesses
    typedef typename property_map<Graph, vertex_index_t>::type vertex_index_map_t;
    vertex_index_map_t vertex_index = get(vertex_index_t(), g);

    // Create some auxiliary property maps
    typedef typename eprop_map_t<size_t>::type::unchecked_t vmap_t;
    vmap_t deg(vertex_index, num_vertices(g));  // Remaining degree
    vmap_t pos(vertex_index, num_vertices(g));  // Position in bin (core)

    std::cout<<"Yeah C++ !"<<std::endl;
    std::cout<<"source: "<<source<<std::endl;
    std::cout<<"target: "<<target<<std::endl;


}