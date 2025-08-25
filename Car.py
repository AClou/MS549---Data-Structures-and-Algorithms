import heapq
import math

import Graph

class Car:
    def __init__(self, car_id, initial_location):
        self.id = car_id
        self.location = initial_location
        self.current_node = None
        self.status = 'available'
        self.destination = None
        self.route = None
        self.route_time = 0
        self.assigned_rider = None

    def display_info(self):
        print(f"Car {self.id} is currently at {self.location}, and is {self.status}.")

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

    def calculate_route(self, destination, graph):

        #Assign starting location (node) as car's current_node
        starting_location = self.current_node

        #Create distances and predecessors dictionaries using Dijkstra's algorithm
        #passing along the city_map and starting_location
        distances, predecessors = Car.dijkstras_algorithm(graph, self.current_node)

        #Find the shortest path to the destination using the 
        #predecessors dictionary and the reconstruct_path method
        shortest_path_to_ending_node = Car.reconstruct_path(predecessors, destination)

        self.route = shortest_path_to_ending_node
        self.route_time = distances[destination]

        #Display results
        if self.route_time != math.inf:
            print(f"    {self.id} - shortest path from '{starting_location}' to '{destination}': {self.route}, {self.route_time}")
        else:
            print(f"    {self.id} - shortest path from '{starting_location}' to '{destination}': None, {self.route_time}")