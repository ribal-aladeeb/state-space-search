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
    print()
    print(35*"=")
    print("Testing regular moves")
    print(35*"=")
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
        {"start": (0, 0), "end": (1, 0), "board": Board(down_puzzle), "simple_cost": 1},
        {"start": (0, 0), "end": (0, 1), "board": Board(right_puzzle), "simple_cost": 1}
    ]

    actual_result = b._generate_regular_moves()

    index = 0
    for results in actual_result:
        assert (results["start"] == expected_result[index]["start"])
        assert (results["end"] == expected_result[index]["end"])
        assert (results["simple_cost"] == expected_result[index]["simple_cost"])
        assert (np.array_equal(results["board"].puzzle, expected_result[index]["board"].puzzle))
        index += 1

def test_move_row_out_of_bound_1():
    print()
    print(35*"=")
    print("Testing bad moves part 1")
    print(35*"=")

    b = Board(puzzle=np.array([[1,2,3,4], [5, 0, 7, 8]]))
    print(f'\ninitial puzzle\n{b.puzzle}')
    print()
    
    bad_move = np.copy(b.puzzle)
    try:
        bad_move[(1, 1)], bad_move[(2, 1)] = bad_move[(2, 1)], bad_move[(1, 1)]
    
    except IndexError:
        print("Assertion caught!")
        assert True

def test_move_row_out_of_bound_2():
    print()
    print(35*"=")
    print("Testing bad moves part 2")
    print(35*"=")

    b = Board(puzzle=np.array([[1, 0, 3, 4], [5, 6, 7, 8]]))
    print(f'\ninitial puzzle\n{b.puzzle}')
    print()
    
    bad_move = np.copy(b.puzzle)
    try:
        bad_move[(0, 1)], bad_move[(-1, 1)] = bad_move[(-1, 1)], bad_move[(0, 1)]
    
    except IndexError:
        print("Assertion caught!")
        assert True

def test_is_corner():
    print()
    print(35*"=")
    print("Testing corners")
    print(35*"=")

    b = Board(puzzle=np.array([[0, 1, 3, 4], [5, 6, 7, 8]]))
    print(f'\ntesting top-left corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True

    b = Board(puzzle=np.array([[2, 1, 3, 0], [5, 6, 7, 8]]))
    print(f'\ntesting top-right corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True

    b = Board(puzzle=np.array([[2, 1, 3, 4], [0, 6, 7, 8]]))
    print(f'\ntesting bottom-left corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True

    b = Board(puzzle=np.array([[2, 1, 3, 4], [5, 6, 7, 0]]))
    print(f'\ntesting bottom-right corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True

    b = Board(puzzle=np.array([[2, 1, 3, 4], [5, 0, 7, 8]]))
    print(f'\ntesting no corner puzzle\n{b.puzzle}')
    assert b.is_corner() == False
    