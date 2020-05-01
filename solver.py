import networkx as nx
from networkx.algorithms.approximation import min_edge_dominating_set
from networkx.algorithms import dominating_set
from networkx.algorithms.tree.mst import minimum_spanning_tree
from networkx.algorithms.approximation.steinertree import steiner_tree

from datetime import datetime, timedelta

from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import os


######################################################################
# CHANGE THIS VARIABLE TO CHANGE THE TIME SPENT OPTIMIZING EACH GRAPH
######################################################################
TIMEOUT = 50


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    end_time = datetime.now() + timedelta(seconds=TIMEOUT)

    graphs_to_consider = []
    graphs_to_consider.append(minimum_spanning_tree(G))
    index = 0
    while datetime.now() < end_time and index < len(G.nodes):
        resulting_graph = create_graph_from_dominating_set(G, dominating_set(G, start_with=index))
        #print( average_pairwise_distance(resulting_graph))
        #resulting_graph = optimize_pairwise_distances(G, resulting_graph, average_pairwise_distance(resulting_graph))

        if not nx.is_empty(resulting_graph) and nx.is_connected(resulting_graph):
            graphs_to_consider.append(resulting_graph)
        index+=1
    return min(graphs_to_consider, key=average_pairwise_distance)

'''
Returns a steiner tree that contains all the nodes from the dominating set.
'''
def create_graph_from_dominating_set(G, domin_set) :
    return steiner_tree(G, domin_set)


'''
Further optimizes the tree by adding nodes not in the tree to see if it
may bring down the average pairwise distance.
'''
def optimize_pairwise_distances(original_graph, tree, avg_dist) :
    edges_difference = set(original_graph.edges).difference(tree.edges)
    tree = tree.copy()

    already_added_nodes = set([])
    current_avg_dist = avg_dist
    for edge in edges_difference :
        # ignore any edges that are not related to the tree
        if edge[1] not in tree.nodes and edge[0] not in tree.nodes :
            continue
        # ignore any edges already in the tree
        if edge[1] in tree.nodes and edge[0] in tree.nodes :
            continue

        if edge[1] in tree.nodes :
            node_to_consider = edge[0]
        else:
            node_to_consider = edge[1]

        if node_to_consider in already_added_nodes :
            continue

        # test to see what happens if we add the node in
        tree.add_node(node_to_consider)
        tree.add_edge(edge[0], edge[1], weight=original_graph[edge[0]][edge[1]]["weight"])

        dist = average_pairwise_distance(tree)
        # if it improves our situation
        if dist < current_avg_dist :
            already_added_nodes.add(node_to_consider)
            current_avg_dist = dist
        # it doesn't improve our situation, so undo the added node
        else :
            tree.remove_node(node_to_consider)

    return tree




# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in


'''
if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    print(list(T.nodes))
    assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
    write_output_file(T, 'out/test.out')
'''

'''
dir = "inputs/"
list_files = os.listdir("inputs/")
index = 0
for file in list_files:

    name = file[0:-3]
    index+=1
    print(name)
    if(os.path.isfile('output/' + name + ".out")) :
        continue
    try:
        G = read_input_file(dir + name + ".in")
        T = solve(G)
        assert is_valid_network(G, T)
        print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
        write_output_file(T, 'output/' + name + ".out")
    except:
        print("ERRORED")

    #if(index == 6) :
    #    break;
    print(index, "/", len(list_files))
'''
def error_check() :
    list_files = os.listdir("inputs/")
    for file in list_files:
        name = file[0:-3]
        #print(name)
        if (os.path.isfile('output/' + name + ".out")):
            continue
        print("error")
error_check()