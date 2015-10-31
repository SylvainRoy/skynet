#!/usr/bin/env python

from Game import Interactive_Player, Random_Player
from TicTacToe import TicTacToe_Game, TicTacToe_Move, TicTacToe_Player
from CrossFour import CrossFour_Game, CrossFour_Move, CrossFour_Player


def run_game(game, player1, player2):
    while True:
        for player in [player1, player2]:
            winner = player.play(game)
            if winner is not None or game.status != "open":
                game.display()
                return


if __name__ == '__main__':
    # TicTacToe
    #run_game(TicTacToe_Game(), TicTacToe_Player(), Interactive_Player())
    #run_game(TicTacToe_Game(), Random_Player(), TicTacToe_Player())

    # CrossFour
    run_game(CrossFour_Game(), CrossFour_Player(), Interactive_Player())
    #run_game(CrossFour_Game(), Random_Player(), CrossFour_Player())
    #run_game(CrossFour_Game(), Random_Player(), Interactive_Player())
