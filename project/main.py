from TTPProblem import TTPProblem

fn = 'eil51_n500_bounded-strongly-corr_01.ttp'

problem = TTPProblem(fn)
print(problem.node_distance(3, 5))