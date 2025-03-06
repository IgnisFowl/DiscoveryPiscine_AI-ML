# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    puzzle_solver_ad.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aarie-c2@c1r4p1.42sp.org.br <aarie-c2@c    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/24 11:23:03 by aarie-c2@c1       #+#    #+#              #
#    Updated: 2025/02/26 13:41:11 by aarie-c2@c1      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
import argparse
from collections import deque

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

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

def bfs(initial_state):
	tries = 0
	
	if not is_solvable(initial_state):
		return None

	queue = deque([(initial_state, [])])
	visited = set()

	visited.add(initial_state)

	while queue:
		current_state, path = queue.popleft()

		print(f"Exploring state: {current_state} (Path so far: {path})")
		tries += 1
		
		if current_state == GOAL_STATE:
			print(f"Goal state reached after {tries} tries!")
			return path
		
		for neighbor in get_neighbors(current_state):
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append((neighbor, path + [neighbor]))
				
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
	solution = bfs(initial_state)
	
	if solution:
			print(f"Solution found in {len(solution)} steps.")
			for step_num, state in enumerate(solution, start=1):
				print(f"Step {step_num}:")
				print_puzzle(state)
	else:
		print("Puzzle is unsolvable!")

if __name__ == "__main__":
	main()
