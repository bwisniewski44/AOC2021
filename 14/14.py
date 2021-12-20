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
    :rtype: (str, dict[(str,str), (str,str)])
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    # The first line gives the initial sequence
    base = list(lines[0])

    # A blank line separates the initial from those defining the productions; starting after those first two lines,
    # iterate over those defining the productions
    productions_by_pair = \
        {}  # type: typing.Dict[typing.Tuple[str,str], typing.Tuple[typing.Tuple[str,str], typing.Tuple[str,str]]]
    i = 2
    while i < len(lines):
        # Line should be a format like "AB -> X"; divide out the "AB" and "X" portions
        line = lines[i]
        try:
            pair_expression, produced_element = map(str.strip, line.split(SEPARATOR))  # type: str, str
        except ValueError:
            raise ValueError(f"Expecting a single separator ({SEPARATOR}) in line {repr(line)}")

        # The first "AB" portion should be a pair of letters; that's our pair key... make sure it's two letters and the
        # production is just one!
        pair = tuple(pair_expression)
        if len(pair) != 2:
            raise ValueError(f"Expecting two elements in generating sequence; got {len(pair)}")
        elif len(produced_element) != 1:
            raise ValueError(f"Expecting a single element in generated production; got {len(produced_element)}")

        # Inserting an element between AB to yield AXB has the following consequences: there is one fewer AB pair,
        # replaced by two new pairs - AX, XB
        productions = (
            (pair[0], produced_element),    # here's the 1st produced pair (AX)
            (produced_element, pair[1])     # here's the 2nd produced pair (XB)
        )
        productions_by_pair[pair] = productions

        # Advance to parse the next line
        i += 1

    return base, productions_by_pair


def generate_tallies(sequence):
    """
    TODO EXPLAIN

    :param str sequence:

    :return:
    :rtype: dict[(str,str), int]
    """

    tally_by_pair = {}  # type: typing.Dict[typing.Tuple[str,str], int]

    # Iterate over the elements
    leading_element = sequence[0]
    i = 1
    while i < len(sequence):
        # Determine this next pair in the sequence
        following_element = sequence[i]
        pair = (leading_element, following_element)

        # Update the tally associated with the pair
        old_tally = tally_by_pair.get(pair, 0)
        tally_by_pair[pair] = old_tally + 1

        # Advance to the next pair; the element concluding this pair begins the next
        leading_element = following_element
        i += 1

    return tally_by_pair


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    load_input()


if __name__ == "__main__":
    main()
