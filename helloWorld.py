from random import random
from random import uniform
import math
import copy
from ast import literal_eval
import island as isl
import escores as esco

#population = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#population = [[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0]]

mutationPropability = 0.001
numberOfGenerations = 20

def initializeIndividual(cromossome):
    # Rastrigin's function
    for value in range(len(cromossome)):
        cromossome[value] = uniform(-5.12, 5.12)

    # Fantinato's function
    #for value in range(len(cromossome)):
    #    if random() < 0.5:
    #        cromossome[value] = 0
    #    else:
    #        cromossome[value] = 1

def initializePopulationParallel(island):
    population = []
    while isl.check(island) == 1:
        isl.wait()
    if isl.check(island) == 0:
        isl.lock(island)
        with open('island_{0}.txt'.format(island), 'r') as f:
            for line in f:
                population.append(literal_eval(line))
        f.close()
        for individual in range(len(population)):
            initializeIndividual(population[individual])
        with open('island_{0}.txt'.format(island), 'w') as f2:
            for ini in range(len(population)):
                f2.write(str(population[ini]) + '\n')
        f2.close()
        isl.unlock(island)

def initializePopulation(population):
    for individual in range(len(population)):
        initializeIndividual(population[individual])

def convertBoolean(cromossome, begin, end):
    aux = 0
    for i in range(begin, end+1):
        aux = aux * 2
        if (cromossome[i] == 1):
            aux = aux + 1
    return aux

def evaluateIndividual(cromossome):

    # Ackley's function
    #firstSum = 0.0
    #secondSum = 0.0
    #for c in chromosome:
    #    firstSum += c ** 2.0
    #    secondSum += math.cos(2.0 * math.pi * c)
    #n = float(len(chromosome))
    #return -20.0 * math.exp(-0.2 * math.sqrt(firstSum / n)) - math.exp(secondSum / n) + 20 + math.e

    # Griewank's function
    #part1 = 0
    #for i in range(len(chromosome)):
    #    part1 += chromosome[i] ** 2
    #    part2 = 1
    #for i in range(len(chromosome)):
    #    part2 *= math.cos(float(chromosome[i]) / math.sqrt(i + 1))
    #return 1 + (float(part1) / 4000.0) - float(part2)


    # Schwefel's function
    #alpha = 418.982887
    #fitness = 0
    #for i in range(len(chromosome)):
    #    fitness -= chromosome[i] * math.sin(math.sqrt(math.fabs(chromosome[i])))
    #return float(fitness) + alpha * len(chromosome)


    # Rastrigin's function
    fitness = 10 * len(cromossome)
    for i in range(len(cromossome)):
        fitness += cromossome[i] ** 2 - (10 * math.cos(2 * math.pi * cromossome[i]))
    return fitness

    # Fantinato's function
    #x = convertBoolean(cromossome, 0, int((len(cromossome))/2)-1)
    #y = convertBoolean(cromossome, int((len(cromossome))/2), len(cromossome)-1)
    #x = x * 0.00004768372718899898 - 100
    #y = y * 0.00004768372718899898 - 100
    #return (((abs(x*y*(math.sin((y*(math.pi))/4)))))+1)

def evaluatePopulation(population):
    sum = 0
    for individual in range(len(population)):
        sum = sum + evaluateIndividual(population[individual])
    return sum

def rouletteSelection(population):
    populationEvaluationSum = evaluatePopulation(population)
    limit = random() * populationEvaluationSum
    i = 0
    aux = evaluateIndividual(population[i])
    while aux < limit:
        i = i + 1
        aux = aux + evaluateIndividual(population[i])
    return i

def singlePointCrossover(cromossome1, cromossome2):
    cutpoint = int(random()*len(cromossome1))
    if random() < 0.5:
        for i in range(cutpoint):
            aux = cromossome1[i]
            cromossome1[i] = cromossome2[i]
            cromossome2[i] = aux
    else:
        for i in range(cutpoint, len(cromossome1)):
            aux = cromossome1[i]
            cromossome1[i] = cromossome2[i]
            cromossome2[i] = aux

