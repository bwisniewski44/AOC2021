"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing

_INITIALIZING_TABLE = [
    ("(", 1, ")", 3),
    ("[", 2, "]", 57),
    ("{", 3, "}", 1197),
    ("<", 4, ">", 25137),
]

SYNTAX_ERROR = 0
COMPLETENESS_ERROR = 1


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: list[str]
    """

    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]
    return lines


def get_scoring_basis():
    """
    TODO EXPLAIN

    :return:
    :rtype: (dict[str,int] , dict[str,(str,int)])
    """

    unpaired_score_by_opener = {}                       # type: typing.Dict[str,int]
    expected_opener_and_mismatch_score_by_closer = {}   # type: typing.Dict[str,(str,int)]

    for opener, unpaired_score, closer, mismatch_close_score in _INITIALIZING_TABLE:
        unpaired_score_by_opener[opener] = unpaired_score
        expected_opener_and_mismatch_score_by_closer[closer] = (opener, mismatch_close_score)

    return unpaired_score_by_opener, expected_opener_and_mismatch_score_by_closer


def scan(line, unpaired_info_by_opener, mismatch_info_by_closer):
    """
    TODO EXPLAIN

    :param str line:
    :param dict[str,int] unpaired_info_by_opener:
    :param dict[str,(str,int)] mismatch_info_by_closer:

    :return:
    :rtype: (int, int) | None
    """

    unpaired_openers = []   # type: typing.List[str]
    for ch in line:
        if ch not in mismatch_info_by_closer:
            unpaired_openers.append(ch)
        else:
            expected_opener, score = mismatch_info_by_closer[ch]
            actual_opener = unpaired_openers.pop()
            if actual_opener != expected_opener:
                return SYNTAX_ERROR, score

    # If there are unpaired symbols, this is where we get a completeness error
    if not unpaired_openers:
        return None
    else:
        completeness_score = 0
        while unpaired_openers:
            opener = unpaired_openers.pop()
            completeness_score *= 5
            addend = unpaired_info_by_opener[opener]
            completeness_score += addend

        return COMPLETENESS_ERROR, completeness_score


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    lines = load_input()
    unmatched_score_by_opener, mismatch_info_by_closer = get_scoring_basis()

    syntax_error_sum = 0
    completeness_error_values = []  # type: typing.List[int]
    for line in lines:
        # Scan the line; it can be ignored unless there's an error
        error = scan(line, unmatched_score_by_opener, mismatch_info_by_closer)
        if error:
            # What we do with the error depends on the kind of error
            error_type, score = error
            if error_type == SYNTAX_ERROR:
                syntax_error_sum += score
            elif error_type == COMPLETENESS_ERROR:
                completeness_error_values.append(score)
            else:
                raise ValueError(f"Unrecognized error-type code {error_type}")

    # Part 1: sum of syntax error scores
    print(syntax_error_sum)

    # Part 2: median completeness error scores
    sorted_completeness_errors = sorted(completeness_error_values)
    if len(sorted_completeness_errors) % 2 == 0:
        raise \
            ValueError(
                f"Puzzle guarantees odd number of completeness scores, but encountered "
                f"{len(sorted_completeness_errors)}"
            )
    median_index = len(sorted_completeness_errors) // 2
    print(sorted_completeness_errors[median_index])


if __name__ == "__main__":
    main()
