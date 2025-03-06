# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    puzzle_solver.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/24 11:23:03 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/25 09:21:59 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
import heapq
import argparse

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def manhattan_distance(state):
	distance = 0
	for i, val in enumerate(state):
		if val == 0:
			continue
		target_pos = GOAL_STATE.index(val)
		target_row, target_col = divmod(target_pos, 3)
		current_row, current_col = divmod(i, 3)
		distance += abs(current_row - target_row) + abs (current_col - target_col)
	return distance

def is_solvable(state):
	inversions = 0
	for i in range(len(state)):
		for j in range(i + 1, len(state)):
			if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
				inversions += 1
	return inversions % 2 == 0

def get_neighbors(state):
	zero_index = state.index(0)
	row, col = divmod(zero_index, 3)
	neighbors = []

	if row > 0:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index - 3] = new_state[zero_index - 3], new_state[zero_index]
		neighbors.append(tuple(new_state))
	
	if row < 2:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index + 3] = new_state[zero_index + 3], new_state[zero_index]
		neighbors.append(tuple(new_state))
	
	if col > 0:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index - 1] = new_state[zero_index - 1], new_state[zero_index]
		neighbors.append(tuple(new_state))
	
	if col < 2:
		new_state = list(state)
		new_state[zero_index], new_state[zero_index + 1] = new_state[zero_index + 1], new_state[zero_index]
		neighbors.append(tuple(new_state))
	
	return neighbors

def a_star(initial_state):
	if not is_solvable(initial_state):
		return None
	
	open_list = []
	closed_set = set()
	came_from = {}
	g_score = {initial_state: 0}
	f_score = {initial_state: manhattan_distance(initial_state)}

	heapq.heappush(open_list, (f_score[initial_state], initial_state))

	while open_list:
		_, current_state =  heapq.heappop(open_list)

		if current_state == GOAL_STATE:
			path = []
			while current_state in came_from:
				path.append(current_state)
				current_state = came_from[current_state]
			path.append(GOAL_STATE)
			path.reverse()
			return path
		
		closed_set.add(current_state)

		for neighbor in get_neighbors(current_state):
			if neighbor in closed_set:
				continue
			
			tentative_g_score = g_score[current_state] + 1

			if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
				came_from[neighbor] = current_state
				g_score[neighbor] = tentative_g_score
				f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor)
				heapq.heappush(open_list, (f_score[neighbor], neighbor))

	return None

def print_puzzle(state):
	for i in range(0, 9, 3):
		print(f"{state[i]} { state[i + 1]} { state[i + 2]}")
	print()

def generate_random_puzzle():
	while True:
		puzzle = list(range(9))
		random.shuffle(puzzle)
		if is_solvable(tuple(puzzle)):
			return tuple(puzzle)

def parse_args():
	parser = argparse.ArgumentParser(description="Solve the 8-puzzle using A* search.")
	parser.add_argument(
		"-s", "--state",
		type=int,
		nargs=9,
		help="Initial puzzle state as sequence of numbers, ex: 1 2 3 4 0 6 7 8)"
	)
	return parser.parse_args()

def main():
	args = parse_args()

	if args.state:
		initial_state = tuple(args.state)
		if len(initial_state) != 9:
			print("Invalid state length. Must contain 9 numbers.")
			return
		if not is_solvable(initial_state):
			print("Puzzle is unsolvable!")
			return
	else:
		initial_state = generate_random_puzzle()
	
	print("Initial state of the puzzle:")
	print_puzzle(initial_state)
	print("Solving the puzzle...")
	solution = a_star(initial_state)
	
	if solution:
			print(f"Solution found in {len(solution) - 1} steps.")
			for step_num, state in enumerate(solution[1:], start=2):
				print(f"Step {step_num}:")
				print_puzzle(state)
	else:
		print("Puzzle is unsolvable!")

if __name__ == "__main__":
	main()
