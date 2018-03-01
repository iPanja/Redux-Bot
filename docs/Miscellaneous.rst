.. Redux documentation master file, created by
   sphinx-quickstart on Wed Feb 28 22:40:25 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _section-miscellaneous:

Miscellaneous
=================================

.. toctree::
   :maxdepth: 2

.. _section-miscellaneous-appearance:

Appearance
------------

   **$updateBot <status>**
      Arguments: (string) status - Any word(s)
      Sets the 'playing' status of the bot

.. _section-miscellaneous-chance:

Chance
-----------

   **$flipcoin**
      Randomly flips a coin.

   **$randcard**
      Gets a random card from a standard deck of 52 cards.

   **$randint (min, max)**
      Picks a random number between 1 and 10, or between <min> and <max> if specified.

   **$rolldie (sides)**
      Arguments: [Optional](int) the amount of sides the die should have.
      Randomly rolls a die between 1 and 6, or 1 and <sides> if specified.

   **$rolldice (sides)**
      Arguments: [Optional](int) the amount of sides the dice should have.
      Randomly rolls 2 dice between 1 and 6, or 1 and <sides> if specified.

   **$solve**
      Solves the equation using the variables specified if applicable

   **Raffle**

      **$rcreate (max players)**
         Arguments: [Optional](int) Max players that can join the raffle
         Creates a raffle that will select a random participant upon ending, default max players is unlimited.

      **$renter**
         Enters you in the current raffle

      **$rend**
         Ends the current raffle

.. _section-miscellaneous-math:

Math
-----------

   **$equation <equation>**
      Arguments: (equation) The equation
      Sets the current math equation to be calculated, 4x must be 4*x

   **$variable <var> <value>**
      Arguments: (string) variable. (int) value
      Sets the current value of the variable that is being used for the equation

   **$solve**
      Solves the equation using the variables specified if applicable

.. _section-miscellaneous-moderation:

Moderation
-------------

    **$clean <amount>**
        Arguments: (int) Amount of messages to be deleted
        Deletes the last *x* amount of messages in the channel the command was issued in

    **$spam <message> <amount>**
        Arguments: (words) message. (int) amount of messages to spam
        Spams the message *x* times in the channel the command was issued in

.. _section-miscellaneous-music:

Music
-------------

   **$summon**
       Summons the bot to your voice channel

   **$play <song url>**
      Arguments: (url) Song url
      Plays the specified song. If one is already playing it is added to the queue.

   **$set**
      Plays the next song in the queue

   **$skip**
      Skips the current song

   **$volume <volume>**
      Arguments: (float) volume level
      Sets the volume of the music player. Must be a value between 0 and 1.

   **$disconnect**
      Disconnects the bot from your voice channel

   **clear**
      Clears the queue

.. _section-miscellaneous-Vote:

Vote
-------------

   **$pcreate <poll name>**
      Arguments: (string) Poll name
      Creates a poll with the specified name

   **$pcurrent**
      Gets information about the current poll

   **$poption <option name>**
      Arguments: (string) Option name
      Adds another option with the specified name to the current poll

   **$pstart**
      **Status: Depreciated** - Does not need to be used
      Starts the poll

   **$pstop**
      Stop the current poll and display the results

   **$pvote <option>**
      Vote for the specified option in the current poll