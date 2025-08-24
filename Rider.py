class Rider:
    def __init__(self, rider_id, pickup_location, dropoff_location):
        self.id = rider_id
        self.initial_location = pickup_location
        self.destination = dropoff_location
        self.status = 'waiting'

    def display_info(self):
        print(f"{self.id} is currently at {self.initial_location} and is {self.status} for pickup. Destination is set for {self.destination}.")

'''
if __name__ == "__main__":

    #create rider objects with unique values
    
    rider1 = Rider('RIDER-01', (75.1235, -43.2235), (105.9584, 64.2435))
    rider1.display_info()

    rider2 = Rider('RIDER-02', (33, 25), (87, -66))
    rider2.display_info()
'''