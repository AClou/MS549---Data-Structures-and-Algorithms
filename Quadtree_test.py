#Quadtree Test Script

import Quadtree
import time
import math
import random

def brute_force_closest_search(query_rider, all_drivers):
        best_driver = None
        min_dist_sq = float('inf')
        for d in all_drivers:
            dist_sq = (d.x - query_rider.x)**2 + (d.y - query_rider.y)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                best_driver = d
        return best_driver, min_dist_sq


#Main Execution Block
if __name__ == "__main__":

    #Set up the map
    map_boundary = Quadtree.Rectangle(0, 0, 1000, 1000)
    quadtree = Quadtree.QuadtreeNode(map_boundary, capacity=4)

    #Add drivers to map
    num_drivers = 5000
    drivers = [Quadtree.Point(random.uniform(0, 1000), random.uniform(0, 1000), f"Driver-{i}") for i in range(num_drivers)]
    for d in drivers:
        quadtree.insert(d)

    #Create a rider
    query_rider = Quadtree.Point(613, 609, "Rider")

    print(f"Looking for nearest driver to rider at {query_rider} among {num_drivers} total drivers.\n")

    #Search using a quadtree
    start_time_quadtree = time.perf_counter()

    best_found_quadtree = {'dist_squared': float('inf'), 'point': None}
    quadtree.query(query_rider, best_found_quadtree)

    end_time_quadtree = time.perf_counter()
    elapsed_quadtree = (end_time_quadtree - start_time_quadtree) * 1000

    print(f"Quadtree search results: {best_found_quadtree['point']} at distance {math.sqrt(best_found_quadtree['dist_squared']):.2f}")
    print(f"Time: {elapsed_quadtree:.6f} ms\n")

    #search using brute force
    start_time_bruteforce = time.perf_counter()

    best_point_bruteforce, best_dist_sq_bruteforce = brute_force_closest_search(query_rider, drivers)

    end_time_bruteforce = time.perf_counter()
    elapsed_bruteforce = (end_time_bruteforce - start_time_bruteforce) * 1000

    print(f"Brute Force search results: {best_point_bruteforce} at distance {math.sqrt(best_dist_sq_bruteforce):.2f}")
    print(f"Time: {elapsed_bruteforce:.6f} ms\n")

    # Compare the resulting times of the two different methods
    print(f"Quadtree-based search was {elapsed_bruteforce / elapsed_quadtree:.2f}x faster than the brute force method.")