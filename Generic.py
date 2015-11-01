#!/usr/bin/env python

"""
Some generic classes for Game, Move and Player.
"""


import random
import Minimax


class Game (object):
    """
    An abstract class for a game.
    """

    def __init__(self):
        self.currentColor = 1 # The color whose turn it is
        self.history = []     # The history of strokes
        self.status = -1      # The status of the game as return by play

    def play(self, move):
        """
        Play a move and return the new status of the game:
         -1: open
          0: draw
          1: player 1 won
          2: player 2 won
        """
        pass

    def revert(self):
        """Revert the last move played, recursively."""
        pass

    def possible_moves(self):
        """Return the list of all the possible moves for this turn."""
        pass

    def to_string(self):
        """Return a string with a 'graphical' display of the board. """
        pass

    def display(self):
        """Print the board."""
        print self.to_string(),

    def pd(self, move):
        """
        Shorcut function to play and redisplay the board in one shot.
        """
        self.play(move)
        self.display()
        return self.status()



class Move (object):
    """
    An abstract class for a Move.
    """

    def __init__(self, color=None):
        """Create a move."""
        self.color = color

    def colorAsChar(self):
        if self.color is None:
            color = "?"
        else:
            color = str(self.color)



class Player (object):
    """
    An abstract player.
    """

    def __init__(self, color=None):
        self.color = color

    def play(self, game):
        # do something...
        return game.play()



class Interactive_Player (Player):
    """
    A generic player that interactively asks for the next move.
    """

    def play(self, game):
        game.display()
        moves = game.possible_moves()
        print "\n".join(["{}: {}".format(i, move) for i,move in enumerate(moves)])
        m = int(raw_input('Choice: '))
        return game.play(moves[m])


class Random_Player (Player):
    """
    A generic player that randomly choose the next move.
    """

    def play(self, game):
        return game.play(random.choice(game.possible_moves()))



class Minimax_Player (Player):
    """
    An abstract player.
    """

    def play(self, game):
        if self.color is None:
            raise RuntimeError("A player cannot play without an assigned color.")
        if self.color != game.currentColor:
            raise RuntimeError("This player ({}) can't"
                               "play this turn ({}).".format(self.color,
                                                             game.currentColor))
        value, move, strokes = Minimax.minimax(game, self, debug=False)
        return game.play(move)
