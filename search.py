import numpy as np
from board import Board
from node import Node
from queue import PriorityQueue
import os
import time


def uniform_cost(board: Board, timeout=60) -> Node:

    start_time = time.time()
    root = Node(is_root=True, board=board)

    open_list = PriorityQueue()     # even though not python list, naming is kept for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is kept for consistency with state space search theory

    created_nodes = 1
    open_list.put((root.total_cost, created_nodes, root))
    current_node = None
    visited_nodes = 0

    while not open_list.empty():

        _, _, current_node = open_list.get()
        visited_nodes += 1

        if current_node.is_goal_state():
            elapsed = round(time.time() - start_time, 2)
            print(f'Uniform Cost: {visited_nodes} visited and {created_nodes} created nodes in {elapsed} seconds')
            return current_node

        #--------This is only related to time execution--------#
        if visited_nodes % 10000 == 0 and timeout > 0:
            elapsed = round(time.time() - start_time, 2)
            if elapsed > timeout:
                return current_node
        #--------This is only related to time execution--------#

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            if closed_list[hashed_node].total_cost < current_node.total_cost:   # we previously got to this configuration with lower cost than we do right now so ignore
                continue

        closed_list[hashed_node] = current_node
        for s in current_node.successors():
            created_nodes += 1
            open_list.put((s.total_cost, created_nodes, s))

    print("This puzzle configuration has no result")
    return current_node


def greedy_best_first(board: Board, H, timeout=60) -> Node:

    start_time = time.time()
    root = Node(is_root=True, board=board, heuristic_func=H)
    # goal_states = root.board.generate_goal_states()

    open_list = PriorityQueue()       # even though not python list, naming is kept for consistency with state space search theory
    closed_list = set()               # even though not python list, naming is kept for consistency with state space search theory

    created_nodes = 1
    open_list.put((root.h_n, created_nodes, root))
    current_node = None
    visited_nodes = 0

    while not open_list.empty():
        _, _, current_node = open_list.get()
        visited_nodes += 1

        if current_node.is_goal_state():
            elapsed = round(time.time() - start_time, 2)
            print(f'Greedy Best First: {visited_nodes} visited and {created_nodes} created nodes in {elapsed} seconds')
            return current_node

        #--------This is only related to time execution--------#
        if visited_nodes % 10000 == 0 and timeout > 0:
            elapsed = round(time.time() - start_time, 2)
            if elapsed > timeout:
                return current_node
        #--------This is only related to time execution--------#

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            continue

        closed_list.add(hashed_node)
        for s in current_node.successors(heuristic_func=H):
            created_nodes += 1
            open_list.put((s.h_n, created_nodes, s))

    print("This puzzle configuration has no result")
    return current_node


def a_star(board: Board, H, timeout=60) -> Node:

    start_time = time.time()
    root = Node(is_root=True, board=board, heuristic_func=H)

    open_list = PriorityQueue()     # even though not python list, naming is kept for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is kept for consistency with state space search theory

    created_nodes = 1
    open_list.put((root.f_n, created_nodes, root))
    current_node = None
    visited_nodes = 0

    while not open_list.empty():

        _, _, current_node = open_list.get()
        visited_nodes += 1

        if current_node.is_goal_state():
            elapsed = round(time.time() - start_time, 2)
            print(f'A*: {visited_nodes} visited and {created_nodes} created nodes in {elapsed} seconds')
            return current_node

        #--------This is only related to time execution--------#
        if visited_nodes % 10000 == 0 and timeout > 0:
            elapsed = round(time.time() - start_time, 2)
            if elapsed > timeout:
                return current_node
        #--------This is only related to time execution--------#

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            if closed_list[hashed_node].g_n <= current_node.g_n:     # we previously got to this configuration with lower f_n than we do right now so ignore
                continue

        closed_list[hashed_node] = current_node
        for s in current_node.successors(heuristic_func=H):
            created_nodes += 1
            open_list.put((s.f_n, created_nodes, s))

    print("This puzzle configuration has no result")
    return current_node


