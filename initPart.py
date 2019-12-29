"""
file		: initPart.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Mon 16 Dec 2019 04:07:24 PM CST
last update	: Tue 17 Dec 2019 09:28:08 AM CST

This file implemented the initial partition process.
This file should modify:
# graph.nodesObjects
# graph.partitionNum
# graph.partitions
# graph.boundaryNodes
# graph.edgecuts
after checking if the graph has been changed by other algorithms.
"""
from exceptions import *
from graph import *
import random, queue


def initPart(graph, n):
    '''
    partition a graph into 2 partitions balancedly.
    from an ramdom node on, adding its neigbors into a set like BFS,
    leaving others another set, until 2 sets are balanced.
    '''

    def sub2Part(partition):
        '''
        Partition the partition(list[]) into 2 partitions(list[[], []])
        This function does not change param partition
        '''
        print('initializing 2-way balanced partitioning...')

        partitionMark = graph.nodesObjects[partition[0]].mark
        nextMark = graph.nodesObjects[partition[0]].nextMark

        enough = False
        it = 0

        while True:
            start_node = partition[random.randint(0, len(partition)-1)]
            while graph.nodesObjects[start_node].mark != partitionMark or not graph.adjList[start_node]:
                start_node = partition[random.randint(0, len(partition)-1)]

            graph.nodesObjects[start_node].mark = nextMark # update graph.nodesObjects

            partition1 = []
            partition2 = []
            partition1.append(start_node)

            # breadth first search
            q = queue.Queue()
            q.put(start_node)
            while not q.empty():
                for x in graph.adjList[q.get()]:
                    if graph.nodesObjects[x].mark != nextMark and graph.nodesObjects[x].mark != partitionMark:
                        continue
                    if graph.nodesObjects[x].mark != nextMark:
                        q.put(x)
                        graph.nodesObjects[x].mark = nextMark # update graph.nodesObjects[].mark
                        partition1.append(x)
                        if abs(len(partition)-2*len(partition1)) < 2:
                            enough = True
                            break
                if enough == True:
                    break
            if enough == True:
                print('graph partition balanced')
                break
            it += 1
            if it > 4:
                break

        partition2 = list(set(partition) - set(partition1)) # may be costly
        Node.nextMark += 1 # update graph.nodesObjects
        graph.partitionNum += 1 # update graph.partitionNum
        return [partition1, partition2]

    def externalConnection(nodeObject):
        weight = 0
        for node in graph.adjList[nodeObject.nodeID]:
            if graph.nodesObjects[node].mark != nodeObject.mark:
                weight += 1
        return weight

    def internalConnection(nodeObject):
        weight = 0
        for node in graph.adjList[nodeObject.nodeID]:
            if graph.nodesObjects[node].mark == nodeObject.mark:
                weight += 1
        return weight



    # check if the graph has been changed by other algorithms.
    try:
        if graph.partitionNum != 1 or len(graph.partitions) != 1 or graph.boundaryNodes or graph.edgecuts:
            raise AlgoPartDuplicatedError()
        elif len(graph.partitions[0]) != graph.verticesNum:
            raise AlgoNoNodeInPartitionsError()
    except AlgoPartDuplicatedError:
        return
    except AlgoNoNodeInPartitionsError:
        return

    if n <= 1:
        print('n must > 1')
        return

    iterations = int(n**0.5) # iterations: how many bisection iteration that should be calculate
    remain = n - 2**iterations # after bisectioning, how many subgraphs remain that should be bisectioning
    # update graph.partitions
    for i in range(iterations):
        for j in range(len(graph.partitions)):
            add = sub2Part(graph.partitions[j])
            none = graph.partitions.pop(2*j)
            graph.partitions.insert(2*j, add[0])
            graph.partitions.insert(2*j+1, add[1])
    for i in range(remain):
        add = sub2Part(graph.partitions[i])
        noname = graph.partitions.pop(2*i)
        graph.partitions.insert(2*i, add[0])
        graph.partitions.insert(2*i+1, add[1])

    # update graph.edgecuts
    for edge in graph.edges:
        if graph.nodesObjects[edge[0]].mark != graph.nodesObjects[edge[1]].mark:
            graph.edgecuts.append(edge)
 
    # update graph.boundaryNodes
    for edge in graph.edgecuts:
        for node in edge:
            graph.boundaryNodes.add(node)

    # update node.isBound
    for node in graph.boundaryNodes:
        graph.nodesObjects[node].isBound = True
    
    # update graph.nodesObjects[].gain
    for nodeObject in graph.nodesObjects[1:]:
        nodeObject.gain = externalConnection(nodeObject) - internalConnection(nodeObject)
