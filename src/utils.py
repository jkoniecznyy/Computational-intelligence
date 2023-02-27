import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
from typing import List, Dict


class OverloadedVehicleException(Exception):
    """ Raised when the vehicle capacity is exceeded. """

    def __init__(self, route_number, generated_capacity, vehicle_capacity):
        self.msg = f'Route {route_number} capacity exceeded: {generated_capacity} > {vehicle_capacity}'

    def __str__(self):
        return self.msg


def create_random_route(points: List[List[int]]) -> List[int]:
    """ Returns random route through all the points, doesn't consider the needs."""
    route = []
    for i in range(len(points)):
        route.append(i)
    np.random.shuffle(route)
    return route


def calculate_random_route_score(route: List[int], distances: ndarray) -> float:
    """ Returns score of the random route."""
    result = 0
    for i in range(len(route) - 1):
        result += distances[route[i]][route[i + 1]]
    return result


def correct_best_route(route: Dict, length: int) -> Dict:
    """ Changes the starting point from Source to 0 and the ending point from Sink to length - 1."""
    for i in range(len(route)):
        for j in range(len(route[i])):
            if route[i][j] == 'Source':
                route[i][j] = 0
            if route[i][j] == 'Sink':
                route[i][j] = length - 1
    return route


def best_route_capacity_dict(route: Dict[int, int], points: List[List[int]], needs: Dict[int, int],
                             vehicle_capacity: int) -> Dict[int, int]:
    """
    Returns a dictionary with the capacity of each route.
    Raises an error if the capacity of any course does exceed the vehicle capacity.
    """
    route = correct_best_route(route, len(points))
    result = {}
    for i in range(len(route)):
        capacity = 0
        for j in range(1, len(route[i]) - 1):
            capacity += needs[route[i][j]]
        if capacity > vehicle_capacity:
            raise OverloadedVehicleException(i, capacity, vehicle_capacity)
        result[i] = capacity
    return result


def plot_points(points: List[List[int]]) -> None:
    """ Plots the points. """
    plt.figure()
    plt.title('Points')
    for i in range(len(points)):
        plt.plot(points[i][0], points[i][1], 'ro')
        plt.text(points[i][0], points[i][1], str(i))
    plt.show()


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
