"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import deque
from structures import Cube


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

    active_positions = 0
    for i, instruction in enumerate(instructions):
        target_space = instruction.cube
        application_range = initialization_space.intersection(target_space)
        if application_range is not None:
            application_space = Cube(application_range)  # type: Cube[bool]
            active_positions += application_space.volume
        print(f"Completed {i+1} of {len(instructions)} instructions")

    return active_positions


def get_non_overlapping_instructions(instructions):
    """
    Expands the instructions sequence such that for any i, j: i < j, instruction[j] does not apply partially to the
    space occupied by instruction[i]. That is, a later instruction shall either totally overlap or totally avoid the
    space occupied by any earlier instruction (no partial overlap).

    :param list[Instruction] instructions:

    :return:
    :rtype: list[Instruction]
    """

    result = []  # type: typing.List[Instruction]

    for i, current_instruction in enumerate(instructions):
        current_cuboids = deque([current_instruction.cube])

        j = i+1
        while j < len(instructions):
            other_cuboid = instructions[j].cube

            k = 0
            comparison_count = len(current_cuboids)
            while k < comparison_count:
                current_cuboid = current_cuboids.popleft()
                if other_cuboid.envelopes(current_cuboid):
                    current_cuboids.append(current_cuboid)  # doesn't need to be broken down; is overlapped entirely
                else:
                    # The later instruction overlaps partially; get the intersection plus the non-intersecting ones
                    intersection, my_cuboids, _ = Cube.get_intersection_composites(current_cuboid, other_cuboid)
                    if intersection is None:
                        current_cuboids.append(current_cuboid)
                    else:
                        current_cuboids.append(Cube(intersection))
                        current_cuboids.extend(my_cuboids)
                        print(f"Created {len(current_cuboids)} sub-instructions at {i}")
                k += 1

            j += 1

        # At this point, the i'th instruction has been broken down into equivalent, composite cuboids; pull out the i'th
        # instruction and replace with each of the current cuboids
        for cuboid in current_cuboids:
            inner_ranges = cuboid.ranges
            result.append(Instruction(current_instruction.activate, inner_ranges[0], inner_ranges[1], inner_ranges[2]))

    print(f"Expended {len(instructions)} instructions to {len(result)}")
    return result


def remove_subcubes(instructions):
    """
    TODO EXPLAIN

    :param list[Instruction] instructions:

    :return: None
    """

    stupid_instructions = set()  # TODO: rename
    for i in reversed(range(len(instructions))):
        potential_superinstruction = instructions[i]

        for j in range(i):
            potential_subinstruction = instructions[j]
            if potential_superinstruction.cube.envelopes(potential_subinstruction.cube):
                stupid_instructions.add(j)

    for index in reversed(sorted(stupid_instructions)):
        instructions.pop(index)
        print(f"Removed redundant instruction {index}")


def reduce_instruction_set(instructions):
    # Break down the cuboids such that each ON is either fully enveloped by or fully independent of any OFF instructions
    non_partial_instructions = get_non_overlapping_instructions(instructions)

    # Resolve the set of instructions for space which is fully-enveloped by later instructions
    enveloped_indices = set()  # type: typing.Set[int]
    for i, current_instruction in enumerate(non_partial_instructions):
        j = i + 1
        while j < len(non_partial_instructions):
            other_instruction = non_partial_instructions[j]
            if other_instruction.cube.envelopes(current_instruction.cube):
                enveloped_indices.add(i)
                break
            j += 1

    # Remove all fully-enveloped spaces
    print(f"Found {len(enveloped_indices)} enveloped indices of {len(non_partial_instructions)}")
    for index in reversed(sorted(enveloped_indices)):
        non_partial_instructions.pop(index)

    # Step 1 saw us get a sequence of instructions such that for all pairs of instructions i, j: i < j, instruction[i]
    # is either fully enveloped by or fully independent of instruction[j]; Step 2 saw us remove all instruction[i] such
    # that its space is fully enveloped by instruction[j]; so, no instruction[i] is affected by instruction[j] ... that
    # is, they're all independent... meaning any OFF instructions don't affect anything... meaning they can be removed
    # entirely
    off_indices = set(i for i, instruction in enumerate(non_partial_instructions) if not instruction.activate)
    for index in reversed(sorted(off_indices)):
        non_partial_instructions.pop(index)
    print(f"Removed {len(off_indices)} useless OFFs")

    print(f"There are {len(non_partial_instructions)} independent ONs")
    return non_partial_instructions


def get_part_2(instructions):
    """
    TODO EXPLAIN

    :param list[Instruction] instructions:

    :return:
    :rtype: int
    """

    active_positions = sum(instruction.cube.volume for instruction in instructions)
    return active_positions


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    instructions = load_input()
    reduced_instruction_set = reduce_instruction_set(instructions)

    print(get_part_1(reduced_instruction_set))

    print(sum(instruction.cube.volume for instruction in reduced_instruction_set))


if __name__ == "__main__":
    main()
