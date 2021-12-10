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
    :rtype: int | None
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
                return score

    return None


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    lines = load_input()

    score = 0
    for line in lines:
        syntax_error_value = scan(line)
        if syntax_error_value is not None:
            score += syntax_error_value
    print(score)


if __name__ == "__main__":
    main()
