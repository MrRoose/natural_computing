import numpy as np
from abc import ABC, abstractmethod
from jmetal.core.problem import Problem
from jmetal.core.solution import BinarySolution, PermutationSolution, CompositeSolution

class TTPProblem(Problem[CompositeSolution], ABC):

    def __init__(self, instance: str = None, dropping_rate: float = 0.9, C: float = 10, p_picking: float = 0.25):
        super(TTPProblem, self).__init__()

        n_cities, n_items, capacity, min_speed, max_speed, renting_ratio, nodes, items, items_per_city = self.__read_from_file(instance)

        self.n_cities = n_cities
        self.n_items = n_items
        self.capacity = capacity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.renting_ratio = renting_ratio
        self.nodes = nodes
        self.items = items
        self.items_per_city = items_per_city

        self.dropping_rate = dropping_rate
        self.C = C
        self.p_picking = p_picking

        self.number_of_objectives = 2
        self.number_of_variables = n_cities
        self.directions = [self.MINIMIZE, self.MAXIMIZE]
        self.obj_labels = ['f(x,z)', 'g(x,z)']

    def __read_from_file(self, filename: str, sort: bool = False):

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
                        # NODE_NR, WEIGHT, PROFIT
                        items[item_idx, :] = np.array([int(item_arr[3])-1, int(item_arr[2]), int(item_arr[1])])

        if sort:
            items = np.sort(items, axis=0)  # Sort by node nr
        else:
            np.random.shuffle(items)

        n_items_per_city = np.zeros((n_cities,), dtype=np.uint16)  # No items in city 0
        for i in range(n_items):
            n_items_per_city[items[i, 0]] += 1
        max_items_per_city = n_items_per_city.max()
        # First col is the amount of items in the city
        items_per_city = np.zeros((n_cities, max_items_per_city + 1), dtype=np.uint16)
        items_per_city[:, 0] = n_items_per_city
        for city_idx in range(1, n_cities):
            items_in_city = np.ravel(np.argwhere(items[:, 0] == city_idx))
            items_per_city[city_idx, 1:len(items_in_city)+1] = items_in_city

        return n_cities, n_items, capacity, min_speed, max_speed, renting_ratio, nodes, items, items_per_city

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:

        tour_time = 0  # total tour time
        velocity = self.max_speed  # current velocity
        cur_weight = 0  # current weight
        time_and_value = np.zeros((self.n_cities - 1, 2))  # keep track of value and time spent in knapsack

        # A tour contains the integer 1, ..., n_cities-1
        # The first city (our starting city) is represented implicitly.
        tour = solution.variables[0].variables
        packing_list = solution.variables[1].variables[0]

        packing_list = self.repair_packing_list(packing_list)
        solution.variables[1].variables[0] = packing_list

        # City 0 to the first city
        tour_time += self.node_distance(0, tour[0]) / velocity

        for i in range(self.items_per_city[tour[0], 0]):
            item_idx = self.items_per_city[tour[0], i+1]
            if packing_list[item_idx]:
                cur_weight += self.items[item_idx, 1]
                time_and_value[0, 1] += self.items[item_idx, 2]

        velocity = self.calc_velocity(cur_weight)

        for i in range(0, self.n_cities-2):
            idx_city_1 = tour[i]
            idx_city_2 = tour[i+1]
            road_time = self.node_distance(idx_city_1, idx_city_2) / velocity
            time_and_value[0:i+1, 0] += road_time

            for j in range(self.items_per_city[idx_city_2, 0]):
                item_idx = self.items_per_city[idx_city_2, j + 1]
                if packing_list[item_idx]:
                    cur_weight += self.items[item_idx, 1]
                    time_and_value[i+1, 1] += self.items[item_idx, 2]

            velocity = self.calc_velocity(cur_weight)

        # Last city in tour to city 0
        road_time = self.node_distance(tour[-1], 0) / velocity
        tour_time += road_time
        time_and_value[:, 0] += road_time

        for i in range(self.items_per_city[tour[-1], 0]):
            item_idx = self.items_per_city[tour[-1], i + 1]
            if packing_list[item_idx]:
                cur_weight += self.items[item_idx, 1]
                time_and_value[-1, 1] += self.items[item_idx, 2]


        # Calculate g(x,z)
        # Renting rate
        final_value = np.subtract(np.sum(time_and_value[:, 1]), np.multiply(tour_time, self.renting_ratio))
        # Dropping rate
        #time_and_value[:, 0] = np.power(np.ones((self.n_cities - 1,)) * self.dropping_rate, np.floor(time_and_value[:, 0] / self.C))
        #final_value = np.sum(np.multiply(time_and_value[:,0], time_and_value[:,1]))

        # TODO: either we manually set the objectives of the two sub solutions or we use these two objectives for both solutions
        solution.objectives[0] = tour_time
        solution.objectives[1] = final_value

    def create_solution(self) -> CompositeSolution:
        binary_solution = BinarySolution(number_of_variables=1, number_of_objectives=2)

        permutation_solution = PermutationSolution(number_of_variables=self.n_cities, number_of_objectives=2)

        binary_solution.variables = \
            [np.random.choice([True, False], self.n_items, p=[self.p_picking, 1 - self.p_picking]).tolist()]
        permutation_solution.variables = np.random.permutation(np.arange(1, self.n_cities)).tolist()

        return CompositeSolution([permutation_solution, binary_solution])


    def get_name(self) -> str:
        return "TTP"

    def repair_packing_list(self, packing_list):
        # Repair mechanism: remove items from plan until capacity is no longer exceeded
        # Start with items at first city that have smallest profit:weight ratio
        total_weight = np.sum(np.multiply(packing_list, self.items[:, 1]))

        if total_weight > self.capacity:
            value_weight_ratio = self.items[:, 2] / self.items[:, 1]
            # Sort items by city idx then by weight:profit ratio
            items_sorted_idx = np.lexsort((value_weight_ratio, self.items[:, 0]))

            # Keep only items that we pack
            idx_isin = np.isin(items_sorted_idx, np.arange(self.n_items)[packing_list])
            items_sorted_idx = items_sorted_idx[idx_isin]

            to_remove_iterator = 0
            to_remove_weight = 0
            while to_remove_weight < (total_weight - self.capacity):
                to_remove_idx = items_sorted_idx[to_remove_iterator]
                to_remove_weight += self.items[to_remove_idx, 1]
                to_remove_iterator += 1
            packing_list_array = np.array(packing_list, dtype=np.bool)
            packing_list_array[items_sorted_idx[:to_remove_iterator]] = False
            packing_list = packing_list_array.tolist()
        return packing_list

    def node_distance(self, idx_node1, idx_node2):
        node1 = self.nodes[idx_node1, :]
        node2 = self.nodes[idx_node2, :]
        return np.linalg.norm(node1 - node2)

    def calc_velocity(self, cur_weight):
        #### TO DO
        if cur_weight > self.capacity:
            cur_weight = self.capacity
        return self.max_speed - cur_weight * (self.max_speed - self.min_speed)/self.capacity
