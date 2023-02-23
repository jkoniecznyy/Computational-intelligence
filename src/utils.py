import matplotlib.pyplot as plt


def correct_best_route(solution, length):
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if solution[i][j] == 'Source':
                solution[i][j] = 0
            if solution[i][j] == 'Sink':
                solution[i][j] = length - 1
    return solution


def best_route_capacity_check(route, points, needs):
    route = correct_best_route(route, len(points))
    capacity = []
    for i in range(len(route)):
        result = 0
        for j in range(1, len(route[i]) - 1):
            result += needs[route[i][j]]
        if result > 1000:
            print(f'Route {i} capacity exceeded: {result} > 1000')
        capacity.append(result)
    return capacity


def plot_random_route(points, route, score):
    plt.figure()
    plt.title(f'Random route: {score:.0f} km')
    for i in range(len(route) - 1):
        plt.plot([points[route[i]][0], points[route[i + 1]][0]], [points[route[i]][1], points[route[i + 1]][1]])
        plt.text(points[route[i]][0], points[route[i]][1], str(route[i]))
    plt.show()


def plot_best_route(points, route, score):
    route = correct_best_route(route, len(points))
    plt.figure()
    plt.title(f'Best route: {score:.0f} km')
    for i in range(len(route)):
        for j in range(len(route[i]) - 1):
            plt.plot([points[route[i][j]][0], points[route[i][j + 1]][0]],
                     [points[route[i][j]][1], points[route[i][j + 1]][1]])
            plt.text(points[route[i][j]][0], points[route[i][j]][1], str(route[i][j]))
    plt.show()
