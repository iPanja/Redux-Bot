.. Redux documentation master file, created by
   sphinx-quickstart on Wed Feb 28 22:40:25 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _section-games:

Games
=================================

.. toctree::
   :maxdepth: 2

.. _section-games-Blackjack:

Blackjack
---------

    **$hangman new**
        Arguments: (Mention) Player 1, Player 2
        Creates a new Blackjack game between you and an AI dealer who follows traditional dealer rules.

    **$hangman guess <letter>**
        Arguments: (1 letter/char) letter
        Guesses the specified letter.

    **$hangman remake**
        Resets the game to allow you to make a new game using *$hangman new*

.. _section-games-Connect4:

Connect 4
-----------

    **$c4 new <@Player> <@Player>**
        Arguments: (Mention) Player 1, Player 2
        Creates a new Connect 4 game between the specified players.

    **$c4 place <Column>**
        Arguments: (int) Column
        Places your chip in the specified column. This command will only work if it is your turn.

    **$c4 remake**
        Resets the game to allow you to make a new game using *$c4 new <@Player> <@Player>*

.. _section-games-Hangman:

Hangman
---------

    **$hangman new**
        Arguments: (Mention) Player 1, Player 2
        Creates a new Blackjack game between you and an AI dealer who follows traditional dealer rules.

    **$hangman guess <letter>**
        Arguments: (1 letter/char) letter
        Guesses the specified letter.

    **$hangman remake**
        Resets the game to allow you to make a new game using *$hangman new*

.. _section-games-TicTacToe:

Tic Tac Toe
-------------

    **$ttt new <@Player> <@Player>**
        Arguments: (Mention) Player 1, Player 2
        Creates a new Tic Tac Toe between the specified players.

    **$ttt place <position>**
        Arguments: (int) position
        Places your chip at the specified location on the board. Only works if it is your turn.

    **$ttt remake**
        Resets the game to allow you to make a new game using *$ttt new*
