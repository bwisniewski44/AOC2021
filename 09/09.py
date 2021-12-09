"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing


class Grid(object):
    """
    TODO EXPLAIN
    """

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    MODIFICATION_BY_MOVE = {
        UP: (-1, 0),
        DOWN: (1, 0),
        LEFT: (0, -1),
        RIGHT: (0, 1),
    }

    def __init__(self, sequence, height):
        """
        :param list[int] sequence:
        :param int height:
        """

        self._values = sequence
        self._height = height
        self._width = len(sequence) // height

        if self._width * self._height != len(sequence):
            raise \
                ValueError(
                    f"Illegal height {height} for {len(sequence)}-length value sequence; height must be a whole-number "
                    f"factor of sequence"
                )

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def in_bounds(self, i, j):
        return (0 <= i < self.height) and (0 <= j < self.width)

    def at(self, i, j):
        """
        TODO EXPLAIN

        :param int i:
        :param int j:

        :return:
        :rtype: int
        """

        if not (0 <= i < self.height):
            raise ValueError(f"Row index {i} violates legal range [0,{self.height})")
        if not (0 <= j < self.width):
            raise ValueError(f"Col index {j} violates legal range [0,{self.width})")

        index = self.width * i + j
        return self._values[index]

    def move(self, coordinate, direction):
        modification = self.MODIFICATION_BY_MOVE[direction]
        result_row = coordinate[0] + modification[0]
        result_col = coordinate[1] + modification[1]

        if self.in_bounds(result_row, result_col):
            return result_row, result_col
        else:
            raise IndexError(f"({result_row},{result_col}) out of bounds for {self.height}x{self.width} grid")

    def __getitem__(self, pos):
        """
        TODO EXPLAIN

        :param int|(int,int) pos:

        :return:
        :rtype: int
        """
        if isinstance(pos, int):
            index = pos
        else:
            row, col = pos
            if not self.in_bounds(row, col):
                raise IndexError(f"Coordinates ({row},{col}) out-of-range for {self.height}x{self.width} grid")
            index = self.width * row + col

        return self._values[index]


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: Grid
    """

    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    digits = "".join(lines)
    value_sequence = [int(digit) for digit in list(digits)]
    grid = Grid(value_sequence, len(lines))

    return grid


def assess_risk(height_ranking):
    """
    TODO EXPLAIN

    :param int height_ranking:

    :return:
    :rtype: int
    """
    return height_ranking + 1


def add_adjacent_value(values, grid, coordinate, direction):
    """
    TODO EXPLAIN

    :param set[int] values:
    :param Grid grid:
    :param (int,int) coordinate:
    :param int direction:

    :return: None
    """

    try:
        adjacency_row, adjacency_col = grid.move(coordinate, direction)
    except IndexError:
        pass
    else:
        value = grid.at(adjacency_row, adjacency_col)
        values.add(value)


def find_minima(grid):
    """
    TODO EXPLAIN

    :param Grid grid:

    :return:
    :rtype: set[(int,int)]
    """

    minima = set()  # type: typing.Set[typing.Tuple[int,int]]

    for i in range(grid.height):
        for j in range(grid.width):
            height_ranking = grid.at(i, j)

            # Resolve all the different height-rankings of adjacent spaces
            adjacent_values = set()  # type: typing.Set[int]
            for direction in {Grid.UP, Grid.DOWN, Grid.LEFT, Grid.RIGHT}:
                add_adjacent_value(adjacent_values, grid, (i, j), direction)

            # This coordinate points to a valley if its height ranking is lower than those of its adjacent values
            if height_ranking < min(adjacent_values):
                minima.add(
                    (i, j)
                )

    return minima


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    grid = load_input()
    minima = find_minima(grid)
    print(sum(assess_risk(grid[coordinate]) for coordinate in minima))


if __name__ == "__main__":
    main()
