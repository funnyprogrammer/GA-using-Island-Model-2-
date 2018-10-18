from random import randint
import os
from ast import literal_eval
import math

def convertBoolean(cromossome, begin, end):
    aux = 0
    for i in range(begin, end+1):
        aux = aux * 2
        if (cromossome[i] == 1):
            aux = aux + 1
    return aux

def evaluateIndividual(cromossome):
    x = convertBoolean(cromossome, 0, int((len(cromossome)) / 2) - 1)
    y = convertBoolean(cromossome, int((len(cromossome)) / 2), len(cromossome) - 1)
    x = x * 0.00004768372718899898 - 100
    y = y * 0.00004768372718899898 - 100

    # Ackley's function
    #firstSum = 0.0
    #secondSum = 0.0
    #for c in chromosome:
    #    firstSum += c ** 2.0
    #    secondSum += math.cos(2.0 * math.pi * c)
    #n = float(len(chromosome))
    #return -20.0 * math.exp(-0.2 * math.sqrt(firstSum / n)) - math.exp(secondSum / n) + 20 + math.e

    # Griewank's function
    #part1 = (x ** 2) + (y ** 2)
    #part2 = math.cos(float(x) / math.sqrt(2)) + math.cos(float(y) / math.sqrt(3))
    #return 1 + (float(part1) / 4000.0) - float(part2)

    # Schwefel's function
    #alpha = 418.982887 * 2
    #fitness = x * math.sin(math.sqrt(math.fabs(x))) + y * math.sin(math.sqrt(math.fabs(y)))
    #return alpha - fitness

    # Rastrigin's function
    #fitness = 20 + (x ** 2 - (10 * math.cos(2 * math.pi * x))) + (y ** 2 - (10 * math.cos(2 * math.pi * y)))
    #return fitness

    # Fantinato's function
    return (((abs(x*y*(math.sin((y*(math.pi))/4)))))+1)


def do_migration(island_number):
    mig_policy_isl = 0.33  # chance of every island
    mig_policy_ind = 0.33  # switch individual
    mig_policy_size = 12
    var_random = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
    if var_random >= mig_policy_isl:
        island = open('island_{0}.txt'.format(island_number), 'r')
        island_content = []
        for line in island:
            island_content.append(literal_eval(line))
        var = 0
        broad = open('broadcast.txt', 'r')
        best_gen_list = []
        for line in broad:
            best_gen_list.append(literal_eval(line))
        while var <= mig_policy_size:
            var_random2 = int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)
            if var_random2 >= mig_policy_ind:
                random_ind = randint(0, len(island_content)-1)
                random_best_gen = randint(0, len(best_gen_list)-1)
                if evaluateIndividual(island_content[random_ind]) < evaluateIndividual(best_gen_list[random_best_gen]):
                    island_content[random_ind] = best_gen_list[random_best_gen] #assumindo que eu posso pegar o msm caso para todas as ilhas
            var = var + 1
        island.close()
        with open('island_{0}.txt'.format(island_number), 'w') as new_island:
            for ini in range(len(island_content)):
                new_island.write(str(island_content[ini]) + '\n')
        new_island.close()
        broad.close()
