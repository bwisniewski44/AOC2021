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


class Node(object):
    """
    TODO EXPLAIN
    """

    def __init__(self, opener):
        """
        :param str opener:
        """
        self.opener = opener
        self.closer = None
        self.children = []  # type: typing.List[Node]


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

    unfinished_nodes = []   # type: typing.List[Node]
    for ch in line:
        if ch not in mismatch_info_by_closer:
            node = Node(ch)
            unfinished_nodes.append(node)
        else:
            expected_opener, score = mismatch_info_by_closer[ch]
            node = unfinished_nodes.pop()
            parent_node = unfinished_nodes[-1]
            parent_node.children.append(node)

            actual_opener = node.opener
            if actual_opener != expected_opener:
                return SYNTAX_ERROR, score

    # If there are unpaired symbols, this is where we get a completeness error
    if not unfinished_nodes:
        return None
    else:
        completeness_score = 0
        for node in unfinished_nodes:
            completeness_score *= 5
            addend = unpaired_info_by_opener[node.opener]
            completeness_score += addend

        return COMPLETENESS_ERROR, completeness_score


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    lines = load_input()
    unmatched_score_by_opener, mismatch_info_by_closer = get_scoring_basis()

    score_by_error = {}  # type: typing.Dict[int,int]
    for line in lines:
        # Scan the line; it can be ignored unless there's an error
        error = scan(line, unmatched_score_by_opener, mismatch_info_by_closer)
        if error:
            # There's an error; increment the respective error-type's score
            error_type, score = error
            old_score = score_by_error.get(error_type, 0)
            score_by_error[error_type] = old_score + score
    print(score_by_error.get(SYNTAX_ERROR, 0))
    print(score_by_error.get(COMPLETENESS_ERROR, 0))


if __name__ == "__main__":
    main()
