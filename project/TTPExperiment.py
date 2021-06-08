import os
import re
import timeit
import logging
import sys
from typing import List

from jmetal.core.solution import BinarySolution, PermutationSolution, CompositeSolution
from jmetal.lab.experiment import Job


class TTPExperiment:

    def __init__(self, output_dir: str, jobs: List[Job]):
        """ Run an experiment to execute a list of jobs.
        :param output_dir: Base directory where each job will save its results.
        :param jobs: List of Jobs (from :py:mod:`jmetal.util.laboratory)`) to be executed.
        """
        self.jobs = jobs
        self.output_dir = output_dir
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='[%(asctime)s] %(levelname)s - %(message)s')

    def run(self) -> None:

        for job in self.jobs:
            logging.debug(f'Executing job {job.run_tag}')
            start_time = timeit.default_timer()
            output_path = os.path.join(self.output_dir, job.algorithm_tag, job.problem_tag)
            job.execute(output_path=output_path)
            elapsed = timeit.default_timer() - start_time
            logging.debug(f'Finished job {job.run_tag} in {elapsed} seconds.')

    def get_solutions(self):
        job_solutions = []
        for job in self.jobs:
            output_path = os.path.join(self.output_dir, job.algorithm_tag, job.problem_tag)
            experiment_name = job.run_tag
            job_solutions.append(self.__get_experiment_solutions(output_path, experiment_name))
        return job_solutions

    def __get_experiment_solutions(self, dir, experiment_name):
        solutions = []
        with open(f'{dir}\\VAR.{experiment_name}.tsv') as f:
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

        with open(f'{dir}\\FUN.{experiment_name}.tsv') as f:
            line_idx = 0
            for line in f:
                objective_vals = line.strip().split(' ')
                if len(objective_vals) != 2:
                    break
                solutions[line_idx].objectives[0] = float(objective_vals[0])
                solutions[line_idx].objectives[1] = float(objective_vals[1])
                line_idx += 1
        return solutions
