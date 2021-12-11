"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from structures import Grid


def assess_risk(height_ranking):
    """
    TODO EXPLAIN

    :param int height_ranking:

    :return:
    :rtype: int
    """
    return height_ranking + 1


def add_adjacent_value(values, grid, coordinate, direction):
    """
    TODO EXPLAIN

    :param set[int] values:
    :param Grid grid:
    :param (int,int) coordinate:
    :param int direction:

    :return: None
    """

    try:
        adjacency_row, adjacency_col = grid.move(coordinate, direction)
    except IndexError:
        pass
    else:
        value = grid.at(adjacency_row, adjacency_col)
        values.add(value)


def find_minima(grid):
    """
    TODO EXPLAIN

    :param Grid grid:

    :return:
    :rtype: set[(int,int)]
    """

    minima = set()  # type: typing.Set[typing.Tuple[int,int]]

    for i in range(grid.height):
        for j in range(grid.width):
            height_ranking = grid.at(i, j)

            # Resolve all the different height-rankings of adjacent spaces
            adjacent_values = set()  # type: typing.Set[int]
            for direction in {Grid.UP, Grid.DOWN, Grid.LEFT, Grid.RIGHT}:
                add_adjacent_value(adjacent_values, grid, (i, j), direction)

            # This coordinate points to a valley if its height ranking is lower than those of its adjacent values
            if height_ranking < min(adjacent_values):
                minima.add(
                    (i, j)
                )

    return minima


def expand_basin(coordinate, members, grid):
    """
    TODO EXPLAIN

    :param (int,int) coordinate:
    :param set[(int,int)] members:
    :param Grid grid:

    :return: None
    """

    if grid[coordinate] != 9:  # TODO: hardcode?
        if coordinate not in members:
            members.add(coordinate)

            for direction in {Grid.UP, Grid.DOWN, Grid.LEFT, Grid.RIGHT}:
                try:
                    next_coordinate = grid.move(coordinate, direction)
                except IndexError:
                    pass
                else:
                    expand_basin(next_coordinate, members, grid)


def get_basin_number_by_coordinate(grid):
    """
    TODO EXPLAIN

    :param grid:

    :return:
    :rtype: dict[(int,int), int]
    """

    basin_number_by_coordinate = {}

    i = 0
    basins = 0
    while i < grid.height:
        j = 0
        while j < grid.width:
            coordinate = (i, j)
            if grid[coordinate] != 9 and coordinate not in basin_number_by_coordinate:
                basin_members = set()   # type: typing.Set[typing.Tuple[int,int]]
                expand_basin(coordinate, basin_members, grid)

                for member in basin_members:
                    basin_number_by_coordinate[member] = basins
                basins += 1

            j += 1
        i += 1

    return basin_number_by_coordinate


def get_basin_geography(grid):
    """
    TODO EXPLAIN

    :param Grid grid:

    :return:
    :rtype: list[set[(int,int)]]
    """

    basin_number_by_coordinate = get_basin_number_by_coordinate(grid)

    basins = []             # type: typing.List[typing.Set[typing.Tuple[int,int]]]
    index_by_number = {}    # type: typing.Dict[int,int]
    for coordinate, basin_number in basin_number_by_coordinate.items():
        # Resolve the index at which this basin's members are being kept
        if basin_number in index_by_number:
            index = index_by_number[basin_number]
        else:
            index = len(basins)
            index_by_number[basin_number] = index
            basins.append(set())

        # Add this coordinate to the basin's members
        basin_members = basins[index]
        basin_members.add(coordinate)

    return basins


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    grid = Grid.load("input.txt")
    minima = find_minima(grid)
    print(sum(assess_risk(grid[coordinate]) for coordinate in minima))

    basins = get_basin_geography(grid)
    ordered_basins = sorted(basins, key=lambda basin: len(basin), reverse=True)
    qualifying_basins = ordered_basins[:3]
    size_product = 1
    for basin in qualifying_basins:
        size_product *= len(basin)
    print(size_product)


if __name__ == "__main__":
    main()
