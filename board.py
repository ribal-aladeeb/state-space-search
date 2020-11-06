from moves import Moves
import numpy as np
from typing import *


class Board:

    def __init__(self, puzzle: np.array = None):
        self.score = 0
        self.puzzle = puzzle

    def is_goal_state(self) -> bool:
        x = self.puzzle
        rows = x.shape[0]
        cols = x.shape[1]
        goal_state = np.concatenate((np.arange(1, rows*cols), np.array([0])))

        return np.array_equal(x.flatten(), goal_state) or np.array_equal(x.T.flatten(), goal_state)

    def is_corner(self) -> bool:
        position = np.where(self.puzzle == 0)
        rows = position[0][0]
        cols = position[1][0]

        #puzzle = np.copy(self.puzzle)
        #corners = puzzle[::puzzle.shape[0]-1, ::puzzle.shape[1]-1]
        #corner_x, corner_y = np.where(corners == 0)[0][0]

        self.is_corner.top_left = rows == 0 and cols == 0
        self.is_corner.top_right = rows == 0 and cols == self.puzzle.shape[1] - 1
        self.is_corner.bottom_right = rows == self.puzzle.shape[0] - 1 and cols == self.puzzle.shape[1] - 1
        self.is_corner.bottom_left = rows == self.puzzle.shape[0] - 1 and cols == 0

        return self.is_corner.top_left or self.is_corner.top_right or self.is_corner.bottom_left or self.is_corner.bottom_right

    def _generate_regular_moves(self) -> List[dict]:
        '''Make sure that this move is legal before performing it'''

        possible_moves = ['up', 'down', 'left', 'right']
        regular_moves = []

        for move in possible_moves:
            try:
                rowof0 = np.where(self.puzzle == 0)[0][0]
                colof0 = np.where(self.puzzle == 0)[1][0]
                new_puzzle = np.copy(self.puzzle)
                start = (rowof0, colof0)

                if move == 'up':
                    end = (rowof0-1, colof0)

                elif move == 'down':
                    end = (rowof0 + 1, colof0)

                elif move == 'left':
                    end = (rowof0, colof0-1)

                else:  # move == 'right'
                    end = (rowof0, colof0+1)

                if end[0] < 0 or end[1] < 0:  # an index must be negative and we dont want that
                    continue

                new_puzzle[start], new_puzzle[end] = new_puzzle[end], new_puzzle[start]
                regular_moves.append({'start': start, 'end': end, 'puzzle': new_puzzle, 'simple_cost': 1})

            except IndexError:
                continue

        return regular_moves

    def wrap_around(self, direction: str):
        pass


    def generate_wrapping_moves(self):
        if not self.is_corner():
            return None

        rows = self.puzzle.shape[0]
        cols = self.puzzle.shape[1]

        can_be_performed = {
            'left': self.is_corner.top_left or self.is_corner.bottom_left,
            'right': self.is_corner.top_right or self.is_corner.bottom_right,
            'up': (self.is_corner.top_left or self.is_corner.top_right) and 2 < rows,
            'down': (self.is_corner.bottom_left or self.is_corner.bottom_right) and 2 < rows,
        }

        for move in can_be_performed:
            if can_be_performed[move]:
                self.wrap_around(move)
