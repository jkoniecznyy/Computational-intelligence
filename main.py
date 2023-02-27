import numpy as np
from src.vehicle_routing_problem import clarke_and_wright

if __name__ == '__main__':
    POINTS_RANGE = (0, 100)
    POINTS_AMOUNT = np.random.randint(low=50, high=51)
    AMOUNT_OF_VEHICLES = np.random.randint(low=3, high=6)
    LOAD_CAPACITY = 1000
    NEEDS_RANGE = (100, 200)
    TIME_LIMIT = 300
    USE_ALL_VEHICLES = True
    RANDOM_ROUTE = False
    print(f'Amount of points: ', POINTS_AMOUNT)
    print(f'Amount of vehicles: ', AMOUNT_OF_VEHICLES)
    best_route, capacity, best_score = clarke_and_wright(POINTS_AMOUNT, AMOUNT_OF_VEHICLES, LOAD_CAPACITY,
                                                         POINTS_RANGE, NEEDS_RANGE, TIME_LIMIT,
                                                         USE_ALL_VEHICLES, RANDOM_ROUTE)
    print(f'Best Route = {best_route}')
    print(f'Capacity = {capacity}')
    print(f'Best Score = {best_score}')
