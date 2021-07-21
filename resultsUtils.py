import os.path
import pickle
import matplotlib.pyplot as plt
from pygmo import de1220

''' savedDictionary['log'] = log
    savedDictionary['pop'] = pop
    parametersdict = dict(zip(parameters, pop.champion_x))
    parametersdict.update(notOptimzedParameters)
    savedDictionary['best_parameters'] = parametersdict
    jsonPath = os.path.join(resultsPath, "champion.json")
    writeXtoJson(pop.champion_x, filename=jsonPath)
    savedDictionary['pupulationSize'] = populationSize
    savedDictionary['numberOfGenerations'] = numberOfGenerations
    savedDictionary['alfa'] = problem.alfa
    savedDictionary['beta'] = problem.beta'''

def takeResultsFromDirectory(directoryPath, numOfFiles):

    fitnessValues = []
    iterations = range(1, numOfFiles +1)

    for i in iterations:
        filePath = os.path.join(directoryPath,'resultsGeneration_'+str(i)+".pickle")

        with (open(filePath, "rb")) as openfile:
            results = pickle.load(openfile)

        algo = results['algorithm']
        uda = algo.extract(de1220)
        log = uda.get_log()
        fitnessValues.append(log[0][2])



def readPickleFile(filepath):

    with (open(filepath, "rb")) as openfile:
        result = pickle.load(openfile)

    return result

def printResultsFromDirectory(directoryPath, numOfFiles):

    fitnessValues = []
    iterations = range(1, numOfFiles +1)

    for i in iterations:
        filePath = os.path.join(directoryPath,'resultsGeneration_'+str(i)+".pickle")

        with (open(filePath, "rb")) as openfile:
            results = pickle.load(openfile)

        algo = results['algorithm']
        uda = algo.extract(de1220)
        log = uda.get_log()
        fitnessValues.append(log[0][2])

    plt.plot(iterations, fitnessValues, 'k')
    plt.show()


def readResults(filepath):

    with (open(filepath, "rb")) as openfile:
            results = pickle.load(openfile)


    pop = results['pop']
    algo = results['algorithm']
    uda = algo.extract(de1220)
    log = uda.get_log()
    pupulation_size = results['pupulationSize']
    best_parameters = results['best_parameters']
    alfa = results['alfa']
    beta = results['beta']
    number_of_generations = results['numberOfGenerations']

    print(log)
    print('------------------ Algorithm Variables --------------')
    print('Population Size: ' + str(pupulation_size))
    print('Number of generations : ' + str(number_of_generations))
    print('Alfa: ' + str(alfa))
    print('Beta: ' + str(beta))
    print('Best parameters key,value are ' + str(best_parameters))
    print(f'Best parameters found are {pop.champion_x} and its score is {pop.champion_f}')





if __name__ == "__main__":
    filename = r"C:\Users\Adria\OneDrive\Documenti\GitHub\natcomp2021\results\Run_210720-143026\resultsGeneration_32.pickle"
    result = readResults(filename)

    directory = r"C:\Users\Adria\OneDrive\Documenti\GitHub\natcomp2021\results\Run_210720-143026"
    printResultsFromDirectory(directory,33)
