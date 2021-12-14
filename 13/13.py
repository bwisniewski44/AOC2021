"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

from structures import Grid


def enforce_fold_size(grid, direction, axis_index):
    """
    Ensures that the grid has sufficient column/row space to allow a fold left/up (respectively) at the given fold
    index.

    :param Grid grid:
    :param int direction:
    :param int axis_index:

    :return: number of vectors added
    :rtype: int
    """

    # Ensure that the direction is valid
    if direction == Grid.UP:
        vector_dimension = Grid.HORIZONTAL
        total_vector_count = grid.height
        vector_size = grid.width
    elif direction == Grid.LEFT:
        vector_dimension = Grid.VERTICAL
        total_vector_count = grid.width
        vector_size = grid.height
    else:
        raise ValueError(f"Unexpected fold-direction code {direction}")

    # Ensure that there are at least as many vectors preceding the fold as there are following the fold; if there aren't
    # already, we'll have to insert new, blank ones
    preceding_vectors = axis_index
    following_vectors = total_vector_count - (preceding_vectors + 1)

    # The new grid will have exactly as many as the larger of the two groups of vectors; if the preceding vectors shall
    # be those to survive the fold, so if they lack sufficient quantity, insert dummy blank vectors ahead of them (this
    # will shift the fold index!)
    if preceding_vectors >= following_vectors:
        vectors_to_add = 0
    else:
        vectors_to_add = following_vectors - preceding_vectors

    i = 0
    while i < vectors_to_add:
        new_vector = [0 for _ in range(vector_size)]
        grid.add_vector(vector_dimension, new_vector, index=0)

    return vectors_to_add


def fold(grid, direction, axis_index):
    """
    TODO EXPLAIN

    :param Grid grid:
    :param int direction:
    :param int axis_index:

    :return:
    :rtype: Grid
    """

    dimension_by_direction = {
        Grid.UP: Grid.HORIZONTAL,
        Grid.LEFT: Grid.VERTICAL
    }
    dimension = dimension_by_direction[direction]
    vectors_added = enforce_fold_size(grid, direction, axis_index)
    axis_index += vectors_added

    # While folding...
    while axis_index < grid.dimlen(dimension):
        vector = grid.remove_vector(dimension, grid.dimlen(dimension)-1)
        distance_from_axis = grid.dimlen(dimension) - axis_index

        if distance_from_axis > 0:
            # Resolve the index of the vector into which to OR this one's values
            receiving_vector = axis_index - distance_from_axis
            receiving_indices = grid.get_vector_positions(dimension, receiving_vector)

            for i, value in enumerate(vector):
                if value:
                    receiving_index = receiving_indices[i]
                    grid[receiving_index] = value


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: Grid
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]
    pass  # TODO: don't pass


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    pass


if __name__ == "__main__":
    main()
