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

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    player = []
    goals = generate_goals(num_human + num_random + len(smart_players))
    for i in range(num_human):
        player.append(HumanPlayer(i, goals[i]))
    for j in range(num_random):
        player.append(RandomPlayer(num_human + j, goals[num_human + j]))
    for k in range(len(smart_players)):
        player.append(SmartPlayer(num_human + num_random + k,
                                  goals[num_human + num_random + k],
                                  smart_players[k]))
    return player


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """

    """
    if level == block.level:  # base case
        if x <= location[0] < x + size and y <= location[1] < y + size:
            return block
        else:
            return None
    else:
        for child in block.children:
            child_lev = lev + 1  # ???
            block_got = _get_block(child, location, level)
            if block_got is not None and level >= child_lev:
                return block_got

        return None
    """
    x = block.position[0]
    y = block.position[1]
    size = block.size
    if not (x <= location[0] < x + size and y <= location[1] < y + size):
        return None

    # a block includes location
    if level == block.level:
        return block
    elif not block.children:  # current block is the deepest
        return block
    else:
        for child in block.children:
            block_got = _get_block(child, location, level)
            if block_got is not None:
                return block_got
        return None


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """Return a tuple consisting of the name of the move, the optional
    direction of certain moves, and the block the move is operated on.
    """
    return action[0], action[1], block


def _get_random_block(board: Block) -> Block:
    """A helper method for <generate_move>.
    Return a block with random level and random position.
    """
    i = 0
    depth_lst = []
    while i <= board.max_depth:
        depth_lst.append(i)
        i += 1  # get a list of depths
    random_depth = random.choice(depth_lst)
    size = board.size
    position = (random.uniform(0, size), random.uniform(0, size))
    block_got = _get_block(board, position, random_depth)
    assert block_got is not None
    return block_got


def _generate_move_and_block(copy: Block, board: Block,
                             goal: Goal) -> \
        Tuple[str, Optional[int], Block]:
    """A helper function for <generate_move>.
    <copy> is a hard copy of the <board> and moves are operated on that copy
    in order not to mutate the original <board>.

    Return a tuple of a random valid move and a random block from the <board>.
    Return None if no moves are valid.
    """
    signal = False
    valid_list = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, SMASH,
                  SWAP_HORIZONTAL, SWAP_VERTICAL, PAINT, COMBINE]
    # get a list of valid moves
    valid_move = None
    while not signal:
        random_move = random.choice(valid_list)
        random_block = _get_random_block(copy)
        actual_block = _get_block(board, random_block.position,
                                  random_block.level)
        if random_move in [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE]:
            if copy.rotate(1) or copy.rotate(3):
                signal = True
                valid_move = _create_move(random_move, actual_block)
        elif random_move in [SWAP_HORIZONTAL, SWAP_VERTICAL]:
            if copy.swap(0) or copy.swap(1):
                signal = True
                valid_move = _create_move(random_move, actual_block)
        elif random_move == SMASH:
            if copy.smash():
                signal = True
                valid_move = _create_move(random_move, actual_block)
        elif random_move == COMBINE:
            if copy.combine():
                signal = True
                valid_move = _create_move(random_move, actual_block)
        elif random_move == PAINT:
            if copy.paint(goal.colour):
                signal = True
                valid_move = _create_move(random_move, actual_block)
    return valid_move


class HumanPlayer(Player):
    """A human player.

    === Private Attributes ===
     _level:
         The level of the Block that the user selected most recently.
     _desired_action:
         The most recent action that the user is attempting to do.


     == Representation Invariants concerning the private attributes ==
         _level >= 0
    """

    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """A random player who makes moves randomly.

    We use <random> module to implement randomness.

     === Public Attributes ===
     id:
       This player's number.
     goal:
       This player's assigned goal for the game.

     === Private Attributes ===
     _proceed:
       True when the player should make a move, False when the player should
       wait.
    """

    id: int
    goal: Goal
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <player_id> and <goal>.
        """
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """No block should be selected manually by the random player.
        Return None always.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event."""

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        copy = board.create_copy()  # make a hard copy
        if not self._proceed:
            return None  # Do not remove
        else:
            move = _generate_move_and_block(copy, board, self.goal)
            self._proceed = False
            return move


class SmartPlayer(Player):
    """A smart player.

     A smart player chooses the option that yields the best score among a
     set of random moves. The size of the set depends on the difficulty to
     play against this smart player.

    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    _difficulty:
      An integer indicating how difficult it is to play against it.
    """
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initialize this SmartPlayer with the given <player_id>, <goal>
        and <difficulty>.
        The <difficulty> is the number of valid moves.

        Precondition: difficulty > 0
        """
        Player.__init__(self, player_id, goal)
        self._proceed = False
        self._difficulty = difficulty

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """No block should be selected manually by the random player.
        Return None always.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        copy = board.create_copy()
        if not self._proceed:
            return None  # Do not remove
        else:
            ori_score = self.goal.score(board)
            cur_score = self.goal.score(copy)
            score_dict = {}
            i = 0
            while i < self._difficulty:
                copy = board.create_copy()
                move = _generate_move_and_block(copy, board, self.goal)
                score = self.goal.score(copy)
                score_dict[score] = move
                if score >= cur_score:
                    cur_score = score
                i += 1
            if cur_score <= ori_score:
                self._proceed = False
                return _create_move(PASS, board)
            else:
                self._proceed = False
                return score_dict[cur_score]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
