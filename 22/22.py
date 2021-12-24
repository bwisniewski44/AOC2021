"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from structures import Cube, Space


def express_range(range_):
    """
    TODO EXPLAIN

    :param (int,int) range_:

    :return:
    :rtype: str
    """
    return f"[{range_[0]},{range_[1]}]"

class Instruction:
    """
    TODO EXPLAIN
    """

    ACTIVATE_INSTRUCTION = "on"
    DEACTIVATE_INSTRUCTION = "off"
    _ACTIVITY_STATE_BY_INSTRUCTION = {
        ACTIVATE_INSTRUCTION: True,
        DEACTIVATE_INSTRUCTION: False
    }

    _X_DIM, _Y_DIM, _Z_DIM = "x", "y", "z"
    _DIMENSION_INDICATORS = {_X_DIM, _Y_DIM, _Z_DIM}

    @staticmethod
    def parse(s):
        """
        TODO EXPLAIN

        :param str s:

        :return:
        :rtype: Instruction
        """

        try:
            instruction_half, ranges_half = s.split()  # type: str, str
        except ValueError:
            raise \
                ValueError(
                    f"Expecting whitespace only where separating the instruction from the ranges to which it applies"
                )

        try:
            is_active = Instruction._ACTIVITY_STATE_BY_INSTRUCTION[instruction_half]
        except KeyError:
            raise \
                ValueError(
                    f"Unrecognized instruction '{instruction_half}'; expecting one of: "
                    f"{','.join(Instruction._ACTIVITY_STATE_BY_INSTRUCTION)}"
                )

        range_expressions = ranges_half.split(",")
        if not len(range_expressions) == 3:
            raise ValueError(f"Expecting three range-expressions, but encountered {len(range_expressions)}")

        range_by_dimension_code = {}  # type: typing.Dict[str,typing.Tuple[int,int]]
        for dimension_and_range in range_expressions:
            try:
                dimension_code, range_ = dimension_and_range.split("=")  # type: str, str
            except ValueError:
                raise \
                    ValueError(
                        f"Expecting a dimension code and range-expression separated by 1 equals-sign ('='); "
                        f"encountered {dimension_and_range.count('=')} such signs for expression "
                        f"{repr(dimension_and_range)}"
                    )
            if dimension_code not in Instruction._DIMENSION_INDICATORS:
                raise \
                    ValueError(
                        f"Unrecognized dimension code '{dimension_code}'; expecting one of: "
                        f"{', '.join(Instruction._DIMENSION_INDICATORS)}"
                    )
            elif dimension_code in range_by_dimension_code:
                raise KeyError(f"Duplicate dimension codes {dimension_code}")

            bounds_expressions = range_.split("..")
            if not len(bounds_expressions) == 2:
                raise \
                    ValueError(f"Expecting 2 bounds for range {dimension_code}; encountered {len(bounds_expressions)}")
            bounds = []
            for boundary_expression in bounds_expressions:
                try:
                    boundary = int(boundary_expression)
                except ValueError:
                    raise \
                        ValueError(
                            f"Illegal non-integer expression '{boundary_expression}' encountered in range for "
                            f"dimension {dimension_code}"
                        )
                bounds.append(boundary)

            ordered_bounds = (
                min(bounds),
                max(bounds)
            )
            range_by_dimension_code[dimension_code] = ordered_bounds

        result = \
            Instruction(
                is_active,
                range_by_dimension_code[Instruction._X_DIM],
                range_by_dimension_code[Instruction._Y_DIM],
                range_by_dimension_code[Instruction._Z_DIM]
            )
        return result

    def __init__(self, activate, x_range, y_range, z_range):
        """
        :param bool activate:
        :param (int,int) x_range:
        :param (int,int) y_range:
        :param (int,int) z_range:
        """
        self.activate = activate
        self.cube = Cube([x_range, y_range, z_range], background=False)

    def __repr__(self):
        active_expression = Instruction.ACTIVATE_INSTRUCTION if self.activate else Instruction.DEACTIVATE_INSTRUCTION
        x_range, y_range, z_range = self.cube.ranges
        return f"{active_expression} X{express_range(x_range)} Y{express_range(y_range)} Z{express_range(z_range)}"


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: list[Instruction]
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    instructions = []   # type: typing.List[Instruction]
    for line in lines:
        instruction = Instruction.parse(line)
        instructions.append(instruction)

    return instructions


