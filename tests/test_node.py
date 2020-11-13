from board import Board
from search import Node
import numpy as np

def test_successors():
    b = Board(puzzle=np.array([[0, 1, 3, 4], [5, 6, 7, 8]]))
    node = Node(parent=None, board=b, is_root=True)

    print()
    print(35*"=")
    print("Testing board moves")
    print(35*"=")
    print("INITIAL BOARD")
    print(b)

    actual_results = node.successors()
    expected_results = [
        {'board': Board(puzzle=np.array([[5, 1, 3, 4], [0, 6, 7, 8]])),
        'total_cost': 1},
        {'board': Board(puzzle=np.array([[1, 0, 3, 4], [5, 6, 7, 8]])),
        'total_cost': 1},
        {'board': Board(puzzle=np.array([[4, 1, 3, 0], [5, 6, 7, 8]])),
        'total_cost': 2},
        {'board': Board(puzzle=np.array([[6, 1, 3, 4], [5, 0, 7, 8]])),
        'total_cost': 3},
        {'board': Board(puzzle=np.array([[8, 1, 3, 4], [5, 6, 7, 0]])),
        'total_cost': 3}
    ]

    index = 0
    assert len(expected_results) == len(actual_results), "Different sizes of moves"
    for moves in actual_results:
        print("move")
        print(moves.board)
        print(f"cost: {moves.total_cost}")
        assert moves.total_cost == expected_results[index]["total_cost"], "The costs are not matching!"
        assert np.array_equal(moves.board.puzzle, expected_results[index]["board"].puzzle)
        index += 1

    print()
    print(35*"=")
    print("Testing children moves")
    print(35*"=")
    print("INITIAL BOARD")
    print(actual_results[0].board)
    print()

    child_successor = actual_results[0].successors()
    expected_child_results = [
        {'board': Board(puzzle=np.array([[0, 1, 3, 4], [5, 6, 7, 8]])),
        'total_cost': 2},
        {'board': Board(puzzle=np.array([[5, 1, 3, 4], [6, 0, 7, 8]])),
        'total_cost': 2},
        {'board': Board(puzzle=np.array([[5, 1, 3, 4], [8, 6, 7, 0]])),
        'total_cost': 3},
        {'board': Board(puzzle=np.array([[5, 0, 3, 4], [1, 6, 7, 8]])),
        'total_cost': 4},
        {'board': Board(puzzle=np.array([[5, 1, 3, 0], [4, 6, 7, 8]])),
        'total_cost': 4}
    ]

    index = 0
    assert len(child_successor) == len(expected_child_results), "Different sizes of moves"
    for moves in child_successor:
        print("move")
        print(moves.board)
        print(f"cost: {moves.total_cost}")
        assert moves.total_cost == expected_child_results[index]["total_cost"], "The costs are not matching!"
        assert np.array_equal(moves.board.puzzle, expected_child_results[index]["board"].puzzle)
        index += 1
