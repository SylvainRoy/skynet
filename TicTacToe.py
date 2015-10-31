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
        self.board = np.zeros(9).reshape(3, 3)
        self.history = []
        self.nextColor = 1
        self.status = "open" # value in {open, white, black, draw}

    def __str__(self):
        return "<TicTacToe game>"

    def play(self, move):
        """
        Play a move.
        If the game is finished, return the end result in {'white', 'black', 'draw'}.
        None is return if the game is still open.
        """
        if self.status != "open":
            raise RuntimeError("This game is finished.")
        # Ensure that this is an acceptable move
        if move.color is None:
            move.color = self.nextColor
        elif move.color != self.nextColor:
            raise RuntimeError("Color {} cannot play this turn.".format(move.color))
        if self.board.item(move.position) != 0:
            raise RuntimeError("This position is already occupied.")
        # Play the move
        self.board.itemset(move.position, move.color)
        self.history.append(move)
        self.nextColor *= -1
        # Check if there is a winner
        winner = self.winner()
        if winner is not None:
            self.status = winner
        return winner

    def revert(self):
        """Revert the last move played."""
        if len(self.history) == 0:
            raise RuntimeError("No more move to revert!")
        move = self.history.pop()
        self.board.itemset(move.position, 0)
        self.nextColor *= -1
        self.status = "open"

    def possible_moves(self):
        """Return all the possible moves for this turn."""
        if self.status != "open":
            return []
        moves = []
        xx, yy = self.board.shape
        for x in xrange(xx):
            for y in xrange(yy):
                if self.board.item(x, y) == 0:
                    moves.append(Move((x,y), self.nextColor))
        return moves

    def to_string(self):
        """Return a string with a 'graphical' display of the board."""
        xx, yy = self.board.shape
        out = "  012-> X\n"
        out += " /" + "-"*xx + "\\\n"
        for i,y in enumerate(xrange(yy)):
            out += "{}|".format(i)
            for x in xrange(xx):
                if self.board[x,y] == 0:
                    out += " "
                elif self.board[x,y] == 1:
                    out += "O"
                else:
                    out += "#"
            out += "|\n"
        out += "|\\" + "-"*xx + "/\n"
        out += "V\nY\n"
        if self.status != "open":
            out += self.status + "\n"
        return out

    def to_small_string(self):
        """Return a string with a 'graphical' display of the board."""
        xx, yy = self.board.shape
        out = "/" + "-"*xx + "\\\n"
        for y in xrange(yy):
            out += "|"
            for x in xrange(xx):
                if self.board[x,y] == 0:
                    out += " "
                elif self.board[x,y] == 1:
                    out += "O"
                else:
                    out += "#"
            out += "|\n"
        out += "\\" + "-"*xx + "/"
        return out

    def current_player(self):
        if self.nextColor == 1:
            return "white"
        else:
            return "black"
        return self.nextColor

    def winner(self):
        """Return the winner of the game."""
        b = self.board
        # Check if three white aligned
        if (b.item(0,0) == 1 and b.item(1,0) == 1 and b.item(2,0) == 1) or \
           (b.item(0,0) == 1 and b.item(0,1) == 1 and b.item(0,2) == 1) or \
           (b.item(0,0) == 1 and b.item(1,1) == 1 and b.item(2,2) == 1) or \
           (b.item(0,1) == 1 and b.item(1,1) == 1 and b.item(2,1) == 1) or \
           (b.item(1,0) == 1 and b.item(1,1) == 1 and b.item(1,2) == 1) or \
           (b.item(2,0) == 1 and b.item(1,1) == 1 and b.item(0,2) == 1) or \
           (b.item(0,2) == 1 and b.item(1,2) == 1 and b.item(2,2) == 1) or \
           (b.item(2,0) == 1 and b.item(2,1) == 1 and b.item(2,2) == 1):
            return "white"
        # Check if three black aligned
        if (b.item(0,0) == -1 and b.item(1,0) == -1 and b.item(2,0) == -1) or \
           (b.item(0,0) == -1 and b.item(0,1) == -1 and b.item(0,2) == -1) or \
           (b.item(0,0) == -1 and b.item(1,1) == -1 and b.item(2,2) == -1) or \
           (b.item(0,1) == -1 and b.item(1,1) == -1 and b.item(2,1) == -1) or \
           (b.item(1,0) == -1 and b.item(1,1) == -1 and b.item(1,2) == -1) or \
           (b.item(2,0) == -1 and b.item(1,1) == -1 and b.item(0,2) == -1) or \
           (b.item(0,2) == -1 and b.item(1,2) == -1 and b.item(2,2) == -1) or \
           (b.item(2,0) == -1 and b.item(2,1) == -1 and b.item(2,2) == -1):
            return "black"
        # Check if the game is complete
        if len(self.history) == 9:
            return "draw"
        return None


class Move (Generic.Move):
    """
    A move of the TicTacToe game.
    """

    def __init__(self, position, color=None):
        """Create a move. Color should be "black", "white" or None. Position is a 2-uplet."""
        if color in ["O", "o", "0", "white", "White", "WHITE", 1]:
            self.color = 1
        elif color in ["#", "black", "Black", "BLACK", -1]:
            self.color = -1
        elif color is None:
            self.color = None
        else:
            raise RuntimeError("Invalid color!")
        self.position = position

    def __str__(self):
        if self.color == 1:
            color = "O"
        elif self.color == -1:
            color = "#"
        else:
            color = "?"
        return "<{}:{}>".format(color, str(self.position))

    def __repr__(self):
        return self.__str__()

    def player(self):
        if self.color == 1:
            return "white"
        else:
            return "black"



class Player (Generic.Player):
    """
    A TicTacToe player based on minimax.
    """

    def play(self, game):
        self.color = game.current_player()
        value, move, strokes = minimax(game, self, debug=False)
        return game.play(move)

    def eval(self, game):
        """
        Evaluate the current state of the game from the point of view of 'player'.
        It only evaluates _final_ states cause TicTacToe is simple enough that we can go
        through the whole tree.
        """
        strokes = len(game.history)
        winner = game.winner()
        if winner is None:
            raise RuntimeError("This evaluation is only for terminal states")
        elif winner == self.color:
            return 20 - strokes  # Let's try to win fast  (11 <= v <= 20)
        elif winner is "draw":
            return strokes       # or to be on par slowly (0 <= v <= 9)
        else:
            return -10 + strokes # or to lose slowly      (-10 <= v <= -1)

    def cutoff(self, game, depth):
        """
        Decide when to stop descent in tree.
        """
        False