def get_points(x_range, y_range, z_range):
    """
    TODO EXPLAIN

    :param (int,int) x_range:
    :param (int,int) y_range:
    :param (int,int) z_range:

    :return:
    :rtype: set[(int,int,int)]
    """

    all_coordinates = set()

    i = x_range[0]
    while i < x_range[1]:
        j = y_range[0]
        while j < y_range[1]:
            k = z_range[0]
            while k < z_range[1]:
                coordinates = (i, j, k)
                all_coordinates.add(coordinates)

    return all_coordinates


def in_range(coordinates, x_range, y_range, z_range):
    """
    TODO EXPLAIN

    :param (int,int,int) coordinates:
    :param (int,int) x_range:
    :param (int,int) y_range:
    :param (int,int) z_range:

    :return:
    :rtype: bool
    """

    ranges = x_range, y_range, z_range

    for i, coordinate in enumerate(coordinates):
        lower_bound, upper_bound = ranges[i]  # type: int, int
        if lower_bound <= coordinate <= upper_bound:
            continue
        else:
            return False

    return True


def count_active_positions(space):
    """
    TODO EXPLAIN

    :param Space[bool] space:

    :return:
    :rtype: int
    """

    tally = 0
    for _ in space.items():
        tally += 1
    return tally


def get_part_1(instructions):
    """
    TODO EXPLAIN

    :param list[Instruction] instructions:

    :return:
    :rtype: int
    """

    init_range_x = init_range_y = init_range_z = (-50, 50)
    initialization_space = \
        Cube(
            (init_range_x, init_range_y, init_range_z), background=False
        )  # type: Cube[bool]

    for i, instruction in enumerate(instructions):
        target_space = instruction.cube
        application_range = initialization_space.intersection(target_space)
        if application_range is not None:
            application_space = Cube(application_range)  # type: Cube[bool]
            for coordinate in application_space.points():
                initialization_space[coordinate] = instruction.activate
        print(f"Completed {i+1} of {len(instructions)} instructions")

    result = count_active_positions(initialization_space)
    return result


def register_intersections(instructions, i, intersections=None):
    """
    TODO EXPLAIN

    :param list[Instruction] instructions:
    :param int i:
    :param set[int] intersections:

    :return:
    :rtype: set[int]
    """

    # If this is the root call, intersections may yet be initialized to the empty-set; ensure we have a set
    if intersections is None:
        intersections = set()  # type: typing.Set[int]

    # If this node has yet to be introduced to the set of intersections...
    if i not in intersections:
        # ... add the node
        intersections.add(i)
        basis = instructions[i]

        # For all other instructions...
        j = 0
        while j < len(instructions):
            comp_instruction = instructions[j]
            has_intersection = (basis.cube.intersection(comp_instruction.cube) is not None)
            if has_intersection:
                # ... add it and its intersections
                register_intersections(instructions, j, intersections)

            j += 1

    return intersections


def get_independent_sequences(instructions):
    """
    Reduces the instruction set to contain those instructions

    :param list[Instruction] instructions:

    :return: list positions identifying ON fields which do not intersect with other cubes
    :rtype: list[list[Instruction]]
    """

    independent_sequences = []  # type: typing.List[typing.List[Instruction]]
    sequence_by_instruction_index = {}      # type: typing.Dict[int,int]
    i = 0
    while i < len(instructions):
        # Resolve the current instruction under consideration; if its intersections have already been found, skip it
        if i not in sequence_by_instruction_index:
            # Find the nodes intersecting this
            intersecting_indices = register_intersections(instructions, i)
            instruction_group = []  # type: typing.List[Instruction]
            for index in sorted(intersecting_indices):
                sequence_by_instruction_index[index] = len(independent_sequences)
                instruction_group.append(instructions[index])
            independent_sequences.append(instruction_group)

        i += 1

    return independent_sequences


def reduce_instruction_set(instructions):
    get_independent_sequences(instructions)


def get_part_2(instructions):
    """
    TODO EXPLAIN

    :param list[Instruction] instructions:

    :return:
    :rtype: int
    """

    space = Space(background=False)  # type: Space[bool]

    for i, instruction in enumerate(instructions):
        application_space = instruction.cube
        for coordinate in application_space.points():
            space[coordinate] = instruction.activate
        print(f"Applied {i+1} of {len(instructions)} instructions")

    result = count_active_positions(space)
    return result


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    instructions = load_input()
    get_independent_sequences(instructions)

    print(get_part_1(instructions))

    print(get_part_2(instructions))


if __name__ == "__main__":
    main()
