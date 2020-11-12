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

def test_generate_goal_states():
    test_cases = [
        Board(puzzle=np.array([[0, 1, 3, 4], [5, 6, 7, 8]])),
        Board(puzzle=np.array([
            [7, 1, 4],
            [5, 6, 0],
            [2, 3, 8]]))
    ]

    expected_results = [
        (np.array([1, 2, 3, 4, 5, 6, 7, 0]), np.array([1, 3, 5, 7, 2, 4, 6, 0])),
        (np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]), np.array([1, 4, 7, 2, 5, 8, 3, 6, 0]))
    ]

    index = 0
    for boards in test_cases:
        assert np.array_equal(boards.generate_goal_states(), expected_results[index])
        index += 1

def test_is_corner():

    print()
    print(35*"=")
    print("Testing corners")
    print(35*"=")

    b = Board(puzzle=np.array([[0, 1, 3, 4], [5, 6, 7, 8]]))
    print(f'\ntesting top-left corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True
    assert b.top_left_corner ^ b.top_right_corner ^ b.bottom_left_corner ^ b.bottom_right_corner, '0 cannot be at multiple corners at the same time'

    b = Board(puzzle=np.array([[2, 1, 3, 0], [5, 6, 7, 8]]))
    print(f'\ntesting top-right corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True
    assert b.top_left_corner ^ b.top_right_corner ^ b.bottom_left_corner ^ b.bottom_right_corner, '0 cannot be at multiple corners at the same time'

    b = Board(puzzle=np.array([[2, 1, 3, 4], [0, 6, 7, 8]]))
    print(f'\ntesting bottom-left corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True
    assert b.top_left_corner ^ b.top_right_corner ^ b.bottom_left_corner ^ b.bottom_right_corner, '0 cannot be at multiple corners at the same time'

    b = Board(puzzle=np.array([[2, 1, 3, 4], [5, 6, 7, 0]]))
    print(f'\ntesting bottom-right corner puzzle\n{b.puzzle}')
    assert b.is_corner() == True
    assert b.top_left_corner ^ b.top_right_corner ^ b.bottom_left_corner ^ b.bottom_right_corner, '0 cannot be at multiple corners at the same time'

    b = Board(puzzle=np.array([[2, 1, 3, 4], [5, 0, 7, 8]]))
    print(f'\ntesting no corner puzzle\n{b.puzzle}')
    assert b.is_corner() == False


def test_generate_regular_moves():

    print(35*"=")
    print("Testing regular moves for a 2x4 puzzle")
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

    def move_sorter(dict_el): return dict_el['end']  # sort the results by the end position on the 0-tile. The order of moves doesn't matter.

    expected_result = sorted(expected_result, key=move_sorter)

    actual_result = sorted(b.generate_regular_moves(), key=move_sorter)

    assert len(actual_result) == len(expected_result), "Number of moves generated should be equal"

    for i in range(len(actual_result)):
        assert actual_result[i]["start"] == expected_result[i]["start"],                                "start position should be equal"
        assert actual_result[i]["end"] == expected_result[i]["end"],                                    "end position should be equal"
        assert actual_result[i]["simple_cost"] == expected_result[i]["simple_cost"],                    "simple_cost of the move should be 1"
        assert np.array_equal(actual_result[i]["board"].puzzle, expected_result[i]["board"].puzzle),    "puzzle configuration is not correct"

    print('\n'+35*"=")
    print("Testing regular moves for a 4x4 puzzle")
    print(35*"="+'\n')

    board = Board(puzzle=np.array([
        [1, 2, 3, 4],
        [5, 6, 0, 7],
        [33, 44, 55, 66],
        [11, 22, 77, 88],
    ]))

    expected_boards = [
        Board(puzzle=np.array([  # up
            [1, 2, 0, 4],
            [5, 6, 3, 7],
            [33, 44, 55, 66],
            [11, 22, 77, 88],
        ])),
        Board(puzzle=np.array([  # left
            [1, 2, 3, 4],
            [5, 0, 6, 7],
            [33, 44, 55, 66],
            [11, 22, 77, 88],
        ])),
        Board(puzzle=np.array([  # right
            [1, 2, 3, 4],
            [5, 6, 7, 0],
            [33, 44, 55, 66],
            [11, 22, 77, 88],
        ])),
        Board(puzzle=np.array([  # down
            [1, 2, 3, 4],
            [5, 6, 55, 7],
            [33, 44, 0, 66],
            [11, 22, 77, 88],
        ]))
    ]

    expected_results = [
        {"start": (1, 2), "end": (0, 2), "board": expected_boards[0], "simple_cost": 1},
        {"start": (1, 2), "end": (1, 1), "board": expected_boards[1], "simple_cost": 1},
        {"start": (1, 2), "end": (1, 3), "board": expected_boards[2], "simple_cost": 1},
        {"start": (1, 2), "end": (2, 2), "board": expected_boards[3], "simple_cost": 1},
    ]

    actual_results = sorted(board.generate_regular_moves(), key=move_sorter)
    expected_results = sorted(expected_results, key=move_sorter)
    assert len(actual_results) == len(expected_results), 'length should be the same'

    for i in range(len(actual_results)):
        print('expected:')
        print(expected_results[i])
        print('actual:')
        print(actual_results[i])
        assert actual_results[i]["start"] == expected_results[i]["start"],                                "start position should be equal"
        assert actual_results[i]["end"] == expected_results[i]["end"],                                    "end position should be equal"
        assert actual_results[i]["simple_cost"] == expected_results[i]["simple_cost"],                    "simple_cost of the move should be 1"
        assert np.array_equal(actual_results[i]["board"].puzzle, expected_results[i]["board"].puzzle),    "puzzle configuration is not correct"


def test_generate_wrapping_moves():

    delimiter = 35*"="
    print(f'\n{delimiter}\nTesting wrapping moves 1\n{delimiter}\n')

    boards_that_should_wrap = [
        Board(puzzle=np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7]
        ])), Board(puzzle=np.array([
            [4, 1, 2, 3],
            [7, 5, 6, 0]
        ])), Board(puzzle=np.array([
            [4, 1, 2, 3],
            [7, 5, 6, 81],
            [9, 8, 34, 0]
        ]))
    ]

    expected_results = [
        [
            {'start': (0, 0), 'end': (0, 3), 'board': Board(puzzle=np.array([
                [3, 1, 2, 0],
                [4, 5, 6, 7]
            ])), 'simple_cost': 2}
        ],

        [
            {'start': (1, 3), 'end': (1, 0), 'board': Board(puzzle=np.array([
                [4, 1, 2, 3],
                [0, 5, 6, 7]
            ])), 'simple_cost': 2}
        ],

        [
            {'start': (2, 3), 'end': (2, 0), 'board': Board(puzzle=np.array([
                [4, 1, 2, 3],
                [7, 5, 6, 81],
                [0, 8, 34, 9]
            ])), 'simple_cost': 2},
            {'start': (2, 3), 'end': (0, 3), 'board': Board(puzzle=np.array([
                [4, 1, 2, 0],
                [7, 5, 6, 81],
                [9, 8, 34, 3]
            ])), 'simple_cost': 2}
        ]
    ]
    def move_sorter(dict_el): return dict_el['end']  # sort the results by the end position on the 0-tile. The order of moves doesn't matter.

    for j in range(len(boards_that_should_wrap)):
        board = boards_that_should_wrap[j]
        expected_result = sorted(expected_results[j], key=move_sorter)
        actual_result = sorted(board.generate_wrapping_moves(), key=move_sorter)

        print(f'board that should wrap looks like:\n{board.puzzle}')
        print(f'expected wrapping moves:\n{expected_result}')
        print(f'actual wrapping moves generated:\n{actual_result}')

        assert len(actual_result) == len(expected_result), "Number of moves generated should be equal"

        for i in range(len(actual_result)):
            assert actual_result[i]["start"] == expected_result[i]["start"],                                "start position should be equal"
            assert actual_result[i]["end"] == expected_result[i]["end"],                                    "end position should be equal"
            assert actual_result[i]["simple_cost"] == expected_result[i]["simple_cost"],                    "simple_cost of the move should be 1"
            assert np.array_equal(actual_result[i]["board"].puzzle, expected_result[i]["board"].puzzle),    "puzzle configuration is not correct"

    boards_that_should_not_wrap = [
        Board(puzzle=np.array([
            [1, 0, 2, 3],
            [4, 5, 6, 7]
        ])), Board(puzzle=np.array([
            [1, 6, 2, 3],
            [4, 5, 0, 7]
        ])),         Board(puzzle=np.array([
            [1, 9, 2, 3],
            [4, 5, 6, 7],
            [14, 15, 0, 17]
        ])), Board(puzzle=np.array([
            [1, 9, 2, 3],
            [0, 5, 6, 7],
            [4, 15, 14, 17]
        ])),
    ]

    for board in boards_that_should_not_wrap:
        assert len(board.generate_wrapping_moves()) == 0, "Should return an empty list"


