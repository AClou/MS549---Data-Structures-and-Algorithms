class Car:
    def __init__(self, car_id, initial_location):
        self.id = car_id
        self.location = initial_location
        self.status = 'available'
        self.destination = None

    def display_info(self):
        print(f"Car {self.id} is currently at {self.location}, and is {self.status}.")



if __name__ == "__main__":
    '''
    create car objects with unique values
    '''
    car1 = Car('CAR-01', (35, 62))
    car1.display_info()

    car2 = Car('CAR-02', (22.0215, 79.2546))
    car2.display_info()

    car3 = Car('CAR-03', (50, 50))
    car3.display_info()