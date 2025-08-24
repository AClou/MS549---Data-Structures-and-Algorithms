import Car
import Rider
import heapq
import time
import random
import math
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class Event:
    timestamp: int
    event_type: str
    data: Any = field(compare=False)

class Simulation:
    def __init__(self):
        self.current_time = 0
        self.event_queue = []

    def schedule_event(self, event):
        #Add event to event queue
        heapq.heappush(self.event_queue, event)

    def find_closest_car_brute_force(self, rider_location, available_cars):
        closest_car = None
        shortest_distance = float('inf')
        available_cars = available_cars

        #x coord is location tuple index [0], y coord is location tuple index [1]
        for car in available_cars:
            distance = (car.location[0] - rider_location[0])**2 + (car.location[1] - rider_location[1])**2
            if distance < shortest_distance:
                shortest_distance = distance
                closest_car = car
        return closest_car

    def calculate_travel_time(self, start_location, end_location):
        TRAVEL_SPEED_FACTOR = 5
        #start location tuple indexes
        x1 = start_location[0]
        y1 = start_location[1]
        #end location tuple indexes
        x2 = end_location[0]
        y2 = end_location[1]

        distance = abs(x1 - x2) + abs(y1 - y2)
        travel_time = distance*TRAVEL_SPEED_FACTOR

        return travel_time

    def handle_rider_request(self, event):
        #create local variables for working with event-specific data
        rider = event.data['rider']
        rider_id = event.data['rider_id']
        rider_location = event.data['rider_location']

        #update user on current status of simulation
        print(f"    Matching {rider_id} with the nearest available car.")
        #find the closest car to this event's rider's location, store it in assigned_car
        assigned_car = self.find_closest_car_brute_force(rider_location, available_cars)
        assigned_car.assigned_rider = rider #assign this rider to this assigned car
        assigned_car.status = "en_route_to_pickup" #update the assigned car's status

        #update user via console message which car is closest and that the car has been assigned
        print(f"    Closest car to {rider_id} at {rider_location} is: {assigned_car.id} at {assigned_car.location}.")
        print(f"    {assigned_car.id} has been assigned {rider_id}. {assigned_car.id} is now {assigned_car.status}.")

        #Update user on simulation progress, calculate pickup duration
        print(f"    Calculating pickup duration...")
        pickup_duration = self.calculate_travel_time(assigned_car.location, rider_location)
        print(f"    Duration of pickup is: {pickup_duration}")

        #schedule new event (add it to heap) for ARRIVAL factoring in the calculated pickup duration
        self.schedule_event(Event(timestamp=((self.current_time + pickup_duration)), event_type='ARRIVAL', data={'car': assigned_car, 'rider': assigned_car.assigned_rider}))

        #update simulation progress to console
        print(f"Time {self.current_time:03d}: {assigned_car.id} dispatched to {rider_id}")

    def handle_arrival(self, car, rider):
        if (car.status == "en_route_to_pickup"): #if arrival event is a PICKUP...
            #update console with current simulation event and time
            print(f"Time {self.current_time:03d}: {car.id} picked up {rider.id}")
            #update car's location to rider's initial location (pickup location)
            car.location = rider.initial_location
            #update status of both the car and the rider
            car.status = "en_route_to_destination"
            rider.status = "in_car" 

            #calculate ride duration to rider's destination
            print(f"    Calculating ride duration to {rider.id}'s destination...")
            dropoff_duration = self.calculate_travel_time(car.location, rider.destination)
            print(f"    Ride duration until dropoff: {dropoff_duration}")


            #create ARRIVAL event for the DROPOFF, calling schedule_event will push it to the heap
            self.schedule_event(Event(timestamp=((self.current_time + dropoff_duration)), event_type='ARRIVAL', data={'car': car, 'rider': rider}))

        elif (car.status == "en_route_to_destination"): #if arrival is a DROPOFF
            #update console with current simulation event and time
            print(f"Time {self.current_time:03d}: {car.id} dropped off {rider.id}")
            #update car's location to rider's destination location (dropoff location)
            car.location = rider.destination
            #update status of both the car and the rider
            car.status = "available"
            rider.status = "complete"
            #clear out assigned rider for this car
            car.assigned_rider = None

            print(f"    {rider.id}'s trip is {rider.status}. {car.id} is now {car.status} for another ride request.")



    def run(self):
        #Show simulation is starting through the console
        print("Beginning Simulation...")

        #Loop continues to run while events are available
        while self.event_queue:
            #Pop the next event with the smallest timestamp
            event = heapq.heappop(self.event_queue)

            #Move the clock forward
            self.current_time = event.timestamp

            #Print current event information to console, showing it is working
            print(f"Time {self.current_time:03d}: Current event: {event.event_type} - More Info: {event.data}")

            # Process each event based on which event type it is
            if event.event_type == 'RIDE_REQUEST':
                self.handle_rider_request(event)
            elif event.event_type == 'ARRIVAL':
                self.handle_arrival(event.data['car'], event.data['rider'])

        print(f"\nEnd of Simulation. \n End Time: {self.current_time}")


#Main execution block
if __name__ == "__main__":
    sim = Simulation()

    #Riders
    rider1 = Rider.Rider('RIDER-01', (75, 43), (10, 64))
    rider2 = Rider.Rider('RIDER-02', (33, 25), (87, 66))
    rider3 = Rider.Rider('RIDER-03', (0,0), (15, 23))

    #Available cars list
    car1 = Car.Car('CAR-01', (35, 62))
    car2 = Car.Car('CAR-02', (22, 79))
    car3 = Car.Car('CAR-03', (50, 50))
    car4 = Car.Car('CAR-04', (70, 65))
    car5 = Car.Car('CAR-05', (0, 0))

    available_cars = {car1, car2, car3, car4, car5}

    #placeholder RIDE_REQUEST events
    sim.schedule_event(Event(timestamp=5, event_type='RIDE_REQUEST', data={'rider': rider1, 'rider_id': rider1.id, 'rider_location': rider1.initial_location}))
    sim.schedule_event(Event(timestamp=2, event_type='RIDE_REQUEST', data={'rider': rider2, 'rider_id': rider2.id, 'rider_location': rider2.initial_location}))
    sim.schedule_event(Event(timestamp=8, event_type='RIDE_REQUEST', data={'rider': rider3, 'rider_id': rider3.id, 'rider_location': rider3.initial_location}))


    #Start the simulation
    sim.run()