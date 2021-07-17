import pygmo as pg
import numpy as np


class optimizationProblem:

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):
        return [sum(x * x)]

    # Deve ritornare una coppia di np array contenente il minimo e massimo valore che i parametri possono assumere
    # I due array sono ordinati rispetto all'ordine dei parametri passati alla funzione di fitness.
    # The problem dimension will be inferred by the return value of the get_bounds function.
    def get_bounds(self):
        return ([-1, -1], [1, 1])

    ############# Altri metodi sono opzionali



if __name__ == "__main__":

    problem = optimizationProblem()
    pgOptimizationProblem = pg.problem(problem)
    print(problem)