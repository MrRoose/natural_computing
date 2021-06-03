import numpy as np
from abc import ABC, abstractmethod
from jmetal.core.problem import Problem
from jmetal.core.solution import BinarySolution, PermutationSolution, CompositeSolution

class TTPProblem(Problem[CompositeSolution], ABC):

    def __init__(self, instance: str = None, dropping_rate: float = 0.9):
        super(TTPProblem, self).__init__()

        n_cities, n_items, capacity, min_speed, max_speed, renting_ratio, nodes, items, items_start_idxs = self.__read_from_file(instance)

        self.n_cities = n_cities
        self.n_items = n_items
        self.capacity = capacity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.renting_ratio = renting_ratio
        self.dropping_rate = dropping_rate
        self.nodes = nodes
        self.items = items

        self.items_start_idxs = items_start_idxs


    def __read_from_file(self, filename: str):

        if filename is None:
            raise FileNotFoundError('Filename can not be None')

        with open(filename, 'r') as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('DIMENSION'):
                    n_cities = int(line.split('\t')[1])
                    nodes = np.zeros((n_cities, 2), int)
                elif line.startswith('NUMBER OF ITEMS:'):
                    n_items = int(line.split('\t')[1])
                    items = np.zeros((n_items, 3), int)
                elif line.startswith('CAPACITY OF KNAPSACK:'):
                    capacity = int(line.split('\t')[1])
                elif line.startswith('MIN SPEED:'):
                    min_speed = float(line.split('\t')[1])
                elif line.startswith('MAX SPEED:'):
                    max_speed = float(line.split('\t')[1])
                elif line.startswith('RENTING RATIO:'):
                    renting_ratio = float(line.split('\t')[1])
                elif line.startswith('NODE_COORD_SECTION'):
                    # Note that we index cities not by their original index in the file, but by INDEX-1
                    for city_idx in range(n_cities):
                        city_line = f.readline().rstrip()
                        city_arr = city_line.split('\t')
                        nodes[city_idx, :] = np.array([int(city_arr[1]), int(city_arr[2])])  # X, Y
                elif line.startswith('ITEMS SECTION'):
                    for item_idx in range(n_items):
                        item_line = f.readline().rstrip()
                        item_arr = item_line.split('\t')
                        # NODE_NR, WEIGHT, PROFIT, P:W RATIO
                        items[item_idx, :] = np.array([int(item_arr[3])-1, int(item_arr[2]), int(item_arr[1]), int(item_arr[1]/item_arr[2])])

        items = np.sort(items, axis=0)  # Sort by node nr

        items_start_idxs = np.zeros((n_cities,), dtype=np.int16) - 1
        for city_idx in range(1, n_cities):
            city_idxs = np.argwhere(items[:, 0] == city_idx)
            if city_idxs.size != 0:
                items_start_idxs[city_idx] = city_idxs[0]

        return n_cities, n_items, capacity, min_speed, max_speed, renting_ratio, nodes, items, items_start_idxs

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:

        tour_time = 0  # total tour time
        velocity = self.max_speed  # current velocity
        weight = 0 # current weight
        time_and_value = np.zeros((self.n_cities - 1, 2))

        # A tour contains the integer 1, ..., n_cities-1
        # The first city (our starting city) is represented implicitly.
        tour = solution.variables[0]
        packing_list = solution.variables[1]

        tour_time += self.node_distance(0, tour[0]) / velocity
        time_and_value[0, 0] = tour_time
        start_idx_city = self.items_start_idxs[1]
        end_idx_city = self.items_start_idxs[2]
        
        for item_idx in range(start_idx_city, end_idx_city):
            if packing_list[item_idx]:
                weight += self.items[item_idx, 1]
                time_and_value[0, 1] += self.items[item_idx, 2]

        # Repair mechanism: remove items from plan until capacity is no longer exceeded
        # Start with items at first city that have smallest profit:weight ratio
        if weight > self.capacity:
            # Sort items by city idx then by weight:profit ratio
            items_sorted_idx = np.lexsort((self.items[:, 3], self.items[:, 0]))
            packing_sorted = packing_list[items_sorted_idx]
            for idx, item in enumerate(packing_sorted):
                if item:
                    packing_list[items_sorted_idx[idx]] = 0
                    weight = weight - self.items[items_sorted_idx[idx], 1]
                    if weight <= self.capacity:
                        break

        for i in range(len(tour) - 1):
            pass

    def create_solution(self) -> CompositeSolution:
        return None

    def get_name(self) -> str:
        return "TTP"

    def node_distance(self, idx_node1, idx_node2):
        node1 = self.nodes[idx_node1, :]
        node2 = self.nodes[idx_node2, :]
        return np.linalg.norm(node1 - node2)
