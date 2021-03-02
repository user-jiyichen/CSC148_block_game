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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains some sample tests for Assignment 2.
Please use this as a starting point to check your work and write your own
tests!
"""
from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten
from player import _get_block, _get_random_block
from renderer import Renderer
from settings import COLOUR_LIST


def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)


@pytest.fixture
def renderer() -> Renderer:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    return Renderer(750)


@pytest.fixture
def child_block() -> Block:
    """Create a reference child block with a size of 750 and a max_depth of 0.
    """
    return Block((0, 0), 750, COLOUR_LIST[0], 0, 0)


@pytest.fixture
def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_2x2() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 1.
    """
    # level 0
    board = Block((0, 0), 750, None, 0, 1)

    # level 1
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board, colours)

    return board


@pytest.fixture
def board_2x2_2() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # level 0
    board = Block((0, 0), 750, None, 0, 2)

    # level 1
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    # level 2

    return board


@pytest.fixture
def board_4x4_3() -> Block:
    """Create a reference board with a size of 100 and a max_depth of 3.
    """
    # level 0
    board = Block((0, 0), 100, None, 0, 3)

    # level 1
    colours = [COLOUR_LIST[3], None, None, None]
    set_children(board, colours)

    # level 2
    colours_1 = [COLOUR_LIST[1], None, COLOUR_LIST[0], COLOUR_LIST[1]]
    set_children(board.children[1], colours_1)
    colour_2 = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[0], COLOUR_LIST[0]]
    set_children(board.children[2], colour_2)
    colour_3 = [COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[2]]
    set_children(board.children[3], colour_3)

    # level 3
    colour = [COLOUR_LIST[0], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[3]]
    set_children(board.children[1].children[1], colour)

    return board


@pytest.fixture
def child_board_swap() -> Block:
    return Block((0, 0), 750, COLOUR_LIST[0], 0, 0)


