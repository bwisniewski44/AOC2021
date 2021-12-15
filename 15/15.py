"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from structures import Grid

DECLINED = 0


def populate_optimum(grid, goal, current_optimum, coordinate=(0, 0), current_score=0):
    """
    Gives the score associated with the optimal path from the given coordinate of the board to the goal coordinate.

    :param Grid grid: board over which to traverse
    :param (int,int) goal: position marking the end of the path
    :param int current_optimum:
    :param (int,int) coordinate: latest-entered position; this shall either be the goal position (base case) or that
      from which to move towards the goal position
    :param int current_score: score already accumulated by entering the given coordinate

    :return: score associated with most-optimal path from the given coordinate
    :rtype: int
    """

    # BASE CASE: the optimum is already better than this competing score - stop trying
    if current_optimum <= current_score:
        optimum = current_optimum
        global DECLINED
        DECLINED += 1
        if DECLINED % 10000 == 0:
            print(f"Shorted {DECLINED} paths")

    # BASE CASE: we're at the goal position... this must be the new optimum
    elif coordinate == goal:
        optimum = current_score
        print(f"Found optimum {optimum}")

    # RECURSIVE CASE: the current score is still better than the latest optimum, but we've yet to reach the necessary
    # position; let's continue accumulating onto this competing score as we head towards the goal
    else:
        optimum = current_optimum
        for direction in {Grid.DOWN, Grid.RIGHT}:
            # Resolve the coordinate to which to move
            try:
                next_coordinate = grid.move(coordinate, direction)  # IndexError if out-of-bounds
            except IndexError:
                continue  # oh well, must be at edge of grid
            destination_value = grid[next_coordinate]
            optimum = \
                populate_optimum(
                    grid, goal, optimum, coordinate=next_coordinate, current_score=current_score+destination_value
                )

    return optimum


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    goal = (board.height-1, board.width-1)
    result = populate_optimum(board, goal, board.width * board.height * 9)
    print(result)


if __name__ == "__main__":
    main()
