from board import Board
import numpy as np


def test_is_goal_state():
    not_goal = Board(puzzle=np.arange(8).reshape(2, 4))

    assert not_goal.is_goal_state() == False

    actual_goal_1 = Board(puzzle=np.array([
        [1, 2, 3, 4],
        [5, 6, 7, 0]]))

    actual_goal_2 = Board(puzzle=np.array([
        [1, 3, 5, 7],
        [2, 4, 6, 0]]))

    assert actual_goal_1.is_goal_state()
    assert actual_goal_2.is_goal_state()
