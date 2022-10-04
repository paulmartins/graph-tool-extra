CXX=g++
# Had to remove -fopenmp from CXXFLAGS
CXXFLAGS=-O3 -std=gnu++17 -Wall -fPIC `pkg-config --cflags --libs graph-tool-py3.10` -shared
ALL: libdisjoint.so

libdisjoint.so: graph_disjoint.hh graph_disjoint.cc
	${CXX} ${CXXFLAGS} graph_disjoint.cc -o ../libdisjoint.so