def heuristic1(n: Node) -> int:
    '''This heuristic will return the number of tiles out of place'''
    goal_states = n.board.generate_goal_states()
    tiles_out_of_place = []
    for state in goal_states:
        config = n.board.puzzle.flatten()
        x = np.where(config != state)[0]
        num_tiles = len(x)
        tiles_out_of_place.append(num_tiles)

    return min(tiles_out_of_place)


def heuristic2(n: Node) -> int:
    '''This heuristic computes the number of tiles out of row place and column place.'''
    goal_states = n.board.generate_goal_states()
    rows, cols = n.board.puzzle.shape

    total_out_of_place = [0, 0]  # always exactly 2

    for i in range(len(goal_states)):
        out_of_row_place = np.zeros(rows)
        out_of_column_place = np.zeros(cols)

        puzzle = n.board.puzzle
        state = goal_states[i].reshape(rows, cols)

        # out of place rows
        for j in range(rows):
            current_row = set(puzzle[j])
            goal_row = set(state[j])
            out_of_row_place[i] += sum([c not in goal_row for c in current_row])

        # out of place columns
        for k in range(cols):
            current_col = set(puzzle[:, k])
            goal_col = set(state[:, k])
            out_of_column_place[k] += sum([c not in goal_col for c in current_col])

        total_out_of_place[i] = sum(out_of_row_place) + sum(out_of_column_place)

    return int(min(total_out_of_place))


def heuristic3(n: Node) -> int:
    '''This heuristic computes the Euclidean distance of the tiles'''
    goal_states = n.board.generate_goal_states()
    rows, cols = n.board.puzzle.shape

    total_euclidean = [0, 0]  # always exactly 2

    for i in range(len(goal_states)):
        state = goal_states[i].reshape(rows, cols)
        puzzle = n.board.puzzle
        total_euclidean[i] = np.linalg.norm(puzzle - state)

    return int(min(total_euclidean))


def heuristic4(n: Node) -> int:
    '''This heuristic computes the permutation inversion of the tiles'''
    goal_states = n.board.generate_goal_states()

    total = [0, 0]  # always exactly 2

    for i in range(len(goal_states)):
        for j in range(len(n.board.puzzle.flatten())):
            total[i] += abs(j - np.where(goal_states[i] == n.board.puzzle.flatten()[j])[0][0])

    return int(min(total))


def write_results_to_disk(solution: str, search: str, algo_name: str, puzzle_number: int, heuristic: str = None) -> bool:
    '''
    Writes the contents of the solution and search strings for puzzle_number using algo_name and heurisic
    '''
    algo_name = algo_name.lower()
    heuristic_string = f'_{heuristic}_' if heuristic != None else ''
    sol_name = f'{puzzle_number}_{algo_name}{heuristic_string}solution.txt'
    search_name = f'{puzzle_number}_{algo_name}{heuristic_string}search.txt'

    result_dir = 'results'

    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)
    else:
        os.replace(result_dir, result_dir)
        # os.rmdir(result_dir)
        # os.makedirs(result_dir)

    with open(os.path.join(result_dir, sol_name), mode='w') as f:
        f.write(solution)

    with open(os.path.join(result_dir, search_name), mode='w') as f:
        f.write(search)

    return True


if __name__ == "__main__":

    puzzles = [
        np.array([
            [7, 0, 1, 6],
            [2, 5, 3, 4]
        ]),
        np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7]
        ])
    ]
    for p in puzzles:
        start_puzzle: Board = Board(puzzle=p)
        print(f'start puzzle:\n{start_puzzle}')
        experiments = {
            "uc":   uniform_cost(start_puzzle),
            "gbf": greedy_best_first(start_puzzle, H=heuristic1),
            "A*": a_star(start_puzzle, H=heuristic1)
        }
        for algo, result in experiments.items():
            print(f'{algo} found with cost = {result.total_cost}:\n{result.board}\n')
            solution_str, search_str = result.generate_solution_and_search_string(algo)
            write_results_to_disk(solution_str, search_str, algo, 0, 'h1')
