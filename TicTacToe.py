#!/usr/bin/env python

"""Implements a TicTacToe game simulator."""


import Generic
from Minimax import minimax
import numpy as np



class Game (Generic.Game):
    """
    The TicTacToe game.
    """


    def __init__(self):
        Generic.Game.__init__(self)
        self._board = np.zeros(9).reshape(3, 3)


    def __str__(self):
        return "<TicTacToe game>"


    def play(self, move):
        """
        Play a move.
        If the game is finished, return the end result in {'white', 'black', 'draw'}.
        None is return if the game is still open.
        """
        if self.status != -1:
            raise RuntimeError("This game is finished.")
        # Ensure that this is an acceptable move
        if type(move) is tuple:
            move = Move(move)
        if move.color is None:
            move.color = self.currentColor
        elif move.color != self.currentColor:
            raise RuntimeError("Color {} cannot play this turn.".format(move.color))
        if self._board.item(move.position) != 0:
            raise RuntimeError("This position is already occupied.")
        # Play the move
        self._board.itemset(move.position, move.color)
        self.history.append(move)
        self.currentColor = self.currentColor % 2 + 1
        # Status has to be recomputed
        return self._compute_status()


    def revert(self):
        """Revert the last move played."""
        if len(self.history) == 0:
            raise RuntimeError("No more move to revert!")
        move = self.history.pop()
        self._board.itemset(move.position, 0)
        self.currentColor = self.currentColor % 2 + 1
        self.status = -1


    def possible_moves(self):
        """Return all the possible moves for this turn."""
        if self.status != -1:
            return []
        moves = []
        xx, yy = self._board.shape
        for x in xrange(xx):
            for y in xrange(yy):
                if self._board.item(x, y) == 0:
                    moves.append(Move((x,y), self.currentColor))
        return moves


    def to_string(self):
        """Return a string with a 'graphical' display of the board."""
        xx, yy = self._board.shape
        out = "  012-> X\n"
        out += " /" + "-"*xx + "\\\n"
        for i,y in enumerate(xrange(yy)):
            out += "{}|".format(i)
            for x in xrange(xx):
                v = self._board[x,y]
                if v == 0:
                    out += " "
                else:
                    out += str(int(v))
            out += "|\n"
        out += "|\\" + "-"*xx + "/\n"
        out += "V\nY\n"
        if self.status != -1:
            out += "Status: " + str(self.status) + "\n"
        return out


    def _compute_status(self):
        """Return the winner of the game."""
        # Look for a winner: three tokens with same color aligned
        b = self._board
        for color in [1, 2]:
            if (b.item(0,0) == color and b.item(1,0) == color and b.item(2,0) == color) or \
               (b.item(0,0) == color and b.item(0,1) == color and b.item(0,2) == color) or \
               (b.item(0,0) == color and b.item(1,1) == color and b.item(2,2) == color) or \
               (b.item(0,1) == color and b.item(1,1) == color and b.item(2,1) == color) or \
               (b.item(1,0) == color and b.item(1,1) == color and b.item(1,2) == color) or \
               (b.item(2,0) == color and b.item(1,1) == color and b.item(0,2) == color) or \
               (b.item(0,2) == color and b.item(1,2) == color and b.item(2,2) == color) or \
               (b.item(2,0) == color and b.item(2,1) == color and b.item(2,2) == color):
                self.status = color
                return self.status
        # Check if the game is complete
        if len(self.history) == 9:
            self.status = 0
            return self.status
        # Well, then the game is still open...
        self.status = -1
        return self.status



class Move (Generic.Move):
    """
    A move of the TicTacToe game.
    """

    def __init__(self, position, color=None):
        """Create a move."""
        Generic.Move.__init__(self, color)
        self.position = position

    def __str__(self):
        return "<{}:{}>".format(self.color, str(self.position))



class Player (Generic.Minimax_Player):
    """
    A TicTacToe player based on minimax.
    """

    def __init__(self, color=None):
        Generic.Player.__init__(self, color)


    def eval(self, game):
        """
        Evaluate the current state of the game from the point of view of the player.
        It only evaluates _final_ states cause TicTacToe is simple enough that we can go
        through the whole tree.
        """
        strokes = len(game.history)
        status = game.status
        if status == -1:
            raise RuntimeError("This evaluation is only for terminal states")
        # If player win
        elif status == self.color:
            return 20 - strokes  # Let's try to win fast  (11 <= v <= 20)
        # If game is on par
        elif status == -1:
            return strokes       # or to be on par slowly (0 <= v <= 9)
        # If player lose
        else:
            return -10 + strokes # or to lose slowly      (-10 <= v <= -1)


    def cutoff(self, game, depth):
        """
        Decide when to stop descent in tree.
        """
        False