@pytest.fixture
def board_16x16_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def board_16x16_swap1() -> Block:
    """Create a reference board that is swapped along the vertical plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    return board


@pytest.fixture
def board_16x16_swap0_top_right() -> Block:
    """Create a reference board that the top-right block of the reference board
     is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_swap1_top_left() -> Block:
    """Create a reference board that the top-left block of the reference board
     is swapped along the vertical plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[0]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def board_2x2_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # level 0
    board = Block((0, 0), 750, None, 0, 1)
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[3]]
    set_children(board, colours)

    return board


@pytest.fixture
def board_16x16_rotate1() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_rotate3_top_right() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated counter-clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_rotate3() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated counter-clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[3], None, COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def flattened_board_16x16() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]


def test_block_to_squares_leaf(child_block) -> None:
    """Test that a board with only one block can be correctly trasnlated into
    a square that would be rendered onto the screen.
    """
    squares = _block_to_squares(child_block)
    expected = [(COLOUR_LIST[0], (0, 0), 750)]

    assert squares == expected


def test_block_to_squares_reference1(board_2x2) -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    squares = set(_block_to_squares(board_2x2))
    expected = {((199, 44, 58), (375, 0), 375),
                ((138, 151, 71), (0, 0), 375),
                ((255, 211, 92), (0, 375), 375),
                ((1, 128, 181), (375, 375), 375)}
    assert squares == expected


def test_block_to_squares_reference2(board_16x16) -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    squares = set(_block_to_squares(board_16x16))
    expected = {((1, 128, 181), (563, 0), 188),
                ((199, 44, 58), (375, 0), 188),
                ((199, 44, 58), (375, 188), 188),
                ((255, 211, 92), (563, 188), 188),
                ((138, 151, 71), (0, 0), 375),
                ((199, 44, 58), (0, 375), 375),
                ((255, 211, 92), (375, 375), 375)
                }

    assert squares == expected


def test_create_copy1(child_block) -> None:
    copy = child_block.create_copy()
    assert id(child_block) != id(copy)


def test_create_copy2(board_16x16) -> None:
    copy = board_16x16.create_copy()
    assert id(board_16x16) != id(copy)
    assert id(board_16x16.children[0] != copy.children[0])
    assert not (id(board_16x16.children[1]) == id(copy.children[1]))


class TestRender:
    """A collection of methods that show you a way to save the boards in your
    test cases to image (i.e., PNG) files.

    NOTE: this requires that your blocky._block_to_squares function is working
    correctly.
    """
    def test_render_reference_board(self, renderer, board_16x16) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('reference-board.png')

    def test_render_reference_board_swap0(self, renderer, board_16x16,
                                          board_16x16_swap0) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_swap0))
        renderer.save_to_file('reference-swap-0.png')

        # Render what your swap does to the reference board
        board_16x16.swap(0)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-swap-0.png')

    def test_render_reference_board_rotate1(self, renderer, board_16x16,
                                            board_16x16_rotate1) -> None:
        """Render the reference board to a file so that you can view it on your
        computer."""
        # Render the reference board swapped
        renderer.draw_board(_block_to_squares(board_16x16_rotate1))
        renderer.save_to_file('reference-rotate-1.png')

        # Render what your swap does to the reference board
        board_16x16.children[0].rotate(1)
        renderer.clear()
        renderer.draw_board(_block_to_squares(board_16x16))
        renderer.save_to_file('your-rotate-1.png')


class TestBlock:
    """A collection of methods that test the Block class.

    NOTE: this is a small subset of tests - just because you pass them does NOT
    mean you have a fully working implementation of the Block class.
    """
    def test_smash_on_child(self, child_block) -> None:
        """Test that a child block cannot be smashed.
        """
        child_block.smash()

        assert len(child_block.children) == 0
        assert child_block.colour == COLOUR_LIST[0]

    def test_smash_on_parent_with_no_children(self, board_16x16) -> None:
        """Test that a block not at max_depth and with no children can be
        smashed.
        """
        block = board_16x16.children[1]
        block.smash()

        assert len(block.children) == 4
        assert block.colour is None

        for child in block.children:
            if len(child.children) == 0:
                # A leaf should have a colour
                assert child.colour is not None
                # Colours should come from COLOUR_LIST
                assert child.colour in COLOUR_LIST
            elif len(child.children) == 4:
                # A parent should not have a colour
                assert child.colour is None
            else:
                # There should only be either 0 or 4 children (RI)
                assert False

    def test_swap0_no_children(self, child_block, child_board_swap) -> None:
        """Test that the reference board stays the same since it has no
        children."""
        child_block.swap(1)
        child_block.swap(0)
        assert child_block == child_board_swap

    def test_swap0_16x16(self, board_16x16, board_16x16_swap0) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        board_16x16.swap(0)
        assert board_16x16 == board_16x16_swap0

    def test_swap1_16x16(self, board_16x16, board_16x16_swap1) -> None:
        """Test that the reference board can be correctly swapped along the
        vertical plane.
        """
        board_16x16.swap(1)
        assert board_16x16 == board_16x16_swap1

    def test_swap0_16x16_top_right(self, board_16x16,
                                   board_16x16_swap0_top_right) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly swapped along the horizontal plane.
        """
        board_16x16.children[0].swap(0)
        assert board_16x16 == board_16x16_swap0_top_right

    def test_swap1_16x16_top_left(self, board_16x16,
                                  board_16x16_swap1_top_left) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly swapped along the vertical plane.
        """
        board_16x16.swap(0)
        board_16x16.children[1].swap(1)
        assert board_16x16 == board_16x16_swap1_top_left

    def test_swap0_2x2(self, board_2x2, board_2x2_swap0) -> None:
        """Test that the reference board can be correctly swapped along the
        horizontal plane.
        """
        board_2x2.swap(0)
        assert board_2x2 == board_2x2_swap0

    def test_rotate1(self, board_16x16, board_16x16_rotate1) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly rotated clockwise.
        """
        board_16x16.children[0].rotate(1)
        assert board_16x16 == board_16x16_rotate1

    def test_rotate3(self, board_16x16, board_16x16_rotate3) -> None:
        """Test that the reference board can be correctly rotated
        counter-clockwise.
        """
        board_16x16.rotate(3)
        assert board_16x16 == board_16x16_rotate3

    def test_rotate3_top_right(self, board_16x16,
                               board_16x16_rotate3_top_right) -> None:
        """Test that the top-right block of reference board on level 1 can be
        correctly rotated counter-clockwise.
        """
        board_16x16.children[0].rotate(3)
        assert board_16x16 == board_16x16_rotate3_top_right


