import networkx as nx
import random as rand
from datetime import datetime, timedelta


def removeVertices(graph, time):

	# keep removing if it's easy to remove vertices

	iterations = 0
	successOfLastTen = 0
	endtime = datetime.now() + timedelta(seconds = time)
	
	while(datetime.now() < end_time):
		if (iterations % 10 == 0 && iterations!= 0):
			# keep removing if it's easy to remove vertices
			if (successOfLastTen == 0):
				return
			successOfLastTen = 0

		node = list(G.nodes)[rand.randrange(0, graph.number_of_nodes())]
		graphWithout = copy.deepcopy(graph)
		graphWithout = graphWithout.remove_node(node)
		if (nx.is_connected(graphWithout)):
			graph = graphWithout
			successOfLastTen += 1

		iterations += 1

def tryRemoveVertices(graph, tries):
	graphs = []
	for i in range(tries):
		g = copy.deepcopy(graph)
		removeVertices(g, 1)
		graphs += [g]

	return graphs