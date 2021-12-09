"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections.abc import Iterable

_LEGAL_SEGMENT_IDS = set("abcdefg")

# Below is a diagram of the segments lit for each respective digit expressed by a seven-segment display
"""

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

"""

TOP, TOP_LEFT, TOP_RIGHT, CENTER, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM = (
    "a", "b", "c", "d", "e", "f", "g"
)

_SEGMENTS_LIT_BY_VALUE = {
    # Resolves...
    # TOP: that of the three-segment expression which doesn't feature in the two-segment expression
    1: "cf",        # unique length!
    7: "acf",       # unique length!
    4: "bdcf",      # unique length!
    8: "abcdefg",   # unique length!

    # Resolves...
    # BOTTOM: it's the only segment common to all below besides TOP (resolved above)
    # CENTER: it's that of the expression containing all of 7's segments which is neither any of those nor top/bottom
    2: "acdeg",     # that containing two of 4's segments
    3: "acdfg",     # that containing all three segments of the 7
    5: "abdfg",     # that containing three of 4's segments

    0: "abcefg",    # that lacking CENTER
    6: "abdefg",
    9: "abcdfg",
}


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: list[(set[str], list[str])]
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    alphabets_and_sequences = []    # type: typing.List[typing.Tuple[typing.Set[str], typing.List[str]]]
    for line in lines:
        alphabet_half, digits_half = line.split("|")
        alphabet = set(normalize(element) for element in str.split(alphabet_half))
        digit_sequence = list(normalize(element) for element in str.split(digits_half))

        if len(digit_sequence) != 4:  # TODO: hardcoded??
            raise \
                ValueError(
                    f"Expecting {4} seven-digit-display expressions; found {len(digit_sequence)}: {digit_sequence}"
                )

        alphabets_and_sequences.append(
            (alphabet, digit_sequence)
        )

    return alphabets_and_sequences


def get_expressions_by_length(expressions):
    """
    TODO EXPLAIN

    :param set[str] expressions:

    :return:
    :rtype: dict[int,set[str]]
    """

    expressions_by_length = {}
    for expression in expressions:
        length = len(expression)

        if length in expressions_by_length:
            like_length_expressions = expressions_by_length[length]
        else:
            like_length_expressions = set()  # type: typing.Set[str]
            expressions_by_length[length] = like_length_expressions

        like_length_expressions.add(expression)

    return expressions_by_length


def normalize(segments):
    """
    TODO EXPLAIN

    :param Iterable[str] segments:

    :return:
    :rtype: str
    """

    unique_segments = set(segments)
    for ch in unique_segments:
        if ch not in _LEGAL_SEGMENT_IDS:
            raise ValueError(f"Encountered illegal segment code '{ch}'")
    normalized_form = "".join(sorted(unique_segments))
    return normalized_form


def extract_element(element_set):
    """
    TODO EXPLAIN

    :param set element_set:

    :return:
    """

    if len(element_set) != 1:
        raise ValueError(f"Expecting a single element in set, encountered {len(element_set)}")
    return next(iter(element_set))


