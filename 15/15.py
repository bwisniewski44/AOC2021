"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import deque
from structures import Grid


class Node:
    def __init__(self, coordinate):
        self.parent = None
        self.position = coordinate

        self.g = 0
        self.f = 0
        self.h = 0

    def __eq__(self, other):
        """
        TODO EXPLAIN

        :param Node other:

        :return:
        :rtype: bool
        """
        return self.position == other.position

    def __repr__(self):
        return f"({self.position[0]},{self.position[1]}): g{self.g} f{self.f} h{self.h}"


def resolve_path(current_node):
    """
    TODO EXPLAIN

    :param Node current_node:

    :return:
    :rtype: list[(int,int)]
    """

    # Follow the chain of nodes up to root
    visitation_order = deque()  # type: typing.Deque[typing.Tuple[int,int]]
    while current_node is not None:
        visitation_order.appendleft(current_node.position)
        current_node = current_node.parent

    return list(visitation_order)


def search(grid, start, end):
    """
    A* search algorithm, inspired by:
    https://towardsdatascience.com/a-star-a-search-algorithm-eb495fb156bb

    :param Grid grid:
    :param (int,int) start:
    :param (int, int) end:

    :return:
    :rtype: list[(int,int)]
    """

    # Create the start and goal nodes
    start_node = Node(start)
    goal_node = Node(end)

    # Initialize the 'yet-to-visit' and 'visited' lists
    yet_to_visit = []   # type: typing.List[Node]
    visited = set()     # type: typing.Set[typing.Tuple[int,int]]

    # Introduce the start node to TODO to what?
    yet_to_visit.append(start_node)  # TODO: maybe faster as heap/deque?

    # While there are nodes to search...
    while yet_to_visit:

        # Search for the most-optimal node; we'll select the leading node and iterate through all others to find that
        # with the best 'f'
        current_node = yet_to_visit[0]
        current_index = 0
        i = 1
        while i < len(yet_to_visit):
            alternative_node = yet_to_visit[i]
            if alternative_node.f < current_node.f:
                current_node = alternative_node
                current_index = i

            i += 1

        # If the node is the goal node, then we can stop
        if current_node == goal_node:
            return resolve_path(current_node)

        # We're still here, so we still have progress to make towards goal; begin by transferring the node out of the
        # 'yet-to-visit' list and into the 'visited' list
        yet_to_visit.pop(current_index)
        visited.add(current_node.position)

        # Find the children node to which we may travel
        for move_direction in (Grid.DOWN, Grid.RIGHT, Grid.UP, Grid.LEFT):
            try:
                next_coordinates = grid.move(current_node.position, move_direction)
            except IndexError:
                continue

            # Disqualify this destination if it's already been visited
            if next_coordinates in visited:
                continue

            # Define the destination's properties, then add to the 'yet to visit' list
            destination = Node(next_coordinates)
            destination.parent = current_node
            destination.g = current_node.g + grid[next_coordinates]
            destination.h = (
                    abs(destination.position[0] - goal_node.position[0]) +
                    abs(destination.position[1] - goal_node.position[1])
                )
            destination.f = destination.g + destination.h

            # Introduce this to the 'yet-to-visit' list if the node isn't already there OR if this one has a lower 'f'
            if any(entrant == destination and entrant.f < destination.f for entrant in yet_to_visit):
                continue
            yet_to_visit.append(destination)


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    begin = (0, 0)
    goal = (board.height-1, board.width-1)

    path = search(board, begin, goal)
    print(path)


if __name__ == "__main__":
    main()
