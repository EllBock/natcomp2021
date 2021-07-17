import multiprocessing

import pygmo as pg
import numpy as np
import json


def writeXtoJson(x):


    META_parameters = {
        "METAclutchslip": 0,
        "METAsortofontrack": -2,
        "METAspincutslp": -1,
        "METAsxappropriatest2": -2,
        "METAsxappropriatest1": 0,
        "METAstst": 0,
        "METAs2cen": -2,
        "METAsteer2edge": -3,
        "METAbrake": -2,
        "METAupsh5rpm": -1,
        "METAupsh3rpm": -2,
        "METAbackontracksx": -1,
        "METAspincutclip": -1,
        "METAoksyp": 0,
        "METAupsh6rpm": 0,
        "METAsycon2": -3,
        "METAdnsh5rpm": -1,
        "METAcarmin": -1,
        "METAstC": 0,
        "METAslipdec": -2,
        "METAoffroad": -3,
        "METAsycon1": 0,
        "METAclutch_release": -3,
        "METAbrakingpacefast": -1,
        "METAclutchspin": -2,
        "METAdnsh2rpm": -2,
        "METAdnsh1rpm": -2,
        "METAcarmaxvisib": 0,
        "METAspincutint": 0,
        "METAs2sen": -1,
        "METAbrakingpaceslow": 0,
        "METAsyint": -3,
        "METAconsideredstr8": -2,
        "METAsensang": -2,
        "METAupsh2rpm": -2,
        "METAst": -2,
        "METAobvious": 0,
        "METAsenslim": -3,
        "METAupsh4rpm": -2,
        "METAstr8thresh": 0,
        "METAseriousABS": 0,
        "METAskidsev1": -1,
        "METAbackward": 0,
        "METAfullstmaxsx": -2,
        "METAsafeatanyspeed": 0,
        "METAfullstis": -1,
        "METAs2ang": -1,
        "METApointingahead": 0,
        "METAwheeldia": 0,
        "METAsyslp": 0,
        "METAwwlim": 0,
        "METAignoreinfleA": 0,
        "METAturnsetup": -1,
        "METAdnsh4rpm": -1,
        "METAaccinc": -2,
        "METAdnsh3rpm": -2,
        "METAobviousbase": -2,

    }


    parameters = json.dump(x)


def executeGame(new_default_parameter):
    pass


def computefitness():
    pass


class optimizationProblem:

    # Deve ritornare un vettore (anche se il risultato è uno scalare) contenente la funzione di fitness valutata
    # nel punto x ( numpy array) .
    def fitness(self, x):


        new_default_parameter = writeXtoJson(x)

        #3001
        first = multiprocessing.Process(target=executeGame, args=('forza.xml',))

        #3002
        second = multiprocessing.Process(target=executeGame, args=('forza.xml',))

        #3003
        third = multiprocessing.Process(target=executeGame, args=('forza.xml',))

        #3004
        fourth = multiprocessing.Process(target=executeGame, args=('forza.xml',))

        first.start()
        second.start()
        third.start()
        fourth.start()

        first.join()
        second.join()
        third.join()
        fourth.join()

        fitness = computefitness()

        return fitness

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