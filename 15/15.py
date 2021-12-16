"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
from collections import deque
from structures import Grid, PriorityQueue


class Node:
    def __init__(self, coordinate, parent=None):
        """
        :param (int,int) coordinate: TODO EXPLAIN
        :param Node parent:
        """
        self.parent = parent
        self.position = coordinate

        self.g = 0
        self.f = 0
        self.h = 0

    def __lt__(self, other):
        """
        TODO EXPLAIN

        :param Node other:

        :return:
        :rtype: bool
        """
        return self.f < other.f

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


def search(grid, start_coordinates, goal_coordinates):
    """
    A* search algorithm, inspired by:
    https://towardsdatascience.com/a-star-a-search-algorithm-eb495fb156bb

    :param Grid grid:
    :param (int,int) start_coordinates:
    :param (int, int) goal_coordinates:

    :return:
    :rtype: list[(int,int)] | None
    """

    # Initialize the 'yet-to-visit' and 'visited' structures
    frontier = PriorityQueue()
    population_by_coordinate = {}  # type: typing.Dict[typing.Tuple[int,int], int]
    visited = set()     # type: typing.Set[typing.Tuple[int,int]]

    # Introduce the start node to the frontier
    start_node = Node(start_coordinates)
    frontier.push(start_node)  # TODO: maybe faster as heap/deque?
    population_by_coordinate[start_node.position] = 1

    # While there are nodes to search...
    path = None  # type: typing.Optional[typing.List[typing.Tuple[int,int]]]
    while len(frontier) > 0:

        # Search for the most-optimal node; we'll select the leading node and iterate through all others to find that
        # with the best 'f'
        optimal_node = frontier.pop()   # type: Node
        updated_population = population_by_coordinate[optimal_node.position] - 1
        if updated_population > 0:
            population_by_coordinate[optimal_node.position] = updated_population
        else:
            population_by_coordinate.pop(optimal_node.position)

        # If the node is the goal node, then we can stop
        if optimal_node.position == goal_coordinates:
            path = resolve_path(optimal_node)
            break

        # We're still here, so we still have progress to make towards goal; begin by transferring the node out of the
        # 'yet-to-visit' list and into the 'visited' list
        visited.add(optimal_node.position)

        # Find the children node to which we may travel
        for move_direction in (Grid.DOWN, Grid.RIGHT):
            try:
                next_coordinates = grid.move(optimal_node.position, move_direction)
            except IndexError:
                continue

            # Disqualify this destination if it's already been visited
            if next_coordinates in visited:
                continue

            # Define the destination's properties, then add to the 'yet to visit' list
            destination = Node(next_coordinates, parent=optimal_node)
            destination.g = optimal_node.g + grid[next_coordinates]
            destination.h = (
                    abs(destination.position[0] - goal_coordinates[0]) +
                    abs(destination.position[1] - goal_coordinates[1])
                )
            destination.f = destination.g + destination.h

            # Introduce this to the 'yet-to-visit' list if the node isn't already there OR if this one has a lower 'f'
            if destination.position not in population_by_coordinate:
                introduce = True
            else:
                # Introduce only if this destination has optimal 'f'
                introduce = True
                for item in frontier._values:
                    if item.position == destination.position and item.f < destination.f:
                        introduce = False
                        break
            if introduce:
                frontier.push(destination)
                population_by_coordinate[destination.position] = \
                    population_by_coordinate.get(destination.position, 0) + 1

    return path


def expand(grid, factor):
    """
    TODO EXPLAIN

    :param Grid grid:
    :param int factor:

    :return:
    :rtype: Grid
    """

    new_height = grid.height * factor
    new_width = grid.width * factor
    new_quantity = new_height * new_width

    new_grid = Grid([0 for _ in range(new_quantity)], new_height)
    for i in range(new_grid.height):
        for j in range(new_grid.width):
            tiles_down = i // grid.height
            tiles_over = j // grid.width
            adjustment = tiles_over + tiles_down

            basis_position = (i % grid.height, j % grid.width)
            basis_value = grid[basis_position]
            adjusted_value = (basis_value + adjustment) % 9
            if adjusted_value == 0:
                adjusted_value = 9
            new_grid[i, j] = adjusted_value

    return new_grid


def find_path(board):
    """
    TODO EXPLAIN

    :param Grid board:

    :return:
    :rtype: (int, list[(int,int)])
    """

    begin = (0, 0)
    goal = (board.height-1, board.width-1)

    path = search(board, begin, goal)
    score = sum(board[coordinate] for coordinate in path) - board[begin]

    return score, path


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    board = Grid.load("input.txt")

    # Part 1
    score, path = find_path(board)
    print(f"{score} for path: {path}")

    # Part 2
    board = expand(board, 5)
    score, path = find_path(board)
    print(f"{score} for path: {path}")


if __name__ == "__main__":
    main()
