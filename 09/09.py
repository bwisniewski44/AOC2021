"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""


class Grid(object):
    """
    TODO EXPLAIN
    """

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

    def __getitem__(self, index):
        """
        TODO EXPLAIN

        :param int index:

        :return:
        :rtype: int
        """
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
    digit_sequence = list(digits)
    grid = Grid(digit_sequence, len(lines))

    return grid


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    grid = load_input()


if __name__ == "__main__":
    main()
