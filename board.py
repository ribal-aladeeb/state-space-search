import numpy as np
from typing import *


class Board:

    def __init__(self, puzzle: np.array = None,):
        self.puzzle = puzzle

    def __repr__(self) -> str:
        return str(self.puzzle)

    def is_goal_state(self) -> bool:
        x = self.puzzle
        rows = x.shape[0]
        cols = x.shape[1]
        goal_state = np.concatenate((np.arange(1, rows*cols), np.array([0])))

        return np.array_equal(x.flatten(), goal_state) or np.array_equal(x.T.flatten(), goal_state)

    def generate_goal_states(self) -> tuple:
        x = self.puzzle
        rows = x.shape[0]
        cols = x.shape[1]
        goal_state1 = np.concatenate((np.arange(1, rows*cols), np.array([0])))
        goal_state2 = goal_state1.reshape(cols,rows).T.flatten()
        return goal_state1, goal_state2

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

    def generate_regular_moves(self) -> List[dict]:
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
                regular_moves.append({'start': start, 'end': end, 'board': Board(new_puzzle), 'simple_cost': 1})

            except IndexError:  # performing this move is not possible because the index goes out of bounds (it is not a possible child state) so skip it.
                continue

        return regular_moves

    def _wrap_around(self, wrapping_direction: str) -> dict:

        new_puzzle = np.copy(self.puzzle)
        start = self.coordinates
        rows = new_puzzle.shape[0] - 1
        cols = new_puzzle.shape[1] - 1

        end_position = {
            'left': (start[0], cols),
            'right': (start[0], 0),
            'up': (rows, start[1]),
            'down': (0, start[1]),
        }

        end = end_position[wrapping_direction]
        new_puzzle[start], new_puzzle[end] = new_puzzle[end], new_puzzle[start]

        return {'start': start, 'end': end, 'board': Board(new_puzzle), 'simple_cost': 2}

    def generate_wrapping_moves(self) -> List[dict]:

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
                moves.append(self._wrap_around(move))

        return moves

    def _move_diagonal(self, wrapping_direction: str) -> dict:

        new_puzzle0 = np.copy(self.puzzle)
        new_puzzle1 = np.copy(self.puzzle)
        start = self.coordinates
        rows = new_puzzle1.shape[0] - 1
        cols = new_puzzle1.shape[1] - 1

        direction_to_endposition_mapping = {
            'bottom-right': [(1, 1), (rows, cols)],
            'bottom-left': [(1, cols-1), (rows, 0)],
            'top-left': [(0, 0), (rows-1, cols-1)],
            'top-right': [(rows-1, 1), (0, cols)],
        }

        end = direction_to_endposition_mapping[wrapping_direction]

        new_puzzle0[start], new_puzzle0[end[0]] = new_puzzle0[end[0]], new_puzzle0[start]
        new_puzzle1[start], new_puzzle1[end[1]] = new_puzzle1[end[1]], new_puzzle1[start]

        return [
            {'start': start, 'end': end[0], 'board': Board(new_puzzle0), 'simple_cost': 3},
            {'start': start, 'end': end[1], 'board': Board(new_puzzle1), 'simple_cost': 3}
        ]

    def generate_diagonal_moves(self) -> List[dict]:

        if not self.is_corner():
            return []

        moves = []

        can_be_performed = {
            'bottom-right': self.top_left_corner,
            'bottom-left': self.top_right_corner,
            'top-right': self.bottom_left_corner,
            'top-left': self.bottom_right_corner,
        }

        for direction in can_be_performed:
            if can_be_performed[direction]:
                move1, move2 = self._move_diagonal(direction)
                moves.append(move1)
                moves.append(move2)

        return moves

    def generate_all_moves(self) -> List[dict]:
        all_moves = self.generate_regular_moves() + self.generate_wrapping_moves() + self.generate_diagonal_moves()
        return all_moves


    def line_representation(self)->str:
        '''return a single line with all board values counted in row-major order'''

        tiles = [str(i) for i in self.puzzle.flatten()]
        return ' '.join(tiles)