def test_generate_diagonal_moves():
    delimiter = 35*"="
    print(f'\n{delimiter}\nTesting diagnonal moves 1\n{delimiter}\n')

    boards_that_should_have_diag = [
        Board(puzzle=np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7]
        ])), Board(puzzle=np.array([
            [4, 1, 2, 3],
            [7, 5, 6, 0]
        ])), Board(puzzle=np.array([
            [4, 1, 2, 3],
            [7, 5, 6, 81],
            [9, 8, 34, 0]
        ]))
    ]

    expected_results = [
        [
            {'start': (0, 0), 'end': (1, 1), 'board': Board(puzzle=np.array([
                [5, 1, 2, 3],
                [4, 0, 6, 7]
            ])), 'simple_cost': 3},
            {'start': (0, 0), 'end': (1, 3), 'board': Board(puzzle=np.array([
                [7, 1, 2, 3],
                [4, 5, 6, 0]
            ])), 'simple_cost': 3}
        ],
        [
            {'start': (1, 3), 'end': (0, 0), 'board': Board(puzzle=np.array([
                [0, 1, 2, 3],
                [7, 5, 6, 4]
            ])), 'simple_cost': 3},
            {'start': (1, 3), 'end': (0, 2), 'board': Board(puzzle=np.array([
                [4, 1, 0, 3],
                [7, 5, 6, 2]
            ])), 'simple_cost': 3},
        ],
        [
            {'start': (2, 3), 'end': (0, 0), 'board': Board(puzzle=np.array([
                [0, 1, 2, 3],
                [7, 5, 6, 81],
                [9, 8, 34, 4]
            ])), 'simple_cost': 3},
            {'start': (2, 3), 'end': (1, 2), 'board': Board(puzzle=np.array([
                [4, 1, 2, 3],
                [7, 5, 0, 81],
                [9, 8, 34, 6]
            ])), 'simple_cost': 3},
        ]
    ]

    def move_sorter(dict_el): return dict_el['end']  # sort the results by the end position on the 0-tile. The order of moves doesn't matter.

    for j in range(len(boards_that_should_have_diag)):
        board = boards_that_should_have_diag[j]
        expected_result = sorted(expected_results[j], key=move_sorter)
        actual_result = sorted(board.generate_diagonal_moves(), key=move_sorter)
        assert len(actual_result) == 2  # if you are at a corner, you can always perform exactly two moves

        print(f'board that should have a diagonal looks like:\n{board.puzzle}')
        print(f'expected diagonal moves:\n{expected_result}')
        print(f'actual diagonal moves generated:\n{actual_result}')

        assert len(actual_result) == len(expected_result), "Number of moves generated should be equal"

        for i in range(len(actual_result)):
            assert actual_result[i]["start"] == expected_result[i]["start"],                                "start position should be equal"
            assert actual_result[i]["end"] == expected_result[i]["end"],                                    "end position should be equal"
            assert actual_result[i]["simple_cost"] == expected_result[i]["simple_cost"],                    "simple_cost of the move should be 1"
            assert np.array_equal(actual_result[i]["board"].puzzle, expected_result[i]["board"].puzzle),    "puzzle configuration is not correct"

    boards_that_dont_have_diagonal_moves = [
        Board(puzzle=np.array([
            [1, 0, 2, 3],
            [4, 5, 6, 7]
        ])), Board(puzzle=np.array([
            [1, 6, 2, 3],
            [4, 5, 0, 7]
        ])),         Board(puzzle=np.array([
            [1, 9, 2, 3],
            [4, 5, 6, 7],
            [14, 15, 0, 17]
        ])), Board(puzzle=np.array([
            [1, 9, 2, 3],
            [0, 5, 6, 7],
            [4, 15, 14, 17]
        ])),
    ]

    for board in boards_that_dont_have_diagonal_moves:
        assert len(board.generate_diagonal_moves()) == 0


def test_move_row_out_of_bounds():  # numpy indices characterization test
    print()
    print(35*"=")
    print("Testing bad moves part 1")
    print(35*"=")

    b = Board(puzzle=np.array([[1, 2, 3, 4], [5, 0, 7, 8]]))
    print(f'\ninitial puzzle\n{b.puzzle}')
    print()

    bad_move = np.copy(b.puzzle)
    try:
        bad_move[(1, 1)], bad_move[(2, 1)] = bad_move[(2, 1)], bad_move[(1, 1)]

    except IndexError:
        print("Assertion caught!")
        assert True
    assert True, 'Assertion not caught'

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

    assert True, 'Assertion not caught'
