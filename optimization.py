import pygmo as pg
from pygmo import rosenbrock
import matplotlib.pyplot as plt
from optimizationProblem import optimizationProblem
from pygmo.core import de1220, algorithm, population



if __name__ == "__main__":

    allowedVariants = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                       18]  # Default [2, 3, 7, 10, 13, 14, 15, 16]

    # Initialize the problem
    problem = optimizationProblem()
    pgOptimizationProblem = pg.problem(problem)
    print(pgOptimizationProblem)

    # Initialize the algorithm
    algo = algorithm(de1220(gen=200, variant_adptv=2, allowed_variants=allowedVariants))
    algo.set_verbosity(1)

    # Run the algorithm
    pop = population(pgOptimizationProblem, 10**2)
    pop = algo.evolve(pop)

    # Take the results
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')
    uda = algo.extract(de1220)
    log = uda.get_log()

    best_fitness = pop.get_f()[pop.best_idx()]
    print(best_fitness)
