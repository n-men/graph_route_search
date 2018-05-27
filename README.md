# graph_route_search
Search for the optimal route from one vertex to another in a weighted non-aligned graph (with no negative weights)

graph.csv - an example of setting a graph for a script

The script is accessed in the following format:
     python graph.py [graph file] [vertex 1] [vertex 2]
An example of accessing a script from the command line:
      `python graph.py "graph.csv" 1 5`
      
Response example:
      `Route from 1 to 5: length: 20, route: 1-3-6-5`
