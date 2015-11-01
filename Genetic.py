#!/usr/bin/env python

"""
Genetic algorithm(s).
"""




def tough_world(generator, numGen, eval_fn, init_list=[]):

    # Build initial population
    population = list(init_list)
    while len(population) < 100:
        population.append(generator())

    generation = 0
    while True:

        # Evaluate the population
        scores = eval_fn(population)
        scoredPopulation = zip(scores, population)

        if generation >= numGen:
            break

        # Select the next generation

        # Crossbreeding and Mutation
