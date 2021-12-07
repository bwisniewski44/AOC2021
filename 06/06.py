"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

from collections import deque
import typing


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: list[int]
    """

    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]
    vector = [int(element) for element in str.split(lines[0], ",")]
    return vector


def build_rotator(values, theoretical_max=7):
    """
    TODO EXPLAIN

    :param Iterable[int] values:
    :param int theoretical_max:

    :return:
    :rtype: deque[int]
    """

    # Group the members by value
    tally_by_value = {}  # type: typing.Dict[int,int]
    for element in values:
        old_tally = tally_by_value.get(element, 0)
        tally_by_value[element] = old_tally + 1

    # Ensure every possible entry is represented, introducing a 0-tally for those absent
    for element in range(theoretical_max+1):
        if element not in tally_by_value:
            tally_by_value[element] = 0

    # Sort the groups by order of ascending value (by group value... NOT by tally)
    sorted_tallies = deque(tally_by_value[value] for value in sorted(tally_by_value.keys()))
    return sorted_tallies


def run_simulation(days, tallies, maturation_period=0):
    """
    TODO EXPLAIN

    :param int days:
    :param deque[int] tallies:
    :param int maturation_period:

    :return:
    :rtype: int
    """
    pass


def main():
    """
    TODO EXPLAIN

    :return: None
    """

    vector = load_input()
    rotator = build_rotator(vector)


if __name__ == "__main__":
    main()
