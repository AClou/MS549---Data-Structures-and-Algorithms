# graph class
import csv

class Graph:
    #Initialize with empty adjacency list
    def __init__(self):
        self.adjacency_list = {}

    #Add nodes so long as they are not already found in list
    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    #Add edge to the list
    def add_edge(self, start_node, end_node, weight):
        self.add_node(start_node)
        self.add_node(end_node)
        self.adjacency_list[start_node].append((end_node, float(weight)))

    #Load the map data from the specified file
    def load_map_from_file(self, filename):
        print(f"Gathering map data from {filename}.")
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:
                        start, end, weight = row
                        self.add_edge(start.strip(), end.strip(), weight.strip())
            print("Map data successfully loaded!")
        except FileNotFoundError:
            print(f"Error: File '{filename}' can not be found.")
        except Exception as e:
            print(f"Unfortunately, an error has occurred: {e}")

    def __str__(self):
        print(f"*** Map Adjacency List ***")
        for node, neighbors in self.adjacency_list.items():
            neighbor_str = ", ".join([f"({n}, {w})" for n, w in neighbors])
            print(f"{node} : [{neighbor_str}]")


#Execution block
if __name__ == "__main__":
    map = Graph()
    map.load_map_from_file('map.csv')
    map.__str__()