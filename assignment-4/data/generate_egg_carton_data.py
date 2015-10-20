#!/usr/bin/python3

import sys
sys.path.append('../../../permve-ntnu-it3105/vi/')

import collections
import numpy

from vi.app.egg_carton import render_output, Problem
from vi.search import simulated_annealing

scenarios = [ [ 5, 5, 2 ] , [ 6, 6, 2 ], [ 8, 8, 1 ], [ 10, 10, 3 ] ]

start_temperatures       = list(numpy.linspace(0.1, 5, 20))
delta_temperature_ratios = list(numpy.linspace(10, 10000, 20))

repeats = 20

results = numpy.zeros(
    (len(scenarios), len(start_temperatures), len(delta_temperature_ratios)))

for s, scenario in enumerate(scenarios):
    problem = Problem(*scenario)

    for i, start_temperature in enumerate(start_temperatures):
        for j, delta_temperature_ratio in enumerate(delta_temperature_ratios):
            print('{0} {1} {2}'.format(s, i, j))

            delta_temperature = start_temperature / delta_temperature_ratio

            values = []

            for _ in range(repeats):
                solution, epochs = simulated_annealing(
                    problem, start_temperature, delta_temperature)

                values.append(solution.sum())

            results[s, i, j] = numpy.mean(values)

for s, scenario in enumerate(scenarios):
    with open('egg-carton-params-scenario-{0}.txt'.format(s + 1), 'w') as output_file:
        for i, start_temperature in enumerate(start_temperatures):
            for j, delta_temperature_ratio in enumerate(delta_temperature_ratios):
                print('{0:f} {1:f} {2:f}'.format(
                    start_temperature,
                    delta_temperature_ratio,
                    results[s, i, j]),
                    file=output_file)

            print('', file=output_file)

best_values = [None] * len(scenarios)
best_iterations = 10000

for s, scenario in enumerate(scenarios):
    best_parameters = numpy.unravel_index(numpy.argmax(results[s]), results[s].shape)

    problem = Problem(*scenario)

    start_temperature       = start_temperatures[best_parameters[0]]
    delta_temperature_ratio = delta_temperature_ratios[best_parameters[1]]
    delta_temperature       = start_temperature / delta_temperature_ratio

    best_solution = (0,)
    num_optimal   = 0

    for _ in range(best_iterations):
        solution, epochs = simulated_annealing(
            problem, start_temperature, delta_temperature)
        solution_value = solution.sum()

        if problem.is_terminal(solution):
            num_optimal += 1

        if solution_value > best_solution[0]:
            best_solution = (solution_value, solution)

    best_values[s] = (start_temperature,
                      delta_temperature,
                      best_solution[0],
                      num_optimal,
                      best_iterations,
                      num_optimal / best_iterations)

    if best_solution[0] > 0:
        render_output('egg-carton-best-scenario-{0}.pdf'.format(s + 1),
            scenario[0], scenario[1], scenario[2], best_solution[1])

with open('egg-carton-best-values.txt', 'w') as output_file:
    for s, scenario in enumerate(scenarios):
        print('{0} {1:f} {2:f} {3} {4} {5} {6:f}'.format(
            s + 1, *best_values[s]),
            file=output_file)

