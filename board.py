import numpy as np


class Board:

    def __init__(self, shape=(2, 4), puzzle: np.array = None):
        self.score = 0
        self.puzzle = puzzle

    def is_goal_state(self) -> bool:
        x = self.puzzle
        rows = x.shape[0]
        cols = x.shape[1]
        goal_state = np.concatenate((np.arange(1,rows*cols),np.array([0])))

        return np.array_equal(x.flatten(), goal_state) or np.array_equal(x.T.flatten(), goal_state)
