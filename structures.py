"""
TODO EXPLAIN
"""


class Grid(object):
    """
    TODO EXPLAIN
    """

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    MODIFICATION_BY_MOVE = {
        UP: (-1, 0),
        DOWN: (1, 0),
        LEFT: (0, -1),
        RIGHT: (0, 1),
    }

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
        modification = self.MODIFICATION_BY_MOVE[direction]
        result_row = coordinate[0] + modification[0]
        result_col = coordinate[1] + modification[1]

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
