# Code from the Computational Intelligence classes
## The purpose of this program is to solve the Vehicle Routing Problem using the Clarke and Wright algorithm

To do so, the program performs the following steps:
1. Generate a set of random 2D points from a given range 
2. Generate a random quantity of needs for each point
3. Calculate the distance matrix
4. Create a DiGraph from the distance matrix
5. Create a VRP problem, with given vehicle capacity
6. Solve the VRP problem using the Clarke and Wright algorithm
7. Check if none of the vehicles was overloaded
8. Plot the best route you have found
9. Create a random route through all the points and compare it to the best route (optional) 

## Features:
- You can choose the number of points and the range of their coordinates
- There is only one magazine, which is the first point in the list
- The coordinates of the magazine are generated somewhere in the middle of the standard points range
- You can choose the needs range
- You can choose the vehicle capacity and the number of vehicles
- You can choose the time limit for the algorithm
- You can choose to use all the vehicles or only the ones that are needed
- If any of the vehicles is overloaded, the program will raise an exception
- You can choose to create a random route through all the points and compare it to the solution

### An example can be found in the results folder