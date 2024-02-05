"""
Acceptance tests for nim.py

Make sure that this file is in the same directory as nim.py!

'Why do we fall sir? So that we can learn to pick ourselves up.'
                                        - Batman Begins (2005)
"""

import pytest

from nim import Nim, train


# Let the AI play against itself for 10 times. If the q function
# is implemented correctly, the AI which moved second should always win.

# My Note:
# Re-generate AI for 10 times to test some hidden bugs.


@pytest.mark.parametrize("execution", range(10))
def test(execution):
    ai = train(10000)
    for _ in range(10):
        assert play_ai_vs_ai(ai) == 1


# helper function


def play_ai_vs_ai(ai):
    game = Nim()
    while True:
        game.move(ai.choose_action(game.piles, epsilon=False))

        if game.winner is not None:
            return game.winner
