import numpy as np
from typing import *

class Board:

    def __init__(self, puzzle: np.array = None, score=0):
        self.puzzle = puzzle
        self.score = score

    def is_goal_state(self) -> bool:
        x = self.puzzle
        rows = x.shape[0]
        cols = x.shape[1]
        goal_state = np.concatenate((np.arange(1, rows*cols), np.array([0])))

        return np.array_equal(x.flatten(), goal_state) or np.array_equal(x.T.flatten(), goal_state)

    def is_corner(self) -> bool:
        position = np.where(self.puzzle == 0)
        row = position[0][0]
        col = position[1][0]

        self.top_left_corner = row == 0 and col == 0
        self.top_right_corner = row == 0 and col == self.puzzle.shape[1] - 1
        self.bottom_right_corner = row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1
        self.bottom_left_corner = row == self.puzzle.shape[0] - 1 and col == 0
        self.coordinates = (row, col)

        return self.top_left_corner or self.top_right_corner or self.bottom_left_corner or self.bottom_right_corner

    def _generate_regular_moves(self) -> List[dict]:
        '''
        Generates all the possible regular move (i.e. cost of one from the
        current state of the board.
        '''

        rowof0 = np.where(self.puzzle == 0)[0][0]
        colof0 = np.where(self.puzzle == 0)[1][0]

        possible_moves = {
            'up': (rowof0-1, colof0),
            'down': (rowof0 + 1, colof0),
            'left': (rowof0, colof0-1),
            'right': (rowof0, colof0+1)
        }

        regular_moves = []

        for move in possible_moves:
            try:
                new_puzzle = np.copy(self.puzzle)
                start = (rowof0, colof0)
                end = possible_moves[move]

                if end[0] < 0 or end[1] < 0:  # an index must be negative and we dont want that
                    continue

                new_puzzle[start], new_puzzle[end] = new_puzzle[end], new_puzzle[start]
                regular_moves.append({'start': start, 'end': end, 'board': Board(new_puzzle, 1), 'simple_cost': 1})

            except IndexError:  # performing this move is not possible because the index goes out of bounds (it is not a possible child state) so skip it.
                continue

        return regular_moves

    def wrap_around(self, wrapping_direction: str) -> dict:

        new_puzzle = np.copy(self.puzzle)
        start = self.coordinates
        rows = new_puzzle.shape[0]
        cols = new_puzzle.shape[1]

        end_position = {
            'left': (start[0], cols-1),
            'right': (start[0], 0),
            'up': (rows-1, start[1]),
            'down': (0, start[1]),
        }

        end = end_position[wrapping_direction]
        new_puzzle[start], new_puzzle[end] = new_puzzle[end], new_puzzle[start]

        return {'start': start, 'end': end, 'board': Board(new_puzzle, 2), 'simple_cost': 2}

    def _generate_wrapping_moves(self) -> dict:
        if not self.is_corner():
            return []

        moves = []

        rows = self.puzzle.shape[0]

        can_be_performed = {
            'left': self.top_left_corner or self.bottom_left_corner,
            'right': self.top_right_corner or self.bottom_right_corner,
            'up': (self.top_left_corner or self.top_right_corner) and 2 < rows,
            'down': (self.bottom_left_corner or self.bottom_right_corner) and 2 < rows,
        }

        for move in can_be_performed:
            if can_be_performed[move]:
                moves.append(self.wrap_around(move))

        return moves
