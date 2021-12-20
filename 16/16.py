"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from structures import KeySet


# TODO EXPLAIN
PACKET_TYPES = KeySet()
LITERAL, OPERATOR_FULL, OPERATOR_PARENT = PACKET_TYPES.enumerate(3)


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: list of ``0`` and ``1`` characters
    :rtype: list[str]
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    # The leading line should be a string of hex digits; convert each such digit into its own string of bits
    bits = []  # type: typing.List[str]
    for hex_digit in lines[0]:
        # Get the abstract integer value represented by this hex digit
        value = int(hex_digit, 16)

        # Resolve the 4-bit binary expression which expresses that value
        binary_expression = bin(value)[2:]  # leading two chars are the '0b' prefix
        binary_expression = binary_expression.zfill(4)
        if len(binary_expression) != 4:
            raise \
                ValueError(
                    f"Expecting 4 binary digits, but found {len(binary_expression)} in binary expression "
                    f"'{binary_expression}'"
                )

        # Add those bits to the bit-list
        bits.extend(binary_expression)

    return bits


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    bits = load_input()


if __name__ == "__main__":
    main()