class TestPlayer:
    """A collection of methods for testing the methods and functions in the
    player module.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation.
    """
    def test_get_block_top_left(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-left corner of the board.
        """
        top_left = (0, 0)
        assert _get_block(board_16x16, top_left, 0) == board_16x16
        assert _get_block(board_16x16, top_left, 1) == board_16x16.children[1]

    def test_get_block_top_right(self, board_16x16) -> None:
        """Test that the correct block is retrieved from the reference board
        when requesting the top-right corner of the board.
        """
        top_right = (board_16x16.size - 1, 0)
        bottom_left = (0, board_16x16.size - 1)
        assert _get_block(board_16x16, top_right, 0) == board_16x16
        assert _get_block(board_16x16, top_right, 1) == board_16x16.children[0]
        assert _get_block(board_16x16, top_right, 2) == \
            board_16x16.children[0].children[0]
        assert _get_block(board_16x16, bottom_left, 0) == board_16x16
        assert _get_block(board_16x16, bottom_left, 1) == \
            board_16x16.children[2]
        assert _get_block(board_16x16, bottom_left, 2) == board_16x16.children[2]

    def test_get_block_middle(self, board_2x2) -> None:
        middle = (board_2x2.size / 2, board_2x2.size / 2)
        assert _get_block(board_2x2, middle, 0) == board_2x2
        assert _get_block(board_2x2, middle, 1) == board_2x2.children[3]

    def test_get_block_middle1(self, board_2x2_2) -> None:
        middle = (board_2x2_2.size / 2, board_2x2_2.size / 2)
        left_middle = (0, board_2x2_2.size / 2)
        assert _get_block(board_2x2_2, middle, 2) == board_2x2_2.children[3]
        assert _get_block(board_2x2_2, left_middle) == board_2x2_2.children[2]


class TestGoal:
    """A collection of methods for testing the sub-classes of Goal.

     NOTE: this is a small subset of tests - just because you pass them does NOT
     mean you have a fully working implementation of the Goal sub-classes.
    """
    def test_block_flatten(self, board_16x16, flattened_board_16x16) -> None:
        """Test that flattening the reference board results in the expected list
        of colours.
        """
        result = _flatten(board_16x16)

        # We are expected a "square" 2D list
        for sublist in result:
            assert len(result) == len(sublist)

        assert result == flattened_board_16x16

    def test_blob_goal_unit(self, child_block) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 0),
            (COLOUR_LIST[2], 0),
            (COLOUR_LIST[3], 0)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(child_block) == expected

    def test_blob_goal_1(self, board_16x16) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 4),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check the results
        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_16x16) == expected

    def test_blob_goal_2(self, board_4x4_3) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 12),
            (COLOUR_LIST[1], 12),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 24)
        ]

        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_4x4_3) == expected

    def test_blob_goal_3(self, board_2x2) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 1),
            (COLOUR_LIST[1], 1),
            (COLOUR_LIST[2], 1),
            (COLOUR_LIST[3], 1)
        ]

        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_2x2) == expected

    def test_blob_goal_4(self, board_2x2_2) -> None:
        correct_scores = [
            (COLOUR_LIST[0], 0),
            (COLOUR_LIST[1], 8),
            (COLOUR_LIST[2], 8),
            (COLOUR_LIST[3], 0)
        ]

        for colour, expected in correct_scores:
            goal = BlobGoal(colour)
            assert goal.score(board_2x2_2) == expected

    def test_perimeter_goal_1(self, board_16x16):
        correct_scores = [
            (COLOUR_LIST[0], 2),
            (COLOUR_LIST[1], 5),
            (COLOUR_LIST[2], 4),
            (COLOUR_LIST[3], 5)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_16x16) == expected

    def test_perimeter_goal_2(self, child_block):
        correct_scores = [
            (COLOUR_LIST[0], 4),
            (COLOUR_LIST[1], 0),
            (COLOUR_LIST[2], 0),
            (COLOUR_LIST[3], 0)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(child_block) == expected

    def test_perimeter_goal_3(self, board_2x2):
        correct_scores = [
            (COLOUR_LIST[0], 2),
            (COLOUR_LIST[1], 2),
            (COLOUR_LIST[2], 2),
            (COLOUR_LIST[3], 2)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_2x2) == expected

    def test_perimeter_goal_4(self, board_4x4_3):
        correct_scores = [
            (COLOUR_LIST[0], 11),
            (COLOUR_LIST[1], 2),
            (COLOUR_LIST[2], 8),
            (COLOUR_LIST[3], 11)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_4x4_3) == expected

    def test_perimeter_goal_5(self, board_2x2_2):
        correct_scores = [
            (COLOUR_LIST[0], 0),
            (COLOUR_LIST[1], 8),
            (COLOUR_LIST[2], 8),
            (COLOUR_LIST[3], 0)
        ]

        # Set up a goal for each colour and check results.
        for colour, expected in correct_scores:
            goal = PerimeterGoal(colour)
            assert goal.score(board_2x2_2) == expected

if __name__ == '__main__':
    pytest.main(['example_tests.py'])
