import os
import timeit
import logging
import sys
from typing import List

from TTPevaluate import get_experiment_solutions
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
        total_start_time = timeit.default_timer()
        for job in self.jobs:
            logging.debug(f'Executing job {job.run_tag}')
            start_time = timeit.default_timer()
            output_path = os.path.join(self.output_dir, job.algorithm_tag, job.problem_tag)
            job.execute(output_path=output_path)
            elapsed = timeit.default_timer() - start_time
            logging.debug(f'Finished job {job.run_tag} in {elapsed} seconds.')
        elapsed = timeit.default_timer() - total_start_time
        logging.debug(f'Finished all jobs in {elapsed} seconds.')

    def get_solutions(self):
        job_solutions = []
        for job in self.jobs:
            output_path = os.path.join(self.output_dir, job.algorithm_tag, job.problem_tag)
            experiment_name = job.run_tag
            job_solutions.append(get_experiment_solutions(output_path, experiment_name))
        return job_solutions


