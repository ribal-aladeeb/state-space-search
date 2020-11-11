from __future__ import annotations  # in order to allow type hints for a class referring to itself
from typing import List
from board import Board
from queue import PriorityQueue
import numpy as np


class Node:

    def __init__(self,
                 move: dict = None,
                 parent: Node = None,
                 simple_cost: int = 0,
                 is_root: bool = False,
                 board: Board = None):

        if is_root:
            assert board != None, "There should be a board argument if is_root=True"
            self.board = board
            self.start = (np.nan, np.nan)
            self.end = (np.nan, np.nan)
            self.total_cost = 0
        else:
            assert move != None, "A node should always be created with a move argument when not root"
            assert parent != None, "If a node is not root, parent cannot be None"
            self.start: tuple = move['start']
            self.end: tuple = move['end']
            self.board: Board = move['board']
            self.total_cost = simple_cost + parent.total_cost

        self.parent: Board = parent

    def successors(self) -> List[Node]:
        moves: List[dict] = self.board.generate_all_moves()
        successors: List[Node] = []

        for move in moves:
            child = Node(move=move, parent=self, simple_cost=move['simple_cost'])
            successors.append(child)

        return successors

    def is_goal_state(self) -> bool:
        return self.board.is_goal_state()


def uniform_cost(board: Board) -> Node:
    root = Node(is_root=True, board=board)

    open_list = PriorityQueue()       # even though not python list, naming is keep for consistency with state space search theory
    closed_list = {}                # even though not python list, naming is keep for consistency with state space search theory

    total_visited = 1
    open_list.put((root.total_cost, total_visited, root))

    while not open_list.empty():
        total_visited += 1
        _, _, current_node = open_list.get()

        if current_node.is_goal_state():
            return current_node

        hashed = hash(tuple(current_node.board.puzzle.flatten()))

        if hashed in closed_list:  # This board configuration has been seen before
            if closed_list[hashed].total_cost < current_node.total_cost:
                continue  # we previously got to this configuration with lower cost than we do right now so ignore

        closed_list[hashed] = current_node
        for s in current_node.successors():
            total_visited += 1
            open_list.put((s.total_cost, total_visited, s))

        if total_visited % 1000 == 0:
            print(f'Visited {total_visited} nodes', end='\r')


if __name__ == "__main__":
    start_puzzle: Board = Board(puzzle=np.array(np.arange(8).reshape(2, 4)))
    print(f'start puzzle:\n{start_puzzle}')
    result: Node = uniform_cost(start_puzzle)
    print(f'resulting puzzle with cost {result.total_cost}:\n{result.board}')
