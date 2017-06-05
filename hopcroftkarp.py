class HopcroftKarp:

    def __init__( self, graph ):
        """
        :param graph: an unweighted bipartite graph represented as a dictionary.
        Vertices in the left and right vertex set must have different labelling
        :return: a maximum matching of the given graph represented as a dictionary.
        """
        self.matching = {}
        self.dfspaths = []
        self.dfsparent = {}

        self.left = set( graph.keys() )
        self.right = set()

        print "values:", graph.values()
        for value in graph.values():
            self.right.update( value )

        print "graph:", graph
        print "left:", self.left
        for vertex in self.left:
            print "vertex:", vertex
            for neighbour in graph[vertex]:
                print "neighbour:", neighbour
                if neighbour not in graph:
                    graph[neighbour] = set()
                
                graph[neighbour].add( vertex )

        self.graph = graph

        print "graph:", self.graph

    def bfs( self ):
        layers = []
        layer = set()
        for vertex in self.left:  # for each free vertex in the left vertex set
            if vertex not in self.matching:  # confirms that the vertex is free
                layer.add( vertex )

        print "layer:", layer
        layers.append( layer )
        visited = set()  # to keep track of the visited vertices
        while True:
            print "visited:", visited
            # we take the most recent layer in the partitioning on every repeat
            layer = layers[-1]
            newlayer = set()  # new list for subsequent layers
            for vertex in layer:
                if vertex in self.left:  # if true, we traverse unmatched edges to vertices in right
                    visited.add( vertex )
                    for neighbour in self.graph[vertex]:
                        # check if the neighbour is not already visited
                        # check if vertex is not matched or the edge between neighbour and vertex is not matched
                        if neighbour not in visited and ( vertex not in self.matching or neighbour != self.matching[vertex] ):
                            newlayer.add( neighbour )
                else:  # we traverse matched edges to vertices in left
                    visited.add( vertex )  # we don't want to traverse the vertex again
                    for neighbour in self.graph[vertex]:
                        # check if the neighbour is not already visited
                        # check if vertex is in the matching and if the edge between vertex and neighbour is matched
                        if neighbour not in visited and ( vertex in self.matching and neighbour == self.matching[vertex] ):
                            newlayer.add( neighbour )

            print newlayer
            layers.append( newlayer )  # we add the new layer to the set of layers
            # if newlayer is empty, we have to break the BFS while loop....
            if len( newlayer ) == 0:
                return layers   # break
            # else, we terminate search at the first layer k where one or more free vertices in V are reached
            if any( vertex in self.right and vertex not in self.matching for vertex in newlayer ):
                return layers  # break
                # break

    # --------------------------------------------------------------------------------------------------------------
    # if we are able to collate these free vertices, we run DFS recursively on each of them
    # this algorithm finds a maximal set of vertex disjoint augmenting paths of length k (shortest path),
    # stores them in P and increments M...
    # --------------------------------------------------------------------------------------------------------------
    def dfs( self, v, index, layers ):
        """
        we recursively run dfs on each vertices in freevertex,

        :param v: vertices in freevertex
        :return: True if P is not empty (i.e., the maximal set of vertex-disjoint alternating path of length k)
        and false otherwise.
        """
        print "index:", index
        if index == 0:
            path = [v]
            while self.dfsparent[v] != v:
                path.append( self.dfsparent[v] )
                v = self.dfsparent[v]
            self.dfspaths.append( path )
            print "path:", path
            return True

        print "adjacentes:", self.graph[v]
        for neighbour in self.graph[v]:  # check the neighbours of vertex
            if neighbour in layers[index - 1]:
                # if neighbour is in left, we are traversing unmatched edges..
                if neighbour in self.dfsparent:
                    continue
                if ( neighbour in self.left and ( v not in self.matching or neighbour != self.matching[v] ) ) or \
                        ( neighbour in self.right and ( v in self.matching and neighbour == self.matching[v] ) ):
                    self.dfsparent[neighbour] = v
                    if self.dfs( neighbour, index-1, layers ):
                        return True

        return False

    def maximumMatching( self ):
        while True:
            layers = self.bfs()
            # we break out of the whole while loop if the most recent layer added to layers is empty
            # since if there are no vertices in the recent layer, then there is no way augmenting paths can be found
            if len( layers[-1] ) == 0:
                break

            freeVertex = set( [vertex for vertex in layers[-1] if vertex not in self.matching] )
            print "freeVertex:", freeVertex

            # the maximal set of vertex-disjoint augmenting path and parent dictionary
            # has to be cleared each time the while loop runs
            # self.dfspaths.clear() - .clear() and .copy() attribute works for python 3.3 and above
            del self.dfspaths[:]
            self.dfsparent.clear()

            for vertex in freeVertex:  # O(m) - every vertex considered once, each edge considered once
                # this creates a loop of the vertex to itself in the parent dictionary,
                self.dfsparent[vertex] = vertex
                self.dfs( vertex, len( layers )-1, layers )

            # if the set of paths is empty, nothing to add to the matching...break
            if len( self.dfspaths ) == 0:
                break

            # if not, we swap the matched and unmatched edges in the paths formed and add them to the existing matching.
            # the paths are augmenting implies the first and start vertices are free. Edges 1, 3, 5, .. are thus matched
            for path in self.dfspaths:
                for i in range( len( path ) ):
                    if i % 2 == 0:
                        self.matching[path[i]] = path[i+1]
                        self.matching[path[i+1]] = path[i]
            print "matching:", self.matching

        return self.matching