"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import deque
from structures import Grid


FOLD_DIRECTION_BY_DIMENSION_INDICATOR = {
    "x": Grid.UP,
    "y": Grid.LEFT
}


def fold(grid, direction, axis_index):
    """
    TODO EXPLAIN

    :param Grid[int] grid:
    :param int direction:
    :param int axis_index:

    :return: None
    """

    dimension_by_direction = {
        Grid.UP: Grid.HORIZONTAL,
        Grid.LEFT: Grid.VERTICAL
    }
    dimension = dimension_by_direction[direction]

    # A fold is expected to occur such that there are at least as many vectors preceding the fold as there are following
    # the fold (the fold vector itself gets eliminated and counts towards neither the preceding nor following vectors)
    preceding_vectors = axis_index
    following_vectors = grid.count(dimension) - (preceding_vectors + 1)
    if preceding_vectors < following_vectors:
        raise IndexError(f"Cannot merge {following_vectors} vectors into {preceding_vectors} vectors")

    # Start merging the vectors by popping those off the furthest ends of the grid
    for receiving_index in range(axis_index-following_vectors, axis_index):
        # Pop the next-furthest vector from the fold
        vector = grid.pop(dimension)

        # Start merging its values into the coordinates of the receiving vector
        coordinates = grid.get_coordinates(dimension, receiving_index)
        for i, coordinates in enumerate(coordinates):
            value = vector[i]
            if value == 0:
                continue

            grid[coordinates] = value

    # All vectors have been merged; all that's left now is to remove the final vector, that which gets consumed by the
    # fold
    grid.pop(dimension)


def get_board(marked_positions):
    """
    TODO EXPLAIN

    :param set[(int,int)] marked_positions:

    :return:
    :rtype: Grid[int]
    """

    board_height = max(coordinates[0] for coordinates in marked_positions) + 1
    board_width = max(coordinates[1] for coordinates in marked_positions) + 1
    total_elements = board_height * board_width

    initial_sequence = [0 for _ in range(total_elements)]
    board = Grid.fromlist(initial_sequence, board_height)  # type: Grid[int]
    for coordinates in marked_positions:
        board[coordinates] = 1

    return board


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: 2-tuple giving...
      1. (Grid[int]) a grid of dots TODO: better explanation
      2. list[(int,int)]
    :rtype: (Grid[int], list[(int,int)])
    """
    with open(path) as infile:
        lines = deque(str.strip(line) for line in infile.readlines())

    # The lines start with coordinates before a blank line separating the coordinates from the fold-sequence
    marked_positions = set()     # type: typing.Set[typing.Tuple[int,int]]
    fold_instructions = []  # type: typing.List[typing.Tuple[int,int]]
    parsing_coordinates = True
    while parsing_coordinates:
        coordinates_expression = lines.popleft()
        if len(coordinates_expression) == 0:
            parsing_coordinates = False
        else:
            x, y = (int(str.strip(digits)) for digits in coordinates_expression.split(","))  # type: int, int
            marked_positions.add(
                (x, y)
            )
    board = get_board(marked_positions)

    # Coordinates-parsing concluded; that must mean that the separating blank line has been popped; what remains are
    # fold instructions
    while lines:
        instruction = lines.popleft()

        # Use the '=' to take the immediately-preceding char (the dimension indicator, 'x'/'y'), and all the following
        # chars (a position, ie: x=500)
        equals_position = instruction.find("=")
        dimension_indicator = instruction[equals_position-1]
        fold_direction = FOLD_DIRECTION_BY_DIMENSION_INDICATOR[dimension_indicator]
        position = int(instruction[equals_position+1:])

        fold_instructions.append(
            (fold_direction, position)
        )

    return board, fold_instructions


def execute_fold_sequence(board, instructions):
    """
    TODO EXPLAIN

    :param Grid[int] board:
    :param list[(int,int)] instructions:

    :return: int
    :rtype: int
    """

    for direction, position in instructions:
        fold(board, direction, position)

    counter = 0
    for i in range(board.height):
        for j in range(board.width):
            if board[i, j]:
                counter += 1

    return counter


def output_board(board, path, separator=" ", positive="#", negative=" "):
    """
    TODO EXPLAIN

    :param Grid[int] board:
    :param str path:
    :param str separator:
    :param str positive:
    :param str negative:

    :return: None
    """

    with open(path, "w") as outfile:
        for row in range(board.height):
            line = separator.join(positive if board[row, col] else negative for col in range(board.width))
            outfile.write(line + '\n')


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board, fold_instructions = load_input()
    print(f"Loaded {board.height}x{board.width} grid")

    # Part 1: Perform just the first of the fold instructions, then count the tiles with dots
    count = execute_fold_sequence(board, fold_instructions[:1])
    print(count)

    # Part 2: Perform the remaining fold instructions; print the board
    execute_fold_sequence(board, fold_instructions[1:])
    output_board(board.transpose(), "output.txt")


if __name__ == "__main__":
    main()
