#!/usr/bin/env python

import re, os, sys
import difflib
import unittest

import Generic
import TicTacToe
import CrossThree
import CrossFour
import Minimax



class CrossFourTest(unittest.TestCase):

    def setUp(self):
        pass

    def testState(self):

        # First "real life" example
        g = CrossFour.Game()
        g.play(1); g.play(0)
        self.assertEqual(g.status, -1)
        g.play(1); g.play(1)
        self.assertEqual(g.status, -1)
        g.play(0); g.play(2)
        self.assertEqual(g.status, -1)
        g.play(1); g.play(3)
        self.assertEqual(g.status, -1)
        g.play(4); g.play(3)
        self.assertEqual(g.status, -1)
        g.play(3); g.play(2)
        self.assertEqual(g.status, -1)
        g.play(3); g.play(2)
        self.assertEqual(g.status, -1)
        g.play(3); g.play(2)
        self.assertEqual(g.status, 2)
        g.revert()
        self.assertEqual(g.status, -1)

        # Some more "to the point" tests
        g = CrossFour.Game(6, 6)
        g._board[5, 2:6] = 1
        self.assertEqual(g._compute_status(), 1)
        self.assertEqual(g.status, 1)

        g = CrossFour.Game(6, 6)
        g._board[5, 0:4] = 1
        self.assertEqual(g._compute_status(), 1)
        self.assertEqual(g.status, 1)

        g = CrossFour.Game(6, 6)
        g._board[4, 0:4] = 1
        self.assertEqual(g._compute_status(), 1)
        self.assertEqual(g.status, 1)

        g = CrossFour.Game(6, 6)
        g._board[0:5, 5] = 1
        self.assertEqual(g._compute_status(), 1)
        self.assertEqual(g.status, 1)

        g = CrossFour.Game(6, 6)
        g._board[2, 2] = 2
        g._board[3, 3] = 2
        g._board[4, 4] = 2
        self.assertEqual(g._compute_status(), -1)
        self.assertEqual(g.status, -1)
        g._board[5, 5] = 2
        self.assertEqual(g._compute_status(), 2)
        self.assertEqual(g.status, 2)

        g = CrossFour.Game(6, 6)
        g._board[2, 5] = 2
        g._board[3, 4] = 2
        g._board[4, 3] = 2
        self.assertEqual(g._compute_status(), -1)
        self.assertEqual(g.status, -1)
        g._board[5, 2] = 2
        self.assertEqual(g._compute_status(), 2)
        self.assertEqual(g.status, 2)



class TicTacToeTest(unittest.TestCase):

    def setUp(self):
        pass

    def testState(self):

        # First "real life" example
        g = TicTacToe.Game()
        g.play((0,0)); g.play((0,1))
        self.assertEqual(g.status, -1)
        g.play((1,1)); g.play((1,0))
        self.assertEqual(g.status, -1)
        g.play((2,2));
        self.assertEqual(g.status, 1)
        with self.assertRaises(RuntimeError) as cm:
            g.play((2,1))

        # Some more "to the point" tests
        g = TicTacToe.Game()
        g._board[0, 0:3] = 1
        self.assertEqual(g._compute_status(), 1)
        self.assertEqual(g.status, 1)

        g = TicTacToe.Game()
        g._board[0:3, 2] = 1
        self.assertEqual(g._compute_status(), 1)
        self.assertEqual(g.status, 1)

        g = TicTacToe.Game()
        g._board[2, 0] = 2
        self.assertEqual(g._compute_status(), -1)
        self.assertEqual(g.status, -1)
        g._board[1, 1] = 2
        self.assertEqual(g._compute_status(), -1)
        self.assertEqual(g.status, -1)
        g._board[0, 2] = 2
        self.assertEqual(g._compute_status(), 2)
        self.assertEqual(g.status, 2)




if __name__ == '__main__':
    unittest.main()
