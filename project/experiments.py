from jmetal.algorithm.multiobjective import SPEA2
from jmetal.core.quality_indicator import HyperVolume
from jmetal.lab.visualization import Plot
from jmetal.operator import NullCrossover
from jmetal.core.solution import BinarySolution, PermutationSolution, CompositeSolution
from jmetal.operator.crossover import PMXCrossover, CompositeCrossover, SPXCrossover
from jmetal.operator.mutation import PermutationSwapMutation, BitFlipMutation, CompositeMutation
from jmetal.util.solution import get_non_dominated_solutions

from jmetal.util.termination_criterion import StoppingByEvaluations, StoppingByTime
from jmetal.lab.experiment import Experiment, Job, generate_summary_from_experiment

import re
import timeit

from TTPExperiment import TTPExperiment
from TTPProblem import TTPProblem


def configure_experiment(problem):
    jobs = []
    max_seconds = 10800

    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), SPXCrossover(0.8)]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='SPX-0,8_run1',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), SPXCrossover(0.8)]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='SPX-0,8_run2',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), SPXCrossover(0.8)]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='SPX-0,8_run3',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), SPXCrossover(0.2)]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='SPX-0,2_run1',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), SPXCrossover(0.2)]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='SPX-0,2_run2',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), SPXCrossover(0.2)]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='SPX-0,2_run3',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), NullCrossover()]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='NullCrossover_run1',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), NullCrossover()]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='NullCrossover_run2',
        )
    )
    jobs.append(
        Job(
            algorithm=SPEA2(
                problem=problem,
                population_size=500,
                offspring_population_size=500,
                mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                crossover=CompositeCrossover([PMXCrossover(0.8), NullCrossover()]),
                termination_criterion=StoppingByTime(max_seconds=max_seconds)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='NullCrossover_run3',
        )
    )

    return jobs

fn = 'eil51_n50_bounded-strongly-corr_01.ttp'
problem = TTPProblem(fn, dropping_rate=1, p_picking=0.05)
jobs = configure_experiment(problem=problem)

# Run the study
output_directory = 'experiments'
experiment = TTPExperiment(output_dir=output_directory, jobs=jobs)
start_time = timeit.default_timer()
experiment.run()
elapsed = timeit.default_timer() - start_time
print(f'{elapsed} seconds for the 9 jobs')
solutions = experiment.get_solutions()




# solutions = get_TTPsolutions('experiments/SPEA/TTP/', 'SPX-0,8')
# front = get_non_dominated_solutions(solutions)
# hypervolume_qi = HyperVolume([1.0,1.0])
# print(hypervolume_qi.compute([solutions[i].objectives for i in range(len(solutions))]))
# for solution in front:
#     solution.objectives[1] *= -1
# plot_front = Plot(title='Pareto front approximation', axis_labels=['tour length', 'value'])
# plot_front.plot(front, label='Multiobjective TTP', filename='TTP', format='png')

