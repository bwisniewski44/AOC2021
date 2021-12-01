"""
TODO EXPLAIN
"""

import sys
import typing


def read_measurement_sequence(path="input.txt"):
    """
    TODO EXPLAIN

    return:
    :rtype: list[int]
    """

    # Open the file for reading
    with open(path) as infile:
        # Get a sequence of measurements from the file, one measurement per line
        measurement_sequence = [int(str.strip(line)) for line in infile.readlines()]

    return measurement_sequence


def aggregate_measurements(measurement_sequence, window_size):
    """
    TODO EXPLAIN

    :param list[int] measurement_sequence:
    :param int window_size:

    :return:
    :rtype:  list[int]
    """

    # Store the result sequence in this list
    depth_sequence = []  # type: typing.List[int]

    # Initialize the first n-width sliding-window depth from the sequence
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
    TODO EXPLAIN

    :param list[int] values:

    :return:
    :rtype: int
    """

    increases = 0
    for i in range(1, len(values)):
        right_value = values[i]
        left_value = values[i-1]

        if right_value > left_value:
            increases += 1

    return increases


def print_increases(measurements, window_size):
    """
    Puts to STDOUT the number of increases observed from one element to the next of the depth-sequence encoded by the
    given measurements.

    The depth-sequence is computed as an n-element sliding-window of measurements.

    :param list[int] measurements:
    :param int window_size:

    :return: None
    """

    if window_size < 1:
        raise ValueError(f"Window size must be a positive number")
    elif window_size == 1:
        depth_sequence = measurements
    else:
        depth_sequence = aggregate_measurements(measurements, window_size)

    increases = count_increases(depth_sequence)

    sys.stdout.write(f"{increases}\n")


def main():
    """
    TODO EXPLAIN

    :return: None
    """

    # Read the measurement sequence from the input-file
    measurements = read_measurement_sequence("input.txt")

    print_increases(measurements, 1)    # print for a 1-width sliding window (PART 1)
    print_increases(measurements, 3)    # print for a 3-width sliding window (PART 2)


if __name__ == "__main__":
    main()
