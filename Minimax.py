#!/usr/bin/env python

"""
The minimax algo with alpha-beta prunning.
"""

import sys


def minimax(game, player, alpha=-sys.maxint, beta=sys.maxint, turn='max', depth=0, path=[], strokes=0, debug=False):
    """
    Minimax algorithm with alpha-beta pruning.
    """

    strokes += 1

    if strokes % 1000 == 0:
        print strokes

    if debug:
        print "+{}MINIMAX: {}/{} (strokes:{})".format(".."*depth, player.color, turn, strokes)
        print "+{}{}".format(".."*depth, game.to_string().replace("\n", "\n+"+".."*depth))

    # Get possible moves for current player
    moves = game.possible_moves()

    # If this is a terminal state or if the player decide to cut off
    if len(moves) == 0 or player.cutoff(game, depth):
        e = player.eval(game)
        if debug:
            print "+{}=>val:{} for {}".format(".."*depth, e, ",".join([str(m) for m in path]))
        return e, None, strokes

    # Max turn: Player tries to maximize the score when playing
    if turn == 'max':
        maxi = -sys.maxint
        movemaxi = None
        for move in moves:
            game.play(move)
            value, nextbestmove, strokes = minimax(game, player, alpha, beta,
                                                   turn='min', depth=depth+1,
                                                   path=path+[move], strokes=strokes,
                                                   debug=debug)
            game.revert()
            if maxi < value:
                maxi, movemaxi = value, move
            if beta <= value:
                break
            alpha = max(alpha, value)
        if debug:
            print "+{}=> max:{} for {}".format(".."*depth, maxi, movemaxi)
        return maxi, movemaxi, strokes

    # Min turn: Opponent tries to minize the score when playing
    if turn == 'min':
        mini = sys.maxint
        movemini = None
        for move in moves:
            game.play(move)
            value, nextbestmove, strokes = minimax(game, player, alpha, beta,
                                                   turn='max', depth=depth+1,
                                                   path=path+[move], strokes=strokes,
                                                   debug=debug)
            game.revert()
            if value < mini:
                mini, movemini = value, move
            if value <= alpha:
                break
            beta = min(beta, value)
        if debug:
            print "+{}=> min:{} for {}".format(".."*depth, mini, movemini)
        return mini, movemini, strokes
