from hopcroftkarp import HopcroftKarp
import sys
import time
import resource

param = sys.argv[1:]

file = open( param[0], "r" )
finish = False
lista = []
dic = {}

m = 0
n = 0

while not finish:
    line = file.readline()

    if not line:
        finish = True

    else:
        line = line.split()
        
        if len( line ) > 0:
            if line[0] == 'p':
                m = int( line[2] )
                n = int( line[3] )

                for i in xrange( m+1 ):
                    lista.append( [] )

            if line[0] == 'e':
                s = "".join( line[1] )
                t = line[2]

                if dic.get( s ) == None:
                    dic[s] = []

                dic[s].append( int( t ) )

hop = HopcroftKarp( dic )
print hop.maximumMatching()