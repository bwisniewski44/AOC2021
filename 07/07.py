"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: tally by distance
    :rtype: dict[int,int]
    """

    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    tally_by_value = {}  # type: typing.Dict[int,int]
    leading_line = lines[0]
    for expression in [str.strip(element) for element in leading_line.split(",")]:
        value = int(expression)
        old_tally = tally_by_value.get(value, 0)
        tally_by_value[value] = old_tally + 1

    return tally_by_value


def average(tally_by_value):
    """
    TODO EXPLAIN

    :param dict[int,int] tally_by_value:

    :return:
    :rtype: int
    """

    total = 0
    count = 0

    for value, scale in tally_by_value.items():
        total += value * scale
        count += scale

    avg = total / count + 0.5   # add 0.5: it's a rounding trick
    whole_average = int(avg)
    return whole_average


def calculate_cost(distance):
    """
    TODO EXPLAIN

    :param int distance:

    :return:
    :rtype: int
    """
    return distance * (distance + 1) // 2


def compute_cost(tally_by_position, destination):
    """
    TODO EXPLAIN

    :param dict[int,int] tally_by_position:
    :param int destination:

    :return:
    :rtype: int
    """

    total = 0
    for position, tally in tally_by_position.items():
        offset = abs(position - destination)
        total += calculate_cost(offset) * tally

    return total


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    tally_by_position = load_input()

    # Find that between the min and max positions to which transition costs less fuel
    max_position = max(tally_by_position)
    min_position = min(tally_by_position)
    range_ = max_position - min_position
    min_distance = calculate_cost(range_) * sum(value for _, value in tally_by_position.items())
    min_convergance = min_position
    for convergence in range(min_position, max_position+1):
        distance = compute_cost(tally_by_position, convergence)
        if distance < min_distance:
            min_distance = distance
            min_convergance = convergence

    print(f"Min distance is {min_distance} for converging at {min_convergance}")


if __name__ == "__main__":
    main()
