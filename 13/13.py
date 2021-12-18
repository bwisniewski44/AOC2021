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


def enforce_fold_size(grid, direction, axis_index):
    """
    Ensures that the grid has sufficient column/row space to allow a fold left/up (respectively) at the given fold
    index.

    :param Grid[int] grid:
    :param int direction:
    :param int axis_index:

    :return: number of vectors added
    :rtype: int
    """

    # Ensure that the direction is valid
    if direction == Grid.UP:
        vector_dimension = Grid.HORIZONTAL
        total_vector_count = grid.height
    elif direction == Grid.LEFT:
        vector_dimension = Grid.VERTICAL
        total_vector_count = grid.width
    else:
        raise ValueError(f"Unexpected fold-direction code {direction}")

    # Ensure that there are at least as many vectors preceding the fold as there are following the fold; if there aren't
    # already, we'll have to insert new, blank ones
    preceding_vectors = axis_index
    vectors_to_remove = total_vector_count - preceding_vectors

    # The new grid will have exactly as many as the larger of the two groups of vectors; if the preceding vectors shall
    # be those to survive the fold, so if they lack sufficient quantity, insert dummy blank vectors ahead of them (this
    # will shift the fold index!)
    if preceding_vectors >= vectors_to_remove:
        vectors_to_add = 0
    else:
        vectors_to_add = vectors_to_remove - preceding_vectors

    i = 0
    while i < vectors_to_add:
        grid.insert(vector_dimension, index=0, fill=0)
        i += 1

    return vectors_to_add


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
    vectors_added = enforce_fold_size(grid, direction, axis_index)
    axis_index += vectors_added

    # While folding...
    while axis_index < grid.count(dimension):
        # ... pop the next-furthest vector from the fold
        vector = grid.pop(dimension)
        distance_from_axis = grid.count(dimension) - axis_index

        # If that vector wasn't the fold itself...
        if distance_from_axis > 0:
            # ... determine the index of the vector into which to OR the values
            receiving_vector_index = axis_index - distance_from_axis
            coordinates = grid.get_coordinates(dimension, receiving_vector_index)
            for i, coordinates in enumerate(coordinates):
                value = vector[i]
                if value == 0:
                    continue

                grid[coordinates] = value


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


def output_board(board, path, separator="", positive="#", negative="."):
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
    output_board(board, "output.txt")


if __name__ == "__main__":
    main()
