"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing

_COORDINATE_SEPARATOR = "->"


class Vector(object):
    """
    TODO EXPLAIN
    """

    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2

    def __init__(self, start, stop):
        """
        :param (int,int) start:
        :param (int,int) stop:
        """

        self.start = start
        self.stop = stop

        # This is either horizontal (column-change), vertical (row-change), or diagonal... if the latter, ensure it's a
        # PERFECT diagonal: the change in row is equal to the change in column
        row_delta = stop[0] - start[0]
        col_delta = stop[1] - start[1]
        if row_delta and col_delta:
            direction = Vector.DIAGONAL
            if abs(row_delta) != abs(col_delta):
                raise ValueError(f"Row-wise delta {row_delta} must equal col-wise delta {col_delta}")
        elif row_delta:
            direction = Vector.VERTICAL
        elif col_delta:
            direction = Vector.HORIZONTAL
        else:
            raise ValueError(f"Vector has no length")
        self.direction = direction

        self._row_step = 1 if row_delta > 0 else -1 if row_delta < 0 else 0
        self._col_step = 1 if col_delta > 0 else -1 if col_delta < 0 else 0
        self._magnitude = abs(row_delta or col_delta)

    def __repr__(self):
        return f"({self.start[0]},{self.start[1]}) {_COORDINATE_SEPARATOR} ({self.stop[0]},{self.stop[1]})"

    def path(self):
        """
        TODO EXPLAIN

        :return:
        :rtype: list[(int,int)]
        """

        coordinates = []    # type: typing.List[typing.Tuple[int,int]]

        i = 0
        x, y = self.start
        intersected_coordinates = self._magnitude + 1  # even magnitude zero (starts/stops on same point) includes one
        while i < intersected_coordinates:
            coordinates.append(
                (x, y)
            )

            x += self._row_step
            y += self._col_step

            i += 1

        return coordinates


def parse_line(s):
    """
    TODO EXPLAIN

    :param str s:

    :return:
    :rtype: Vector
    """

    try:
        start_expression, stop_expression = s.split(_COORDINATE_SEPARATOR)
    except ValueError:
        raise RuntimeError(f"There must be exactly one coordinate separator ({_COORDINATE_SEPARATOR}) for line")

    comma_separated_elements = str.split(start_expression, ",") + str.split(stop_expression, ",")
    values = []  # type: typing.List[int]
    for element in comma_separated_elements:
        formatted_expression = element.strip()
        value = int(formatted_expression)

        values.append(value)

    expected_count = 4
    if len(values) != expected_count:
        raise RuntimeError(f"Expecting {expected_count} integers for line; encountered {len(values)}")

    start_coordinate = (values[0], values[1])
    stop_coordinate = (values[2], values[3])

    return Vector(start_coordinate, stop_coordinate)


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: list[Vector]
    """

    with open(path) as infile:
        vectors = [parse_line(line) for line in infile.readlines()]
    return vectors


def tally_hits(vectors, direction_filter=None):
    """
    TODO EXPLAIN

    :param list[Vector] vectors:
    :param int|set[int] direction_filter:

    :return: count of overlapping vectors, keyed by coordinate
    :rtype: dict[(int,int), int]
    """

    if direction_filter is None:
        qualifying_directions = {Vector.HORIZONTAL, Vector.VERTICAL, Vector.DIAGONAL}
    elif isinstance(direction_filter, int):
        qualifying_directions = {direction_filter}
    else:
        qualifying_directions = direction_filter

    hits_by_coordinate = {}  # type: typing.Dict[typing.Tuple[int,int], int]

    for vector in vectors:
        if vector.direction in qualifying_directions:
            # Get the points affected by this vector
            for coordinate in vector.path():
                old_tally = hits_by_coordinate.get(coordinate, 0)
                hits_by_coordinate[coordinate] = old_tally + 1

    return hits_by_coordinate


def tally_affected_points(overlaps_by_coordinate, threshold=1):
    """
    TODO EXPLAIN

    :param dict[(int,int), int] overlaps_by_coordinate:
    :param int threshold:

    :return:
    :rtype: int
    """

    points_by_tally = {}    # type: typing.Dict[int, typing.Set[typing.Tuple[int,int]]]

    for coordinate, overlap_tally in overlaps_by_coordinate.items():
        if overlap_tally in points_by_tally:
            coordinates = points_by_tally[overlap_tally]
        else:
            coordinates = set()
            points_by_tally[overlap_tally] = coordinates

        coordinates.add(coordinate)

    qualifying_coordinates_count = 0
    for overlap_tally, coordinates in points_by_tally.items():
        if overlap_tally >= threshold:
            qualifying_coordinates_count += len(coordinates)

    return qualifying_coordinates_count


def main():
    """
    TODO EXPLAIN

    :return: None
    """

    vectors = load_input()
    overlap_tally_by_coordinate = tally_hits(vectors, direction_filter={Vector.HORIZONTAL, Vector.VERTICAL})
    part_1 = tally_affected_points(overlap_tally_by_coordinate, threshold=2)
    print(part_1)


if __name__ == "__main__":
    main()
