"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from structures import Grid


def find_optimal_path_from(grid, coordinate=(0, 0), current_score=0):
    """
    Gives the score associated with the optimal path from the given coordinate of the board to the goal coordinate.

    :param Grid grid: board over which to traverse
    :param (int,int) coordinate: latest-entered position; the position from which to move to another
    :param int current_score: score already accumulated by entering the given coordinate

    :return: score associated with most-optimal path from the given coordinate
    :rtype: int
    """

    # BASE CASE: we're at the goal position
    row, col = coordinate
    if row+1 == grid.height and col+1 == grid.width:
        result_score = current_score

    # RECURSIVE CASE: we have to choose the optimal of two paths: one if moving to the right, another moving downwards
    else:
        result_score = None
        for direction in {Grid.DOWN, Grid.RIGHT}:
            # Resolve the coordinate to which to move
            try:
                next_coordinate = grid.move(coordinate, direction)  # IndexError if out-of-bounds
            except IndexError:
                continue  # oh well, must be at edge of grid
            destination_value = grid[next_coordinate]
            inner_score = find_optimal_path_from(grid, next_coordinate, current_score + destination_value)
            if result_score is None or inner_score < result_score:
                result_score = inner_score

    return result_score


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    result_score = find_optimal_path_from(board)
    print(result_score)


if __name__ == "__main__":
    main()
