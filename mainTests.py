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

                #if dic.get( t ) == None:
                #    dic[t] = []

                dic[s].append( int( t ) )
                #dic[t].append( int( s ) )
                #lista[  ].append( line[2] )
                #lista[ int( line[2] ) ].append( line[1] )


#for key in dic.keys():
#    print key,"-",dic[key]

#dic = {"8": {22}, "150": {16}, "100": {30}, "7": {25}, "6": {25, 26, 29}}

#print dic

hop = HopcroftKarp( dic )
ini = time.time()
res = hop.maximumMatching()
fim = time.time()
print res, hop.phases - 1, hop.paths, ( fim - ini ) * 1000, resource.getrusage( resource.RUSAGE_SELF ).ru_maxrss