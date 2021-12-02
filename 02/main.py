
import sys
import typing

HORIZONTAL = 0
VERTICAL = 1
POSITIVE = True
NEGATIVE = not POSITIVE

DIMENSION_AND_PARITY_BY_KEYWORD = {
    "forward": (HORIZONTAL, POSITIVE),
    "down": (VERTICAL, POSITIVE),
    "up": (VERTICAL, NEGATIVE)
}   # type: typing.Dict[str, typing.Tuple[int,bool]]


def load_instructions(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path:

    :return:
    :rtype: list[(int,int)]
    """

    with open(path) as infile:
        lines = [line.strip() for line in infile.readlines()]

    instruction_sequence = []   # type: typing.List[typing.Tuple[int,int]]
    for i, line in enumerate(lines):
        try:
            keyword, magnitude_expression = line.split()                    # ValueError on incorrect number of elements
            dimension, parity = DIMENSION_AND_PARITY_BY_KEYWORD[keyword]    # KeyError on invalid keyword
        except ValueError as error:
            sys.stderr.write(f"Formatting error at line index {i}: [{type(error)}][{error}]")
        except KeyError:
            sys.stderr.write(f"Unrecognized instruction at line index {i}; line: {repr(line)}")
        else:
            magnitude = int(magnitude_expression)
            scalar = magnitude if (parity == POSITIVE) else magnitude * -1

            # Resolve the instruction and append
            instruction = (dimension, scalar)
            instruction_sequence.append(instruction)

    return instruction_sequence


def multiply_aggregations(instructions, track_aim):
    """
    TODO EXPLAIN

    :param list[(int,int)] instructions:
    :param bool track_aim:

    :return: product of sums
    :rtype: int
    """

    aim = 0
    horizontal_position = 0
    vertical_position = 0
    for direction, scalar in instructions:
        if direction == HORIZONTAL:
            horizontal_position += scalar
            vertical_position += scalar * aim
        elif track_aim:
            aim += scalar
        else:
            vertical_position += scalar

    return horizontal_position * vertical_position


def do():
    """
    TODO EXPLAIN

    :return: None
    """
    instructions = load_instructions()

    aim_tracking = [False, True]
    for aim_tracking_status in aim_tracking:
        result = multiply_aggregations(instructions, aim_tracking_status)
        sys.stdout.write(f"{result}\n")


if __name__ == "__main__":
    do()
