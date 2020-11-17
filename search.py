import numpy as np
from board import Board
from node import Node
from queue import PriorityQueue
import os
import time
import heuristics
import shutil


def uniform_cost(board: Board, timeout=60) -> Node:

    start_time = time.time()
    elapsed = start_time

    root = Node(is_root=True, board=board)

    open_list = PriorityQueue()     # even though not python list, naming is kept for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is kept for consistency with state space search theory
    search_space = []               # Used to reconstructed the order in which nodes were traversed

    created_nodes = 1
    open_list.put((root.total_cost, created_nodes, root))
    current_node = None
    visited_nodes = 0

    while not open_list.empty():

        _, _, current_node = open_list.get()
        visited_nodes += 1

        if current_node.is_goal_state():
            elapsed = round(time.time() - start_time, 2)
            return {
                'algo': 'UCS',
                'current_node': current_node,
                'runtime': elapsed,
                'visited_nodes': visited_nodes,
                'created_nodes': created_nodes,
                'search_space':  search_space,
                'success': True,
                'message': 'solution found'
            }

        #--------This is only related to time execution--------#
        if visited_nodes % 10000 == 0 and timeout > 0:
            elapsed = round(time.time() - start_time, 2)
            if elapsed > timeout:
                return {
                    'algo': 'UCS',
                    'current_node': current_node,
                    'runtime': elapsed,
                    'visited_nodes': visited_nodes,
                    'created_nodes': created_nodes,
                    'search_space':  search_space,
                    'success': False,
                    'message': f"timeout after {timeout} seconds"
                }
        #--------This is only related to time execution--------#

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            if closed_list[hashed_node].total_cost < current_node.total_cost:   # we previously got to this configuration with lower cost than we do right now so ignore
                continue

        closed_list[hashed_node] = current_node
        search_space.append(current_node)
        for s in current_node.successors():
            created_nodes += 1
            open_list.put((s.total_cost, created_nodes, s))

    return {
        'algo': 'UCS',
        'current_node': current_node,
        'runtime': elapsed,
        'visited_nodes': visited_nodes,
        'created_nodes': created_nodes,
        'search_space':  search_space,
        'success': False,
        'message': 'no more nodes in open list'
    }


def greedy_best_first(board: Board, H, timeout=60) -> Node:

    start_time = time.time()
    elapsed = start_time

    root = Node(is_root=True, board=board, heuristic_func=H)
    # goal_states = root.board.generate_goal_states()

    open_list = PriorityQueue()       # even though not python list, naming is kept for consistency with state space search theory
    closed_list = set()               # even though not python list, naming is kept for consistency with state space search theory
    search_space = []               # Used to reconstructed the order in which nodes were traversed

    created_nodes = 1
    open_list.put((root.h_n, created_nodes, root))
    current_node = None
    visited_nodes = 0

    while not open_list.empty():
        _, _, current_node = open_list.get()
        visited_nodes += 1

        if current_node.is_goal_state():
            elapsed = round(time.time() - start_time, 2)
            return {
                'algo': 'GBF',
                'current_node': current_node,
                'runtime': elapsed,
                'visited_nodes': visited_nodes,
                'created_nodes': created_nodes,
                'search_space':  search_space,
                'success': True,
                'message': 'solution found'
            }

        #--------This is only related to time execution--------#
        if visited_nodes % 10000 == 0 and timeout > 0:
            elapsed = round(time.time() - start_time, 2)
            if elapsed > timeout:
                return {
                    'algo': 'GBF',
                    'current_node': current_node,
                    'runtime': elapsed,
                    'visited_nodes': visited_nodes,
                    'created_nodes': created_nodes,
                    'search_space':  search_space,
                    'success': False,
                    'message': f"timeout after {timeout} seconds"
                }
        #--------This is only related to time execution--------#

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            continue

        closed_list.add(hashed_node)
        search_space.append(current_node)
        for s in current_node.successors(heuristic_func=H):
            created_nodes += 1
            open_list.put((s.h_n, created_nodes, s))

    return {
        'algo': 'GBF',
        'current_node': current_node,
        'runtime': elapsed,
        'visited_nodes': visited_nodes,
        'created_nodes': created_nodes,
        'search_space':  search_space,
        'success': False,
        'message': 'no more nodes in open list'
    }


