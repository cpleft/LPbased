"""
file		: LPbasedAlgo.py 
by		: yang yi   16130120200	    429426523@qq.com
date		: Tue 17 Dec 2019 09:30:06 AM CST
last update	: 

This file implemented the Multi-objective Optimization Graph Partitioning Method
Based on Label Propagation 
"""
import random
from graph import *

def LPbased2(graph):
    '''
    2-way Multi-objective Optimization Graph Partitioning Method Based on Label Propagation
    '''

    def receiveLabel(node):
        '''
        A sub process of LP: changes the node's label to maximum number of the same label
        among its neighbors.
        return True if label changed, otherwise reture False
        '''
        d = {}
        for neighbor in graph.adjList[node]:
            neighbor_label = graph.nodesObjects[neighbor].label
            if neighbor_label != -1:
                if d.has_key(neighbor_label):
                    d.[neighbor_label] += 1
                else:
                    d.[neighbor_label] = 1
        l = sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        max_value = l[0][1]
        for i in range(0, len(l)):
            #TODO i may produce bug
            if l[i][1] != max_value:
                break
        # randomly select a max_label if there are more than one max_value label
        random_index = random.randint(0, i-1)
        max_label = l[random_index][0]

        # change label
        if graph.nodesObjects[node].label != max_label:
            graph.nodesObjects[node].label = max_label
            return True
        else:
            return False


    def LP(area):
        '''
        perform Label Propagation Algorithm on the specific area
        '''
        # init node.label
        for node in area:
            graph.nodesObjects[node].label = random.randint(1, self.verticesNum)

        # iterator
        it = 0
        label_changed = 0
        while it < 10:
            label_changed = 0

            # Arrange the nodes in ther network in a random sequence X.
            X = list(area)
            random.shuffle(X)

            # Each node changes its label to maximum number of the same label among its
            # neighbors in the order of sequence X.
            for node in X:
                if receiveLabel(node):
                    label_changed += 1
            
            if label_changed == 0:
                break

    def incrementalLP(base_area, additional_area):
        '''
        Perform incremental Label Propagation Algorithm when 
        additional_area added in base_area
        '''
        pass


    # algorithm starts

    # set param
    balance_straint = 1000
    end_iteration = 500
    incremental_depth = 5
    k_optimal = 3

    # store useful information of 2 partitions
    mark1 = graph.partitions[0][0].mark
    mark2 = graph.partitions[1][0].mark
    size1 = len(graph.partitions[0])
    size2 = len(graph.partitions[1])

    # init LP cover range (boundary + 'incremental_depth' search)
    LPset = set(graph.boundaryNodes)
    # bfs 'incremental_depth' times, add searched nodes into LPset
    new_searched_LPset = set(LPset)
    search_time = 0
    while search_time < incremental_depth:
        tmp_st = set()
        for node in new_searched_LPset:
            for neighbor in graph.adjList[node]:
                if graph.nodesObjects[neighbor].isLPcovered == False:
                    tmp_st.add(neighbor)
                    graph.nodesObjects[neighbor].isLPcovered = True
        LPset = LPset.union(tmp_st)
        new_searched_LPset = set(tmp_st)

    # initial LP
    LP(LPset)

    active_clusters1 = {} # key is clusterID, value is timestamp
    active_clusters2 = {}
    timestamp = 1 # each time incrementalLP() is invoked, timestamp +1
    clusters = [] # store Cluster objects reference
    clusters.append(Cluster([])) # cluster index from 1 on
    # init initial clusters
    # for each boundary node, bfs
    for boundary_node in graph.boundaryNodes:
        if graph.nodesObjects[boundary_node].clustered == True:
            continue
        # bfs
        cluster_nodes = [boundary_node]
        this_mark = graph.nodesObjects[boundary_node].mark
        this_label = graph.nodesObjects[boundary_node].label
        for searched_node in cluster_nodes:
            for neighbor in graph.adjList[searched_node]:
                if graph.nodesObjects[neighbor].label == this_label and graph.nodesObjects[neighbor].mark == this_mark and graph.nodesObjects[neighbor].isLPcovered:
                    if graph.nodesObjects[neighbor].isBound:
                        graph.nodesObjects[neighbor].clustered = True
                    cluster_nodes.append(neighbor)
        # end bfs
        # make cluster
        cl = Cluster(cluster_nodes)
        # init cl
        cl.clusterID = Cluster.nextID
        Cluster.nextID += 1
        for node in cl.nodes:
            graph.nodesObjects[node].belonging_cluster = cl.clusterID
        cl.size = len(cl.nodes)
        cl.mark = this_mark
        for node in cl.nodes:
            belong = True
            for neighbor in graph.adjList[node]:
                if graph.nodesObjects[neighbor].label != this_label or graph.nodesObjects[neighbor].mark != this_mark:
                    belong = False
                    break
            if belong:
                cl.boundaryNodes.add(node)
        for node in cl.boundaryNodes:
            for neighbor in graph.adjList[node]:
                if graph.nodesObjects[neighbor].belonging_cluster != cl.clusterID:
                    if graph.nodesObjects[neighbor].mark != this_mark:
                        cl.gain += 1
                    else:
                        cl.gain -= 1
        # put cl into clusters
        clusters.append(cl)
        if cl.mark == mark1:
            active_clusters1[cl.clusterID] = timestamp
        elif cl.mark == mark2:
            active_clusters2[cl.clusterID] = timestamp
    # end initial clusters

    # init record
    kPath = [[] for i in range(k_optimal)]
    kGain = [[0] for i in range(k_optimal)]
    kGainSum = [[0] for i in range(k_optimal)]

    kmaxCluster = [0 for i in range(k_optimal)]
    kpercentCluster = [(i+1)*(1/k_optimal) for i in range(k_optimal)]

    # k-Optimization
    average_cluster_size1 = 0
    average_cluster_size2 = 0
    average_gain1 = 0 # must be greater than 0, using abs() to calculate
    average_gain2 = 0
    for cluster1 in active_clusters1.keys():
        average_cluster_size1 += clusters[cluster1].size
        average_gain1 += abs(clusters[cluster1].gain)
    average_cluster_size1 = average_cluster_size1 / len(active_clusters1.keys())
    average_gain1 = average_gain1 / len(active_clusters1.keys())
    for cluster2 in active_clusters2.keys():
        average_cluster_size2 += clusters[cluster2].size
        average_gain2 += abs(clusters[cluster2].gain)
    average_cluster_size2 = average_cluster_size2 / len(active_clusters2.keys())
    average_gain2 = average_gain2 / len(active_clusters2.keys())

    # find max cluster respectively
    for i in range(k_optimal):
        max_score = 0
        max_cluster = 0
        for cluster1 in active_clusters1.keys():
            score = clusters[cluster1].size / average_cluster_size1 + clusters[cluster1].gain / average_gain1
            if score > max_score:
                max_score = score
                max_cluster = cluster1
        kmaxCluster[i] = max_score
        #TODONext

    # iteration starts
    while True:


    # revert back

    # evaluation k-Optimization

    # update graph
