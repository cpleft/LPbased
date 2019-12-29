"""
file		: hillClimbAlgo.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Mon 16 Dec 2019 03:59:41 PM CST
last update	: 

This file implemented Hill-Climbing Refinement Algorithm
"""
import queue

def hillScan2(graph):
    '''
    2-way hill-scan graph partitioning.
    Refine from initial 2 partitions.
    This algorithm is not move-and-revert
    '''

    def findHill(base_node, max_size):
        '''
        If the gain of a vertice is < 0, then it's time to find a hill to
        find a positive gain.
        Return a list consists of nodes of a hill
        '''
        hill = []
        inner_pq = queue.PriorityQueue()
        inner_pq.get(graph.nodesObjects[base_node])
        hill_mark = graph.nodesObjects[base_node].mark
        book = [0 for i in range(graph.vertexNum+1)]
        gain_gt0 = False

        while not inner_pq.empty() and len(hill) <= 16:
            node = inner_pq.get().nodeID
            hill.append(node)

            # if moving hill is benefical then break
            book[node] = 1 # book[i] == 1 means i is in hill

            external_edges = 0
            internal_edges = 0
            for hill_node in hill:
                for neighbor_node in graph.adjList[hill_node]:
                    if graph.nodesObjects[neighbor_node].mark != hill_mark:
                        external_edges += 1
                    if graph.nodesObjects[neighbor_node].mark == hill_mark and book[neighbor_node] == 0:
                        internal_edges += 1
            hill_gain = external_edges - internal_edges

            if hill_gain > 0:
                gain_gt0 = True
                break

            # add all movable neighbors of 'node' into inner_pq 
            for neighbor_node in graph.adjList[node]:
                if graph.nodesObjects[neighbor_node].mark == hill_mark and book[neighbor_node] == 0 and graph.nodesObjects[neighbor_node].status == 'free':
                    inner_pq.put(neighbor_node)

        # if moving hill is benefical
        if gain_gt0:
            return hill
        else:
            return []

        return


    # store useful information of 2 partitions
    mark1 = graph.partitions[0][0].mark
    mark2 = graph.partitions[1][0].mark
    size1 = len(graph.partitions[0])
    size2 = len(graph.partitions[1])

    # create 2 priority_queues pq1 and pq2, insert all boundary nodes into pq1 and pq2 respectively
    pq1 = queue.PriorityQueue()
    pq2 = queue.PriorityQueue()
    for node in graph.boundaryNodes:
        if graph.nodesObjects[node].mark == mark1:
            pq1.put(graph.nodesObjects[node])
        elif graph.nodesObjects[node].mark == mark2:
            pq2.put(graph.nodesObjects[node])

    add_list1 = [] # store new boundary nodes for partition1
    add_list2 = [] # store new boundary nodes for partition2

    while True:
        # This while statement breaks until no vertices are moved
        moved = 0

        # add new boundary nodes into pq1
        for node in add_list1:
            pq1.put(graph.nodesObjects[node])
        add_list1.clear()

        # add new boundary nodes into pq2
        for node in add_list1:
            pq2.put(graph.nodesObjects[node])
        add_list2.clear()

        while not pq1.empty() or not pq2.empty():
            # compare balance constraint
            if size1 > size2: # should move nodes from partition1 to partition2
                if pq1.empty():
                    break
            if size1 < size2: # should move nodes from partition1 to partition2
                if pq2.empty():
                    break

            # find base_node, base_node is the node to be moved
            if size1 > size2:
                base_node = pq1.queue[0].nodeID
            elif size1 < size2:
                base_node = pq2.queue[0].nodeID
            else:
                if not pq1.empty() and pq2.empty():
                    base_node = pq1.queue[0].nodeID
                if pq1.empty() and not pq2.empty():
                    base_node = pq2.queue[0].nodeID
                if not pq1.empty() and not pq2.empty():
                    base_node = max(pq1.queue[0], pq2.queue[0]).nodeID

            # move node
            if graph.nodesObjects[base_node].gain >= 0:
                # update neighbor nodes of base_node
                for node in graph.adjList[base_node]:
                    if graph.nodesObjects[node].status == 'free': # only move free nodes
                        # update gain
                        if graph.nodesObjects[base_node].mark == graph.nodesObjects[node].mark:
                            graph.nodesObjects[node].gain += 2
                        else:
                            graph.nodesObjects[node].gain -= 2
                        # add new boundary nodes to add_listN
                        if graph.nodesObjects[node].isBound == False:
                            if graph.nodesObjects[node].mark == mark1:
                                add_list1.append(node)
                            if graph.nodesObjects[node].mark == mark2:
                                add_list2.append(node)

                # move base_node
                # update node
                graph.nodesObjects[base_node].status = 'locked'
                if graph.nodesObjects[base_node].mark == mark1:
                    graph.nodesObjects[base_node].mark = mark2
                    size1 -= 1
                    size2 += 1
                    pq1.get()
                else:
                    graph.nodesObjects[base_node].mark = mark1
                    size1 += 1
                    size2 -= 1
                    pq2.get()
                # There is no need to update node.gain and node.isBound becase the node will never be moved(locked)

                # update graph
                # In order to make algorithm efficient, we will update graph.partitions, graph.boundaryNodes, 
                # graph.edgecuts using 'marks' later out of loop 

                moved += 1


            # find hill
            else: 
                hill = findHill(base_node, 16) # set the hill's max_size as 16
                if len(hill) > 0:
                    # move hill
                    moved += len(hill)
                    # update neighbors
                    # update hill nodes
                    # update graph

                pq.get()

        if moved = 0:
            break

    # update graph
