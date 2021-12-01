"""
Script to compute the answers to Day 1's puzzles of the 'Advent of Code' challenge:
https://adventofcode.com/
"""

import sys
import typing


def read_measurement_sequence(path="input.txt"):
    """
    Reads a sequence of numbers from the file at the given path

    :param str path: path to file to read

    :return: value-sequence within the file
    :rtype: list[int]
    """

    # Open the file for reading
    with open(path) as infile:
        # Get a sequence of measurements from the file, one measurement per line
        measurement_sequence = [int(str.strip(line)) for line in infile.readlines()]

    return measurement_sequence


def aggregate_measurements(measurement_sequence, window_size):
    """
    Builds a sequence of values from the given measurements by sliding an n-width window over the measurements,
    computing a sum of values therein,

    :param list[int] measurement_sequence: value sequence from which to aggregate
    :param int window_size: size of sliding-window

    :return: aggregate value sequence
    :rtype:  list[int]
    """

    # Store the result sequence in this list
    depth_sequence = []  # type: typing.List[int]

    # Initialize the first n-width sliding-window value from the sequence
    accumulator = sum(measurement_sequence[i] for i in range(window_size))  # initialize to sum of first n entries
    depth_sequence.append(accumulator)                                      # append the initial entry

    # Every other measurement can be computed by removing the oldest entry and adding in the next entry
    i = window_size
    while i < len(measurement_sequence):
        # Resolve the value to introduce and that to drop out
        next_measurement = measurement_sequence[i]
        old_measurement = measurement_sequence[i-window_size]

        # Update the accumulator by dropping out the old measurement and introducing the new; append this updated depth
        # to the result sequence
        accumulator -= old_measurement
        accumulator += next_measurement
        depth_sequence.append(accumulator)

        # Prepare to move to the next measurement
        i += 1

    return depth_sequence


def count_increases(values):
    """
    Gives the number of elements in the sequence which are a greater value than that of the immediately-preceding
    element.

    :param list[int] values: sequence of values

    :return: number of increases
    :rtype: int
    """

    # Initialize the result counter
    increases = 0

    # Begin iterating over the values from the second element (skip the first element - it doesn't have an
    # 'immediately-preceding' value against which to compare)
    for i in range(1, len(values)):
        # Resolve the values to compare for this index
        element = values[i]
        preceding_element = values[i-1]

        # Increment the counter if the element at this index has a value greater-than that of the preceding element
        if element > preceding_element:
            increases += 1

    return increases


def print_increases(measurements, window_size):
    """
    Puts to STDOUT the number of increases observed from one element to the next of the depth-sequence encoded by the
    given measurements.

    The depth-sequence is computed as an n-element sliding-window of measurements.

    :param list[int] measurements: sequence from which to build the depth sequence
    :param int window_size: width of the sliding-window to slide over the measurements

    :return: None
    """

    # Resolve the sequence of depths from which to count increases
    if window_size < 1:
        raise ValueError(f"Window size must be a positive number")
    elif window_size == 1:
        depth_sequence = measurements
    else:
        depth_sequence = aggregate_measurements(measurements, window_size)

    # Count the increases, then print a line to STDOUT
    increases = count_increases(depth_sequence)
    sys.stdout.write(f"{increases}\n")


def main():
    """
    Reads the puzzle input, then prints a result per puzzle part.

    :return: None
    """

    # Read the measurement sequence from the input-file
    measurements = read_measurement_sequence("input.txt")

    # Each puzzle part differs by the width of the window sliding over the measurements
    window_sizes = [1, 3]
    for window_size in window_sizes:
        print_increases(measurements, window_size)


if __name__ == "__main__":
    main()
