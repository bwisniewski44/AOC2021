"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from structures import Grid


def find_optimal_path_from(grid, coordinate=None, current_path=None, current_score=0):
    """
    TODO EXPLAIN

    :param Grid grid:
    :param (int,int) coordinate:
    :param list[(int,int)] current_path:
    :param int current_score:

    :return: gives a 2-tuple consisting of...
      1. list[(int,int)] - sequence of coordinates visited
      2. int - score associated with the sequence
    :rtype: (list[(int,int)], int)
    """

    # Initialize any undefined structures (root call may be omitting these)
    if coordinate is None:
        coordinate = (0, 0)
    if current_path is None:
        current_path = []

    # Add the coordinate to the current path apply its score to the sum
    copied_path = list(current_path)
    copied_path.append(coordinate)
    current_score += grid[coordinate]

    # BASE CASE: we're at the goal position
    row, col = coordinate
    if row+1 == grid.height and col+1 == grid.width:
        result_path = copied_path
        result_score = current_score

    # RECURSIVE CASE: we have to choose the optimal of two paths: one if moving to the right, another moving downwards
    else:
        result_path, result_score = None, 0
        for direction in {Grid.DOWN, Grid.RIGHT}:
            # Resolve the coordinate to which to move
            try:
                next_coordinate = grid.move(coordinate, direction)  # IndexError if out-of-bounds
            except IndexError:
                continue  # oh well, must be at edge of grid

            # Get the optimal path from that coordinate
            inner_path, inner_score = find_optimal_path_from(grid, next_coordinate, copied_path, current_score)

            # Compare that path to any current result; if no current result, or latest path is better than current
            # result, update the current result
            if result_path is None or inner_score < result_score:
                result_path = inner_path
                result_score = inner_score

    return result_path, result_score


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    result_path, result_score = find_optimal_path_from(board)
    print(result_score)


if __name__ == "__main__":
    main()
