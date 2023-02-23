import matplotlib.pyplot as plt
from typing import List, Dict


def correct_best_route(route: Dict, length: int) -> Dict:
    """ Corrects the best route to be able to plot it."""
    for i in range(len(route)):
        for j in range(len(route[i])):
            if route[i][j] == 'Source':
                route[i][j] = 0
            if route[i][j] == 'Sink':
                route[i][j] = length - 1
    return route


def best_route_capacity_check(route: Dict[int, int], points: List[List[int]], needs: Dict[int, int],
                              vehicle_capacity: int) -> List:
    """ Checks if the capacity of every course does not exceed the vehicle capacity."""
    route = correct_best_route(route, len(points))
    all_capacities = []
    for i in range(len(route)):
        capacity = 0
        for j in range(1, len(route[i]) - 1):
            capacity += needs[route[i][j]]
        if capacity > vehicle_capacity:
            print(f'Route {i} capacity exceeded: {capacity} > {vehicle_capacity}')
        all_capacities.append(capacity)
    return all_capacities


def plot_random_route(route: List[int], points: List[List[int]], score: float) -> None:
    """ Plots the random route. """
    plt.figure()
    plt.title(f'Random route: {score:.0f} km')
    for i in range(len(route) - 1):
        plt.plot([points[route[i]][0], points[route[i + 1]][0]], [points[route[i]][1], points[route[i + 1]][1]])
        plt.text(points[route[i]][0], points[route[i]][1], str(route[i]))
    plt.show()


def plot_best_route(route: Dict[int, int], points: List[List[int]], score: float) -> None:
    """ Plots the best route. """
    route = correct_best_route(route, len(points))
    plt.figure()
    plt.title(f'Best route: {score:.0f} km')
    for i in range(len(route)):
        for j in range(len(route[i]) - 1):
            plt.plot([points[route[i][j]][0], points[route[i][j + 1]][0]],
                     [points[route[i][j]][1], points[route[i][j + 1]][1]])
            plt.text(points[route[i][j]][0], points[route[i][j]][1], str(route[i][j]))
    plt.show()
