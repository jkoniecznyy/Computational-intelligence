import numpy as np
from src.vehicle_routing_problem import vehicle_routing_problem

if __name__ == '__main__':
    # np.random.seed(14)
    # SIZE = 60
    SIZE = np.random.randint(low=400, high=600)
    # AMOUNT_OF_VEHICLES = 3
    AMOUNT_OF_VEHICLES = np.random.randint(low=3, high=6)
    LOAD_CAPACITY = 1000
    NEEDS_RANGE = (100, 200)
    TIME_LIMIT = 200
    USE_ALL_VEHICLES = True
    RANDOM_ROUTE = True
    print(f'Number of points: ', SIZE)
    print(f'Amount of vehicles: ', AMOUNT_OF_VEHICLES)
    best_score, best_route = vehicle_routing_problem(SIZE, AMOUNT_OF_VEHICLES, LOAD_CAPACITY, NEEDS_RANGE,
                                                     TIME_LIMIT, USE_ALL_VEHICLES, RANDOM_ROUTE)
    # print(f'best_route {best_score} : {best_route}')
