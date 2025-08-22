# MS549---Data-Structures-and-Algorithms

Project Title: Ride Share Simulator

Purpose: Simulator of a ride share application to showcase the use of different data structures and algorithms. 
          Structures used are for making the simulation run efficiently, even as the data involved increases in scale.
          Algorithms used are for simplifying the development process and creating reusable code that will be less likely to break.

How to Run: Had issues here! Not sure about this part...

Dependencies: None

Map Data Format: Comma-Separated-Values (.csv). Each start point (node) has a corresponding end point and weight (in minutes). Ex. A,B,3 

Updates: Car class includes Dijkstra's algorithm to find shortest path from a starting point to a destination. Graph class usable outside of itself.
          Includes test script test_dijkstra.py to allow independent algorithm testing.

          Quadtree Data Structure:
                    Added to find the nearest point (driver) to a certain point (rider) efficiently by 
                              repeatedly dividing the map data into manageable sections (nodes). This limits the
                              needed search area by eliminating sections (nodes) that are already farther away from
                              the point being queried.
                    Reduces time to finding the answer to the nearest-neighbor search with O(logN) efficiency compared to a brute force method with O(N) efficiency.
          

Project developed by Aaron Cloutier
          For MS549 - Data Structures and Algorithms taught by Dr. B