def mutation(cromossome, probability):
    for i in range(len(cromossome)):
        if random() < probability:

            # Rastrigin's function
            cromossome[i] = uniform(-5.12, 5.12)

            # Fantinato's function
            #if cromossome[i] == 0:
            #    cromossome[i] = 1
            #else:
            #    cromossome[i] = 0

def generation(population):
    i = 0
    auxPopulation = copy.deepcopy(population)
    while i < len(population):
        auxPopulation[i] = copy.deepcopy(population[rouletteSelection(population)])
        auxPopulation[i+1] = copy.deepcopy(population[rouletteSelection(population)])
        singlePointCrossover(auxPopulation[i], auxPopulation[i+1])
        mutation(auxPopulation[i], mutationPropability)
        mutation(auxPopulation[i+1], mutationPropability)
        i = i + 2
    return auxPopulation

def showPopulation(i, population):
    for individual in range(len(population)):
        x = convertBoolean(population[individual], 0, int((len(population[individual])) / 2) - 1)
        y = convertBoolean(population[individual], int((len(population[individual])) / 2), len(population[individual]) - 1)
        x = x * 0.00004768372718899898 - 100
        y = y * 0.00004768372718899898 - 100
        print(individual, ':', x,';',y, ':', evaluateIndividual(population[individual]))

def chooseBetter(population,island):
    bestValue = -1
    for individual in range(len(population)):
        if(evaluateIndividual(population[individual])) > bestValue:
            bestValue = evaluateIndividual(population[individual])
            best_ind = population[individual]
            while esco.check() == 1:
                print("Wait")
            if esco.check() == 0:
                esco.lock()
                esc = open('escores.txt', 'r')
                resul = []
                for line in nonblank_lines(esc):
                    resul.append(literal_eval(line))
                esc.close()
                resul.append(bestValue)
                esc2 = open('escores.txt', 'w')
                for ini in range(len(resul)):
                    esc2.write(str(resul[ini]) + '\n')
                esc2.close()
                esco.unlock()
    set_broadcast(best_ind,island)
    return bestValue

def chooseWorst(population, betterValue):
    worstValue = betterValue
    for individual in range(len(population)):
        if(evaluateIndividual(population[individual])) < worstValue:
            worstValue = evaluateIndividual(population[individual])
    return(worstValue)

def calculateAverage(population):
    sum = 0
    for individual in range(len(population)):
        sum = sum + evaluateIndividual(population[individual])
    return(sum/len(population))

def rewriteFile(island, population):
    with open('island_{0}.txt'.format(island), 'w') as f:
        for ini in range(len(population)):
            f.write(str(population[ini]) + '\n')
    f.close()

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def set_broadcast(individual,island):
    allBests = []
    with open('broadcast_{0}.txt'.format(island), 'r') as broad1:
        for line in nonblank_lines(broad1):
            allBests.append(literal_eval(line))
    broad1.close()
    allBests.append(individual)
    with open('broadcast_{0}.txt'.format(island), 'w') as broad2:
        for ini in range(len(allBests)):
            broad2.write(str(allBests[ini]) + '\n')
    broad2.close()

def initializeGA(island):
    print("entrei aqui")
    population = []
    while isl.check(island) == 1:
        isl.wait()
    if isl.check(island) == 0:
        isl.lock(island)
        with open('island_{0}.txt'.format(island), 'r') as f:
            for line in f:
                population.append(literal_eval(line))
        f.close()
    for i in range(numberOfGenerations):
        print("start")
        population = generation(population)
        print("ok")
        betterValue = chooseBetter(population,island)
        worstValue = chooseWorst(population, betterValue)
        averageValue = calculateAverage(population)
        print('GENERATION:', i, '     /     BETTER:', betterValue, '     /      AVERAGE:', averageValue, '     /      WORST:', worstValue)
    print("right on")
    rewriteFile(island, population)
    isl.unlock(island)









