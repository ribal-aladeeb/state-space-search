from node import Node
import numpy as np
import math


def hamming_distance(n: Node) -> int:
    '''
    This heuristic will return the number of tiles out of place.
    '''

    goal_states = n.board.generate_goal_states()
    tiles_out_of_place = []
    for state in goal_states:
        config = n.board.puzzle.flatten()
        x = np.where(config != state)[0]
        num_tiles = len(x)
        tiles_out_of_place.append(num_tiles)

    return int(min(tiles_out_of_place))


def manhattan_distance(n: Node) -> int:

    goal_states = n.board.generate_goal_states()
    puzzle = n.board.puzzle
    man_dist = [0, 0]  # one for each goal state, always 2

    for i in range(len(goal_states)):
        goal = goal_states[i].reshape(n.board.puzzle.shape)

        for y in range(puzzle.shape[0]):  # x y are grid coordinate
            for x in range(puzzle.shape[1]):

                tile_value = puzzle[y, x]
                if tile_value == 0:
                    continue
                goal_coordinate = np.where(goal == tile_value)
                y_goal = goal_coordinate[0][0]
                x_goal = goal_coordinate[1][0]

                distance = math.fabs(y_goal-y) + math.fabs(x_goal-x)
                man_dist[i] += int(distance)

    return min(man_dist)


def row_col_out_of_place(n: Node) -> int:
    '''
    This heuristic computes the number of tiles out of row place and column place.
    '''

    goal_states = n.board.generate_goal_states()
    rows, cols = n.board.puzzle.shape

    total_out_of_place = [0, 0]  # always exactly 2

    for i in range(len(goal_states)):
        out_of_row_place = np.zeros(rows)
        out_of_column_place = np.zeros(cols)

        puzzle = n.board.puzzle
        state = goal_states[i].reshape(rows, cols)

        # out of place rows
        for j in range(rows):
            current_row = set(puzzle[j])
            goal_row = set(state[j])
            out_of_row_place[i] += sum([c not in goal_row for c in current_row])

        # out of place columns
        for k in range(cols):
            current_col = set(puzzle[:, k])
            goal_col = set(state[:, k])
            out_of_column_place[k] += sum([c not in goal_col for c in current_col])

        total_out_of_place[i] = sum(out_of_row_place) + sum(out_of_column_place)

    return int(min(total_out_of_place))


def euclidean_distance(n: Node) -> int:
    '''
    This heuristic computes the Euclidean distance of the tiles.
    '''

    goal_states = n.board.generate_goal_states()
    rows, cols = n.board.puzzle.shape

    total_euclidean = [0, 0]  # always exactly 2

    for i in range(len(goal_states)):
        state = goal_states[i].reshape(rows, cols)
        puzzle = n.board.puzzle
        total_euclidean[i] = np.linalg.norm(puzzle - state)

    return int(min(total_euclidean))


def permutation_inversion(n: Node) -> int:
    '''
    This heuristic computes the permutation inversion of the tiles.
    '''

    goal_states = n.board.generate_goal_states()

    total = [0, 0]  # always exactly 2

    for i in range(len(goal_states)):
        for j in range(len(n.board.puzzle.flatten())):
            total[i] += abs(j - np.where(goal_states[i] == n.board.puzzle.flatten()[j])[0][0])

    return int(min(total))