def a_star(board: Board, H, timeout=60) -> Node:

    start_time = time.time()
    elapsed = start_time

    root = Node(is_root=True, board=board, heuristic_func=H)

    open_list = PriorityQueue()     # even though not python list, naming is kept for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is kept for consistency with state space search theory
    search_space = []               # Used to reconstructed the order in which nodes were traversed
    created_nodes = 1
    open_list.put((root.f_n, created_nodes, root))
    current_node = None
    visited_nodes = 0

    while not open_list.empty():

        _, _, current_node = open_list.get()
        visited_nodes += 1

        if current_node.is_goal_state():
            elapsed = round(time.time() - start_time, 2)
            return {
                'algo': 'A*',
                'current_node': current_node,
                'runtime': elapsed,
                'visited_nodes': visited_nodes,
                'created_nodes': created_nodes,
                'search_space':  search_space,
                'success': True,
                'message': 'solution found'
            }

        #--------This is only related to time execution--------#
        if visited_nodes % 10000 == 0 and timeout > 0:
            elapsed = round(time.time() - start_time, 2)
            if elapsed > timeout:
                return {
                    'algo': 'A*',
                    'current_node': current_node,
                    'runtime': elapsed,
                    'visited_nodes': visited_nodes,
                    'created_nodes': created_nodes,
                    'search_space':  search_space,
                    'success': False,
                    'message': f"timeout after {timeout} seconds"
                }
        #--------This is only related to time execution--------#

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            if closed_list[hashed_node].g_n <= current_node.g_n:     # we previously got to this configuration with lower f_n than we do right now so ignore
                visited_nodes -= 1                                   # we don't consider a node visited if you don't expand it (i.e generate it's children)
                continue

        closed_list[hashed_node] = current_node
        search_space.append(current_node)
        for s in current_node.successors(heuristic_func=H):
            created_nodes += 1
            open_list.put((s.f_n, created_nodes, s))

    return {
        'algo': 'A*',
        'current_node': current_node,
        'runtime': elapsed,
        'visited_nodes': visited_nodes,
        'created_nodes': created_nodes,
        'search_space':  search_space,
        'success': False,
        'message': 'no more nodes in open list'
    }


def generate_search_string(search_space: list, algo: str) -> str:
    '''
    Generates the search string given closed_list (actually a dict) which is
    returned by a search algorithm.
    '''
    search_str = ''
    algo = algo.upper()
    for node in search_space:
        board_as_str = node.board.line_representation()

        if node.is_root:
            search_str += f'0 0 0 {board_as_str}\n'
            continue

        f = node.f_n if algo == 'A*' else 0
        g = 0 if algo == 'GBF' else node.g_n
        h = 0 if algo == 'UCS' else node.h_n

        search_str += f'{f} {g} {h} {board_as_str}\n'

    return search_str


def write_results_to_disk(solution: str, search: str, algo_name: str, puzzle_number: int, heuristic: str = None) -> bool:
    '''
    Writes the contents of the solution and search strings for puzzle_number using algo_name and heurisic
    '''
    algo_name = algo_name.lower()
    heuristic_string = f'_{heuristic}_' if heuristic != None else '_'
    sol_name = f'{puzzle_number}_{algo_name}{heuristic_string}solution.txt'
    search_name = f'{puzzle_number}_{algo_name}{heuristic_string}search.txt'

    result_dir = 'results'

    with open(os.path.join(result_dir, sol_name), mode='w') as f:
        f.write(solution)

    with open(os.path.join(result_dir, search_name), mode='w') as f:
        f.write(search)

    return True


def main(chosen_heurisitics=[heuristics.manhattan_distance, heuristics.row_col_out_of_place]):
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

    if os.path.isdir("results"):
        shutil.rmtree("results")
    os.makedirs("results")

    for j, p in enumerate(puzzles):
        start_puzzle: Board = Board(puzzle=p)
        print('*'*80)
        print(f'Puzzle {j+1}:\n{start_puzzle}')
        for i in range(len(chosen_heurisitics)):
            experiments = [
                uniform_cost(start_puzzle),
                greedy_best_first(start_puzzle, H=chosen_heurisitics[i]),
                a_star(start_puzzle, H=chosen_heurisitics[i])
            ]
            print(f'\nUsing heuristic \"{chosen_heurisitics[i].__name__}\":')

            for result in experiments:

                logged = f"\n\t{result['algo']} visited {result['visited_nodes']} nodes, created {result['created_nodes']} and "
                logged += f"found with cost = {result['current_node'].total_cost} in {result['runtime']} seconds:"
                logged += f"\n{result['current_node'].board}\n"

                print(logged)

                solution_str = result['current_node'].generate_solution_string(result['algo'])
                search_str = generate_search_string(result['search_space'], result['algo'])

                write_results_to_disk(solution_str, search_str, result['algo'], 0, f'h{i+1}')


if __name__ == "__main__":
    main()
