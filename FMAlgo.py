"""
file		: FMAlgo.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Tue 17 Dec 2019 11:11:16 AM CST
last update	: 

This file implemented FM algorithm.
"""
from graph import *

def FM2(graph):
    '''
    Refine a graph by 2-way FM algorithm.
    '''

    def moveNode(node):
        node_mark = graph.nodesObjects[node].mark
        if node_mark == mark1:
            graph.nodesObjects[node].mark = mark2
        elif node_mark == mark2:
            graph.nodesObjects[node].mark = mark1
        else:
            pass

    # FM algorithm uses bucket-sorting to maintain a sorted list of node gains.
    maxPin = Node.maxPin

    # Create data structures: Bucket list
    # for 2-way partitioning, create data structures for each partition
    bucket1 = [[] for i in range(2*maxPin+1)]
    bucket2 = [[] for i in range(2*maxPin+1)]

    # store useful information of 2 partitions
    mark1 = graph.partitions[0][0].mark
    mark2 = graph.partitions[1][0].mark
    size1 = len(graph.partitions[0])
    size2 = len(graph.partitions[1])

    max_gain1 = -maxPin-1
    max_gain2 = -maxPin-1
    # init bucket1
    for node in graph.partitions[0]:
        g = graph.nodesObjects[node].gain
        p = maxPin - g
        bucket1[p].append(node)
        if max_gain1 < g:
            max_gain1 = g
    # init bucket2
    for node in graph.partitions[1]:
        g = graph.nodesObjects[node].gain
        p = maxPin - g
        bucket2[p].append(node)
        if max_gain2 < g:
            max_gain2 = g

    # record move path
    Gain = [0]
    GainSum = [0]
    Path = []

    while True:
        # This loop breaks until no nodes is moved
        moved = 0

        if size1 > size2:
            # if bucket1 is empty
            if max_gain1 <= -maxPin-1:
                break
        if size1 < size2:
            # if bucket2 is empty
            if max_gain2 <= -maxPin-1:
                break
        if size1 == size2 and max_gain1 <= -maxPin-1 and max_gain2 <= -maxPin-1:
            break

        # find base_node
        base_node_from = 0
        if size1 > size2:
            base_node = bucket1[maxPin-max_gain1][0]
            base_node_from = 1
        elif size1 < size2:
            base_node = bucket2[maxPin-max_gain2][0]
            base_node_from = 2
        else:
            if max_gain1 >= max_gain2 and max_gain1 >= -maxPin-1:
                base_node = bucket1[maxPin-max_gain1][0]
                base_node_from = 1
            elif max_gain1 < max_gain2 and max_gain2 >= -maxPin-1:
                base_node = bucket2[maxPin-max_gain2][0]
                base_node_from = 2
            else:
                break

        if base_node_from == 1:
            bucket1[maxPin-max_gain1].pop(0)
            base_node_gain = max_gain1
            # find next max_gain
            while len(bucket1[maxPin-max_gain1]) <= 0:
                max_gain1 += 1
                if max_gain1 <= -maxPin-1:
                    break
        elif base_node_from == 2:
            bucket2[maxPin-max_gain2].pop(0)
            base_node_gain = max_gain2
            # find next max_gain
            while len(bucket2[maxPin-max_gain2]) <= 0:
                max_gain2 += 1
                if max_gain2 <= -maxPin-1:
                    break
        else:
            pass
        # update base_node's neighbors gain
        graph.nodesObjects[base_node].status = 'locked'
        for node in graph.adjList[base_node]:
            if graph.nodesObjects[node].status == 'free': # only move free nodes
                # update gain
                current_gain = graph.nodesObjects[node].gain
                if graph.nodesObjects[base_node].mark == graph.nodesObjects[node].mark:
                    graph.nodesObjects[node].gain += 2
                else:
                    graph.nodesObjects[node].gain -= 2

                # find the neighbor node in the data structure
                # if it exists, remove it
                if graph.nodesObjects[node].mark == mark1:
                    if node in bucket1[maxPin-current_gain]:
                        bucket1[maxPin-current_gain].remove(node)
                    bucket1[maxPin-graph.nodesObjects[node].gain].append(node)

        # record base_node
        Gain.append(base_node_gain)
        GainSum.append(GainSum[-1]+base_node_gain)
        Path.append(base_node)
    
    # revert
    revert_till = GainSum.index(max(GainSum))
    for node in Path[0:revert_till]:
        moveNode(node)

    # update graph
