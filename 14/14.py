"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing

SEPARATOR = "->"


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: productions by pair
    :rtype: (list[str], dict[(str,str), str])
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    base = list(lines[0])

    productions_by_pair = {}  # type: typing.Dict[typing.Tuple[str,str], str]
    i = 2
    while i < len(lines):
        line = lines[i]
        try:
            pair_expression, production = map(str.strip, line.split(SEPARATOR))
        except ValueError:
            raise ValueError(f"Expecting a single separator ({SEPARATOR}) in line {repr(line)}")

        pair = tuple(pair_expression)
        if len(pair) != 2:
            raise ValueError(f"Expecting two elements in generating sequence; got {len(pair)}")
        elif len(production) != 1:
            raise ValueError(f"Expecting a single element in generated production; got {len(production)}")
        productions_by_pair[pair] = production

        i += 1

    return base, productions_by_pair


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    load_input()


if __name__ == "__main__":
    main()
