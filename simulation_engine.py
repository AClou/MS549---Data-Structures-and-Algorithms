import Car
import Rider
import Graph
import Quadtree

import heapq
import time
import random
import math
import matplotlib.pyplot as plt

from dataclasses import dataclass, field
from typing import Any

import argparse
parser = argparse.ArgumentParser()

parser.add_argument(
    "max_trips", type=int, help="How many trips should the simulation create? Make sure it is an integer."
)

args = parser.parse_args()

@dataclass(order=True)
class Event:
    timestamp: int
    event_type: str
    data: Any = field(compare=False)

class Simulation:
    def __init__(self):
        self.current_time = 0
        self.event_queue = []
        self.trip_log = []
        self.num_cars = 0
        self.available_cars = []
        self.num_trips = 0
        self.max_trips = abs(args.max_trips)

    def schedule_event(self, event):
        #Add event to event queue
        heapq.heappush(self.event_queue, event)

    def generate_rider_request(self, timestamp):
        if (self.num_trips < self.max_trips):
            self.num_trips += 1
            rider = Rider.Rider((f"Rider-{self.num_trips}"), Quadtree.Point(random.uniform(0, 1000), random.uniform(0, 1000)), Quadtree.Point(random.uniform(0, 1000), random.uniform(0, 1000)))
            self.schedule_event(Event(timestamp, event_type='RIDE_REQUEST', data={'rider': rider, 'rider_id': rider.id, 'rider_location': rider.initial_location}))
            print(f"TIME: {self.current_time:.2f} - RIDE REQUEST SCHEDULED for {rider.id} \n    - Pickup Location: {rider.initial_location} - Destination: {rider.destination}.")

    def find_closest_car_quadtree(self, rider_location, quadtree):
        closest_point = {'dist_squared': float('inf'), 'point': None}
        quadtree.query(rider_location, closest_point)

        #if there is a closest point, return the associated car object
        if closest_point['point'] is not None:
            return closest_point['point'].data
        return None

    def calculate_travel_time(self, start_location, end_location):
        TRAVEL_SPEED_FACTOR = 5
        #start location coords
        x1 = start_location.x
        y1 = start_location.y
        #end location coords
        x2 = end_location.x
        y2 = end_location.y

        distance = abs(x1 - x2) + abs(y1 - y2)
        travel_time = distance*TRAVEL_SPEED_FACTOR

        return travel_time

    def find_nearest_vertex(self, point, graph):
        min_distance = float('inf')
        nearest_node = None

        for node_id, (node_x, node_y) in graph.node_coordinates.items():
            #calculate the distance from coords to node
            distance = math.sqrt((point.x - node_x) ** 2 + (point.y - node_y) ** 2)
            
            #if a closer node is found, update the min_distance and nearest_node variables
            if distance < min_distance:
                min_distance = distance
                nearest_node = node_id
    
        return nearest_node

    def handle_rider_request(self, event, quadtree, graph):
        #create local variables for working with event-specific data
        rider = event.data['rider']
        rider_id = event.data['rider_id']
        rider_location = event.data['rider_location']

        #update user on current status of simulation
        print(f"    Matching {rider_id} with the nearest available car.")
        #find the closest car to this event's rider's location, store it in assigned_car
        assigned_car = self.find_closest_car_quadtree(rider_location, quadtree)
        assigned_car.assigned_rider = rider #assign this rider to this assigned car
        assigned_car.status = "en_route_to_pickup" #update the assigned car's status

        #remove car's old quadtree point
        old_point = Quadtree.Point(assigned_car.location.x, assigned_car.location.y, assigned_car)
        quadtree.remove(old_point)

        #convert actual location to nearest node, call dijkstra's to find shortest path
        assigned_car.current_node = self.find_nearest_vertex(assigned_car.location, graph)
        rider_location = self.find_nearest_vertex(rider_location, graph)
        print(f"    {rider_id} is located at vertex {rider_location}. {assigned_car.id} is located at vertex {assigned_car.current_node}.")

        #update which car has been dispatched to which rider
        print(f"TIME: {self.current_time:.2f} - CAR DISPATCHED - {assigned_car.id} dispatched to {rider_id}, {assigned_car.status}")

        assigned_car.calculate_route(rider_location, graph)

        #Update user on simulation progress, calculate pickup duration
        pickup_duration = assigned_car.route_time
        print(f"    Rider wait time: {pickup_duration:.2f}")

        #schedule new event (add it to heap) for ARRIVAL factoring in the calculated pickup duration
        self.schedule_event(Event(timestamp=((self.current_time + pickup_duration)), event_type='ARRIVAL', data={'car': assigned_car, 'rider': assigned_car.assigned_rider}))

        #generate new RIDE REQUEST for later time
        next_request_time = self.current_time + random.expovariate(1.0)
        self.generate_rider_request(next_request_time)


    def handle_arrival(self, car, rider, quadtree, graph):
        if (car.status == "en_route_to_pickup"): #if arrival event is a PICKUP...
            #update status of both the car and the rider
            car.status = "en_route_to_destination"
            rider.status = "in_car" 
            rider.pickup_time = self.current_time

            #update console with current simulation event and time
            print(f"TIME: {self.current_time:.2f} - ARRIVAL -> PICKUP - {car.id} picked up {rider.id}, {car.status}")
            #update car's location to rider's initial location (pickup location)
            car.location = rider.initial_location

            #convert actual location to nearest node, call dijkstra's to find shortest path
            car.current_node = self.find_nearest_vertex(car.location, graph)
            rider.destination_node = self.find_nearest_vertex(rider.destination, graph)

            #calculate route from pickup location to destination
            car.calculate_route(rider.destination_node, graph)

            #calculate ride duration to rider's destination
            dropoff_duration = car.route_time
            print(f"    Ride duration until dropoff: {dropoff_duration:.2f}")


            #create ARRIVAL event for the DROPOFF, calling schedule_event will push it to the heap
            self.schedule_event(Event(timestamp=((self.current_time + dropoff_duration)), event_type='ARRIVAL', data={'car': car, 'rider': rider}))

        elif (car.status == "en_route_to_destination"): #if arrival is a DROPOFF
            #update console with current simulation event and time
            print(f"TIME: {self.current_time:.2f} - ARRIVAL -> DROPOFF - {car.id} dropped off {rider.id}")

            #update car's location to rider's destination location (dropoff location)
            car.location = rider.destination

            #add car's new point to the quadtree
            new_point = Quadtree.Point(car.location.x, car.location.y, car)
            quadtree.insert(new_point)

            rider.dropoff_time = self.current_time
            self.log_trip_data(rider)

            #update status of both the car and the rider
            car.status = "available"
            rider.status = "complete"
            #clear out assigned rider for this car
            car.assigned_rider = None

            print(f"    {rider.id}'s trip is {rider.status}. {car.id} is now {car.status} for another ride request.")


    def run(self):
        #Show simulation is starting through the console
        print("Beginning Simulation...")

        #load the map data from the file
        city_map = Graph.Graph()
        city_map.load_map_data('Final_Map_1000_Node_Grid.csv')

        #Set up the map boundary
        map_boundary = Quadtree.Rectangle(0, 0, 1000, 1000)
        quadtree = Quadtree.QuadtreeNode(map_boundary, capacity=4)

        #Add cars to map
        self.num_cars = 100

        for i in range(self.num_cars):
            car = Car.Car(f"Car-{i+1}", Quadtree.Point(random.uniform(0, 1000), random.uniform(0, 1000)))
            self.available_cars.append(car)
            car_point = Quadtree.Point(car.location.x, car.location.y, car)
            quadtree.insert(car_point)
            print(f"{car.id} created at {car.location}.")

        #generate a rider and request
        self.generate_rider_request(self.current_time)

        #Loop continues to run while events are available
        while self.event_queue:
            #Pop the next event with the smallest timestamp
            event = heapq.heappop(self.event_queue)

            #Move the clock forward
            self.current_time = event.timestamp

            # Process each event based on which event type it is
            if event.event_type == 'RIDE_REQUEST':
                self.handle_rider_request(event, quadtree, city_map)
            elif event.event_type == 'ARRIVAL':
                self.handle_arrival(event.data['car'], event.data['rider'], quadtree, city_map)

        print(f"\nEnd of Simulation. \n End Time: {self.current_time:.2f}")
    
    def log_trip_data(self, rider):
        trip_record = {
            'rider_id': rider.id,
            'request_time': rider.request_time,
            'pickup_time': rider.pickup_time,
            'dropoff_time': rider.dropoff_time,
            'wait_time': rider.pickup_time - rider.request_time,
            'trip_duration': rider.dropoff_time - rider.pickup_time
        }
        self.trip_log.append(trip_record)
        print(f"TIME: {self.current_time:.2f} - TRIP COMPLETED for {rider.id} - Data logged.")

    def analyze_results(self):
        if not self.trip_log:
            print("No trips were completed, no analysis to run.")
            return None
        
        print("Calculating Key Performance Indicators (KPIs)...")
        #calculate Key Performance Indicators (KPIs)
        total_wait_time = sum(trip['wait_time'] for trip in self.trip_log)
        total_trip_duration = sum(trip['trip_duration'] for trip in self.trip_log)

        total_time_on_trips = total_trip_duration
        total_potential_time = self.num_cars * self.current_time if self.num_cars > 0 else 0

        print("Compiling results...")

        #compile results into dictionary
        results = {
            "completed_trips": len(self.trip_log),
            "average_wait_time": total_wait_time / len(self.trip_log),
            "average_trip_duration": total_trip_duration / len(self.trip_log),
            "driver_utilization_percent": (total_time_on_trips / total_potential_time) * 100 if total_potential_time > 0 else 0
        }
                
        return results

    def create_simulation_summary(self, analysis_results):
        results = analysis_results

        #unzip car coords for plotting
        car_x = [car.location.x for car in self.available_cars]
        car_y = [car.location.y for car in self.available_cars]

        #create a figure and an axes object
        plt.figure(figsize=(8, 4))

        #create subplot space for text data
        plt.subplot(1, 2, 1)

        #plot cars as black squares
        plt.scatter(car_x, car_y, c='black', label='Car Locations', marker='o', s=100)

        #set plot boundaries, title and labels
        plt.xlim(0, 1000)
        plt.ylim(0, 1000)
        plt.title("Car Locations at End of Simulation")
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend() #Display the labels
        plt.grid(True) #Add grid for readability

        
        #Display formatted summary alongside plot
        plt.text(1100, 900, "--- Simulation Analysis ---")
        plt.text(1100, 800, f"Completed Trips: {results['completed_trips']}")
        plt.text(1100, 700, f"Average Rider Wait Time: {results['average_wait_time']:.2f} time units")
        plt.text(1100, 600, f"Average Trip Duration: {results['average_trip_duration']:.2f} time units")
        plt.text(1100, 500, f"Driver Utilization: {results['driver_utilization_percent']:.2f}%")
        plt.text(1100, 400, "---------------------------")

        #Save plot to a file
        plt.savefig("simulation_summary.png")
        print("Simulation summary information saved to 'simulation_summary.png'")


#Main execution block
if __name__ == "__main__":
    #create instance of a Simulation object
    sim = Simulation()

    #Start the simulation
    sim.run()

    sim.create_simulation_summary(sim.analyze_results())
