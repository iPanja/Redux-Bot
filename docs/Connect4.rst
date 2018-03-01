.. Redux documentation master file, created by
   sphinx-quickstart on Wed Feb 28 22:40:25 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _command-game-Connect4:

Connect 4
=================================

.. toctree::
   :maxdepth: 2


Commands
---------

    **$c4 new <@Player> <@Player>**
        Arguments: (Mention) Player 1, Player 2
        Creates a new Blackjack game between you and an AI dealer who follows traditional dealer rules.

    **$c4 place <Column>**
        Arguments: (int) Column
        Places your chip in the specified column. This command will only work if it is your turn.

    **$c4 remake**
        Resets the game to allow you to make a new game using *$c4 new <@Player> <@Player>*
