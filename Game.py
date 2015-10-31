#!/usr/bin/env python

"""
Some generic classes for Game, Move and Player.
"""

import random

class Game (object):
    """
    An abstract class for a game.
    """

    def play(self, move):
        """Play a move and return the value of self.winner()."""
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

    def current_player(self):
        """Return the color (e.g. "white") of the current player."""
        pass

    def winner(self):
        """
        Return one of the following value:
         - The color of the winner (e.g. "white")
         - "draw"
         - None if the game is still open.
        """
        pass

    def pd(self, move):
        r = self.play(move)
        self.display()
        return r


class Move (object):
    """
    An abstract class for a Move.
    """

    def player(self):
        """Return the player (e.g. "white") of the move."""
        pass



class Player (object):
    """
    An abstract player.
    """

    def play(self, game):
        """Play the next move and return the result."""
        pass



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
