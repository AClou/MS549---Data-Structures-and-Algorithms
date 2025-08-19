import heapq
import math

import Graph

def dijkstras_algorithm(graph, starting_node):
    #Create dictionaries of distances and predecessors using Dijkstra's algorithm
    distances = {node: math.inf for node in graph}
    distances[starting_node] = 0
    predecessors = {node: None for node in graph}
    priority_queue = [(0, starting_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances, predecessors

def reconstruct_path(predecessors, ending_node):
    #Use the predecessors dictionary to rebuild the path using the ending node
    path = []
    current = ending_node
    while current is not None:
        path.insert(0, current)
        current = predecessors[current]
    return path

def find_shortest_path(graph, starting_node, ending_node):

    #Create distances and predecessors dictionaries using Dijkstra's algorithm
    #passing along the city_map and starting_location
    distances, predecessors = dijkstras_algorithm(city_map, starting_location)

    #Find the shortest path to the destination using the 
    #predecessors dictionary and the reconstruct_path method
    shortest_path_to_ending_node = reconstruct_path(predecessors, destination)

    #Display results
    if distances[destination] != math.inf:
        print(f"\nShortest path from '{starting_location}' to '{destination}': {shortest_path_to_ending_node}, {distances[destination]}")
    else:
        print(f"\nShortest path from '{starting_location}' to '{destination}': None, {distances[destination]}")

#Execution block
if __name__ == "__main__":
    
    
    #Create instance of city_map from Graph.py
    city_map = Graph.Graph()
    city_map.load_map_from_file('map.csv')
    city_map.__str__()

    starting_location = 'B'
    destination = 'D'


    find_shortest_path(city_map, starting_location, destination)