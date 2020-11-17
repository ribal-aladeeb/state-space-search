import argparse, sys, search, os, glob
import numpy as np
from board import Board
import heuristics, shutil

def write_report(search_length: tuple, sol_length: tuple, time: tuple):
    sol_total_length = f'Total length of solution paths: {sol_length[0]} line(s)\n'
    sol_avg_length = f'Average length of solution paths: {round(sol_length[1], 3)} line(s)\n'
    search_total_length = f'Total length of search paths: {search_length[0]} line(s)\n'
    search_avg_length = f'Average length of search paths: {round(search_length[1], 3)} line(s)\n'
    total_time = f'The total execution time is: {round(time[0], 2)} seconds\n'
    avg_time = f'The average execution time is: {round(time[1], 2)} seconds'

    with open("analysis.txt", 'w') as f:
        f.write(str(sol_total_length))
        f.write(str(sol_avg_length))
        f.write(str(search_total_length))
        f.write(str(search_avg_length))
        f.write(str(total_time))
        f.write(str(avg_time))

    print(f"Your report was generated at {os.path.abspath('analysis.txt')}")

def compute_time_stats(time_stats: list) -> tuple:
    '''
    The following function inputs a tuple with the algorithm type
    and the time taken to execute it. We compute the total time taken
    to execute the algorithm & average execution time.
    '''
    total_time = np.sum(time_stats)
    avg_time = np.average(time_stats)

    return avg_time, total_time

def compute_length_stats(fileType: str) -> tuple:
    '''
    The following function inputs a file type [solution, search] and
    computes the average & total length which are returned in a tuple.
    (avg, total)
    '''
    num_of_lines = 0
    num_of_files = 0   
    for fileName in glob.glob(f"results/*{fileType}*"):
        num_of_lines += sum(1 for line in open(fileName))
        num_of_files += 1
    avg_length_solution = num_of_lines / num_of_files
    return (avg_length_solution, num_of_lines)

def generate_analysis_report(time_taken: list):
    '''
    The following function generates a report consisting of:
    1 - average & total length of the solution and search paths
    2 - average & total number of no solution
    3 - average & total cost and execution time
    4 - optimality of the solution path
    '''
    avg_sol, len_sol = compute_length_stats("solution")
    avg_search, len_search = compute_length_stats("search")
    
    total_time_taken = 0
    avg_time_taken = 0
    for puzzles in time_taken:
        avg_time, total_time = compute_time_stats(puzzles)
        total_time_taken += total_time
        avg_time_taken += avg_time

    write_report((len_search, avg_search), (len_sol, avg_sol), (total_time_taken, avg_time_taken))

def generate_random_puzzles(numOfPuzzles: int) -> list:
    '''
    The following function generates randomly shuffled puzzles. Once generated,
    the puzzles are saved to disk. The function returns the list of arrays.
    '''
    puzzles = []
    for i in range(int(numOfPuzzles)):
        arr = np.arange(8)
        np.random.shuffle(arr)
        puzzles.append(arr)

    np.savetxt('random_puzzles.txt', puzzles, fmt='%.18g', delimiter=' ', newline=os.linesep)
    print(f"{numOfPuzzles} puzzles generated! File created at {os.path.abspath('random_puzzles.txt')}")
    
    return puzzles

def convert_to_numpy_arrays(file_name: str) -> list:
    '''
    The following function converts a file to a list of numpy arrays.
    '''
    string_puzzles = []
    np_puzzle = []
    with open(file_name, 'r') as f:
        string_puzzles = f.read().split("\n")

    string_puzzles = list(filter(lambda puzzle: puzzle != '\n' and puzzle != None and puzzle != '', string_puzzles))

    for puzzle in string_puzzles:
        np_puzzle.append(np.fromstring(puzzle, dtype=int, sep=' '))

    return np_puzzle
    
if __name__ == "__main__":
    print("Welcome to the X-puzzle solver!")
    puzzles = []
    choice = input("Would you like to use an [1] INPUT FILE or [2] GENERATE RANDOM BOARDS?: ")
    while (choice not in ["1", "2"]):
        print("Please enter a valid value (1 or 2)")
        choice = input("Would you like to use an [1] INPUT FILE or [2] GENERATE RANDOM BOARDS?: ")

    if choice == "1":
        print(f"Please place the file in the root directory at {os.path.abspath(os.getcwd())}")
        fileName = input("Please enter the file name: ")
        while (not os.path.isfile(fileName)):
            print("The file was not found.")
            fileName = input("Please enter the file name: ")

        puzzles = convert_to_numpy_arrays(fileName)
    
    if choice == "2":
        numOfPuzzles = input("How many puzzles would you like to generate?: ")
        while (not numOfPuzzles.isdigit() or int(numOfPuzzles) < 1):
            print("Please enter a valid number starting 1.")
            numOfPuzzles = input("How many puzzles would you like to generate?: ")

        puzzles = generate_random_puzzles(numOfPuzzles)

    puzzleNumber = 0
    time_taken = []

    if os.path.isdir("results"):
        shutil.rmtree("results")
    
    os.makedirs("results")

    for p in puzzles:
        start_puzzle: Board = Board(puzzle=p.reshape(2, 4))
        print(f'start puzzle:\n{start_puzzle}')
        experiments_h1 = {
            "ucs": search.uniform_cost(start_puzzle),
            "gbf": search.greedy_best_first(start_puzzle, H=heuristics.row_col_out_of_place),
            "A*": search.a_star(start_puzzle, H=heuristics.row_col_out_of_place)
        }
        experiments_h2 = {
            "ucs": search.uniform_cost(start_puzzle),
            "gbf": search.greedy_best_first(start_puzzle, H=heuristics.hamming_distance),
            "A*": search.a_star(start_puzzle, H=heuristics.hamming_distance)
        }
        times = []
        for algo, result in experiments_h1.items():
            times.append(result["runtime"])
            print(f'{algo} found with cost = {result["current_node"].total_cost}:\n{result["current_node"].board}\n')
            solution_str, search_str = result["current_node"].generate_solution_and_search_string(algo)
            if algo == "ucs": search.write_results_to_disk(solution_str, search_str, algo, puzzleNumber)
            else: search.write_results_to_disk(solution_str, search_str, algo, puzzleNumber, 'h1')
        for algo, result in experiments_h2.items():
            times.append(result["runtime"])
            print(f'{algo} found with cost = {result["current_node"].total_cost}:\n{result["current_node"].board}\n')
            solution_str, search_str = result["current_node"].generate_solution_and_search_string(algo)
            if algo == "ucs": search.write_results_to_disk(solution_str, search_str, algo, puzzleNumber)
            else: search.write_results_to_disk(solution_str, search_str, algo, puzzleNumber, 'h2')
        puzzleNumber += 1
        time_taken.append(times)

    generate_analysis_report(time_taken)

    print("Thank you for using X-solver! Written by Ribal Aladeeb & Mohanad Arafe")