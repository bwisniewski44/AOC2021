
import typing
import math
from collections import deque

_EXPECTED_BOARD_SIZE = 5


def square_root(n):
    """
    TODO EXPLAIN

    :param int n:

    :raises ValueError: if given a value which is not a perfect square

    :return:
    :rtype: int
    """
    sqrt = math.floor(math.sqrt(n))
    actual_square = sqrt * sqrt
    if n == actual_square:
        return sqrt
    else:
        raise ValueError(f"{n} is not a perfect square")


class Board(object):

    class _Vector(object):
        """
        TODO EXPLAIN
        """

        def __init__(self, values):
            """
            :param list[int] values: TODO EXPLAIN
            """
            self.values = values
            self._marked_status_by_value = {value: False for value in values}    # type: typing.Dict[int,bool]
            self._unmarked_values = set(values)

        @property
        def all_marked(self):
            return len(self._unmarked_values) == 0

        def mark(self, value):
            """
            TODO EXPLAIN

            :param int value:

            :raises ValueError: if value doesn't belong to this vector

            :return: TRUE if this vector is fully-marked, FALSE otherwise (some values remain unmarked)
            :rtype: bool
            """

            self._marked_status_by_value[value] = True
            if value in self._unmarked_values:
                self._unmarked_values.remove(value)

            return self.all_marked

        def is_marked(self, value):
            """
            TODO EXPLAIN

            :param int value:

            :return:
            :rtype: bool
            """
            return self._marked_status_by_value[value]

    def __init__(self, numbers):
        """
        :param list[int] numbers: TODO EXPLAIN
        """

        if len(numbers) == 0:
            raise ValueError("Cannot initialize an empty board")

        board_width = square_root(len(numbers))

        # An element of any vector (row/column) is a 2-tuple:
        # 1. list[int] - sequence of values in the vector
        # 2. set[int]  - unmarked values in the vector
        # So, when that second element becomes an empty set, bingo has been achieved!
        rows = []     # type: typing.List[Board._Vector]
        columns = []  # type: typing.List[Board._Vector]
        for i in range(board_width):
            # Get i'th row-vector
            row_start_index = board_width * i               # inclusive bound
            row_end_index = row_start_index + board_width   # exclusive bound
            row_elements = numbers[row_start_index:row_end_index]
            rows.append(Board._Vector(row_elements))

            # Get the i'th column-vector
            column_elements = []    # type: typing.List[int]
            column_element_index = i
            while column_element_index < len(numbers):
                column_elements.append(numbers[column_element_index])
                column_element_index += _EXPECTED_BOARD_SIZE
            columns.append(Board._Vector(column_elements))

        # At this point, there should be 2X vectors (X being the width of the board): X vectors for the rows + X vectors
        # for the columns; we'll represent the board internally with a list of those vectors - rows first, then columns
        self._vectors = list(rows)
        self._vectors.extend(columns)

        # It'd also help to know which vectors to modify given a value being marked on this board, so we'll map possible
        # values to the vectors requiring modification
        self._vector_indices_by_value = {}  # type: typing.Dict[int,typing.Set[int]]
        for vector_index, vector in enumerate(self._vectors):
            for value in vector.values:
                # Get the set of vectors to be updated upon marking the value; we'll have to add this vector to that set
                if value in self._vector_indices_by_value:
                    vectors_to_update = self._vector_indices_by_value[value]
                else:
                    vectors_to_update = set()   # type: typing.Set[int]
                    self._vector_indices_by_value[value] = vectors_to_update

                # Introduce this vector (well, its index) to the set of those which merit update upon marking the
                # respective value
                vectors_to_update.add(vector_index)

        # Finally, we'll flip this variable upon having detected a win
        self._bingo_achieved = False

    @property
    def bingo(self):
        return self._bingo_achieved

    @property
    def width(self):
        return len(self._vectors[0].values)

    @property
    def height(self):
        return self.width

    def at(self, i, j):
        """
        TODO EXPLAIN

        :param int i:
        :param int j:

        :return:
        :rtype: (int, bool)
        """
        width = height = self.width
        if i > height or j > width:
            raise \
                ValueError(
                    f"Illegal coordinates ({i},{j}); max row index is {height-1} and max column index is {width-1}"
                )

        row_vector = self._vectors[i]   # type: Board._Vector
        value = row_vector.values[j]    # type: int
        is_marked = row_vector.is_marked(value)
        return value, is_marked

    def mark(self, n):
        """
        TODO EXPLAIN

        :param int n:

        :return: TRUE if the 'bingo' status of this board changed; FALSE otherwise (already had bingo, or value failed
          to deliver bingo to an incomplete board)
        :rtype: bool
        """

        already_had_bingo = self.bingo

        # If this board is sensitive to the given value...
        has_completed_vector = already_had_bingo
        if n in self._vector_indices_by_value:
            # ... update all sensitive vectors
            for i in self._vector_indices_by_value[n]:
                vector = self._vectors[i]
                has_completed_vector |= vector.mark(n)

        # Update the state of this board
        self._bingo_achieved = has_completed_vector
        bingo_for_this_call = not already_had_bingo and has_completed_vector
        return bingo_for_this_call


