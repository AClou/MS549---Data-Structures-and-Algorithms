class Simulation:
    def __init__(self, map_filename):
        cars = {Car.id: Car}
        riders = {Rider.id: Rider}

        self.map = Graph()
        self.map.load_map_from_file('map.csv')
        self.map.__str__()

'''
if __name__ == "__main__":
    map = Graph()
    map.load_map_from_file('map.csv')
    map.__str__()
'''