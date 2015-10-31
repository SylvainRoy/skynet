#!/usr/bin/env python

from Game import Interactive_Player, Random_Player
import TicTacToe
import CrossFour


def run_game(game, player1, player2):
    while True:
        for player in [player1, player2]:
            winner = player.play(game)
            if winner is not None or game.status != "open":
                game.display()
                return


if __name__ == '__main__':
    # TicTacToe
    run_game(TicTacToe.Game(), TicTacToe.Player(), Interactive_Player())
    #run_game(TicTacToe.Game(), Random_Player(), TicTacToe.Player())

    # CrossFour
    #run_game(CrossFour.Game(), CrossFour.Player(), Interactive_Player())
    #run_game(CrossFour.Game(), Random_Player(), CrossFour.Player())
    #run_game(CrossFour.Game(), Random_Player(), Interactive_Player())
