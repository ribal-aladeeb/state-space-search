from __future__ import annotations  # in order to allow type hints for a class referring to itself
from typing import List, Tuple
from board import Board
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
            self.g_n = self.total_cost

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
        search.txt files. The algo parameter takes one of ['ucs' , 'gbf', 'a*'].
        '''
        solution = ''
        search = ''

        current_node = self

        while current_node.parent != None:
            moved_tile_index = current_node.start
            moved_tile_value = current_node.board.puzzle[moved_tile_index]

            board_as_string = current_node.board.line_representation()

            solution = f'{moved_tile_value} {current_node.simple_cost} {board_as_string}\n' + solution

            f = current_node.f_n if algo.lower() == 'a*' else 0
            g = 0 if algo.lower() == 'gbf' else current_node.g_n
            h = 0 if algo.lower() == 'ucs' else current_node.h_n

            search = f'{f} {g} {h} {board_as_string}\n' + search

            current_node = current_node.parent

        root_node = current_node.board.line_representation()
        solution = f'0 0 {root_node}\n' + solution
        search = f'0 0 0 {root_node}\n' + search

        return solution, search
