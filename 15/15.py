"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""
import math
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


def get_pass(key, remaining_passes_by_key):
    """
    TODO EXPLAIN

    :param key:
    :param dict[int,int] remaining_passes_by_key:

    :return: TRUE if a pass was granted
    :rtype: bool | None
    """

    if key not in remaining_passes_by_key:
        return None
    else:
        remaining_passes = remaining_passes_by_key[key]
        if remaining_passes == 0:
            return False
        else:
            remaining_passes_by_key[key] = remaining_passes - 1
            return True


def update_declined(current_minimum):
    global DECLINED
    DECLINED += 1
    if DECLINED % 100000 == 0:
        print(f"Shorted {DECLINED} times; current min: {current_minimum}")


def populate_optimum(results, grid, path, stop, accumulated_penalty, legal_moves, limit_by_penalty):
    """
    Gives the score associated with the optimal path from the given coordinate of the board to the goal coordinate.

    :param Results results: container into which to place optima
    :param Grid grid: board over which to traverse
    :param list[(int,int)] path: sequence of coordinates entered
    :param (int,int) stop: coordinate of position to reach
    :param int accumulated_penalty: penalty for all elements in path
    :param set[int] legal_moves: codes identifying the legal directions in which movement towards goal may occur
    :param dict[int,int] limit_by_penalty:

    :return: None
    """

    global DECLINED

    # BASE CASE: the current penalty has already accrued to a value in excess of that for the current optimum; we can
    # stop trying
    if results.score <= accumulated_penalty:
        update_declined(results.score)

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

            acquired = get_pass(destination_penalty, limit_by_penalty)
            if acquired is False:
                update_declined(results.score)
                continue

            # Introduce the destination to the path
            path.append(next_coordinate)
            accumulated_penalty += destination_penalty
            populate_optimum(results, grid, path, stop, accumulated_penalty, legal_moves, limit_by_penalty)

            # Back away from the destination
            path.pop()
            accumulated_penalty -= destination_penalty
            if acquired:
                limit_by_penalty[destination_penalty] += 1


def build_allowances(begin, end, allowance):
    """
    TODO EXPLAIN

    :param (int,int) begin:
    :param (int,int) end:
    :param float allowance: percentage of moves which may be the maximally-costly

    :return:
    :rtype: dict[int,int]
    """

    allowances_by_penalty = {}
    total_moves = sum(abs(end[i] - begin[i]) for i in range(len(end)))
    exponent = math.log(1/allowance) / math.log(9)
    for penalty in range(1, 9+1):
        allowance = math.floor(total_moves / math.pow(penalty, exponent) + 0.5)
        allowances_by_penalty[penalty] = allowance

    return allowances_by_penalty


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    begin = (0, 0)
    goal = (board.height-1, board.width-1)
    allowances_by_penalty = build_allowances(begin, goal, 0.15)

    results = Results(board.width * board.height * 9)
    current_path = [begin]
    populate_optimum(results, board, current_path, goal, 0, {Grid.DOWN, Grid.RIGHT}, allowances_by_penalty)
    print(f"{results.score}: {results.steps}")


if __name__ == "__main__":
    main()
