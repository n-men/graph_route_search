import sys
import os.path
import pandas as pd
import numpy as np


def find_route():
	"""Find route in graph from one node to another using Dijkstra's algorithm"""
	
	edges, first_node, last_node = get_params()
	df = init_df(edges, first_node, last_node)
	
	# do while last node is not visited
	while df.loc[[last_node]]['visited'].values[0] == 0:
	
		current_node = df.loc[df['visited'] == 0]['route_length'].argmin()
		
		try:
			current_row = df.loc[[current_node]]
		except KeyError:
			print("There is no route from node {} to node {}".format(first_node, last_node))
			exit()
	
		# check all neighbours of current node
		for neighbour, distance in current_row['neighbours'].values[0].items():

			route_length = df.get_value(neighbour, 'route_length')
			new_route_length = current_row['route_length'].values[0] + distance
			
			if (df.get_value(neighbour, 'visited') == 0) and (new_route_length < route_length):
				# refresh the route to the neighbour node

				route = current_row['route'].values[0] + str(neighbour)
				df.set_value(neighbour, 'route', route)
				df.set_value(neighbour, 'route_length', new_route_length)		   

		# mark current node as visited
		df.set_value(current_node, 'visited', 1)  
		
	print("Route from {first_node} to {last_node}: length: {route_length}, route: {route}".format(
		first_node=first_node,
		last_node=last_node,
		route_length=int(df.get_value(last_node, 'route_length')),
		route='-'.join(df.get_value(last_node, 'route'))
	))


def get_params():
	"""Read params and check their validity"""

	try:
		sys.argv[3]
	except IndexError:
		print("Not enough parameters")
		exit()
	
	filename = sys.argv[1]
	if not os.path.exists(filename):
		print("File with edges is not found")
		exit()
		
	dtype={'node1': str, 
		   'node2': str, 
		   'distance': np.int64}
	edges = pd.read_csv(filename, delimiter=";", dtype=dtype)
	if set(edges.columns.values) <> set(['node1', 'node2', 'distance']):
		print("Wrong format in edges file")
		exit()
	
	first_node = sys.argv[2]
	last_node = sys.argv[3]
	
	check_graph(edges, first_node, last_node)
	
	return edges, first_node, last_node


def check_graph(edges, first_node, last_node):
	"""Input data validity check"""

	# check that nodes are in graph
	nodes = np.unique(edges[['node1', 'node2']].values)
	for node in first_node, last_node:
		if node not in nodes:
			print("Node '{}' is not in graph".format(node))
			exit()
	
	# check edges for duplicates
	tmp_edges = edges[['node2', 'node1', 'distance']]
	tmp_edges.columns = ['node1', 'node2', 'distance']
	tmp_edges = tmp_edges.append(edges, ignore_index=True)
	if any(tmp_edges.duplicated(['node1', 'node2'])):
		"There are duplicates found in edges file. Please, remove duplicate edges"
		exit()


def get_neighbours(node, edges):
	"""Create neighbours dictionary for every node based on edges"""
	
	neighbours = dict()
	
	for index, edge in edges.loc[edges['node1'] == node].iterrows():
		neighbours[edge['node2']] = edge['distance']
	
	for index, edge in edges.loc[edges['node2'] == node].iterrows():
		neighbours[edge['node1']] = edge['distance']
		
	return neighbours


def init_df(edges, first_node, last_node):
	"""Create storage for iteratios' results"""
	
	# create empty dataframe to store results of iterations
	nodes = np.unique(edges[['node1', 'node2']].values)
	index = nodes
	columns = ['neighbours', 'visited', 'route', 'route_length']
	df = pd.DataFrame(columns=columns, index=index)
	
	# fill dataframe with initial values
	df['neighbours'] = df.index.map(lambda x: get_neighbours(x, edges))
	df['visited'] = 0
	df['route_length'] = float('inf')
	df.set_value(first_node, 'route_length', 0)
	df['route'] = ''
	df.set_value(first_node, 'route', str(first_node))
	
	return df


if __name__ == "__main__":
	find_route()