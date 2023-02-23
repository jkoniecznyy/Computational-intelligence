import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from vrpy import VehicleRoutingProblem


# np.random.seed(420)


def generate_starting_point():
    return [np.random.randint(low=40, high=60),
            np.random.randint(low=40, high=60)]


def generate_points(amount):
    staring_point = generate_starting_point()
    points = [staring_point]
    for i in range(amount):
        points.append([np.random.randint(low=0, high=100),
                       np.random.randint(low=0, high=100)])
    points.append(staring_point)
    return points


def calculate_distance_for_all_points(points):
    distances = np.zeros((len(points), len(points)))
    for i in range(len(points)):
        for j in range(len(points)):
            distances[i][j] = calculate_distance_for_one_point(points[i], points[j])
    return distances


def calculate_distance_for_one_point(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def correct_distances(distances):
    for i in range(len(distances)):
        distances[i][0] = 0
    for i in range(len(distances[0])):
        distances[-1][i] = 0
    return distances


def create_random_route(points):
    route = []
    for i in range(len(points)):
        route.append(i)
    np.random.shuffle(route)
    return route


def calculate_random_route_score(route, distances):
    result = 0
    for i in range(len(route) - 1):
        result += distances[route[i]][route[i + 1]]
    return result


def generate_needs(length):
    d = {}
    for i in range(1, length - 1):
        need = np.random.randint(low=100, high=200)
        d[i] = need
    return d


def correct_best_route(solution, length):
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if solution[i][j] == 'Source':
                solution[i][j] = 0
            if solution[i][j] == 'Sink':
                solution[i][j] = length - 1
    return solution


def plot_random_route(points, route, score):
    plt.figure()
    plt.title(f'Random route: {score:.2f}')
    for i in range(len(route) - 1):
        plt.plot([points[route[i]][0], points[route[i + 1]][0]], [points[route[i]][1], points[route[i + 1]][1]])
        plt.text(points[route[i]][0], points[route[i]][1], str(route[i]))
    plt.show()


def plot_best_route(points, route, score):
    route = correct_best_route(route, len(points))
    plt.figure()
    plt.title(f'Best route: {score:.2f}')
    for i in range(len(route)):
        for j in range(len(route[i]) - 1):
            plt.plot([points[route[i][j]][0], points[route[i][j + 1]][0]],
                     [points[route[i][j]][1], points[route[i][j + 1]][1]])
            plt.text(points[route[i][j]][0], points[route[i][j]][1], str(route[i][j]))
    plt.show()


# amount = np.random.randint(low=400, high=600)
size = 500
print(f'Number of points: ', size)
destinations = generate_points(size - 1)
# print(f'destinations: {destinations}')

distance_array = calculate_distance_for_all_points(destinations)
distance_array = correct_distances(distance_array)
# print(f'distance_array: {distance_array}')

random_route = create_random_route(destinations)
random_route_score = calculate_random_route_score(random_route, distance_array)

needs = generate_needs(len(destinations))
# print(f'needs: {needs}')

A = np.array(distance_array, dtype=[("cost", float)])
G = nx.from_numpy_array(A, create_using=nx.DiGraph())

nx.set_node_attributes(G, values=needs, name="demand")

G = nx.relabel_nodes(G, {0: "Source", len(destinations) - 1: "Sink"})

print('distance_np_array: ', A)
print('distance_DiGraph: ', G)
# print('G edges: ', G.edges(data=True))

# Create vrp
prob = VehicleRoutingProblem(G, load_capacity=1000)
prob.num_vehicles = 6
prob.use_all_vehicles = True

# Solve and display solution
# heuristic_only means the solution found by the Clarke and Wright algorithm.
prob.solve(heuristic_only=True, time_limit=300)

# prob.solve(time_limit=300)
# prob.solve(greedy=True, time_limit=3000)

print(f'random_route: ', random_route)
print('best route: ', prob.best_routes)

print(f'random_route_score: ', random_route_score)
print('best value: ', prob.best_value)
plot_random_route(destinations, random_route, random_route_score)
plot_best_route(destinations, prob.best_routes, prob.best_value)
