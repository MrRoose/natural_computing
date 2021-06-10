from jmetal.algorithm.multiobjective import SPEA2
from jmetal.operator import NullCrossover
from jmetal.operator.crossover import PMXCrossover, CompositeCrossover, SPXCrossover
from jmetal.operator.mutation import PermutationSwapMutation, BitFlipMutation, CompositeMutation

from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.experiment import Job


from TTPExperiment import TTPExperiment
from TTPProblem import TTPProblem
from TTPevaluate import read_and_write_hypervolumes, create_plots


def configure_experiment(problem, n_runs=31):
    jobs = []
    max_evaluations = 10000

    for run in range(n_runs):
        jobs.append(
            Job(
                algorithm=SPEA2(
                    problem=problem,
                    population_size=500,
                    offspring_population_size=500,
                    mutation=CompositeMutation([PermutationSwapMutation(1.0 / problem.n_cities), BitFlipMutation(0.1)]),
                    crossover=CompositeCrossover([PMXCrossover(0.8), NullCrossover()]),
                    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                ),
                algorithm_tag='SPEA',
                problem_tag='TTP',
                run=f'NullCrossover_run{str(run)}',
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
                    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                ),
                algorithm_tag='SPEA',
                problem_tag='TTP',
                run=f'SPX-0,2_run{str(run)}',
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
                    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
                ),
                algorithm_tag='SPEA',
                problem_tag='TTP',
                run=f'SPX-0,8_run{str(run)}',
            )
        )

    return jobs


fn = 'eil51_n50_bounded-strongly-corr_01.ttp'
problem = TTPProblem(fn, dropping_rate=1, p_picking=0.05)
jobs = configure_experiment(problem=problem)
output_directory = 'experiments'
experiment = TTPExperiment(output_dir=output_directory, jobs=jobs)
experiment.run()
solutions = experiment.get_solutions()

read_and_write_hypervolumes('experiments/SPEA/TTP')
create_plots('experiments/SPEA/TTP')



