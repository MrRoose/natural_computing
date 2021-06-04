from jmetal.algorithm.multiobjective import SPEA2
from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.operator import NullCrossover, BinaryTournamentSelection
from jmetal.operator.crossover import PMXCrossover, CompositeCrossover, SPXCrossover
from jmetal.operator.mutation import PermutationSwapMutation, BitFlipMutation, CompositeMutation
from jmetal.problem.singleobjective.knapsack import Knapsack
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations

from TTPProblem import TTPProblem
import numpy as np

fn = 'eil51_n500_bounded-strongly-corr_01.ttp'

problem = TTPProblem(fn)
mutation_TSP = PermutationSwapMutation(1.0 / problem.n_cities)
mutation_KP = BitFlipMutation(np.sqrt(1.0 / problem.n_items))
mutation_TTP = CompositeMutation([mutation_TSP, mutation_KP])
crossover_TSP = PMXCrossover(0.8)
crossover_KP = SPXCrossover(0.8)
crossover_TTP = CompositeCrossover([crossover_TSP, crossover_KP])

max_evaluations = 20000
algorithm = SPEA2(
    problem=problem,
    population_size=200,
    offspring_population_size=200,
    mutation=mutation_TTP,
    crossover=crossover_TTP,
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
)

algorithm.run()
front = get_non_dominated_solutions(algorithm.get_result())
from jmetal.lab.visualization import Plot

plot_front = Plot(title='Pareto front approximation', axis_labels=['x', 'y'])
plot_front.plot(front, label='NSGAII-ZDT1', filename='NSGAII-ZDT1', format='png')
# problem = Knapsack(from_file=True, filename='KnapsackInstance_50_0_0.kp')
#
# algorithm = GeneticAlgorithm(
#     problem=problem,
#     population_size=100,
#     offspring_population_size=1,
#     mutation=BitFlipMutation(probability=0.1),
#     crossover=SPXCrossover(probability=0.8),
#     selection=BinaryTournamentSelection(),
#     termination_criterion=StoppingByEvaluations(max_evaluations=25000)
# )
#
# algorithm.run()
# subset = algorithm.get_result()
