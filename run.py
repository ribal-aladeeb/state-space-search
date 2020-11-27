import search
import os
import glob
import numpy as np
from board import Board
import heuristics
import shutil


def write_report(search_length: tuple, sol_length: tuple, time: tuple, costs: tuple, timeouts: tuple):
    sol_total_length = f'Total length of solution paths: {sol_length[0]} line(s)\n'
    sol_avg_length = f'Average length of solution paths: {round(sol_length[1], 3)} line(s)\n'
    search_total_length = f'Total length of search paths: {search_length[0]} line(s)\n'
    search_avg_length = f'Average length of search paths: {round(search_length[1], 3)} line(s)\n'
    total_time = f'The total execution time is: {round(time[0], 2)} seconds\n'
    avg_time = f'The average execution time is: {round(time[1], 2)} seconds\n'
    total_cost = f'The total cost is: {costs[0]}\n'
    avg_cost = f'The average cost is: {round(costs[1], 2)}\n'
    total_timeouts = f'The total number of timeouts is: {timeouts[1]} timeout(s)\n'
    avg_timeouts = f'The average number of timeouts is: {round(timeouts[0], 3)} timeout(s)'

    with open("analysis.txt", 'w') as f:
        f.write(str(sol_total_length))
        f.write(str(sol_avg_length))
        f.write(str(search_total_length))
        f.write(str(search_avg_length))
        f.write(str(total_time))
        f.write(str(avg_time))
        f.write(str(total_cost))
        f.write(str(avg_cost))
        f.write(str(total_timeouts))
        f.write(str(avg_timeouts))

    return f"Your report was generated at {os.path.abspath('analysis.txt')}"


def compute_timeouts(timeouts: list):
    '''
    The following function returns the average and total number of timeouts.
    '''
    total_timeouts = len(timeouts) - np.sum(timeouts)
    avg_timeouts = total_timeouts / len(timeouts)

    return (avg_timeouts, total_timeouts)


def compute_cost_stats(costs: list) -> tuple:
    '''
    The following function returns a tuple of the total and average cost.
    '''
    total_cost = np.sum(costs)
    avg_cost = np.average(costs)

    return avg_cost, total_cost


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


def generate_analysis_report(results: list):
    '''
    The following function generates a report consisting of:
    1 - average & total length of the solution and search paths
    2 - average & total number of no solution
    3 - average & total cost and execution time
    4 - optimality of the solution path
    '''
    avg_sol, len_sol = compute_length_stats("solution")
    avg_search, len_search = compute_length_stats("search")

    timeout_values = []
    cost_values = []
    time_taken_values = []
    for puzzles in results:
        timeout_values.append(puzzles["success"])
        cost_values.append(puzzles["current_node"].g_n)
        time_taken_values.append(puzzles["runtime"])

    avg_timeouts, total_timeouts = compute_timeouts(timeout_values)
    avg_cost, total_cost = compute_cost_stats(cost_values)
    avg_time, total_time = compute_time_stats(time_taken_values)

    return write_report((len_search, avg_search),
                        (len_sol, avg_sol),
                        (total_time, avg_time),
                        (total_cost, avg_cost),
                        (avg_timeouts, total_timeouts))


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


def prompt_user() -> list:
    '''
    The following function prompts the user input. One can generate random boards or
    use an input file.
    '''
    print("Welcome to the X-puzzle solver!")
    puzzles = []
    choice = input("Would you like to use an [1] INPUT FILE or [2] GENERATE RANDOM BOARDS?: ")
    while (choice not in ["1", "2"]):
        print("Please enter a valid value (1 or 2)")
        choice = input("Would you like to use an [1] INPUT FILE or [2] GENERATE RANDOM BOARDS?: ")

    if os.path.isdir("results"):
        shutil.rmtree("results")

    os.makedirs("results")

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

    return puzzles


def main(chosen_heurisitics=[heuristics.manhattan_distance, heuristics.row_col_out_of_place]):
    puzzles = prompt_user()
    print('Solving...')
    search_output = ""
    res = []
    for index, p in enumerate(puzzles):
        start_puzzle: Board = Board(puzzle=p.reshape(2, 4))
        print('\n'+'*'*80)
        search_output += '\n'+'*'*80+'\n'
        print(f'Puzzle {index+1}:\n{start_puzzle}')
        search_output += f'Puzzle {index+1}:\n{start_puzzle}\n'

        for i in range(len(chosen_heurisitics)):
            experiments = {
                # "UCS":   search.uniform_cost,
                "GBF":   search.greedy_best_first,
                "A*": search.a_star,
            }
            print(f'\nUsing heuristic "{chosen_heurisitics[i].__name__}":')
            search_output+= f'\nUsing heuristic "{chosen_heurisitics[i].__name__}":\n'

            results = []

            for algo in experiments:
                # if algo == 'UCS':
                #     if i == 1:
                #         continue
                # results.append(experiments[algo](start_puzzle))
                # else:
                # results.append(experiments[algo](start_puzzle, H=chosen_heurisitics[i]))
                results.append(experiments[algo](start_puzzle, H=chosen_heurisitics[i]))

            for result in results:
                res.append(result)
                print(f"{result['algo']}\tfound with cost = {result['current_node'].total_cost}\tin {result['runtime']} seconds")
                search_output += f"{result['algo']}\t\tfound with cost = {result['current_node'].total_cost}\tin {result['runtime']} seconds\n"
                # print(f"\n\t{result['algo']} found with cost = {result['current_node'].total_cost} in {result['runtime']} seconds:\n{result['current_node'].board}\n")
                solution_str = result['current_node'].generate_solution_string(result['algo'])
                search_str = search.generate_search_string(result['search_space'], result['algo'])
                if result['algo'] == "UCS":
                    search.write_results_to_disk(solution_str, search_str, result['algo'], index)
                else:
                    search.write_results_to_disk(solution_str, search_str, result['algo'], index, f'h{i+1}')

    report_message = generate_analysis_report(res)
    print(f'\n{report_message}')
    search_output += f'\n{report_message}\n'
    search_output += "Thank you for using X-solver! Written by Ribal Aladeeb & Mohanad Arafe"

    with open('./search_output.txt', mode='w')as f:
        f.write(search_output)

    print("Thank you for using X-solver! Written by Ribal Aladeeb & Mohanad Arafe")


if __name__ == "__main__":
    main()