def pop_values(lines, separator=None):
    """
    TODO EXPLAIN

    :param deque[str] lines:
    :param str separator:

    :return:
    :rtype: list[int]
    """

    next_line = lines.popleft()

    if separator:
        unformatted_values = str.split(next_line, separator)
    else:
        unformatted_values = str.split(next_line)

    formatted_values = []   # type: typing.List[int]
    for unformatted_value in unformatted_values:
        formatted_value = int(str.strip(unformatted_value))
        formatted_values.append(formatted_value)

    return formatted_values


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :return: 2-tuple giving...
      1. list[int] - sequence of drawn numbers
      2. list[Board] - sequence of game-boards
    :rtype: (list[int], list[Board])
    """
    with open(path) as infile:
        lines = deque(str.strip(line) for line in infile.readlines())

    # Read the leading line; should be a sequence of comma-separated values: the sequence of numbers to be drawn
    drawn_numbers = pop_values(lines, separator=",")

    # What lines remain are the board definitions; ensure that the number of lines is a multiple of the number of lines
    # which define a board (if not, then some board didn't get completely expressed)
    game_boards = []    # type: typing.List[Board]
    board_lines = _EXPECTED_BOARD_SIZE + 1  # number of lines required for a single board (rows + separating line)
    if len(lines) % board_lines != 0:
        raise \
            ValueError(
                f"Format error for file '{path}'; found {len(lines)} lines to give board definitions: expecting a "
                f"multiple of {board_lines}"
            )
    while len(lines) > 0:
        lines.popleft()  # discard the separating line

        # Build up the sequence of numbers, left-to-right then top-to-bottom, representing the board
        board_values = []   # type: typing.List[int]
        i = 0
        while i < _EXPECTED_BOARD_SIZE:
            board_values.extend(pop_values(lines))
            i += 1
        game_boards.append(Board(board_values))

    return drawn_numbers, game_boards


def compute_score(board, last_number):
    """
    TODO EXPLAIN

    :param Board board:
    :param int last_number:

    :return:
    :rtype: bool
    """
    sum_unmarked_numbers = 0
    for row_index in range(board.height):
        for column_index in range(board.width):
            value, is_marked = board.at(row_index, column_index)
            if not is_marked:
                sum_unmarked_numbers += value

    return sum_unmarked_numbers * last_number


def get_win_sequence(value_sequence, boards):
    """
    TODO EXPLAIN

    :param list[int] value_sequence:
    :param list[Board] boards:

    :raises RuntimeError: if no board wins

    :return: sequence of 2-tuples representing the sequence of wins; each 2-tuple gives...
      1. (int) the index of the draw which resulted in the respective win
      2. (int) the index of the board of the respective win
    :rtype: list[(int,int)]
    """

    if len(value_sequence) == 0:
        raise ValueError("Cannot supply an empty value sequence")

    # Iterate over the values until we have a winning board
    remaining_boards = set(range(len(boards)))
    win_sequence = []       # type: typing.List[typing.Tuple[int,int]]  # index of draw, index of board
    for draw_index, value in enumerate(value_sequence):
        # If all the boards have bingo, no point in drawing further numbers
        if not remaining_boards:
            break

        for board_index in sorted(remaining_boards):
            board = boards[board_index]
            bingo = board.mark(value)
            if bingo:
                win_sequence.append((draw_index, board_index))
                remaining_boards.remove(board_index)

    return win_sequence


def do():
    """
    TODO EXPLAIN

    :return: None
    """

    value_sequence, game_boards = load_input()

    win_sequence = get_win_sequence(value_sequence, game_boards)

    wins_to_print = [win_sequence[0], win_sequence[-1]]
    for draw_index, board_index in wins_to_print:
        drawn_value = value_sequence[draw_index]
        board = game_boards[board_index]
        print(f"{compute_score(board, drawn_value)}")


if __name__ == "__main__":
    do()
