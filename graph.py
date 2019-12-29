'''
file		: src/graph.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Mon 16 Dec 2019 11:46:28 AM CST
last update	: Tue 17 Dec 2019 01:59:17 PM CST

This file defined some classes: class Node, class Graph
'''
from exceptions import *
import random

class Node:
    '''
    class to describe the nodes in the graph
    '''
    nextMark = 1
    maxPin = 0 # maxPin = max{p(i)|cell(i) is initially free} (for algorithm FM)
    def __init__(self, nodeID=0, mark=-1, gain=0):
        # attributes of each Node
        self.nodeID = nodeID
        self.mark = mark
        self.gain = gain
        self.status = 'free' # free to be moved
        self.label = -1
        self.isBound = False

        # for clusters
        self.belonging_cluster = 0 # 0 means the node belongs to no cluster
        self.clustered = False
        self.isLPcovered = False

    def __lt__(self, other):
        if self.gain > other.gain:
            return True
        elif self.gain == other.gain:
            if self.nodeID < other.nodeID:
                return True
        return False

    def __gt__(self, other):
        if self.gain < other.gain:
            return True
        elif self.gain == other.gain:
            if self.nodeID > other.nodeID:
                return True
        return False

    # this case is impossible because nodeID is different from each other
    def __eq__(self, other):
        if self.gain == other.gain:
            if self.nodeID == other.nodeID:
                return True
        return False


class Cluster:
    nextID = 1 
    def __init__(self, nodes):
        self.clusterID = 0
        self.nodes = list(nodes)
        self.size = 0
        self.gain = 0
        self.mark = -1 # the same as its nodes' mark
        self.boundaryNodes = set()


class Graph:
    '''
    class to describe the graph
    '''
    def __init__(self, fileName, dataType):
        # read-only data
        self.adjList = [] # the 1st line is [verticesNum, edgesNum], node number from 1 on
        self.adjMatrix = []
        self.edges = [] # [[node, node], [node, node],..., [node, node]]
        self.verticesNum = 0
        self.edgesNum = 0

        # data to be operated
        self.nodesObjects = [] # store Node objects, associated with partitions
        self.partitionNum = 0
        self.partitions = [] # [[partition1], [partition2], ...]
        self.boundaryNodes = set()
        self.edgecuts = []


        # read data from specified file
        # consider dataType from specified file
        if dataType == 'edgesDirected':
            self.readEdgesDirectedly(fileName) # init self.edges
            self.edgesToAdjList() # init self.adjList
        elif dataType == 'edgesUndirected':
            self.readEdgesUndirectedly(fileName) # init self.edges
            self.edgesToAdjList() # init self.adjList
        elif dataType == 'adjList':
            self.readAdjList(fileName) # init self.adjList
            self.adjListToEdges() # init self.edges
        else:
            pass

        # init num
        self.verticesNum = self.adjList[0][0]
        self.edgesNum = self.adjList[0][1]

        # init self.adjMatrix
        # costly, invoke self.createAdjMatrix() by hand outside if needed
        # time: O(n^2) space: O(n^2)

        # init self.nodesObjects
        for i in range(self.verticesNum+1):
            if i == 0:
                node = Node() # nodeID = 0, mark = -1, gain = 0
            else:
                node = Node(i, 0, 0) # nodeID = i, mark = 0, gain = 0
            self.nodesObjects.append(node)

        # init partitionNum
        self.partitionNum = 1
        # init partitions
        self.partitions = [[x for x in range(1, self.verticesNum+1)]]
        # self.boundaryNodes and self.edgecuts have already been empty
        self.boundaryNodes = set()
        self.edgecuts = []

        # init Node.maxPin
        Node.maxPin = len(max(self.adjList[1:]))

        return

    def edgesToAdjList(self):
        # init head of self.adjList
        line0 = [self.edges[-1][0], len(self.edges)]
        self.adjList.append(line0)

        for edge in self.edges:
            while edge[0] > len(self.adjList)-1:
                self.adjList.append([])
            self.adjList[edge[0]].append(edge[1])
        return

    def adjListToEdges(self):
        for i in range(1, len(self.adjList)):
            leftEdge = i
            for rightEdge in self.adjList[i]:
                edge = [leftEdge, rightEdge]
                self.edges.append(edge)
        return

    def readEdgesDirectedly(self, fileName):
        if fileName == '':
            raise NoFileError()
        try:
            f = open(fileName)
            print('openning', fileName)
            for line in f:
                if line[0] != '#':
                    line_data = [int(x) for x in line.split()]
                    self.edges.append(line_data)
        except OSError:
            print('can not open', fileName, 'OSError')
        finally:
            if f:
                f.close()
        return

    def readEdgesUndirectedly(self, fileName):
        if fileName == '':
            raise NoFileError()
        try:
            f = open(fileName)
            print('openning', fileName)
            for line in f:
                if line[0] != '#':
                    line_data = [int(x) for x in line.split()]
                    self.edges.append(line_data)
                    line_data_rvs = [line_data[-1], line_data[0]] # reverse
                    self.edges.append(line_data_rvs)
            self.edges.sort() # sort self.edges
        except OSError:
            print('can not open', fileName, 'OSError')
        finally:
            if f:
                f.close()
        return

    def readAdjList(self, fileName):
        if fileName == '':
            raise NoFileError()
        try:
            f = open(fileName)
            print('openning', fileName)
            for line in f:
                if line[0] != '#': # comment symbol
                    line_data = [int(x) for x in line.split()]
                    self.adjList.append(line_data)
        except OSError:
            print('can not open', fileName)
        finally:
            if f:
                f.close()
        return

    def createAdjMatrix(self):
        self.adjMatrix = [[0 for i in range(self.verticesNum+1)] for j in range(self.verticesNum+1)]
        for i in range(1, self.verticesNum+1):
            for j in self.adjList[i]:
                self.adjMatrix[i][j] = 1
        return
