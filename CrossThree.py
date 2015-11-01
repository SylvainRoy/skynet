#!/usr/bin/env python

"""
Implements a Cross Four game simulator.
"""



import Generic
from Minimax import minimax
import numpy as np
import random
import sys


class Game (Generic.Game):
    """
    The Cross Four game.
    """

    def __init__(self, columns=4, rows=4):
        Generic.Game.__init__(self)
        self.X = columns
        self.Y = rows
        self._board = np.zeros(self.X*self.Y).reshape(self.X, self.Y)
        self._rows = [0]*self.X
        self._status = -1


    def __str__(self):
        return "<CrossFour game>"


    def play(self, move):
        """
        Play a move.
        If the game is finished, return the end result in {'white', 'black', 'draw'}.
        None is return if the game is still open.
        """
        if self._status != -1:
            raise RuntimeError("This game is finished.")
        # Ensure that this is an acceptable move
        if move.color is None:
            move.color = self.currentColor
        elif move.color != self.currentColor:
            raise RuntimeError("Color {} cannot play this turn.".format(move.color))
        if self._rows[move.column] >= self.Y:
            raise RuntimeError("This column is full.")
        # Play the move
        self._board.itemset((move.column, self._rows[move.column]), move.color)
        self._rows[move.column] += 1
        self.history.append(move)
        self.currentColor = self.currentColor % 2 + 1
        # Status will have to be recomputed
        self._status = None


    def revert(self):
        """Revert the last move played."""
        if len(self.history) == 0:
            raise RuntimeError("No more move to revert!")
        move = self.history.pop()
        self._rows[move.column] -= 1
        self._board.itemset((move.column, self._rows[move.column]), 0)
        self.currentColor = self.currentColor % 2 + 1
        self._status = -1

    def possible_moves(self):
        """Return all the possible moves for this turn."""
        if self.status() != -1:
            return []
        return [Move(x, self.currentColor)
                for x in range(self.X)
                if self._rows[x] < self.Y]

    def to_string(self):
        """Return a string with a 'graphical' display of the board."""
        out = " " + "".join([str(i) for i in range(self.X)]) + "\n"
        for y in xrange(self.Y-1, -1, -1):
            out += "|"
            for x in xrange(self.X):
                v = self._board[x,y]
                if v == 0:
                    out += " "
                else:
                    out += str(int(v))
            out += "|\n"
        out += "-"*self.X + "--\n"
        out += " " + "".join([str(i) for i in range(self.X)]) + "\n"
        if self.status() != -1:
            out += "Status: " + str(self.status()) + "\n"
        return out


    def status(self):
        """Return the winner of the game."""
        # No need to recompute if no change
        if self._status is not None:
            return self._status
        # Look for a winner: three tokens with same color aligned
        b = self._board
        for color in [1, 2]:
            for y in range(self.Y - 2):
                for x in xrange(self.X - 2):
                    if (b.item(x,y) == color and b.item(x+1,y) == color and b.item(x+2,y) == color) or \
                       (b.item(x,y) == color and b.item(x,y+1) == color and b.item(x,y+2) == color) or \
                       (b.item(x,y) == color and b.item(x+1,y+1) == color and b.item(x+2,y+2) == color) or \
                       (b.item(x+2,y) == color and b.item(x+1,y+1) == color and b.item(x,y+2) == color):
                        self._status = color
                        return color
            for y in range(self.Y - 2):
                if (b.item(self.X-1,y) == color and b.item(self.X-1,y+1) == color and b.item(self.X-1,y+2) == color) or \
                   (b.item(self.X-2,y) == color and b.item(self.X-2,y+1) == color and b.item(self.X-2,y+2) == color):
                    self._status = color
                    return color
            for x in range(self.X - 2):
                if (b.item(x,self.Y-1) == color and b.item(x+1,self.Y-1) == color and b.item(x+2,self.Y-1) == color) or \
                   (b.item(x,self.X-2) == color and b.item(x+1,self.X-2) == color and b.item(x+2,self.X-2) == color):
                    self._status = color
                    return color
        # Check if the game is complete
        if len(self.history) == self.X * self.Y:
            self._status = 0
            return self._status
        # Well, then the game is still open...
        self._status = -1
        return self._status



