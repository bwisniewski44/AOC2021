
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


def multiply_aggregations(instructions):
    """
    TODO EXPLAIN

    :param list[(int,int)] instructions:

    :return: product of sums
    :rtype: int
    """

    sum_by_direction = {}   # type: typing.Dict[int, int]
    for direction, magnitude in instructions:
        old_sum = sum_by_direction.get(direction, 0)
        sum_by_direction[direction] = old_sum + magnitude

    product = 1
    for _, aggregate in sum_by_direction.items():
        product *= aggregate

    return product


def do():
    """
    TODO EXPLAIN

    :return: None
    """
    instructions = load_instructions()

    part_one_result = multiply_aggregations(instructions)
    sys.stdout.write(f"{part_one_result}\n")


if __name__ == "__main__":
    do()
