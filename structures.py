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
    TODO EXPLAIN
    """

    @staticmethod
    def fromlist(items, rows):
        """
        TODO EXPLAIN

        :param list items:
        :param int rows:

        :return:
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
        TODO EXPLAIN

        :param list[Sequence] nested_lists:

        :return:
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
                for j in range(width):
                    result[i, j] = row[j]

        return result

    DIRECTIONS = KeySet()   # type: KeySet[int,typing.Tuple[int,int]]

    UP_LEFT, UP, UP_RIGHT, LEFT, RIGHT, DOWN_LEFT, DOWN, DOWN_RIGHT = \
        DIRECTIONS.enumerate(
            (
                (-1, -1), (-1, 0), (-1, 1),

                (0, -1), (0, 1),

                (1, -1), (1, 0), (1, 1)
            )
        )   # type: int, int, int, int, int, int, int, int


    DIMENSIONS = KeySet()
    HORIZONTAL, VERTICAL = DIMENSIONS.enumerate(2)

    def __init__(self, height=0, width=0, fill=None):
        """
        :param int height: TODO EXPLAIN
        :param int width:
        :param object fill:
        """
        self._rows = []  # type: typing.List[typing.List]
        self._width = width

        for _ in range(height):
            row = [fill for _ in range(width)]
            self._rows.append(row)

    @property
    def height(self):
        return len(self._rows)

    @property
    def width(self):
        return self._width

    def __len__(self):
        return self.height * self.width

    def in_bounds(self, i, j):
        return (0 <= i < self.height) and (0 <= j < self.width)

    def move(self, coordinate, direction):
        """
        TODO EXPLAIN

        :param (int,int) coordinate:
        :param int direction:

        :raises IndexError: on attempt to produce out-of-bounds coordinates

        :return:
        :rtype: (int,int)
        """
        if direction not in Grid.DIRECTIONS:
            raise ValueError(f"Unrecognized direction specifier {repr(direction)}")
        modification_vector = Grid.DIRECTIONS[direction]

        result_row, result_col = (coordinate[i] + adjustment for i, adjustment in enumerate(modification_vector))

        if self.in_bounds(result_row, result_col):
            return result_row, result_col
        else:
            raise IndexError(f"({result_row},{result_col}) out of bounds for {self.height}x{self.width} grid")

    def size(self, height, width, fill=None):
        """
        TODO EXPLAIN

        :param int height:
        :param int width:
        :param object fill:

        :return: None
        """

        if any(dimension < 0 for dimension in [height, width]):
            raise ValueError(f"Illegal negative grid dimensions {height}x{width}")

        self._rows.clear()
        self._rows = [
            [fill for _ in range(width)] for _ in range(height)
        ]

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
    TODO EXPLAIN

    :param str path:

    :return:
    :rtype: Grid[int]
    """

    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    rows = [
        [int(digit) for digit in line] for line in lines
    ]
    result = Grid.fromlists(rows)
    return result
