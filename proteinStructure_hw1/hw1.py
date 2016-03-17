#!/usr/bin/env python
import random
from math import exp, log
import numpy as np
import matplotlib.pyplot as plt


def print_hist(data):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    numBins = 50
    ax.hist(data, 25, (-25.5, -0.5), color='green')
    plt.xlabel("Energy")
    plt.ylabel("Number")
    plt.title("Histogram")
    plt.show()
    return


def printMatrix(Matrix):
    length = len(Matrix[0])
    matrix_rotated = [[0 for i in xrange(length)]
                      for i in xrange(length)]
    for i in xrange(length):
        for j in xrange(length):
            matrix_rotated[length-1-j][i] = Matrix[i][j]
    print('\n'.join([''.join(['{:1}'.format(item)
                              for item in row]) for row in matrix_rotated]))


def print_folding(protein_sequence, folding):
    sizeofmatrix = 2 * len(folding) + 3
    center = (sizeofmatrix - 1) / 2
    matrix = [[0 for i in xrange(sizeofmatrix)] for i in xrange(sizeofmatrix)]
    # generate the matrix with protein_sequence and folding
    x = center
    y = center
    i = 0
    matrix[x][y] = protein_sequence[i]  # initial at the center of matrix
    for letter in folding:
        i += 1
        if letter == 'r':
            x += 1
        elif letter == 'u':
            y += 1
        elif letter == 'l':
            x -= 1
        elif letter == 'd':
            y -= 1
        matrix[x][y] = protein_sequence[i]
    printMatrix(matrix)

    return


def validate_structure(folding):
    sizeofmatrix = 2 * len(folding) + 3
    center = (sizeofmatrix - 1) / 2
    matrix = [[0 for i in xrange(sizeofmatrix)] for i in xrange(sizeofmatrix)]

    x = center
    y = center
    matrix[x][y] = 1  # initial at the center of matrix
    for letter in folding:
        if letter == 'r':
            x += 1
        elif letter == 'u':
            y += 1
        elif letter == 'l':
            x -= 1
        elif letter == 'd':
            y -= 1
        if matrix[x][y] > 0:
            # printMatrix(matrix)
            return 'notvalid'
        else:
            matrix[x][y] += 1
    # printMatrix(matrix)
    # print "notvalid"
    return 'valid'


def get_energy(protein_sequence, folding):
    sizeofmatrix = 2 * len(folding) + 3
    center = (sizeofmatrix - 1) / 2
    matrix = [[0 for i in xrange(sizeofmatrix)] for i in xrange(sizeofmatrix)]
    # generate the matrix with protein_sequence and folding
    x = center
    y = center
    i = 0
    matrix[x][y] = protein_sequence[i]  # initial at the center of matrix
    for letter in folding:
        i += 1
        if letter == 'r':
            x += 1
        elif letter == 'u':
            y += 1
        elif letter == 'l':
            x -= 1
        elif letter == 'd':
            y -= 1
        matrix[x][y] = protein_sequence[i]

    # calculate the total energy
    E = 0
    x = center
    y = center
    for letter in folding:
        if matrix[x][y] == 'H':
            if matrix[x + 1][y] == 'H':
                E -= 1
            if matrix[x][y + 1] == 'H':
                E -= 1
            if matrix[x - 1][y] == 'H':
                E -= 1
            if matrix[x][y - 1] == 'H':
                E -= 1
        if letter == 'r':
            x += 1
        elif letter == 'u':
            y += 1
        elif letter == 'l':
            x -= 1
        elif letter == 'd':
            y -= 1
    if matrix[x][y] == 'H':
        if matrix[x + 1][y] == 'H':
            E -= 1
        if matrix[x][y + 1] == 'H':
            E -= 1
        if matrix[x - 1][y] == 'H':
            E -= 1
        if matrix[x][y - 1] == 'H':
            E -= 1
    E = E / 2
    # printMatrix(matrix)

    # GET E0 which is energy due to connected H.
    E0 = 0
    for i in xrange(len(protein_sequence) - 1):
        if protein_sequence[i] == 'H' and protein_sequence[i + 1] == 'H':
            E0 -= 1
    return E - E0


# the length of folding string is less than protein string by one.
# generate a folding that is valid
def random_folding(length):
    while(1):  # loop until get a valid folding
        folding = ""
        deadend = False
        sizeofmatrix = 2 * length + 1
        center = (sizeofmatrix - 1) / 2
        matrix = [[0 for i in xrange(sizeofmatrix)]
                  for i in xrange(sizeofmatrix)]
        x = center
        y = center
        matrix[x][y] = 1  # initial at the center of matrix
        for n in range(1, length):
            choices = ""  # search which orientation is valid
            if matrix[x + 1][y] == 0:
                choices += 'r'  # right
            if matrix[x][y + 1] == 0:
                choices += 'u'  # up
            if matrix[x - 1][y] == 0:
                choices += 'l'  # left
            if matrix[x][y - 1] == 0:
                choices += 'd'  # down
            if choices == "":
                deadend = True
                break  # deadend, restart the folding

            orientation = random.choice(choices)
            if orientation == 'r':
                x += 1
            elif orientation == 'u':
                y += 1
            elif orientation == 'l':
                x -= 1
            elif orientation == 'd':
                y -= 1
            matrix[x][y] += 1
            folding += orientation
        if deadend:
            continue
        # print folding
        return folding


def opposite(orientation):
    if orientation == 'r':
        return 'l'
    if orientation == 'l':
        return 'r'
    if orientation == 'u':
        return 'd'
    if orientation == 'd':
        return 'u'


