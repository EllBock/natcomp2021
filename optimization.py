import pygmo as pg
from pygmo import rosenbrock

from optimizationProblem import optimizationProblem
from pygmo.core import de1220, algorithm, population

allowedVariants = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

if __name__ == "__main__":

    # Initialize the problem
    problem = optimizationProblem()
    pgOptimizationProblem = pg.problem(problem)
    print(pgOptimizationProblem)

    # Initialize the algorithm
    algo = algorithm(de1220(gen=300, variant_adptv=2, allowed_variants=allowedVariants))
    algo.set_verbosity(200)

    # Run the algorithm
    pop = population(pgOptimizationProblem, 10**2)
    pop = algo.evolve(pop)

    # Take the results
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')



