import gplearn
from gplearn import functions, fitness, genetic
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
np.random.seed(101110)
pd.set_option('display.expand_frame_repr', False)

depVar = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2,
          -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
yVar = [0.0000, -0.1629, -0.2624, -0.3129, -0.3264, -0.3125, -0.2784, -0.2289, -0.1664,
        -0.0909, 0.0, 0.1111, 0.2496, 0.4251, 0.6496, 0.9375, 1.3056, 1.7731, 2.3616, 3.0951, 4.0000]

popSize = 1000
noGens = 50
crossoverProb = 0.7
mutationProb = 0.0


# https://gplearn.readthedocs.io/en/stable/advanced.html#custom-functions
# Custom safe exponent function
def _protected_exponent(x1):
    with np.errstate(over='ignore'):
        return np.where(np.abs(x1) < 100, np.exp(x1), 0.)


exp = functions.make_function(function=_protected_exponent,
                              name='exp',
                              arity=1)


# https://gplearn.readthedocs.io/en/stable/advanced.html#custom-fitness
# Custom fitness function for - sum of absolute errors
def _nsae(true_y, pred_y, w):
    diffs = np.abs(true_y - pred_y)
    return -sum(diffs)


nsae = fitness.make_fitness(_nsae, greater_is_better=True)


# Run symbolic regression
def symbolicRegr(funcs):
    gpRun = genetic.SymbolicRegressor(population_size=popSize, generations=noGens, tournament_size=20,
                                      const_range=None, function_set=funcs, metric=nsae,
                                      p_crossover=crossoverProb, p_subtree_mutation=mutationProb,
                                      p_hoist_mutation=mutationProb, p_point_mutation=mutationProb, verbose=0)
    gpRun.fit(np.array(depVar).reshape(-1, 1), np.array(yVar))
    print(
        f'Expression: {gpRun._program}\nFitness: {gpRun._program.fitness_}\nLength: {gpRun._program.length_}')
    return gpRun


# Generate 10 solutions with different random states
def generateSolutions(funcs):
    genSolutions = []
    for i in range(10):
        print(f'Iteration {i+1}')
        regrRun = symbolicRegr(funcs)
        genSolutions.append(regrRun)
    return genSolutions


# Find best run
def findBestRun(runsList):
    bestF = -100
    for run in runsList:
        currentF = run._program.fitness_
        if (currentF > bestF):
            bestF = currentF
            bestRun = run
    print(
        f'Best solution\nExpression: {bestRun._program}\nFitness: {bestRun._program.fitness_}\nLength: {bestRun._program.length_}')
    return bestRun


# Get fitness, size and equation of top 15 individuals of last generation
# https://github.com/trevorstephens/gplearn/issues/47
def fitnessLastGen(regr_obj):
    ranking = pd.DataFrame(columns=['Fitness', 'Length', 'Equation'])
    lastGen = regr_obj.generations - 1
    for i in range(regr_obj.population_size):
        if(regr_obj._programs[lastGen][i] != None):
            ranking = ranking.append({'Fitness': regr_obj._programs[lastGen][i].fitness_,
                                      'Length': regr_obj._programs[lastGen][i].length_,
                                      'Equation': str(regr_obj._programs[lastGen][i])},
                                     ignore_index=True)

    print('Top 15 equations:')
    print(ranking.sort_values('Fitness', ascending=False)[:15])


# Plot ground truth and estimation
def plotResults(regr_obj):
    plt.figure(1)
    plt.plot(depVar, yVar, label='Truth')
    plt.plot(depVar, regr_obj.predict(
        np.array(depVar).reshape(-1, 1)), label='Solution')
    plt.legend()
    plt.xlabel('Dependent variable')
    plt.ylabel('Y variable')


# Plot size vs generation
def plotSize(regr_obj):
    plt.figure(2)
    bestSize = regr_obj.run_details_['best_length']
    plt.plot(range(noGens), bestSize)
    plt.xlabel('Generation')
    plt.ylabel('Size of best solution')


# Plot fitness vs generation
def plotFitness(regr_obj):
    plt.figure(3)
    bestFitness = regr_obj.run_details_['best_fitness']
    plt.plot(range(noGens), bestFitness)
    plt.xlabel('Generation')
    plt.ylabel('Fitness of best solution')


def main():
    functionList = ['add', 'sub', 'mul', 'log', exp, 'sin', 'cos', 'div']
    solutionList = generateSolutions(functionList)
    bestSolution = findBestRun(solutionList)
    # fitnessLastGen(bestSolution)
    plotResults(bestSolution)
    plotFitness(bestSolution)
    plotSize(bestSolution)
    plt.show()


if __name__ == "__main__":
    main()
