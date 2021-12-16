"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import deque
from structures import Grid, PriorityQueue


class Node:
    def __init__(self, coordinate, parent=None):
        """
        :param (int,int) coordinate: TODO EXPLAIN
        :param Node parent:
        """
        self.parent = parent
        self.position = coordinate

        self.g = 0
        self.f = 0
        self.h = 0

    def __lt__(self, other):
        """
        TODO EXPLAIN

        :param Node other:

        :return:
        :rtype: bool
        """
        return self.f < other.f

    def __eq__(self, other):
        """
        TODO EXPLAIN

        :param Node other:

        :return:
        :rtype: bool
        """
        return self.position == other.position

    def __repr__(self):
        return f"({self.position[0]},{self.position[1]}): g{self.g} f{self.f} h{self.h}"


def resolve_path(current_node):
    """
    TODO EXPLAIN

    :param Node current_node:

    :return:
    :rtype: list[(int,int)]
    """

    # Follow the chain of nodes up to root
    visitation_order = deque()  # type: typing.Deque[typing.Tuple[int,int]]
    while current_node is not None:
        visitation_order.appendleft(current_node.position)
        current_node = current_node.parent

    return list(visitation_order)


def search(grid, start_coordinates, goal_coordinates):
    """
    A* search algorithm, inspired by:
    https://towardsdatascience.com/a-star-a-search-algorithm-eb495fb156bb

    :param Grid grid:
    :param (int,int) start_coordinates:
    :param (int, int) goal_coordinates:

    :return:
    :rtype: list[(int,int)] | None
    """

    # Initialize the 'yet-to-visit' and 'visited' structures
    frontier = PriorityQueue()
    finalized = set()     # type: typing.Set[typing.Tuple[int,int]]

    # Introduce the start node to the frontier
    start_node = Node(start_coordinates)
    frontier.push(start_node)

    # While there are nodes to search...
    path = None  # type: typing.Optional[typing.List[typing.Tuple[int,int]]]
    while len(frontier) > 0:
        # Transfer the next node out of the pending nodes and into the processed nodes; if it was the goal node, then
        # we're done
        optimal_node = frontier.pop()   # type: Node
        finalized.add(optimal_node.position)
        if optimal_node.position == goal_coordinates:
            path = resolve_path(optimal_node)
            break

        # Introduce this node's neighbors to the frontier
        for move_direction in (Grid.DOWN, Grid.RIGHT):
            try:
                next_coordinates = grid.move(optimal_node.position, move_direction)
            except IndexError:
                continue

            # Disqualify this destination if it's already been visited
            if next_coordinates in finalized:
                continue

            # Define the destination's properties, then add to the 'yet to visit' list
            destination = Node(next_coordinates, parent=optimal_node)
            destination.g = optimal_node.g + grid[next_coordinates]
            destination.h = (
                    abs(destination.position[0] - goal_coordinates[0]) +
                    abs(destination.position[1] - goal_coordinates[1])
                )
            destination.f = destination.g + destination.h
            frontier.push(destination)

    return path


def expand(grid, factor):
    """
    TODO EXPLAIN

    :param Grid grid:
    :param int factor:

    :return:
    :rtype: Grid
    """

    # Resolve the dimensions of the expanded grid to be returned
    new_height = grid.height * factor
    new_width = grid.width * factor
    new_quantity = new_height * new_width

    # Initialize a new grid of the expanded dimensions
    new_grid = Grid([0 for _ in range(new_quantity)], new_height)

    # For each cell of the expanded, initialized grid...
    for i in range(new_grid.height):
        for j in range(new_grid.width):
            # Expansion involves expanding to a multiple of the original number of rows/cols; the values therein are
            # based on those of the original board; for this position, resolve the original board position to which it
            # corresponds
            basis_position = (i % grid.height, j % grid.width)
            basis_value = grid[basis_position]

            # If this board is N over from the original board, then the value should be incremented N times
            tiles_down = i // grid.height           # number of original board-heights down from the original board
            tiles_over = j // grid.width            # number of original board-widths over from the original board
            adjustment = tiles_over + tiles_down    # adjustments to apply to

            # Values are on a 1-based, 9-digit system; before applying the adjustment, downshift to a 0-based system,
            # apply the adjustment, MOD 9, then up-shift back to the 1-based system
            adjusted_value = (((basis_value-1) + adjustment) % 9) + 1
            new_grid[i, j] = adjusted_value

    return new_grid


def find_path(board):
    """
    TODO EXPLAIN

    :param Grid board:

    :return:
    :rtype: (int, list[(int,int)])
    """

    begin = (0, 0)
    goal = (board.height-1, board.width-1)

    import time
    begin_time = time.time()
    path = search(board, begin, goal)
    total_time = time.time() - begin_time
    score = sum(board[coordinate] for coordinate in path) - board[begin]
    print(f"{score} in {total_time:2.2f}s. for path across {board.height}x{board.width} grid: {path}")

    return score, path


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    # Part 1
    score, path = find_path(board)

    # Part 2
    board = expand(board, 5)
    score, path = find_path(board)


if __name__ == "__main__":
    main()
