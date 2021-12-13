"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing

KEY_GOAL = "end"
KEY_START = "start"
SEPARATOR = "-"


class NodeInfo(object):
    """
    TODO EXPLAIN
    """

    # TODO: explain
    SMALL = 0
    LARGE = 1

    def __init__(self, name):
        """
        :param str name: TODO EXPLAIN
        """
        self.name = name
        self.size = NodeInfo.LARGE if name.isupper() else NodeInfo.SMALL
        self.visits = 0
        self.neighbors = set()  # type: typing.Set[str]


def add_destination(all_nodes, origin, destination):
    """
    TODO EXPLAIN

    :param dict[str,NodeInfo] all_nodes:
    :param str origin:
    :param str destination:

    :return: None
    """

    if origin in all_nodes:
        node_info = all_nodes[origin]
    else:
        node_info = NodeInfo(origin)
        all_nodes[origin] = node_info
    node_info.neighbors.add(destination)


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return:
    :rtype: dict[str,NodeInfo]
    """

    info_by_node = {}  # type: typing.Dict[str,NodeInfo]

    with open(path) as infile:
        for line in infile.readlines():
            # Extract and validate the content of this line
            try:
                half_a, half_b = map(str.strip, line.split(SEPARATOR))  # type: str, str
            except ValueError:
                raise \
                    ValueError(
                        f"Expecting exactly two elements, joined by separator '{SEPARATOR}'; found "
                        f"{line.count(SEPARATOR)+1} element(s)"
                    )
            if half_a == half_b:
                raise ValueError(f"Node {repr(half_a)} cannot be its own neighbor")
            elif not all(name.isalpha() for name in {half_a, half_b}):
                raise \
                    ValueError(
                        f"Expecting all-letters for node names; encountered: "
                        f"{', '.join(repr(name) for name in {half_a, half_b})}"
                    )

            # Ensure the nodes are registered and see each other as neighbors
            add_destination(info_by_node, half_a, half_b)
            add_destination(info_by_node, half_b, half_a)

    return info_by_node


def add_paths_from(node, info_by_node, all_paths, allow_double_dipping, current_path=None, double_dipped=False):
    """
    TODO EXPLAIN

    :param str node:
    :param dict[str,NodeInfo] info_by_node:
    :param list[list[str]] all_paths:
    :param bool allow_double_dipping:
    :param list[str] | None current_path:
    :param bool double_dipped:

    :return: None
    """

    # Before we do anything, a bit of housekeeping: if the current path is NONE, this must be the root call of this
    # recursive function... initialize the current path to an empty sequence of visited nodes
    if current_path is None:
        current_path = []

    # We've arrived at a new node! Increment its visitation counter
    current_path.append(node)
    node_info = info_by_node[node]
    node_info.visits += 1
    if node_info.size == NodeInfo.SMALL and node_info.visits == 2:
        double_dipped = True

    if node == KEY_GOAL:
        all_paths.append(list(current_path))
    else:
        # This isn't the goal node; need to explore further nodes to be able to reach the goal
        for destination in node_info.neighbors:
            # We can visit bigger nodes whenever we want; the smaller nodes however have limits, so if we've visited the
            # node before...
            destination_info = info_by_node[destination]
            if destination_info.size == NodeInfo.SMALL and destination_info.visits > 0:
                # ... we can only re-visit (double-dip) only if we've yet to double-dip AND if the node is neither the
                # start/end nodes; so, if we've already double-dipped or the dest. would otherwise be start/end, skip
                if not allow_double_dipping or double_dipped or destination in {KEY_START, KEY_GOAL}:
                    continue

            # We haven't "continued", so we must be OK to proceed to destination
            add_paths_from(destination, info_by_node, all_paths, allow_double_dipping, current_path, double_dipped)

    # All paths stemming from the 'current path' have been added; let's pop the node off the 'current path' as if we
    # never arrived here... the caller can then explore other routes to GOAL
    current_path.pop()
    node_info.visits -= 1


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    info_by_node = load_input()

    legality_modes = [False, True]
    for allow_double_dipping in legality_modes:
        all_paths = []  # type: typing.List[typing.List[str]]
        add_paths_from(KEY_START, info_by_node, all_paths, allow_double_dipping)
        print(len(all_paths))


if __name__ == "__main__":
    main()
