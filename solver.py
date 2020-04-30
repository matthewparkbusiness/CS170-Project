import networkx as nx
from networkx.algorithms.approximation import min_edge_dominating_set
from networkx.algorithms import dominating_set
from networkx.algorithms.tree.mst import minimum_spanning_tree

from datetime import datetime, timedelta

from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import copy


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    timeout = 4000
    end_time = datetime.now() + timedelta(seconds=timeout)

    graph_size = len(G.nodes)
    graphs_to_consider = []

    index = 0
    while (datetime.now() < end_time and index < graph_size):
        domin_set = dominating_set(G, start_with=index)
        resulting_graph = copy_graph_from_dominating_set(G, domin_set)

        graphs_to_consider.append(resulting_graph)
        index+=1

    print(type(graphs_to_consider[0]))
    #print(graphs_to_consider)
    return min(graphs_to_consider, key=average_pairwise_distance)


def copy_graph_from_dominating_set(G, domin_set) :
    graph_copy = copy.deepcopy(G)
    return graph_copy.subgraph(domin_set)

'''
Takes in a dominating set. Runs MST on the graph and
optimizes the average pairwise distance
'''
def process_graph(original_graph, dominating_set) :
    mst = minimum_spanning_tree(dominating_set)
    return mst
    #return add_back_vertices(original_graph, mst)

def add_back_vertices(original_graph, mst) :
    #prakash's job
    pass

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    print(list(T.nodes))
    assert is_valid_network(G, T)
    print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
    write_output_file(T, 'out/test.out')
