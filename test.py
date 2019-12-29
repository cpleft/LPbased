"""
file		: test.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Mon 16 Dec 2019 03:46:19 PM CST
last update	: 
"""

import sys, getopt
import initPart
from graph import *

dataType = "edgesUndirected" # data type: edgesDirected, edgesUndirected, adjList
filename = ""

def usage():
    print("usage: LPbased.py [OPTION]... [FILE]...\n"
            "filename for inputfile name\n"
            "-h, --help for help\n"
            "-i, -f, --inputfile for inputfile name")

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hudgf:", ["help", "inputfile="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-d":
            dataType = "edgesDirected"
        elif o == "-u":
            dataType = "edgesUndirected"
        elif o == "-g":
            dataType = "adjList"
        elif o in ("-f", "--inputfile"):
            filename = a
        else:
            pass
    if args and filename == "":
        filename = args[0]

    g = Graph(filename, dataType)
    print(g.verticesNum, g.edgesNum)
    print(g.adjList[0:30])
    print(g.edges[0:30])

    print('before initPart')
    print(g.partitionNum)
    print('edgecuts:')
    print(len(g.edgecuts))
    print(g.edgecuts[0:30])
    print('boundaryNodes')
    print(len(g.boundaryNodes))
    print(g.boundaryNodes[0:30])
    initPart.initPart(g, 8)
    print('after initPart')
    print(g.partitionNum)
    print('edgecuts:')
    print(len(g.edgecuts))
    print(g.edgecuts[0:30])
    print('boundaryNodes')
    print(len(g.boundaryNodes))
    print(g.boundaryNodes[0:30])

    print(g.nodesObjects[0].nextMark)
    print()
    for i in range(100):
        print(g.nodesObjects[i].gain, end=',')
