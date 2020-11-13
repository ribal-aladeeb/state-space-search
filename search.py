from __future__ import annotations  # in order to allow type hints for a class referring to itself
from typing import List, Tuple
from board import Board
from queue import PriorityQueue
import numpy as np


class Node:

    def __init__(self,
                 move: dict = None,
                 parent: Node = None,
                 simple_cost: int = 0,
                 is_root: bool = False,
                 board: Board = None,
                 heuristic_func=None):

        if is_root:
            assert board != None, "There should be a board argument if is_root=True"
            self.board = board
            self.start = (np.nan, np.nan)
            self.end = (np.nan, np.nan)
            self.simple_cost = 0
            self.total_cost = 0
        else:
            assert move != None, "A hashed_node should always be created with a move argument when not root"
            assert parent != None, "If a hashed_node is not root, parent cannot be None"
            self.start: tuple = move['start']
            self.end: tuple = move['end']
            self.board: Board = move['board']
            self.simple_cost = move['simple_cost']
            self.total_cost = self.simple_cost + parent.total_cost

        self.parent: Board = parent

        if heuristic_func:
            self.h_n = heuristic_func(self)
            self.g_n = self.total_cost
            self.f_n = self.g_n + self.h_n

    def successors(self, heuristic_func=None) -> List[Node]:
        moves: List[dict] = self.board.generate_all_moves()
        successors: List[Node] = []

        for move in moves:
            child = Node(move=move, parent=self, heuristic_func=heuristic_func)
            successors.append(child)

        return successors

    def is_goal_state(self) -> bool:
        return self.board.is_goal_state()

    def generate_solution_and_search_string(self, algo: str) -> Tuple[str, str]:
        '''
        This function returns the strings needed to create the solution.txt and
        search.txt files. The algo parameter takes one of ['uc' , 'gbf', 'a*'].
        '''
        solution = ''
        search = ''

        current_node = self

        while current_node.parent != None:
            moved_tile_index = current_node.end
            moved_tile_value = current_node.board.puzzle[moved_tile_index]

            board_as_string = current_node.board.line_representation()

            solution = f'{moved_tile_value} {current_node.simple_cost} {board_as_string}\n' + solution

            f = current_node.f_n if algo.lower() == 'a*' else 0
            g = 0 if algo.lower() == 'gbf' else current_node.g_n
            h = 0 if algo.lower() == 'uc' else current_node.h_n

            search = f'{f} {g} {h} {board_as_string}\n' + search

        return solution, search


def uniform_cost(board: Board) -> Node:
    root = Node(is_root=True, board=board)

    open_list = PriorityQueue()     # even though not python list, naming is kept for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is kept for consistency with state space search theory

    total_visited = 1
    open_list.put((root.total_cost, total_visited, root))
    current_node = None

    while not open_list.empty():
        total_visited += 1
        _, _, current_node = open_list.get()

        if current_node.is_goal_state():
            print(f'Visited {total_visited} nodes')
            return current_node

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            if closed_list[hashed_node].total_cost < current_node.total_cost:   # we previously got to this configuration with lower cost than we do right now so ignore
                continue

        closed_list[hashed_node] = current_node
        for s in current_node.successors():
            total_visited += 1
            open_list.put((s.total_cost, total_visited, s))

    print("This puzzle configuration has no result")
    return current_node


def greedy_best_first(board: Board, H) -> Node:
    root = Node(is_root=True, board=board, heuristic_func=H)
    # goal_states = root.board.generate_goal_states()

    open_list = PriorityQueue()       # even though not python list, naming is kept for consistency with state space search theory
    closed_list = set()               # even though not python list, naming is kept for consistency with state space search theory

    total_visited = 1
    open_list.put((root.h_n, total_visited, root))
    current_node = None

    while not open_list.empty():
        total_visited += 1
        _, _, current_node = open_list.get()

        if current_node.is_goal_state():
            print(f'Visited {total_visited} nodes')
            return current_node

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            continue

        closed_list.add(hashed_node)
        for s in current_node.successors(heuristic_func=H):
            total_visited += 1
            open_list.put((s.h_n, total_visited, s))

    print("This puzzle configuration has no result")
    return current_node


def a_star(board: Board, H) -> Node:
    root = Node(is_root=True, board=board, heuristic_func=H)

    open_list = PriorityQueue()     # even though not python list, naming is kept for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is kept for consistency with state space search theory

    total_visited = 1
    open_list.put((root.f_n, total_visited, root))
    current_node = None

    while not open_list.empty():
        total_visited += 1
        _, _, current_node = open_list.get()

        if current_node.is_goal_state():
            print(f'Visited {total_visited} nodes')
            return current_node

        hashed_node = tuple(current_node.board.puzzle.flatten())

        if hashed_node in closed_list:
            if closed_list[hashed_node].f_n < current_node.f_n:     # we previously got to this configuration with lower f_n than we do right now so ignore
                continue

        closed_list[hashed_node] = current_node
        for s in current_node.successors(heuristic_func=H):
            total_visited += 1
            open_list.put((s.total_cost, total_visited, s))


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
            "uniform":   uniform_cost(start_puzzle),
            "greedy bfs": greedy_best_first(start_puzzle, H=heuristic1),
            "A*": a_star(start_puzzle, H=heuristic1)
        }
        for algo, result in experiments.items():
            print(f'{algo} found with cost = {result.total_cost}:\n{result.board}\n')
