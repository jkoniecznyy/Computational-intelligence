# The purpose of this project is to solve the Vehicle Routing Problem

To do so, the program performs the following steps:

1. Generate a random set of points (x, y) 
2. Calculate the distance matrix
3. Generate a random set of needs for each point
4. Create a DiGraph from the distance matrix
5. Create a VRP problem from the DiGraph, with given vehicle capacity
6. Solve the VRP problem using the Clarke and Wright algorithm
7. Plot the solution
8. Create a random route through all the points and compare it to the solution

