from jmetal.algorithm.multiobjective import SPEA2
from jmetal.operator import NullCrossover, BinaryTournamentSelection
from jmetal.operator.crossover import PMXCrossover, CompositeCrossover, SPXCrossover
from jmetal.operator.mutation import PermutationSwapMutation, BitFlipMutation, CompositeMutation

from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.experiment import Experiment, Job, generate_summary_from_experiment


from TTPProblem import TTPProblem

def configure_experiment(problem):
    jobs = []
    max_evaluations = 500000

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
            run='SPX-0,8',
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
            run='SPX-0,2',
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
                termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
            ),
            algorithm_tag='SPEA',
            problem_tag='TTP',
            run='NullCrossover',
        )
    )

    return jobs

fn = 'eil51_n50_bounded-strongly-corr_01.ttp'
problem = TTPProblem(fn, dropping_rate=1, p_picking=0.05)
jobs = configure_experiment(problem=problem)

# Run the study
output_directory = 'experiments'
experiment = Experiment(output_dir=output_directory, jobs=jobs)
experiment.run()