def evaluate_expressions(expressions):
    """
    TODO EXPLAIN

    :param set[str] expressions:

    :raises ValueError: on invalid input or incomplete set of mappings

    :return: mapping of normalized expression (str) to value of digit it represents (int)
    :rtype: dict[str,int]
    """

    # Instantiate the result object and normalize the inbound expressions
    value_by_segments = {}  # type: typing.Dict[str, int]
    normalized_expressions = {normalize(expression) for expression in expressions}  # type: typing.Set[str]
    if not len(normalized_expressions) == 10:
        raise \
            ValueError(
                f"Expecting 10 distinct expressions, one for each digit; encountered {len(normalized_expressions)}"
            )

    # We can learn a lot by grouping the expressions together by length
    expressions_by_length = get_expressions_by_length(normalized_expressions)

    # Several of these have unique length: the 1 has two segments, the 7 has three, the 4 has four, the 8 has seven
    one_key, seven_key, four_key, eight_key = (
        extract_element(expressions_by_length[length]) for length in [2, 3, 4, 7]
    )  # type: str, str, str, str
    value_by_segments.update(
        {
            one_key: 1,
            seven_key: 7,
            four_key: 4,
            eight_key: 8
        }
    )

    # The top segment is that of 7's segments which isn't among 1's segments
    seven_segments = set(seven_key)
    one_segments = set(one_key)
    top_segment = next(iter(seven_segments.difference(one_segments)))

    # The five-segment expressions can really break this open for us...
    # * The 3 is that containing all of 7's segments
    # * The bottom is that common to all and *not* the top
    five_segment_expressions = expressions_by_length[5]
    two_segments = None     # type: typing.Optional[typing.Set[str]]    # to contain the 2's segments
    three_segments = None   # type: typing.Optional[typing.Set[str]]    # to contain the 3's segments
    five_segments = None    # type: typing.Optional[typing.Set[str]]    # to contain the 5's segments
    common_segments = set(next(iter(five_segment_expressions)))         # random pick, to be whittled down as iterating
    for five_segment_expression in five_segment_expressions:
        segments = set(five_segment_expression)

        # If this expression has all of 7's segments, it's the 3!
        commonalities_with_seven = segments.intersection(seven_segments)
        commonalities_with_four = segments.intersection(four_key)
        if len(commonalities_with_seven) == len(seven_segments):
            if three_segments is not None:
                raise ValueError("Already defined the 3-expression!")
            three_segments = segments

        # Otherwise, if it has two of 4's segments, it's the 2
        elif len(commonalities_with_four) == 2:
            two_segments = segments

        # Otherwise, it should have three commonalities with 4
        elif len(commonalities_with_four) == 3:
            five_segments = segments

        else:
            raise \
                ValueError(
                    f"Expression {five_segment_expression} fails to satisfy the requirements relative to "
                    f"commonalities shared with the 7's segments ({seven_segments}) and the 4's segments ({four_key})"
                )

        # Common segments can only be those shared by this expression
        common_segments = common_segments.intersection(five_segment_expression)

    # 3's segments should be defined by now
    two_key, three_key, five_key = (normalize(segments) for segments in [two_segments, three_segments, five_segments])
    value_by_segments.update(
        {
            two_key: 2,
            three_key: 3,
            five_key: 5
        }
    )

    # There should be three segments common to the 5-segment expressions: top, center, and bottom; we already know the
    # top... center is that which can be found in the 4, and bottom is that which is leftover
    if len(common_segments) != 3:
        raise \
            ValueError(
                f"Expecting exactly two segments common to the five-segment expressions: the bottom segment and the "
                f"top; found {len(common_segments)} segments"
            )
    try:
        common_segments.remove(top_segment)
    except KeyError:
        raise ValueError(f"Failed to find top segment {top_segment} among the common segments")
    commonalities_with_four = {segment in four_key: segment for segment in common_segments}
    try:
        center_segment = commonalities_with_four[1]
    except KeyError:
        raise ValueError(f"Expecting to find center segment as that being in the 4")
    try:
        bottom_segment = commonalities_with_four[0]
    except KeyError:
        raise ValueError(f"Expecting to find bottom segment as that not presenting in the 4")

    # At this point, only three keys elude us: 0, 6, and 9; we can find them as follows:
    #   0: that which lacks a center segment
    #   6: that which shares three segments with 4
    #   9: that which shares four segments with 4
    unsolved_keys = set(normalized_expressions).difference(value_by_segments)
    for key in unsolved_keys:
        if center_segment not in key:
            value_by_segments[key] = 0
        else:
            four_commonalities = len(set(key).intersection(four_key))
            if four_commonalities == 3:
                value_by_segments[key] = 6
            elif four_commonalities == 4:
                value_by_segments[key] = 9
            else:
                raise \
                    ValueError(
                        f"Key '{key}' neither has the center segment '{center_segment}' nor shares an expected number "
                        f"of segments with the 4-key '{four_key}'"
                    )

    # Done. Whew.
    if not len(value_by_segments) == 10:
        raise ValueError(f"Expecting 10 keys, but found {len(value_by_segments)}")
    return value_by_segments


def tally_digits_encountered(subject_values, alphabets_and_expressions):
    """
    TODO EXPLAIN

    :param set[int] subject_values:
    :param list[(set[str], list[str])] alphabets_and_expressions:

    :return:
    :rtype: int
    """

    tally_by_value = {}

    for alphabet, expressions in alphabets_and_expressions:
        value_by_expression = evaluate_expressions(alphabet)
        for expression in expressions:
            value = value_by_expression[expression]
            if value in subject_values:
                old_tally = tally_by_value.get(value, 0)
                tally_by_value[value] = old_tally + 1

    total_occurrences = sum(tally for _, tally in tally_by_value.items())
    return total_occurrences


def sum_output(alphabets_and_readings):
    """
    TODO EXPLAIN

    :param list[(set[str], list[str])] alphabets_and_readings:

    :return:
    :rtype: int
    """

    sum_total = 0

    for alphabet, expressions in alphabets_and_readings:
        values_by_expression = evaluate_expressions(alphabet)

        # Resolve the decimal digits for this sequence of output expressions
        decimal_digits = []  # type: typing.List[str]
        for expression in expressions:
            decimal_value = values_by_expression[expression]
            decimal_digits.append(str(decimal_value))

        # Resolve the value encoded by the decimal digit sequence
        output_value = int("".join(decimal_digits))
        sum_total += output_value

    return sum_total


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    alphabets_and_readings = load_input()

    print(tally_digits_encountered({1, 4, 7, 8}, alphabets_and_readings))
    print(sum_output(alphabets_and_readings))


if __name__ == "__main__":
    main()
