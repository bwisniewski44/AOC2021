"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import time
import sys
import typing
from collections import defaultdict
from structures import Grid, PriorityQueue, load_int_block


def expand(grid, factor):
    """
    TODO EXPLAIN

    :param Grid[int] grid:
    :param int factor:

    :return:
    :rtype: Grid[int]
    """

    # Resolve the dimensions of the expanded grid to be returned
    new_height = grid.height * factor
    new_width = grid.width * factor

    # Initialize a new grid of the expanded dimensions
    new_grid = Grid(height=new_height, width=new_width)

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

    :param Grid[int] board:

    :return:
    :rtype: (int, list[(int,int)])
    """

    # Define the start and goal positions (top-left to bottom-right)
    begin = (0, 0)
    goal = (board.height-1, board.width-1)

    # Perform the search; note down the start-time before doing so: let's measure how long it takes
    begin_time = time.time()
    path = dijkstras_search(board, begin, goal)
    total_time = time.time() - begin_time

    # A path was returned; the score is the sum of its parts (less the begin node... the puzzle dictates that its cost
    # is not incurred)
    score = sum(board[coordinate] for coordinate in path) - board[begin]
    print(f"{score} in {total_time:2.2f}s. for path across {board.height}x{board.width} grid: {path}")

    return score, path


def resolve_path(parent_by_node, leaf):
    """
    TODO EXPLAIN

    :param dict[(int,int), (int,int)|None] parent_by_node:
    :param (int,int) leaf:

    :return:
    :rtype: list[(int,int)]
    """

    leaf_to_root = [leaf]
    current_node = leaf
    while current_node in parent_by_node:
        current_node = parent_by_node[current_node]
        leaf_to_root.append(current_node)

    root_to_leaf = leaf_to_root[::-1]  # reverse the list
    return root_to_leaf


def dijkstras_search(grid, start, goal):
    """
    TODO EXPLAIN

    :param Grid[int] grid:
    :param (int,int) start:
    :param (int,int) goal:

    :return:
    :rtype: list[(int,int)]
    """

    finalized_coordinates = set()   # type: typing.Set[typing.Tuple[int,int]]
    parent_by_node = {}             # type: typing.Dict[typing.Tuple[int,int], typing.Tuple[int,int]]

    priority_queue = PriorityQueue()
    travel_cost_by_node = defaultdict(lambda: sys.maxsize)  # type: typing.Dict[typing.Tuple[int,int], int]

    # Introduce the initial node, then begin the search loop
    travel_cost_by_node[start] = 0
    priority_queue.push(start, 0)
    while priority_queue:
        # Pop the next node from the queue; as it is that which is most-optimal, it is now finalized; in fact, if it's
        # the goal node, then we've finalized an optimal route and can stop
        finalized_node = priority_queue.pop()
        finalized_coordinates.add(finalized_node)
        if finalized_node == goal:
            break

        # Perhaps this optimal route to the current node offers a newly-optimal route to its neighbors; for each
        # neighbor...
        for direction in (Grid.DOWN, Grid.RIGHT, Grid.UP, Grid.LEFT):
            # ... resolve the neighbor node; skip if it has already been finalized
            try:
                neighbor = grid.move(finalized_node, direction)
            except IndexError:
                continue
            if neighbor in finalized_coordinates:
                continue

            # Determine the cost involved with travelling to the neighbor from this node; if that cost is less than its
            # current cost...
            prospective_travel_cost = travel_cost_by_node[finalized_node] + grid[neighbor]
            if prospective_travel_cost < travel_cost_by_node[neighbor]:
                # ... register the newly-optimal cost
                parent_by_node[neighbor] = finalized_node
                travel_cost_by_node[neighbor] = prospective_travel_cost

                # Add the neighbor to the priority queue
                priority_queue.push(neighbor, prospective_travel_cost)

    path = resolve_path(parent_by_node, goal)
    return path


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = load_int_block("input.txt")

    # Part 1
    score, path = find_path(board)

    # Part 2
    board = expand(board, 5)
    score, path = find_path(board)


if __name__ == "__main__":
    main()
