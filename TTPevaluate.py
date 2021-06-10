import os
import re
from typing import List
import numpy as np
import matplotlib.pyplot as plt

from jmetal.core.quality_indicator import HyperVolume
from jmetal.core.solution import BinarySolution, PermutationSolution, CompositeSolution
from jmetal.lab.visualization import Plot
from jmetal.util.solution import get_non_dominated_solutions


def get_experiment_names(path: str):
    names = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.startswith("VAR.") and entry.is_file():
                filename = entry.name[4:-4]
                names.append(filename)
    return names


def get_experiment_solutions(path: str, experiment_name: str, return_front: bool = False):
    solutions = []

    with open(os.path.join(path, f'VAR.{experiment_name}.tsv')) as f:
        for line in f:
            tour = []
            bitstring = []

            variables = re.findall(r"\[(.*?)\]", line)
            str_tour = variables[0]
            str_bitstring = variables[3]
            for word in str_tour.split(','):
                word = word.strip()
                tour.append(int(word))
            for word in str_bitstring.split(','):
                if 'True' in word:
                    bitstring.append(True)
                elif 'False' in word:
                    bitstring.append(False)
                else:
                    print('Error, no true or false found.')
            binary_solution = BinarySolution(number_of_variables=1, number_of_objectives=2)

            permutation_solution = PermutationSolution(number_of_variables=len(tour), number_of_objectives=2)
            binary_solution.variables = bitstring
            permutation_solution.variables = tour
            solution = CompositeSolution([permutation_solution, binary_solution])
            solutions.append(solution)

    with open(os.path.join(path, f'FUN.{experiment_name}.tsv')) as f:
        line_idx = 0
        for line in f:
            objective_vals = line.strip().split(' ')
            if len(objective_vals) != 2:
                break
            solutions[line_idx].objectives[0] = float(objective_vals[0])
            solutions[line_idx].objectives[1] = float(objective_vals[1])
            line_idx += 1

    if return_front:
        solutions = get_non_dominated_solutions(solutions)
    return solutions


def get_reference_point(fronts_objectives: List[List[float]]):
    reference_point = [0, 0]
    for front in fronts_objectives:
        for objective in front:
            reference_point[0] = max(objective[0], reference_point[0])
            reference_point[1] = max(objective[1], reference_point[1])
    return reference_point


def calculate_hypervolume(objectives: List[float], return_reference_point: bool = False):
    reference_point = get_reference_point(objectives)
    hv = HyperVolume(reference_point)
    hypervolumes = []
    for objective in objectives:
        hypervolumes.append(hv.compute(objective))
    if return_reference_point:
        return hypervolumes, reference_point
    else:
        return hypervolumes


def write_hypervolumes(path: str, names: List[str], hypervolumes: List[float], reference_point: List[float] = None):
    # We append in case there's already an existing file. The user will have to handle this.
    with open(os.path.join(path, 'hypervolumes.csv'), 'a') as f:
        if reference_point:
            f.write(f'r {reference_point}\n')
        for i in range(len(names)):
            f.write(f'{names[i]}, {hypervolumes[i]}\n')


def read_and_write_hypervolumes(path: str):
    names = get_experiment_names(path)
    fronts = []
    fronts_objectives = []
    for name in names:
        front_objectives = []
        front = get_experiment_solutions(path, name, return_front=True)
        fronts.append(front)
        for solution in front:
            front_objectives.append(solution.objectives)
        fronts_objectives.append(front_objectives)
    hypervolumes, reference_point = calculate_hypervolume(fronts_objectives, return_reference_point=True)
    write_hypervolumes(path, names, hypervolumes, reference_point)


def create_plots(path: str, run_nr: int = 1):
    names = get_experiment_names(path)
    fronts = []
    for name in names:
        front = get_experiment_solutions(path, name, return_front=True)
        for solution in front:
            solution.objectives[1] *= -1
        fronts.append(front)
        plot_front = Plot(title='Pareto front approximation', axis_labels=['tour length', 'value'])
        plot_front.plot(front, label=name, filename=os.path.join(path, name), format='png')

    # Combined scatter plot
    # Uses only one of the runs
    fig = plt.figure()
    for i in range(len(names)):
        name = names[i]
        if 'run' in name:
            if name[name.find('run')+3] != str(run_nr):
                continue
        front = fronts[i]
        points = np.zeros((len(front), 2))
        for j in range(len(front)):
            points[j, :] = front[j].objectives
        plt.scatter(points[:, 0], points[:, 1], s=6, label=name)
    fig.suptitle('Pareto front approximation')
    fig.legend(loc='lower right')
    plt.xlabel('tour length')
    plt.ylabel('value')
    plt.savefig(os.path.join(path, f'combined_run{run_nr}.png'), dpi=200)


def get_objectives(solutions: List[CompositeSolution]):
    objectives = []
    for solution in solutions:
        objectives.append(solution.objectives)
    return objectives
