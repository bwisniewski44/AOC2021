"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing

EXPECTED_OPENER_AND_SCORE_BY_CLOSER = {
    ")": ("(", 3),
    "]": ("[", 57),
    "}": ("{", 1197),
    ">": ("<", 25137),
}

COMPLETENESS_POINTS_BY_OPENER = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

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


def scan(line):
    """
    TODO EXPLAIN

    :param str line:

    :return:
    :rtype: (int, int) | None
    """

    unfinished_nodes = []   # type: typing.List[Node]
    for ch in line:
        if ch not in EXPECTED_OPENER_AND_SCORE_BY_CLOSER:
            node = Node(ch)
            unfinished_nodes.append(node)
        else:
            expected_opener, score = EXPECTED_OPENER_AND_SCORE_BY_CLOSER[ch]
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
            addend = COMPLETENESS_POINTS_BY_OPENER[node.opener]
            completeness_score += addend

        return COMPLETENESS_ERROR, completeness_score


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    lines = load_input()

    score_by_error = {}  # type: typing.Dict[int,int]
    for line in lines:
        # Scan the line; it can be ignored unless there's an error
        error = scan(line)
        if error:
            # There's an error; increment the respective error-type's score
            error_type, score = error
            old_score = score_by_error.get(error_type, 0)
            score_by_error[error_type] = old_score + score
    print(score_by_error.get(SYNTAX_ERROR, 0))
    print(score_by_error.get(COMPLETENESS_ERROR, 0))


if __name__ == "__main__":
    main()
