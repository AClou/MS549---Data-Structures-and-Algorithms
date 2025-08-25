#Graph class
import csv
import collections

class Graph:
    #Initialize with empty adjacency list and node coordinates dictionary
    def __init__(self):
        self.adjacency_list = collections.defaultdict(list)
        self.node_coordinates = {}

    #make the Graph object iterable
    def __iter__(self):
        return iter(self.adjacency_list)

    def __getitem__(self, node):
        return self.adjacency_list[node]

    #Load the map data from the specified file
    def load_map_data(self, filename):
        print(f"Gathering map data from {filename}.")
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if line.startswith('#') or not line.strip():
                        continue

                    parts = line.strip().split(',')
                    start_id, start_x, start_y, end_id, end_x, end_y, weight = parts

                    #store coords for both nodes
                    self.node_coordinates[start_id] = (float(start_x), float(start_y))
                    self.node_coordinates[end_id] = (float(end_x), float(end_y))

                    #store the edge for the undirected graph
                    self.adjacency_list[start_id].append((end_id, float(weight)))
                    self.adjacency_list[end_id].append((start_id, float(weight)))
                
            print("Map data successfully loaded!")
        except FileNotFoundError:
            print(f"Error: File '{filename}' can not be found.")
        except Exception as e:
            print(f"Unfortunately, an error has occurred: {e}")
