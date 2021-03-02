"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def _select_colour(copy: List) -> Tuple[int, int, int]:
    """A private helper function of [generate_goals].
    Randomly choose a colour in the COLOUR_LIST for the goal.
    """
    colour = random.choice(copy)
    copy.remove(colour)
    return colour


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    i = 0
    goal = []
    goal_type = ['Perimeter', 'Blob']
    colour_copy = COLOUR_LIST[:]
    if random.choice(goal_type) == 'Perimeter':
        while i < num_goals:
            colour = _select_colour(colour_copy)
            goal.append(PerimeterGoal(colour))
            i += 1
        return goal
    else:
        while i < num_goals:
            colour = _select_colour(colour_copy)
            goal.append(BlobGoal(colour))
            i += 1
        return goal


def _combine(lst1: List[List], lst2: List[List]) -> List[List]:
    """A helper function for [_flatten].
    Return a nested list of combining every sublist of [lst1] and [lst2] at
    the same index.
    Precondition: len(lst1) == len(lst2)
    """
    lst = []
    for i in range(len(lst1)):
        lst.append(lst1[i] + lst2[i])
    return lst


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    grid = []
    max_depth = block.max_depth
    grid_size = 2 ** (max_depth - block.level)
    if len(block.children) == 0:  # base case when the block has no children
        i = 0
        while i < grid_size:
            column = []
            j = 0
            while j < grid_size:
                column.append(block.colour)
                j += 1
            grid.append(column)
            i += 1
        return grid
    else:
        child_grid = []
        children = block.children
        for child in children:
            child_grid.append(_flatten(child))
        grid = _combine(child_grid[1], child_grid[2]) + _combine(child_grid[0],
                                                                 child_grid[3])
        return grid


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A perimeter goal which is to put the most possible units of the target
     colour on the outer perimeter of the board. The corner cells are counted
     twice towards the score.

    """
    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """Return the current score for the perimeter goal on the given board.
        Non-corner unit cells are counted once towards the score and corner
        unit cells are counted twice.

        The score is greater than or equal to 0.

        """
        flatten = _flatten(board)
        count = 0
        if len(flatten) == 1:
            return count + self._boundary_score(flatten[0])
        if len(flatten) > 2:
            for clm in flatten[1:-1]:
                if clm[0] == self.colour:
                    count += 1
                if clm[-1] == self.colour:
                    count += 1
        return count + self._boundary_score(flatten[0]) + \
            self._boundary_score(flatten[-1])

    def _boundary_score(self, lst: List) -> int:
        """A helper function of [score]. Calculate the score the player gets
        on the boundary column [lst]. The first and the second items of the
        column [lst] count twice towards the score.
        """
        score = 0
        if lst[0] == self.colour:
            score += 2
        if lst[-1] == self.colour:
            score += 2
        if len(lst) > 2:
            for colour in lst[1:-1]:
                if colour == self.colour:
                    score += 1
        return score

    def description(self) -> str:
        """Return a string describing the rule of the perimeter goal and
        the target colour of this goal.
        """
        return f"Perimeter goal! Put the most possible" \
               f" {colour_name(self.colour)} units on the outer perimeter."


class BlobGoal(Goal):
    """A blob goal in the game of blocky.

     A blob is a group of connected blocks with the same colour.
     Two blocks are connected if their sides touch; touching corners does not
     count.

     The BlobGoal is to find the largest blob with the target colour.

    """
    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """Return the current score for the blob goal on the given board.
       The player’s score is the number of unit cells in the largest blob of
       the target colour.

       The score is greater than or equal to 0.
       """
        score = []
        visited = []

        j = 0
        flatten = _flatten(board)
        while j < len(flatten):
            i = 0
            minus_1 = []
            while i < len(flatten):
                minus_1.append(-1)
                i += 1
            visited.append(minus_1)
            j += 1
        # now we get the visited list

        for c in range(len(flatten)):
            for r in range(len(flatten)):
                score.append(self._undiscovered_blob_size((c, r),
                                                          flatten, visited))
        return max(score)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        clm = pos[0]
        row = pos[1]
        size = 1
        if clm >= len(board) or row >= len(board) or clm < 0 or \
                row < 0:
            return 0
        # the case when out of bounds

        elif board[clm][row] != self.colour:
            visited[clm][row] = 0
            return 0
        elif visited[clm][row] != -1:
            return 0
        else:
            visited[clm][row] = 1
            size += self._undiscovered_blob_size((clm + 1, row),
                                                 board, visited)
            size += self._undiscovered_blob_size((clm - 1, row),
                                                 board, visited)
            size += self._undiscovered_blob_size((clm, row + 1),
                                                 board, visited)
            size += self._undiscovered_blob_size((clm, row - 1),
                                                 board, visited)
            return size

    def description(self) -> str:
        """Return a string describing the rule of the blob goal and
        the target colour of this goal.
        """
        return f"Blob goal! Your aim is to connect the largest " \
               f"{colour_name(self.colour)} blocks."


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
