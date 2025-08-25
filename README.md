# MS549---Data-Structures-and-Algorithms

Project Title: Ride Share Simulator

Purpose: Simulator of a ride share application to showcase the use of different data structures and algorithms. 
          Structures used are for making the simulation run efficiently, even as the data involved increases in scale.
          Algorithms used are for simplifying the development process and creating reusable code that will be less likely to break.

How to Run:
1. Install Python, if not already installed, on your computer.
	1.1 Visit https://www.python.org/downloads/
	1.2 During installation, check the option for "Add Python to PATH"
2. Open the Command Prompt (on Windows).
	2.1 Find the Directory containing the Python scripts, make sure all needed scripts 
		are in the same directory.
		Do this by entering 'cd' followed by the path of the directory.
			Ex: cd C:\Users\Bob\Desktop\PythonFiles
	2.2 Type the 'python' command, followed by the name of the desired script.
		Ex: python simulation_engine.py 5 -> this int is required: number of trips to simulate.
	2.3 Press Enter key to begin running the chosen script.
3. Enjoy!

Dependencies: None

Map Data Format: Comma-Separated-Values (.csv). Each start point (node) has a corresponding end point and weight (in minutes). Ex. A,B,3 


Updates: 

Car class includes Dijkstra's algorithm to find shortest path from a starting point to a destination. Graph class usable           outside of itself.
          Includes test script test_dijkstra.py to allow independent algorithm testing.

Quadtree Data Structure:
          Added to find the nearest point (driver) to a certain point (rider) efficiently by 
          repeatedly dividing the map data into manageable sections (nodes). This limits the
          needed search area by eliminating sections (nodes) that are already farther away from
          the point being queried.
          Reduces time to finding the answer to the nearest-neighbor search with O(logN) efficiency compared
          to a brute force method with O(N) efficiency.
          
Simulation Engine Prototype:
          Created prototype simulation engine to handle events (ride requests, arrivals) and logging of simulation
          actions. While events are available to process, the event information is used to find
          the closest car to a rider, calculating the distance between each car and the rider from a list of manually
          created cars, calculate trip time, and update the console as the simulation progresses. Requests are handled
          in the order of their time stamp (first in, first out) using a min-heap, so the rider to first request a ride
          gets taken care of before other requests that occurred afterward.

Analytics and Visualization
          Simulator compiles Key Performance Indicators retrieved during the simulation into a png image file.
          File includes locations of cars at the end of the simulation and a list of the KPI to the right, measuring
          how well the program performed in certain aspects.
          

Project developed by Aaron Cloutier
          For MS549 - Data Structures and Algorithms taught by Dr. B
