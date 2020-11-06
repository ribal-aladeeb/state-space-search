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


def test_generate_regular_moves():
    b = Board(puzzle=np.arange(8).reshape(2, 4))
    print(f'initial puzzle\n{b.puzzle}')
    print()

    down_puzzle = np.copy(b.puzzle)
    down_puzzle[(0, 0)], down_puzzle[(1, 0)] = down_puzzle[(1, 0)], down_puzzle[(0, 0)]
    print(f'puzzle after moving tile down\n{down_puzzle}')
    print()

    right_puzzle = np.copy(b.puzzle)
    right_puzzle[(0, 0)], right_puzzle[(0, 1)] = right_puzzle[(0, 1)], right_puzzle[(0, 0)]
    print(f'puzzle after moving tile right\n{right_puzzle}')

    expected_result = [
        {"start": (0, 0), "end": (1, 0), "puzzle": down_puzzle, "simple_cost": 1},
        {"start": (0, 0), "end": (0, 1), "puzzle": right_puzzle, "simple_cost": 1}
    ]

    actual_result = b._generate_regular_moves()

    index = 0
    for results in actual_result:
        print(results)
        print("\n")
        print(expected_result[index])
        assert (results == expected_result[index]).all()
        index += 1