def mutate(folding):
    while(1):
        n = random.randint(0, len(folding) - 1)
        choices = "ruld"
        # mutate must be different from the current orientation
        choices = choices.replace(folding[n], '')
        if n == 0:
            choices = choices.replace(opposite(folding[1]), '')
        elif n == len(folding) - 1:
            choices = choices.replace(opposite(folding[n - 1]), '')
        else:
            choices = choices.replace(opposite(folding[n - 1]), '')
            choices = choices.replace(opposite(folding[n + 1]), '')
        # put the folding into a list for change the letter.
        list_folding = list(folding)
        list_folding[n] = random.choice(choices)
        folding_new = "".join(list_folding)
        validate_structure(folding_new)
        if validate_structure(folding_new) == 'valid':
            return folding_new
        else:
            pass


# crossover father and mother, return the better child between two child
def crossover(protein_sequence, father, mother):
    # repeat until find a child
    while(1):
        r = random.randint(0, len(father) - 1)
        father1 = father[0:r]
        father2 = father[r:]
        mother1 = mother[0:r]
        mother2 = mother[r:]
        child1 = father1 + mother2
        child2 = father2 + mother1
        valid1 = validate_structure(child1)
        valid2 = validate_structure(child2)
        if valid1 == 'valid' and valid2 == 'valid':
            # assume only the healthier child can grow up
            if get_energy(protein_sequence, child1) < get_energy(protein_sequence, child2):
                return child1
            else:
                return child2
        elif valid1 == 'valid' and valid2 != 'valid':
            return child1
        elif valid1 != 'valid' and valid2 == 'valid':
            return child2
        else:
            continue


# Metropolis algorithms
def Metropolis(protein_sequence, NumberOfLoops, T):
    length = len(protein_sequence)
    protein_folding = random_folding(length)  # initialize a folding
    energy = get_energy(protein_sequence, protein_folding)
    energys = []
    for i in xrange(NumberOfLoops):  # xrange from 0 to n-1
        # mutate the configuration
        protein_folding_new = mutate(protein_folding)
        energy_new = get_energy(protein_sequence, protein_folding_new)
        if energy_new <= energy:
            protein_folding = protein_folding_new
            energy = energy_new
        elif random.random() < exp((energy-energy_new) / T):
            print exp((energy-energy_new)/ T)
            protein_folding = protein_folding_new
            energy = energy_new
        else:
            continue # reject

        energys.append(energy)
        
        print protein_folding + " " + str(energy)
    print energys
    print_folding(protein_sequence, protein_folding)
    print_hist(energys)

# Genetic Algorithm with simulated annealing.


def GeneticAlgorithm(protein_sequence,NumberOfGeneration, t):
    length = len(protein_sequence)
    population = 500
    protein_foldings = []
    T = t
    best_of_ever=0
    best = 0
    best_folding_ever = ""
    best_folding = ""
    # initialize the population
    for i in xrange(population):
        protein_foldings.append(random_folding(length))
    # g is iterator for generation
    for g in xrange(NumberOfGeneration):
        best=0
        n = 2 # start from 2 , in case of t/ln(n) is not valid
        # get the best structure in current generation
        for i in xrange(population):
            if get_energy(protein_sequence, protein_foldings[i]) <= best:
                best = get_energy(protein_sequence, protein_foldings[i]) # best in current generation
                best_folding = protein_foldings[i]
        if best<= best_of_ever:  #store the best configuratoin in all generation
            best_of_ever=best
            best_folding_ever=best_folding
        print best
        # pointwise mutation of current generation
        for i in xrange(population):
            protein_foldings[i] = mutate(protein_foldings[i])

        # create the next generation
        protein_foldings_new = []
        next_generation = False
        while next_generation == False:
            random.shuffle(protein_foldings)
            for i in xrange(population / 2):
                father = protein_foldings[2 * i]
                mother = protein_foldings[2 * i + 1]
                child = crossover(protein_sequence, father, mother)
                # get energys
                energy_father = get_energy(protein_sequence, father)
                energy_mother = get_energy(protein_sequence, mother)
                energy_child = get_energy(protein_sequence, child)

                if child == 'null':
                    continue
                if energy_child <= (energy_father + energy_mother) / 2:
                    protein_foldings_new.append(child)
                    n += 1
                elif random.random() < exp(((energy_father + energy_mother)/2-energy_child)/ T):
                    protein_foldings_new.append(child)
                    n += 1
                T = t / log(n)
                if n > population + 1:
                    protein_foldings = protein_foldings_new
                    next_generation = True
                    break
    print best_folding_ever
    print_folding(protein_sequence, best_folding_ever)


def test_crossover(protein_sequence):
    length = len(protein_sequence)
    for i in xrange(5):
        protein_folding1 = random_folding(length)
        protein_folding2 = random_folding(length)
        print protein_folding1
        print protein_folding2
        print crossover(protein_sequence, protein_folding1, protein_folding2)
        print ""



protein_sequence='PHPHPHPHPPHPHPPPPHHPPPHPHPPHPPPHPPHPHHPPPHHHHPHPHPPHPHHPHHHHPPHPHPPHPHHPHHPHPHPPHPHHHH'
# second value gives the number of loops, third number is temperature
Metropolis(protein_sequence, 10000, 1)  

# second value gives the number of generations, third number is temperature
#GeneticAlgorithm(protein_sequence,200, 3)  

# print get_energy(protein_sequence,'ldluuulldrddlldrrrdrrddrruluurdrrruurrddrurdrddddluuulldrddldrrrrrrddrurrrddddluuuldl')
