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


def build_rotator(values, theoretical_max=6):
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


def run_simulation(days, mature_members, maturation_period=2):
    """
    TODO EXPLAIN

    :param int days:
    :param deque[int] mature_members:
    :param int maturation_period:

    :return:
    :rtype: int
    """

    # Get a copy of the given values
    mature_members = deque(mature_members)

    # Stores tally of new members which are waiting to be introduced to the mature rotation; for each day, the leftmost
    # tally shall be popped and the rightmost element of the mature tallies shall be incremented
    on_deck = deque(0 for _ in range(maturation_period))
    introduction_index = len(mature_members) - 1

    day = 0
    while day < days:
        # Leftmost of the mature population give birth; add an immature population
        birthing_population = mature_members.popleft()
        on_deck.append(birthing_population)
        mature_members.append(birthing_population)

        # The oldest of the immature fish mature and join the population which just birthed; they'll birth on the same
        # schedule
        new_members = on_deck.popleft()
        mature_members[introduction_index] += new_members

        # Advance to the next day
        day += 1

    # Count the populations, both mature and immature
    mature_population = sum(mature_members)
    immature_population = sum(on_deck)
    full_population = mature_population + immature_population
    return full_population


def main():
    """
    TODO EXPLAIN

    :return: None
    """

    vector = load_input()
    rotator = build_rotator(vector)

    print(run_simulation(80, rotator, maturation_period=2))
    print(run_simulation(256, rotator, maturation_period=2))


if __name__ == "__main__":
    main()
