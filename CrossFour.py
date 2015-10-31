#!/usr/bin/env python

"""Implements a Cross Four game simulator."""


from Game import Game, Move, Player
from Minimax import minimax
import numpy as np



class CrossFour_Game (Game):
    """
    The Cross Four game.
    """

    def __init__(self):
        self.X = 4
        self.Y = 4
        self.board = np.zeros(self.X*self.Y).reshape(self.X, self.Y)
        self.rows = [0]*self.X
        self.history = []
        self.nextColor = 1
        self.status = "open" # value in {open, white, black, draw}

    def __str__(self):
        return "<CrossFour game>"

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
        if self.rows[move.column] >= self.Y:
            raise RuntimeError("This column is full.")
        # Play the move
        self.board.itemset((move.column, self.rows[move.column]), move.color)
        self.rows[move.column] += 1
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
        self.rows[move.column] -= 1
        self.board.itemset((move.column, self.rows[move.column]), 0)
        self.nextColor *= -1
        self.status = "open"

    def possible_moves(self):
        """Return all the possible moves for this turn."""
        if self.status != "open":
            return []
        return [CrossFour_Move(x, self.nextColor)
                for x in range(self.X)
                if self.rows[x] < self.Y]

    def to_string(self):
        """Return a string with a 'graphical' display of the board."""
        out = " " + "".join([str(i) for i in range(self.X)]) + "\n"
        for y in range(self.Y-1, -1, -1):
            out += "|"
            for x in xrange(self.X):
                if self.board[x,y] == 0:
                    out += " "
                elif self.board[x,y] == 1:
                    out += "O"
                else:
                    out += "#"
            out += "|\n"
        out += "-"*self.X + "--\n"
        out += " " + "".join([str(i) for i in range(self.X)]) + "\n"
        if self.status != "open":
            out += self.status + "\n"
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
        for y in range(self.Y - 2):
            for x in xrange(self.X - 2):
                if (b.item(x,y) == 1 and b.item(x+1,y) == 1 and b.item(x+2,y) == 1) or \
                   (b.item(x,y) == 1 and b.item(x,y+1) == 1 and b.item(x,y+2) == 1) or \
                   (b.item(x,y) == 1 and b.item(x+1,y+1) == 1 and b.item(x+2,y+2) == 1) or \
                   (b.item(x+2,y) == 1 and b.item(x+1,y+1) == 1 and b.item(x,y+2) == 1):
                    return "white"
                if (b.item(x,y) == -1 and b.item(x+1,y) == -1 and b.item(x+2,y) == -1) or \
                   (b.item(x,y) == -1 and b.item(x,y+1) == -1 and b.item(x,y+2) == -1) or \
                   (b.item(x,y) == -1 and b.item(x+1,y+1) == -1 and b.item(x+2,y+2) == -1) or \
                   (b.item(x+2,y) == -1 and b.item(x+1,y+1) == -1 and b.item(x,y+2) == -1):
                    return "black"
        for y in range(self.Y - 2):
            if (b.item(self.X-1,y) == 1 and b.item(self.X-1,y+1) == 1 and b.item(self.X-1,y+2) == 1) or \
               (b.item(self.X-2,y) == 1 and b.item(self.X-2,y+1) == 1 and b.item(self.X-2,y+2) == 1):
                return "white"
            if (b.item(self.X-1,y) == -1 and b.item(self.X-1,y+1) == -1 and b.item(self.X-1,y+2) == -1) or \
               (b.item(self.X-2,y) == -1 and b.item(self.X-2,y+1) == -1 and b.item(self.X-2,y+2) == -1):
                return "black"
        for x in range(self.X - 2):
            if (b.item(x,self.Y-1) == 1 and b.item(x+1,self.Y-1) == 1 and b.item(x+2,self.Y-1) == 1) or \
               (b.item(x,self.X-2) == 1 and b.item(x+1,self.X-2) == 1 and b.item(x+2,self.X-2) == 1):
                return "white"
            if (b.item(x,self.Y-1) == -1 and b.item(x+1,self.Y-1) == -1 and b.item(x+2,self.Y-1) == -1) or \
               (b.item(x,self.X-2) == -1 and b.item(x+1,self.X-2) == -1 and b.item(x+2,self.X-2) == -1):
                return "black"
        # Check if the game is complete
        if all([i==self.Y for i in self.rows]):
            return "draw"
        return None


class CrossFour_Move (Move):
    """
    A move of the CrossFour game.
    """

    def __init__(self, column, color=None):
        """Create a move. Color should be "black", "white" or None. Column is an int."""
        if color in ["O", "o", "0", "white", "White", "WHITE", 1]:
            self.color = 1
        elif color in ["#", "black", "Black", "BLACK", -1]:
            self.color = -1
        elif color is None:
            self.color = None
        else:
            raise RuntimeError("Invalid color!")
        self.column = column

    def __str__(self):
        if self.color == 1:
            color = "O"
        elif self.color == -1:
            color = "#"
        else:
            color = "?"
        return "<{}:{}>".format(color, str(self.column))

    def __repr__(self):
        return self.__str__()

    def player(self):
        if self.color == 1:
            return "white"
        else:
            return "black"



class CrossFour_Player (Player):
    """
    A CrossFour player based on minimax.
    """

    def play(self, game):
        self.color = game.current_player()
        value, move, strokes = minimax(game, self, debug=False)
        return game.play(move)

    def eval(self, game):
        """
        Evaluate the current state of the game from the point of view of 'player'.
        It only evaluates _final_ states cause CrossFour is simple enough that we can go
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
