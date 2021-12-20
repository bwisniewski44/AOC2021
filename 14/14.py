"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import defaultdict

SEPARATOR = "->"


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: productions by pair
    :rtype: (str, dict[(str,str), str])
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    # The first line gives the initial sequence
    base = list(lines[0])

    # A blank line separates the initial from those defining the productions; starting after those first two lines,
    # iterate over those defining the productions
    productions_by_pair = {}  # type: typing.Dict[typing.Tuple[str,str], str]
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
        productions_by_pair[pair] = produced_element

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


def get_element_tally(element_sequence):
    """
    TODO EXPLAIN

    :param str element_sequence:

    :return:
    :rtype: dict[str,int]
    """
    tally_by_element = {}  # type: typing.Dict[str,int]
    for ch in element_sequence:
        old_tally = tally_by_element.get(ch, 0)
        tally_by_element[ch] = old_tally + 1

    return tally_by_element


def generate(initial_sequence, productions_by_pair, generations):
    """
    TODO EXPLAIN

    :param str initial_sequence:
    :param dict[(str,str), str] productions_by_pair:
    :param int generations:

    :return: tally by element
    :rtype: dict[str,int]
    """

    # Keep track of the population-by-element
    tally_by_element = get_element_tally(initial_sequence)
    tally_by_pair = generate_tallies(initial_sequence)

    i = 0
    while i < generations:
        # Another round of generating values; let's measure the population changes here
        delta_by_pair = defaultdict(lambda: 0)  # type: typing.DefaultDict[typing.Tuple[str,str], int]

        # For each pair...
        for manufacturer, tally in tally_by_pair.items():
            # ... determine what element gets produced; the act of producing X destroys the manufacturer AB to yield two
            # new manufacturers: AX and XB
            produced_element = productions_by_pair[manufacturer]    # this is our X
            production_a = (manufacturer[0], produced_element)      # this is our AX
            production_b = (produced_element, manufacturer[1])      # this is our XB

            # # POPULATION ADJUSTMENT # #

            # Increment the element-wise tally for X
            tally_by_element[produced_element] = tally_by_element.get(produced_element, 0) + tally

            # The population of AX and XB are boosted by the number of manufacturers having produced such pairs
            delta_by_pair[production_a] += tally
            delta_by_pair[production_b] += tally

            # ... and the population-change of the manufacturer falls as it is destroyed to produce the pairs
            delta_by_pair[manufacturer] -= tally

        # Apply the population changes
        for key, delta in delta_by_pair.items():
            old_tally = tally_by_pair.get(key, 0)
            new_tally = old_tally + delta
            if new_tally < 0:
                raise ValueError(f"Unexpected negative count for pair {key} in {i}th generation")

            tally_by_pair[key] = new_tally

        # Advance to the next round of generation
        i += 1

    return tally_by_element


def diff_optima(tallies_by_element):
    """
    Gives the difference in population between the most- and least-populous elements in the tally.

    :param dict[str, int] tallies_by_element:

    :return:
    :rtype: int
    """

    if len(tallies_by_element) < 2:
        raise ValueError(f"Expecting to diff two populations; found only {len(tallies_by_element)}")

    max_tally = max(tally for _, tally in tallies_by_element.items())
    min_tally = min(tally for _, tally in tallies_by_element.items())

    top_populations = set(key for key, tally in tallies_by_element.items() if tally == max_tally)
    bottom_populations = set(key for key, tally in tallies_by_element.items() if tally == min_tally)

    if len(top_populations) != 1:
        raise \
            ValueError(
                f"Expecting to find a single, authoritative maximum population; found {len(top_populations)}: "
                f"{', '.join(top_populations)}"
            )
    elif len(bottom_populations) != 1:
        raise \
            ValueError(
                f"Expecting to find a single, authoritative minimum population; found {len(bottom_populations)}: "
                f"{', '.join(bottom_populations)}"
            )

    difference = max_tally - min_tally
    return difference


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    initial_sequence, productions_by_pair = load_input()

    # Part 1: TODO EXPLAIN
    tallies_by_element = generate(initial_sequence, productions_by_pair, 10)
    print(diff_optima(tallies_by_element))

    # Part 2: "second verse, same as the first"
    tallies_by_element = generate(initial_sequence, productions_by_pair, 40)
    print(diff_optima(tallies_by_element))


if __name__ == "__main__":
    main()
