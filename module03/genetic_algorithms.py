# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    genetic_algorithms.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/25 13:41:42 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/26 09:45:09 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
import subprocess
import argparse

def generate_population(pop_size, min_freq, max_freq):
	population = []
	for _ in range(pop_size):
		individual = [random.uniform(min_freq, max_freq) for _ in range(4)]
		population.append(individual)
	return population

def evaluate_individual(individual):
	try:
		result = subprocess.run(
			['./cellular'] + [str(f) for f in individual],
			capture_output=True, text=True, check=True
		)
		output = result.stdout
		fitness = parse_fitness(output)
		return fitness
	except subprocess.CalledProcessError as e:
		print(f"Error during cellular evaluation: {e}")
		return float('inf')
	
def parse_fitness(output):
	reliability_indices = {
		'dorms': 0.0,
		'kitchen': 0.0,
		'showers': 0.0,
		'cluster': 0.0,
		'entrance': 0.0
		}
	for line in output.splitlines():
		if "dorms" in line:
			reliability_indices['dorms'] = float(line.split(":")[1].strip())
		elif "kitchen" in line:
			reliability_indices['kitchen'] = float(line.split(":")[1].strip())
		elif "showers" in line:
			reliability_indices['showers'] = float(line.split(":")[1].strip())
		elif "cluster" in line:
			reliability_indices['cluster'] = float(line.split(":")[1].strip())
		elif "entrance" in line:
			reliability_indices['entrance'] = float(line.split(":")[1].strip())
	fitness = sum(reliability_indices.values())
	return fitness

def select_population(population, fitness_scores, num_selected):
	selected = sorted(zip(population, fitness_scores), key=lambda x: x[1])
	selected_individuals = [ind for ind, _ in selected[:num_selected]]
	return selected_individuals

def crossover(parent1, parent2):
	crossover_point = random.randint(1, len(parent1) - 1)
	offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
	offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
	return offspring1, offspring2

def mutate(individual, mutation_rate):
	if random.random() < mutation_rate:
		mutation_index = random.randint(0, len(individual) - 1)
		mutation_value = random.uniform(45.0, 50.0)
		individual[mutation_index] = mutation_value
	return individual

def genetic_algorithm(pop_size, generations, mutation_rate, min_freq, max_freq):
	population = generate_population(pop_size, min_freq, max_freq)
	print(f"Optmizing Antenna Frequencies using Genetic Algorithm.")
	print(f"If you want to customize, run program with arguments.")
	print(f"Population: {pop_size}. Generations: {generations}. Mutation Rate: {mutation_rate}. Minimum frequency: {min_freq}. Maximum frequency: {max_freq}.")

	for generation in range(generations):
		fitness_scores = [evaluate_individual(ind) for ind in population]
		selected_population = select_population(population, fitness_scores, num_selected=pop_size // 2)
		if len(selected_population) % 2 == 1:
			selected_population.append(selected_population[-1])
		
		new_population = []
		for i in range(0, len(selected_population), 2):
			parent1, parent2 = selected_population[i], selected_population[i + 1]
			offspring1, offspring2 = crossover(parent1, parent2)
			new_population.append(mutate(offspring1, mutation_rate))
			new_population.append(mutate(offspring2, mutation_rate))
		
		population = new_population
		best_individual = min(population, key=lambda ind: evaluate_individual(ind))
		best_fitness = evaluate_individual(best_individual)

		print(f"Generation {generation + 1}: Best Individual: {best_individual}")
		print(f"Fitness score: {best_fitness}")
		
	final_best_individual = min(population, key=lambda ind: evaluate_individual(ind))
	print("\nOptimal frequency settings found!")
	print(f"Best individual frequencies: {final_best_individual}")
	print(f"Fitness score: {evaluate_individual(final_best_individual)}")

def parse_args():
	parser = argparse.ArgumentParser(description="Optmize Antenna Frequencies using Genetic Algorithm")
	parser.add_argument("--pop_size", type=int, default=1000, help="Size of the population")
	parser.add_argument("--generations", type=int, default=100, help="Number of generations")
	parser.add_argument("--mutation_rate", type=float, default=0.01, help="Mutation rate(probability)")
	parser.add_argument("--min_freq", type=float, default=45.0, help="Minimum frequency value")
	parser.add_argument("--max_freq", type=float, default=50.0, help="Maximum frequency value")

	return parser.parse_args()

if __name__ == "__main__":
	args = parse_args()
	genetic_algorithm(
		pop_size=args.pop_size,
		generations=args.generations,
		mutation_rate=args.mutation_rate,
		min_freq=args.min_freq,
		max_freq=args.max_freq
	)




	