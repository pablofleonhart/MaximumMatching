class HopcroftKarp:
    def __init__( self, graph ):
        self.matching = {}
        self.dfspaths = []
        self.dfsparent = {}
        self.phases = 0
        self.paths = 0

        self.left = set( graph.keys() )
        self.right = set()

        for value in graph.values():
            self.right.update( value )

        for vertex in self.left:
            for neighbour in graph[vertex]:
                if neighbour not in graph:
                    graph[neighbour] = set()
                
                graph[neighbour].add( vertex )

        self.graph = graph

    def bfs( self ):
        self.phases += 1
        layers = []
        layer = set()
        for vertex in self.left:
            if vertex not in self.matching:
                layer.add( vertex )

        layers.append( layer )
        visited = set()
        while True:
            layer = layers[-1]
            newlayer = set()
            for vertex in layer:
                if vertex in self.left:
                    visited.add( vertex )
                    for neighbour in self.graph[vertex]:
                        if neighbour not in visited and ( vertex not in self.matching or neighbour != self.matching[vertex] ):
                            newlayer.add( neighbour )
                else:
                    visited.add( vertex )
                    for neighbour in self.graph[vertex]:
                        if neighbour not in visited and ( vertex in self.matching and neighbour == self.matching[vertex] ):
                            newlayer.add( neighbour )

            layers.append( newlayer )
            if len( newlayer ) == 0:
                return layers
            if any( vertex in self.right and vertex not in self.matching for vertex in newlayer ):
                return layers

    def dfs( self, v, index, layers ):
        self.paths += 1
        if index == 0:
            path = [v]
            while self.dfsparent[v] != v:
                path.append( self.dfsparent[v] )
                v = self.dfsparent[v]
            self.dfspaths.append( path )
            return True

        for neighbour in self.graph[v]:
            if neighbour in layers[index - 1]:
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
            if len( layers[-1] ) == 0:
                break

            freeVertex = set( [vertex for vertex in layers[-1] if vertex not in self.matching] )

            del self.dfspaths[:]
            self.dfsparent.clear()

            for vertex in freeVertex:
                self.dfsparent[vertex] = vertex
                self.dfs( vertex, len( layers )-1, layers )

            if len( self.dfspaths ) == 0:
                break

            for path in self.dfspaths:
                for i in range( len( path ) ):
                    if i % 2 == 0:
                        self.matching[path[i]] = path[i+1]
                        self.matching[path[i+1]] = path[i]
                        
        return len( self.matching )/2