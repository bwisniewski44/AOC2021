"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

from structures import KeySet
import typing

KEY_GOAL = "end"
KEY_START = "start"
SEPARATOR = "-"


def add_destination(destinations_by_origin, origin, destination):
    """
    TODO EXPLAIN

    :param dict[str,set[str]] destinations_by_origin:
    :param str origin:
    :param str destination:

    :return: None
    """

    if origin in destinations_by_origin:
        destinations = destinations_by_origin[origin]
    else:
        destinations = set()
        destinations_by_origin[origin] = destinations
    destinations.add(destination)


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: dict[str,set[str]]
    """

    destinations_by_origin = {}  # type: typing.Dict[str,typing.Set[str]]

    with open(path) as infile:
        for line in infile.readlines():
            half_a, half_b = map(str.strip, line.split(SEPARATOR))  # type: str, str
            add_destination(destinations_by_origin, half_a, half_b)
            add_destination(destinations_by_origin, half_b, half_a)

    return destinations_by_origin


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    destinations_by_origin = load_input()


if __name__ == "__main__":
    main()
