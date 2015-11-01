#!/usr/bin/env python

from Generic import Interactive_Player, Random_Player
import TicTacToe
import CrossFour
from Genetic import tough_world


#
#
# Run some games
#
#

def interactive_run_game(game, player1, player2):
    player1.color = game.currentColor
    player2.color = game.currentColor % 2 + 1
    while True:
        for player in [player1, player2]:
            status = player.play(game)
            if status != -1:
                game.display()
                return


#
#
# Let's build the best CrossFour player ever!
#
#


def breed():
    "Generate the best CrossFour player ever!!"
    return tough_world(CrossFour.AdvancedPlayer, 10, eval_population)


def eval_population(population):
    """Evaluate all the menbers of a population by having them fight each others."""
    card = len(population)
    scores = [0]*card
    total_played = [0]*card
    for a in xrange(card):
        for b in xrange(a+1, card):
            print "Playing {} against {}".format(population[a], population[b])
            score = run_game(population[a], population[b])
            score -= run_game(population[b], population[a])
            scores[a] += score
            scores[b] -= score
            total_played[a] += 1
            total_played[b] += 1
            print " - score: ", score
    print "scores: ", scores
    print "total: ", total_played
    return scores


def run_game(player1, player2):
    game = CrossFour.Game(8, 8)
    player1.color = game.currentColor
    player2.color = game.currentColor % 2 + 1
    while True:
        for player in [player1, player2]:
            winner = player.play(game)
            if winner == player1.color:
                game.display()
                return 1
            elif winner == player2.color:
                game.display()
                return -1
            elif winner == 0:
                game.display()
                return 0


if __name__ == '__main__':
    # TicTacToe
    #interactive_run_game(TicTacToe.Game(), TicTacToe.Player(), Interactive_Player())
    interactive_run_game(TicTacToe.Game(), Random_Player(), TicTacToe.Player())

    # CrossFour
    #interactive_run_game(CrossFour.Game(), CrossFour.Player(), Interactive_Player())
    #interactive_run_game(CrossFour.Game(4, 4), Random_Player(), CrossFour.Player())
    #interactive_run_game(CrossFour.Game(), Random_Player(), Interactive_Player())

    # Breeding a CrossFour player
    #print breed()
