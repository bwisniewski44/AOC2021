"""
TODO EXPLAIN
"""
import heapq
import itertools
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

    @staticmethod
    def load(path):
        """
        TODO EXPLAIN

        :param str path:

        :return:
        :rtype: Grid
        """

        with open(path) as infile:
            lines = [str.strip(line) for line in infile.readlines()]

        height = len(lines)
        values = []  # type: typing.List[int]
        for digits in lines:
            values.extend(int(digit) for digit in digits)

        return Grid(values, height)

    DIRECTIONS = KeySet()   # type: KeySet[int,typing.Tuple[int,int]]

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


    DIMENSIONS = KeySet()
    HORIZONTAL, VERTICAL = DIMENSIONS.enumerate(2)

    def __init__(self, sequence, height):
        """
        :param list[int] sequence: TODO EXPLAIN
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

    def get_vector_positions(self, dimension, index):
        """
        TODO EXPLAIN

        :param int dimension:
        :param int index:

        :return:
        :rtype: list[int]
        """

        # Count the number of vectors aligned along the specified dimension
        if dimension == Grid.HORIZONTAL:
            current_vector_count = self.height
            element_count = self.width
            element_index = index * self.width
            index_increment = 1
        elif dimension == Grid.VERTICAL:
            current_vector_count = self.width
            element_count = self.height
            element_index = index
            index_increment = self.width
        else:
            raise ValueError(f"Encountered unexpected dimension code {dimension}")

        # Enforce the index restriction
        if not (0 <= index < current_vector_count):
            raise \
                IndexError(
                    f"Vector index specification {index} violates legal range [0,{current_vector_count}) for "
                    f"{self.height}x{self.width} grid"
                )

        # We survived to this point: must be a valid ask; let's gather the positions of the specified vector
        element_indices = []    # type: typing.List[int]
        while len(element_indices) < element_count:
            element_indices.append(element_index)
            element_index += index_increment

        return element_indices

    def _get_max_legal_index(self, dimension):
        """
        TODO EXPLAIN

        :param int dimension:

        :return:
        :rtype: int
        """

        if dimension == Grid.HORIZONTAL:
            max_legal_index = self.height - 1
        elif dimension == Grid.VERTICAL:
            max_legal_index = self.width - 1
        else:
            raise ValueError(f"Unexpected dimension code {dimension}")

        return max_legal_index

    def add_vector(self, dimension, values, index=None):
        """
        TODO EXPLAIN

        :param int dimension:
        :param list[int] values:
        :param int index:

        :return: None
        """

        # Increment the respective dimension before anything; all the other functions invoked in here will work better
        # if we've tricked them into thinking that we're at the correct width/height already
        if dimension == Grid.HORIZONTAL:
            self._height += 1
        elif dimension == Grid.VERTICAL:
            self._width += 1
        if index is None:
            index = self._get_max_legal_index(dimension)

        # Ensure that the number of values supplied precisely matches the number of values expected for a vector in this
        # dimension; then, add the values to this object
        insertion_positions = self.get_vector_positions(dimension, index)
        if len(insertion_positions) != len(values):
            raise ValueError(f"Expecting {len(insertion_positions)} elements in {len(values)}-length values vector")
        for i, insertion_index in enumerate(insertion_positions):
            insertion_value = values[i]
            self._values.insert(insertion_index, insertion_value)

    def remove_vector(self, dimension, index=None):
        """
        TODO EXPLAIN

        :param int dimension:
        :param int index:

        :return:
        :rtype: list[int]
        """

        # Ensure we have a sensible index
        if index is None:
            index = self._get_max_legal_index(dimension)
        positions_to_remove = self.get_vector_positions(dimension, index)

        removed_values = []
        while positions_to_remove:
            next_index = positions_to_remove.pop()
            next_value = self._values.pop(next_index)
            removed_values.append(next_value)

        original_values = reversed(removed_values)
        return original_values

    def read_vector(self, dimension, index):
        """
        TODO EXPLAIN

        :param int dimension:
        :param int index:

        :return:
        :rtype: list[int]
        """

        if index is None:
            index = self._get_max_legal_index(dimension)
        positions_to_read = self.get_vector_positions(dimension, index)

        result = [self._values[i] for i in positions_to_read]
        return result

    def dimlen(self, dimension):
        if dimension == Grid.HORIZONTAL:
            return self.height
        elif dimension == Grid.VERTICAL:
            return self.width
        else:
            raise ValueError(f"Unexpected dimension code {dimension}")

    def __setitem__(self, key, value):
        """
        TODO EXPLAIN

        :param (int,int)|int key:
        :param int value:

        :return: None
        """

        # TODO: normalize keys!
        if isinstance(key, int):
            index = key
        elif isinstance(key, tuple):
            try:
                row, col = key
            except ValueError:
                raise ValueError(f"Expecting 2-tuple giving (i,j) coordinates; received {len(key)}-tuple")
            else:
                if not (0 <= row < self.height):
                    raise IndexError
                if not (0 <= col < self.width):
                    raise IndexError
                index = row * self.width + col
        else:
            raise TypeError(f"Expecting int or 2-tuple specifier; got {type(key)}")

        self._values[index] = value

    def __len__(self):
        return len(self._values)


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