class Move (Generic.Move):
    """
    A move of the CrossFour game.
    """

    def __init__(self, column, color=None):
        """Create a move."""
        Generic.Move.__init__(self, color)
        self.column = column

    def __str__(self):
        return "<{}:{}>".format(self.colorAsChar(), str(self.column))



class Player (Generic.Minimax_Player):
    """
    A CrossFour player based on minimax.
    This player explore the whole tree. So, it is "slow".
    """

    def __init__(self, color=None):
        Generic.Player.__init__(self, color)


    def eval(self, game):
        """
        Evaluate the current state of the game from the point of view of 'player'.
        It only evaluates _final_ states cause 'small' CrossFour are simple enough that we can go
        through the whole tree.
        """
        strokes = len(game.history)
        status = game.status()
        if status == -1:
            raise RuntimeError("This evaluation is only for terminal states")
        elif status == self.color:
            return 20 - strokes  # Let's try to win fast  (11 <= v <= 20)
        elif status == 0:
            return strokes       # or to be on par slowly (0 <= v <= 9)
        else:
            return -10 + strokes # or to lose slowly      (-10 <= v <= -1)

    def cutoff(self, game, depth):
        """
        Decide when to stop descent in tree.
        """
        False


class AdvancedPlayer (Player):
    """
    A CrossFour player that cope with big boards.
    It does not explore the whole tree and relies on evaluation of non-final states.
    """

    def __init__(self, genome=None, color=None):
        Player.__init__(self, color)
        self.len_genome = 6
        if genome is None:
            self.genome = [random.randint(0, 99) for i in range(self.len_genome)]
        elif len(genome) != self.len_genome:
            raise RuntimeError("Wrong genome lenght")
            self.genome = genome

    def __str__(self):
        return "<ACrossFour Player: " + repr(self.genome) + ">"

    def clone(self):
        return AdvancedPlayer(list(self.genome))

    def mutate(self, probability=0.01):
        for i in range(self.len_genome):
            if random.random() <= probability:
                self.genome[i] = random.randint(0, 99)

    def crossbreed(self, daddy):
        cut = random.randint(0, self.len_genome-1)
        genome_a = self.genome[:cut] + daddy.genome[cut:]
        genome_b = daddy.genome[:cut] + self.genome[cut:]
        return [AdvancedPlayer(genome_a), AdvancedPlayer(genome_b)]

    def eval(self, game):
        """
        Evaluate the current state of the game.
        """
        strokes = len(game.history)
        status = game.status()
        board = game._board

        # Player win
        if status == self.color:
            #print "e:w({})".format(sys.maxint - strokes)
            return sys.maxint - strokes

        # Opponent win
        if status == self.color % 2 + 1:
            #print "e:l({})".format(-sys.maxint + strokes)
            return -sys.maxint + strokes

        # Draw
        elif status == 0:
            #print "e:d({})".format(self.genome[0] * strokes + self.genome[1])
            return self.genome[0] * strokes + self.genome[1]

        # Non final state
        elif status == -1:
            twoWithSpaceForThreeForPlayer = 0
            twoWithSpaceForThreeForOpponent = 0
            for column in range(game.X):
                row = game._rows[column]
                if row >= game.Y:
                    continue
                if board.item(column, row) == self.color:
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            if (x, y) == (0, 0) or \
                               column-x < 0 or game.X <= column+x or \
                               row-y < 0 or game.Y <= row+y:
                                continue
                            if (boad.item(column+y, row+x) == self.color) and \
                               (boad.item(column-y, row-x) == 0):
                                twoWithSpaceForThreeForPlayer += 1
                elif board.item(column, row) == self.color % 2 + 1:
                    for x in [-1, 0, 1]:
                        for y in [-1, 0, 1]:
                            if (x, y) == (0, 0) or \
                               column-x < 0 or game.X <= column+x or \
                               row-y < 0 or game.Y <= row+y:
                                continue
                            if (boad.item(column+y, row+x) == self.color % 2 + 1) and \
                               (boad.item(column-y, row-x) == 0):
                                twoWithSpaceForThreeForOpponent += 1
            out = self.genome[2] * twoWithSpaceForThreeForPlayer + \
                  self.genome[3] * twoWithSpaceForThreeForOpponent + \
                  self.genome[4] * strokes + \
                  self.genome[5]
            #print "e:n({})".format(out)
            return out



    def cutoff(self, game, depth):
        """
        Decide when to stop descent in tree.
        """
        return depth >= 3
