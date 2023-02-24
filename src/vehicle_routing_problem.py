import numpy as np
import networkx as nx
from typing import Tuple, List, Dict

from numpy import ndarray
from vrpy import VehicleRoutingProblem
from src.utils import plot_best_route, plot_random_route, best_route_capacity_check, \
    calculate_random_route_score, create_random_route


def generate_starting_point(low: int = 40, high: int = 60) -> List[int]:
    """ Returns starting point coordinates from given range."""
    return [np.random.randint(low=low, high=high),
            np.random.randint(low=low, high=high)]


def generate_points(amount: int = 400, low: int = 0, high: int = 100) -> List[List[int]]:
    """ Returns List of points from given range."""
    staring_point = generate_starting_point(int(high * 0.4), int(high * 0.6))
    points = [staring_point]
    for i in range(amount - 1):
        points.append([np.random.randint(low=low, high=high),
                       np.random.randint(low=low, high=high)])
    points.append(staring_point)
    return points


def generate_distance_array(points: List[List[int]]) -> ndarray:
    """ Returns array of distances between all points."""
    distance_array = np.zeros((len(points), len(points)))
    for i in range(len(points)):
        for j in range(len(points)):
            distance_array[i][j] = calculate_distance_between_points(points[i], points[j])
    return distance_array


def calculate_distance_between_points(point1: List[int], point2: List[int]) -> float:
    """ Returns distance between two points."""
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def prepare_distances_for_di_graph(distances: ndarray) -> ndarray:
    """ Deletes all edges coming to Source node and coming out of the Sink node."""
    for i in range(len(distances)):
        distances[i][0] = 0
    for i in range(len(distances[0])):
        distances[-1][i] = 0
    return distances


def generate_needs(length: int, low: int = 100, high: int = 200) -> Dict[int, int]:
    """ Returns Dictionary of needs for each point."""
    needs = {}
    for i in range(1, length - 1):
        need = np.random.randint(low=low, high=high)
        needs[i] = need
    return needs


def clarke_and_wright(points_amount: int, amount_of_vehicles: int, load_capacity: int,
                      points_range: Tuple[int, int], needs_range: Tuple[int, int], time_limit: int,
                      use_all_vehicles: bool, random_route: bool) -> List:
    """ Solves Vehicle Routing Problem and displays the best route."""
    # Prepare the data
    points = generate_points(points_amount, points_range[0], points_range[1])
    needs = generate_needs(len(points), needs_range[0], needs_range[1])
    distance_array = generate_distance_array(points)
    distance_array = prepare_distances_for_di_graph(distance_array)
    A = np.array(distance_array, dtype=[("cost", float)])
    G = nx.from_numpy_array(A, create_using=nx.DiGraph())
    nx.set_node_attributes(G, values=needs, name="demand")
    G = nx.relabel_nodes(G, {0: "Source", len(points) - 1: "Sink"})
    # Create VRP
    prob = VehicleRoutingProblem(G, load_capacity=load_capacity)
    prob.num_vehicles = amount_of_vehicles
    prob.use_all_vehicles = use_all_vehicles
    # Use the Clarke and Wright algorithm.
    prob.solve(heuristic_only=True, time_limit=time_limit)
    best_route = prob.best_routes
    best_score = prob.best_value
    # Check if the best route is viable and plot it
    best_route_capacity_check(best_route, points, needs, load_capacity)
    plot_best_route(best_route, points, best_score)
    # Plot random route and compare it to the best route
    if random_route:
        random_route = create_random_route(points)
        random_route_score = calculate_random_route_score(random_route, distance_array)
        plot_random_route(random_route, points, random_route_score)
        how_much_better = round(random_route_score * 100 / best_score, 0)
        print(f'Heuristic route score ({best_score:.0f}) is {how_much_better}% '
              f'better than random route score ({random_route_score:.0f})')
    return [best_route, best_score]
