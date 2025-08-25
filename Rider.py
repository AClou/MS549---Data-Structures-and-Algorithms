class Rider:
    def __init__(self, rider_id, pickup_location, dropoff_location):
        self.id = rider_id
        self.initial_location = pickup_location
        self.destination = dropoff_location
        self.destination_node = None
        self.status = 'waiting'
        self.request_time = 0
        self.pickup_time = 0
        self.dropoff_time = 0