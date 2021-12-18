"""
TODO EXPLAIN
"""
import heapq
import itertools
from collections.abc import Hashable, Sequence
import typing
from typing import Generic, TypeVar


class KeySet(dict):
    """
    This object contains a set of identifying values, optionally storing a piece of information for each.

    TODO EXPLAIN MORE
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def define(self, key, item=None):
        """
        TODO EXPLAIN

        :param Hashable key:
        :param object item:

        :raises KeyError: on key collision

        :return: echoes back the key
        :rtype: Any
        """

        if self.__contains__(key):
            raise KeyError(f"Key set already contains key {repr(key)}")
        self.__setitem__(key, item)

    def enumerate(self, spec):
        """
        TODO EXPLAIN

        :param int|Iterable spec:

        :return:
        :rtype: tuple[int]
        """

        keys = []   # type: typing.List[int]
        if isinstance(spec, int):
            keys.extend(range(spec))
        else:
            for key, item in enumerate(spec):
                keys.append(key)
                self.define(key, item)

        return tuple(keys)


_T = TypeVar("_T")


class Grid(Generic[_T]):
    """
    Wrapper around nested lists of items
    """

    @staticmethod
    def fromlist(items, rows):
        """
        Returns the grid formed by breaking down a single sequence of items into like-length rows.

        :param list items: sequence of items; length must be a multiple of the ``rows`` argument
        :param int rows: length of each row to form

        :return: two-dimensional array of items
        :rtype: Grid
        """

        width = len(items) // rows
        if width * rows != len(items):
            raise ValueError(f"Cannot evenly divide {len(items)} items into {rows} rows")

        result = Grid(height=rows, width=width)
        for i, item in enumerate(items):
            row = i // width
            col = i % width
            result[row, col] = item

        return result

    @staticmethod
    def fromlists(nested_lists):
        """
        Builds a ``Grid`` instance out of the 2-dimensional array of items.

        :param list[Sequence] nested_lists: inner-nested values; each inner-nested array must be of like-length

        :raises IndexError: on failure to observe the like-length constraint

        :return: ``Grid`` instance represented by the two-dimensional array
        :rtype: Grid
        """

        # Validate that each list has the same number of elements
        if len(nested_lists) == 0:
            result = Grid()
        else:
            leading_row = nested_lists[0]
            height = len(nested_lists)
            width = len(leading_row)

            result = Grid(height=height, width=width)
            for i, row in enumerate(nested_lists):
                if len(row) != width:
                    raise \
                        IndexError(
                            f"{height}x{width} grid expects rows of length {width}, but encountered {i}th row of "
                            f"length {len(row)}"
                        )
                for j in range(width):
                    result[i, j] = row[j]

        return result

    # The following are class constants which are used when navigating relative to some origin position
    DIRECTIONS = KeySet()   # type: KeySet[int,typing.Tuple[int,int]]
    UP_LEFT, UP, UP_RIGHT, LEFT, RIGHT, DOWN_LEFT, DOWN, DOWN_RIGHT = \
        DIRECTIONS.enumerate(
            (
                (-1, -1), (-1, 0), (-1, 1),

                (0, -1), (0, 1),

                (1, -1), (1, 0), (1, 1)
            )
        )   # type: int, int, int, int, int, int, int, int

    # Constant codes identifying the two dimensions of a grid
    DIMENSIONS = KeySet()
    HORIZONTAL, VERTICAL = DIMENSIONS.enumerate(2)

    def __init__(self, height=0, width=0, fill=None):
        """
        :param int height: number of rows to populate
        :param int width: number of columns to populate
        :param object fill: value to populate into each cell
        """
        self._rows, self._width = self.resize(height, width, fill=fill)

    @property
    def height(self):
        return len(self._rows)

    @property
    def width(self):
        return self._width

    def __len__(self):
        return self.height * self.width

    def dimlen(self, dimension):
        """
        Gives the number of elements for each among the vectors inhabiting the given dimension.

        :param int dimension: code by which to identify the horizontal or the vertical vectors

        :return:
        :rtype: int
        """
        if dimension == Grid.HORIZONTAL:
            return self.width
        elif dimension == Grid.VERTICAL:
            return self.height
        else:
            raise ValueError(f"Unexpected dimension code {dimension}")

    def _raise_oob(self, pos):
        """
        Raises an out-of-bounds ``IndexError`` for a set of coordinates violating the bounds of this ``Grid``.

        :param (int,int) pos: coordinates violating the bounds of this grid; a ``ValueError`` is raised if these
          coordinates are actually in-bounds

        :raises IndexError: on out-of-bounds coordinates
        :raises ValueError: on in-bounds coordinates

        :return: N/A - this function always results in an ``Exception`` being raised
        :rtype: NoReturn
        """

        if self.in_bounds(*pos):
            raise ValueError(f"Cannot raise OOB error for in-bounds coordinates {pos}")
        else:
            raise IndexError(f"Illegal coordinates for {self.height}x{self.width} grid: {pos}")

    def in_bounds(self, i, j):
        return (0 <= i < self.height) and (0 <= j < self.width)

    def move(self, coordinate, direction, distance=1):
        """
        Gives the in-bounds grid coordinates which would be the destination for moving from the specified space.

        :param (int,int) coordinate: position from which to measure movement
        :param int direction: code specifying the direction in which to move
        :param distance: number of times to perform the move

        :raises IndexError: on attempt to produce out-of-bounds coordinates

        :return: in-bounds destination coordinates
        :rtype: (int,int)
        """
        if direction not in Grid.DIRECTIONS:
            raise ValueError(f"Unrecognized direction specifier {repr(direction)}")
        modification_vector = Grid.DIRECTIONS[direction]

        result_row, result_col = (
            coordinate[i] + (adjustment*distance) for i, adjustment in enumerate(modification_vector)
        )

        if self.in_bounds(result_row, result_col):
            return result_row, result_col
        else:
            raise IndexError(f"({result_row},{result_col}) out of bounds for {self.height}x{self.width} grid")

    def resize(self, height, width, fill=None):
        """
        Clears and resizes this grid.

        :param int height: new size of columns
        :param int width: new size of rows
        :param _T fill: object to occupy each of this grid's cells

        :return: 2-tuple giving...
          1. nested lists of elements
        :rtype: (list[list[_T]], int)
        """

        if any(dimension < 0 for dimension in [height, width]):
            raise ValueError(f"Illegal negative grid dimensions {height}x{width}")

        self._rows = [
            [fill for _ in range(width)] for _ in range(height)
        ]
        self._width = width

        return self._rows, self._width

    def insert(self, dimension, values=None, index=None, fill=None):
        """
        TODO EXPLAIN

        :param int dimension:
        :param list[_T] values:
        :param int index:
        :param _T fill: (ignored if a values-vector is given for insertion)

        :raises IndexError: on out-of-bounds index

        :return: None
        """

        # Ensure that the values vector is defined and of appropriate length
        values_vector_length = self.width if dimension == Grid.HORIZONTAL else self.height
        if values is None:
            values = [fill for _ in range(values_vector_length)]
        elif len(values) != values_vector_length:
            raise \
                IndexError(
                    f"Expecting vector of length {values_vector_length} for entry into {self.height}x{self.width} "
                    f"grid, but encountered {len(values)}-element values vector"
                )

        # If vector is specified as being a row...
        if dimension == Grid.HORIZONTAL:
            if index is None:
                index = self.height
            elif not (0 <= index <= self.height):
                self._raise_oob((index, 0))

            row = [fill for _ in range(self.width)]
            self._rows.insert(index, row)

        # If vector is specified as being a column...
        elif dimension == Grid.VERTICAL:
            if index is None:
                index = self.width
            elif not (0 <= index <= self.width):
                self._raise_oob((0, index))

            for i, row in enumerate(self._rows):  # type: int, typing.List
                row.insert(index, values[i])

        # Otherwise, vector was specified as being neither a row nor a column; can't handle this :(
        else:
            raise ValueError(f"Unexpected dimension code {repr(dimension)}")

    def pop(self, dimension, index=None):
        """
        TODO EXPLAIN

        :param int dimension:
        :param int index:

        :return:
        :rtype: list[_T]
        """

        if dimension == Grid.HORIZONTAL:
            if index is None:
                index = self.height - 1
            elif not (0 <= index < self.height):
                self._raise_oob((index, 0))
            result = self._rows.pop(index)

        elif dimension == Grid.VERTICAL:
            if index is None:
                index = self.width - 1
            elif not (0 <= index < self.width):
                self._raise_oob((0, index))

            result = []
            for row in self._rows:  # type: list
                result.append(
                    row.pop(index)
                )

        else:
            raise ValueError(f"Unexpected dimension code {repr(dimension)}")

        return result

    def __getitem__(self, pos):
        """
        TODO EXPLAIN

        :param (int,int) pos:

        :return:
        :rtype: _T
        """
        row, col = pos
        return self._rows[row][col]

    def __setitem__(self, key, value):
        """
        TODO EXPLAIN

        :param (int,int) key:
        :param _T value:

        :return: None
        """
        row, col = key
        self._rows[row][col] = value


class PriorityQueue:
    def __init__(self):
        self._values = []
        self._counter = itertools.count()

    def pop(self):
        _, _, item = heapq.heappop(self._values)
        return item

    def push(self, item, priority):
        heapq.heappush(self._values, (priority, -next(self._counter), item))

    def __len__(self):
        return len(self._values)


def load_int_block(path):
    """
    Loads the grid of integers encoded by the content of a file. The file content shall be a sequence of like-length
    lines containing all-digits ahead of their new-line.

    :param str path: path to file containing digits

    :return: grid of integers
    :rtype: Grid[int]
    """

    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    rows = [
        [int(digit) for digit in line] for line in lines
    ]
    result = Grid.fromlists(rows)
    return result
