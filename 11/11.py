"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import deque
from structures import Grid

_DISCHARGE_THRESHOLD = 10


def increment(grid, coordinate):
    """
    TODO EXPLAIN

    :param Grid grid:
    :param (int,int) coordinate:

    :return:
    :rtype: bool
    """

    updated_level = grid[coordinate] + 1
    grid[coordinate] = updated_level

    return updated_level == _DISCHARGE_THRESHOLD


def do_round(grid):
    """
    TODO EXPLAIN

    :param Grid grid:

    :return: number of coordinates at which discharge occurred
    :rtype: int
    """

    # The initial batch of coordinates to increment includes all those on the board!
    coordinates_to_increment = deque(
        (i, j) for i in range(grid.height) for j in range(grid.width)
    )  # type: typing.Deque[typing.Tuple[int,int]]

    discharging_coordinates = set()  # type: typing.Set[typing.Tuple[int,int]]
    while coordinates_to_increment:
        next_coordinate = coordinates_to_increment.popleft()
        reached_threshold = increment(grid, next_coordinate)

        if reached_threshold:
            discharging_coordinates.add(next_coordinate)
            for direction in Grid.DIRECTIONS:
                try:
                    neighbor = grid.move(next_coordinate, direction)
                except IndexError:
                    continue  # oh well... must be at edge of board
                coordinates_to_increment.append(neighbor)

    # Excitability has settled; apply the flashes
    coordinates_discharged = len(discharging_coordinates)
    for i, j in discharging_coordinates:
        grid[i, j] = 0

    return coordinates_discharged


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    grid = Grid.load("input.txt")

    discharges = 0
    for _ in range(100):
        discharges += do_round(grid)
    print(discharges)


if __name__ == "__main__":
    main()
