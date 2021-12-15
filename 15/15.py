"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from math import factorial
from structures import Grid

DECLINED = 0


class Results:
    def __init__(self, max_penalty):
        """
        :param int max_penalty: TODO EXPLAIN
        """
        self.score = max_penalty    # type: int
        self.steps = None           # type: typing.Optional[typing.List[typing.Tuple[int,int]]]    # seq. of coords


def calculate_paths(begin_coordinates, end_coordinates):
    """
    Gives the number of combinations of HORIZONTAL and VERTICAL moves required to get from an origin coordinate to an
    end coordinate.

    :param (int,int) begin_coordinates:
    :param (int,int) end_coordinates:

    :return:
    :rtype: int
    """

    x_delta = abs(end_coordinates[0] - begin_coordinates[0])
    y_delta = abs(end_coordinates[1] - begin_coordinates[1])

    combinations = factorial(x_delta + y_delta) // (factorial(x_delta) * factorial(y_delta))

    return combinations


def populate_optimum(results, grid, path, stop, accumulated_penalty, legal_moves):
    """
    Gives the score associated with the optimal path from the given coordinate of the board to the goal coordinate.

    :param Results results: container into which to place optima
    :param Grid grid: board over which to traverse
    :param list[(int,int)] path: sequence of coordinates entered
    :param (int,int) stop: coordinate of position to reach
    :param int accumulated_penalty: penalty for all elements in path
    :param set[int] legal_moves: codes identifying the legal directions in which movement towards goal may occur

    :return: None
    """

    # BASE CASE: the current penalty has already accrued to a value in excess of that for the current optimum; we can
    # stop trying
    if results.score <= accumulated_penalty:
        global DECLINED
        DECLINED += 1
        if DECLINED % 10000 == 0:
            print(f"Shorted {DECLINED} paths")

    # Otherwise, this penalty is lower than that which is the current optimum; if we're at the goal position, then we
    # have a new optimum
    elif path[-1] == stop:
        results.score = accumulated_penalty
        results.steps = list(path)
        print(f"Found optimum {results.score}")

    # Otherwise, the current score is still better than the latest optimum, but we've yet to reach the necessary
    # position; let's continue accruing penalty as we head towards the goal
    else:
        for direction in {Grid.DOWN, Grid.RIGHT}:
            # Resolve the coordinate to which to move
            try:
                next_coordinate = grid.move(path[-1], direction)  # IndexError if out-of-bounds
                destination_penalty = grid[next_coordinate]
            except IndexError:
                continue  # oh well, must be at edge of grid

            # Introduce the destination to the path
            path.append(next_coordinate)
            accumulated_penalty += destination_penalty
            populate_optimum(results, grid, path, stop, accumulated_penalty, legal_moves)

            # Back away from the destination
            path.pop()
            accumulated_penalty -= destination_penalty


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    goal = (board.height-1, board.width-1)
    results = Results(board.width * board.height * 9)
    current_path = [(0, 0)]
    populate_optimum(results, board, current_path, goal, 0, {Grid.DOWN, Grid.RIGHT})
    print(f"{results.score}: {results.steps}")


if __name__ == "__main__":
    main()
