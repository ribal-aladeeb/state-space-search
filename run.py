import argparse, sys, search
from os import path
import numpy as np
from board import Board

def init_params():
    parser = argparse.ArgumentParser(description='Process input path parameter')
    parser.add_argument('-i', '--input_file', default=sys.stdin, help='Input from file, default stdin')  # all blocks
    init_params.args = parser.parse_args()

    if type(init_params.args.input_file) is str:
        common_check_path(init_params.args.input_file)
        init_params.args.input_file = open(init_params.args.input_file)

    return init_params.args

def common_check_path(file):
    assert path.exists(file), "input file does not exists"

def convert_to_numpy_arrays(file_name):
    string_puzzles = []
    np_puzzle = []
    with open(file_name, 'r') as f:
       string_puzzles = f.read().split("\n")

    string_puzzles.pop()
    for puzzle in string_puzzles:
        np_puzzle.append(np.fromstring(puzzle, dtype=int, sep=' '))
    
    return np_puzzle
    
if __name__ == "__main__":
    args = init_params()
    filename = args.input_file.name
    puzzles = convert_to_numpy_arrays(filename)

    for p in puzzles:
        start_puzzle: Board = Board(puzzle=p.reshape(2, 4))
        print(f'start puzzle:\n{start_puzzle}')
        experiments = {
            "uc":   search.uniform_cost(start_puzzle),
            "gbf": search.greedy_best_first(start_puzzle, H=search.heuristic4),
            "A*": search.a_star(start_puzzle, H=search.heuristic4)
        }
        for algo, result in experiments.items():
            print(f'{algo} found with cost = {result.total_cost}:\n{result.board}\n')
            solution_str, search_str = result.generate_solution_and_search_string(algo)
            search.write_results_to_disk(solution_str, search_str, algo, 0, 'h1')
