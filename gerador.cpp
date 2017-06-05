#include <fstream>
#include <iostream>
#include <cassert>
using namespace std;
 
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/max_cardinality_matching.hpp>
using namespace boost;
 
// graph element descriptors
typedef adjacency_list_traits<vecS,vecS,undirectedS>::vertex_descriptor Node;
typedef adjacency_list_traits<vecS,vecS,undirectedS>::edge_descriptor Edge;
 
// information stored in vertices
struct VertexInformation {
  Node mate; // partner or graph_traits<Graph>::null_vertex()
};
// information stored in edges
struct EdgeInformation {};
 
// graph is an adjacency list represented by vectors
typedef adjacency_list<vecS,vecS,undirectedS,VertexInformation,EdgeInformation> Graph;
 
int main(int argc, char *argv[]) {
  assert(argc == 4);
  unsigned n = atoi(argv[1]);
  double p = atof(argv[2]);
  char *filename = argv[3];
 
  srand48(time(0));
 
  // (1) generate random bi-partite graph
  Graph g;
 
  for(unsigned i=0; i<2*n; i++)
    add_vertex(g);
 
  for(unsigned i=0; i<n; i++)
    for(unsigned j=n; j<2*n; j++)
      if (drand48() < p) {
        Edge e = add_edge(i,j,g).first;
      }
 
  // (2) get maximum matching
  edmonds_maximum_cardinality_matching(g, get(&VertexInformation::mate,g));
  unsigned card = 0;
  graph_traits<Graph>::vertex_iterator vb, ve;
  for ( tie(vb, ve)=vertices(g); vb != ve; vb++)
    if (g[*vb].mate != graph_traits<Graph>::null_vertex())
      card++;
  cout << "The cardinality of a maximum matching is " << card/2 << "." << endl;
 
  ofstream file;
  file.open( filename );
  // (3) print out in DIMACS format
  file << "c Bi-partite graph" << endl << endl;
  file << "p edge " << num_vertices(g) << " " << num_edges(g) << endl;
  graph_traits<Graph>::edge_iterator eb, ee;
  for ( tie(eb, ee)=edges(g); eb != ee; eb++)
    file << "e " << source(*eb,g)+1 << " " << target(*eb, g)+1 << endl;

  file.close();
}