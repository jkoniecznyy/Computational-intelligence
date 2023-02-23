import numpy as np
import networkx as nx
from typing import Tuple, List, Dict

from numpy import ndarray
from vrpy import VehicleRoutingProblem
from src.utils import plot_best_route, plot_random_route, best_route_capacity_check


def generate_starting_point(low: int = 40, high: int = 60) -> List[int]:
    """ Returns starting point coordinates from given range."""
    return [np.random.randint(low=low, high=high),
            np.random.randint(low=low, high=high)]


def generate_points(amount: int = 100, low: int = 0, high: int = 100) -> List[List[int]]:
    """ Returns List of points from given range."""
    staring_point = generate_starting_point()
    points = [staring_point]
    for i in range(amount):
        points.append([np.random.randint(low=low, high=high),
                       np.random.randint(low=low, high=high)])
    points.append(staring_point)
    return points


def calculate_distance_for_all_points(points: List[List[int]]) -> ndarray:
    """ Returns array of distances between all points."""
    distances = np.zeros((len(points), len(points)))
    for i in range(len(points)):
        for j in range(len(points)):
            distances[i][j] = calculate_distance_for_one_point(points[i], points[j])
    return distances


def calculate_distance_for_one_point(point1: List[int], point2: List[int]) -> float:
    """ Returns distance between two points."""
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def prepare_distances_for_di_graph(distances: ndarray) -> ndarray:
    """ Deletes all edges coming to Source node and coming out of the Sink node."""
    for i in range(len(distances)):
        distances[i][0] = 0
    for i in range(len(distances[0])):
        distances[-1][i] = 0
    return distances


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


def generate_needs(length: int, low: int = 100, high: int = 200) -> Dict[int, int]:
    """ Returns Dictionary of needs for each point."""
    d = {}
    for i in range(1, length - 1):
        need = np.random.randint(low=low, high=high)
        d[i] = need
    return d


def vehicle_routing_problem(size: int, amount_of_vehicles: int, load_capacity: int,
                            needs_range: Tuple[int, int], time_limit: int,
                            use_all_vehicles: bool, random_route: bool):
    points = generate_points(size - 1)
    # print(f'points: {points}')

    distance_array = calculate_distance_for_all_points(points)
    distance_array = prepare_distances_for_di_graph(distance_array)
    # print(f'distance_array: {distance_array}')

    needs = generate_needs(len(points), needs_range[0], needs_range[1])
    # print(f'needs: {needs}')

    A = np.array(distance_array, dtype=[("cost", float)])
    G = nx.from_numpy_array(A, create_using=nx.DiGraph())
    nx.set_node_attributes(G, values=needs, name="demand")
    G = nx.relabel_nodes(G, {0: "Source", len(points) - 1: "Sink"})
    # print('distance_DiGraph: ', G)
    # print('G edges: ', G.edges(data=True))

    # Create vrp
    prob = VehicleRoutingProblem(G, load_capacity=load_capacity)
    prob.num_vehicles = amount_of_vehicles
    prob.use_all_vehicles = use_all_vehicles

    # Solve and display solution
    # prob.solve(time_limit=300)
    # prob.solve(greedy=True, time_limit=3000)

    # heuristic_only means the solution found by the Clarke and Wright algorithm.
    prob.solve(heuristic_only=True, time_limit=time_limit)
    best_route = prob.best_routes
    best_score = prob.best_value

    # print(f'best_route {best_score} : {best_route}')
    capacity_check = best_route_capacity_check(best_route, points, needs)
    # print('capacity check: ', capacity_check)
    plot_best_route(points, best_route, best_score)

    if random_route:
        random_route = create_random_route(points)
        random_route_score = calculate_random_route_score(random_route, distance_array)
        # print(f'random_route: {random_route_score} : {random_route}')
        plot_random_route(points, random_route, random_route_score)
        how_much_better = round(random_route_score * 100 / best_score, 0)
        print(f'Best score: {best_score:.0f} is {how_much_better}% '
              f'better than random_route score: {random_route_score:.0f}')
