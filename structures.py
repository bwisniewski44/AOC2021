"""
TODO EXPLAIN
"""

from collections.abc import Hashable
import typing


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


class Grid(object):
    """
    TODO EXPLAIN
    """

    DIRECTIONS = KeySet()

    UP_LEFT,\
        UP,\
        UP_RIGHT,\
        LEFT,\
        RIGHT,\
        DOWN_LEFT,\
        DOWN,\
        DOWN_RIGHT = \
        DIRECTIONS.enumerate(
            (
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            )
        )   # type: int, int, int, int, int, int, int, int

    def __init__(self, sequence, height):
        """
        :param list[int] sequence:
        :param int height:
        """

        self._values = sequence
        self._height = height
        self._width = len(sequence) // height

        if self._width * self._height != len(sequence):
            raise \
                ValueError(
                    f"Illegal height {height} for {len(sequence)}-length value sequence; height must be a whole-number "
                    f"factor of sequence"
                )

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def in_bounds(self, i, j):
        return (0 <= i < self.height) and (0 <= j < self.width)

    def at(self, i, j):
        """
        TODO EXPLAIN

        :param int i:
        :param int j:

        :return:
        :rtype: int
        """

        if not (0 <= i < self.height):
            raise ValueError(f"Row index {i} violates legal range [0,{self.height})")
        if not (0 <= j < self.width):
            raise ValueError(f"Col index {j} violates legal range [0,{self.width})")

        index = self.width * i + j
        return self._values[index]

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

    def __getitem__(self, pos):
        """
        TODO EXPLAIN

        :param int|(int,int) pos:

        :return:
        :rtype: int
        """
        if isinstance(pos, int):
            index = pos
        else:
            row, col = pos
            if not self.in_bounds(row, col):
                raise IndexError(f"Coordinates ({row},{col}) out-of-range for {self.height}x{self.width} grid")
            index = self.width * row + col

        return self._values[index]
