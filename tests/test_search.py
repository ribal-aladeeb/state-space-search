from search import Node, heuristic2, uniform_cost, heuristic1
from board import Board
import numpy as np


def test_2x4_ufc_search():
    print()
    print(35*"=")
    print("Testing 2x4 boards")
    print(35*"=")

    test_cases = [
        Board(puzzle=np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7]])),
        Board(puzzle=np.array([
            [7, 0, 1, 6],
            [2, 5, 3, 4]])),
        Board(puzzle=np.array([
            [4, 1, 7, 0],
            [3, 6, 2, 5]]))
    ]

    for board in test_cases:
        print("\nTesting board")
        print(board)
        result = uniform_cost(board)
        print("Solved!")
        print(result.board)
        assert result.board.is_goal_state(), "The board could not be solved!"


def test_3x3_ufc_board():

    print()
    print(35*"=")
    print("Testing 3x3 boards")
    print(35*"=")

    test_cases = [
        Board(puzzle=np.array([
            [4, 1, 7],
            [3, 0, 2],
            [6, 5, 8]])),
        Board(puzzle=np.array([
            [7, 1, 4],
            [5, 6, 0],
            [2, 3, 8]]))
    ]

    for board in test_cases:
        print("\nTesting board")
        print(board)
        result = uniform_cost(board)
        print("Solved!")
        print(result.board)
        assert result.board.is_goal_state(), "The board could not be solved!"


def test_heuristic2():
    b = Board(puzzle=np.array([
        [0, 5, 6, 7],
        [1, 2, 3, 4] 
    ]))

    node = Node(is_root=True, board=b, heuristic_func=heuristic2)
    assert heuristic2(node) == 9, "The heuristic is wrongly calculated!"