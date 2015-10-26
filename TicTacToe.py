#!/usr/bin/env python

import numpy as np


class Game (object):
    """The TicTacToe game."""

    def __init__(self):
        self.board = np.zeros(9).reshape(3, 3)
        self.history = []
        self.nextColor = 1

    def pd(self, *args):
        """Shortcut method to play and display in one shot."""
        self.play(*args)
        self.display()

    def play(self, *args):
        """Play a move."""
        # Try (strongly) to understand the args.
        move = None
        if len(args) == 1:
            if type(args[0]) == tuple:             # play((x,y))
                move = Move(move, self.nextColor)
            elif type(args[0]) == Move:            # play(Move(x,y,color))
                move = args[0]
        elif len(args) == 2:
            if type(args[0]) == tuple:             # play((x,y), color)
                move = Move(args[0], args[1])
            else:                                  # play(x, y)
                move = Move((args[0], args[1]))
        elif len(args) == 3:                       # play(x, y, color)
            move = Move((args[0], args[1]), args[2])
        if move is None:
            RuntimeError("Wrong argument")
        # Check that this is an acceptable move
        if move.color is None:
            move.color = self.nextColor
        elif move.color != self.nextColor:
            raise RuntimeError("Color {} cannot play this turn.".format(move.color))
        if abs(move.color) != 1:
            raise RuntimeError("Invalid color!")
        if self.board.item(move.position) != 0:
            raise RuntimeError("This position is already occupied.")
        # Play the move
        self.board.itemset(move.position, move.color)
        self.history.append(move)
        self.nextColor *= -1

    def revert(self):
        """Revert the last move."""
        if len(self.history) == 0:
            raise RuntimeError("No more move to revert!")
        move = self.history.pop()
        self.board.itemset(move.position, 0)

    def moves(self):
        """Return all the possible moves for this turn."""
        moves = []
        xx, yy = self.board.shape
        for x in xrange(xx):
            for y in xrange(yy):
                if self.board.item(x, y) == 0:
                    moves.append(Move((x,y), self.nextColor))
        return moves

    def toString(self):
        """Return a string with a textual display of the board."""
        xx, yy = self.board.shape
        out = "  012--> X\n"
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
        out += "|\nV\nY\n"
        return out

    def display(self):
        print self.toString(),

    def __str__(self):
        return "<TicTacToe game: {} moves>".format(len(self.history))

    def winner(self):
        """Return the winner of the game."""
        b = self.board
        if (b.item(0,0) == 1 and b.item(1,0) == 1 and b.item(2,0) == 1) or \
           (b.item(0,0) == 1 and b.item(0,1) == 1 and b.item(0,2) == 1) or \
           (b.item(0,0) == 1 and b.item(1,1) == 1 and b.item(2,2) == 1) or \
           (b.item(0,1) == 1 and b.item(1,1) == 1 and b.item(2,1) == 1) or \
           (b.item(1,0) == 1 and b.item(1,1) == 1 and b.item(1,2) == 1) or \
           (b.item(2,0) == 1 and b.item(1,1) == 1 and b.item(0,2) == 1) or \
           (b.item(0,2) == 1 and b.item(1,2) == 1 and b.item(2,2) == 1) or \
           (b.item(2,0) == 1 and b.item(2,1) == 1 and b.item(2,2) == 1):
            return "white"
        if (b.item(0,0) == -1 and b.item(1,0) == -1 and b.item(2,0) == -1) or \
           (b.item(0,0) == -1 and b.item(0,1) == -1 and b.item(0,2) == -1) or \
           (b.item(0,0) == -1 and b.item(1,1) == -1 and b.item(2,2) == -1) or \
           (b.item(0,1) == -1 and b.item(1,1) == -1 and b.item(2,1) == -1) or \
           (b.item(1,0) == -1 and b.item(1,1) == -1 and b.item(1,2) == -1) or \
           (b.item(2,0) == -1 and b.item(1,1) == -1 and b.item(0,2) == -1) or \
           (b.item(0,2) == -1 and b.item(1,2) == -1 and b.item(2,2) == -1) or \
           (b.item(2,0) == -1 and b.item(2,1) == -1 and b.item(2,2) == -1):
            return "black"
        return None


class Move (object):
    """A move of the TicTacToe game."""

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
        return "<Put {} at {}>".format(color, str(self.position))

    def __repr__(self):
        return self.__str__()
