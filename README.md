# Redux-Bot
A discord bot for a TSA competition, written in Python.

# Overview
Redux is a Discord bot created for the 2018 TSA Software Development competition. If you have any issues or requests, please open up an issue.

# Commands
* updateBot <game> : Sets the game that the bot is currently playing
* Blackjack
  * create : sets up the game
  * hit (1) : Hit, add an additional card to your hand
  * stay (2) : Stay, end your turn
* Games of Chance
  * flipcoin
  * randcard
  * randint min max
  * Raffle
    * rcreate (max players) - Create a raffle (set the max amount of participants)
    * renter - Enter the current raffle
    * rend - End the raffle
    * rolldie (sides)
    * rolldice (sides)
* Dictionary
  * define <word> - Gets the definition of a word from the Oxford Dictionary
  * urban <word> - Gets the urban dictionary definition of the word
* Fornite
  * flookup <pc/xbox/ps4> < epic username> - Gets the user's solo total kills, K/D, and time spent
  * fstats <weapon name> - Gets the stats of the closest match of the weapon that you typed in
* Google
  * expand <url> - Expands a goo.gl shortened link to get where it would redirect you to
  * shorten <url> - Shortens a url into a goo.gl link
* Math
  * equation - Sets the current math equation to be calculated, 4x must be 4*x
  * variable <var> <value> - Sets the current value of the variable that is being used for the equation
  * solve - Solves the equation using the variables specified if applicable
* Moderation
  * clean <amount> - Deletes the x last messages in the channel the command was issued in
  * spam <message> <amount> - Spams the message x times in the channel the command was issued in
* Music
  * **UNDER CONSTRUCTION**
  * summon - Summons the bot to your voice channel
  * play <song url> - Plays the current song, if one is already playing it will be added to the queue
  * set - Plays the next song in the queue
  * skip - Skips the current song
  * volume <volume> - Sets the volume of the music player. Must be a value between 0 and 1.
  * disconnect - Disconnects the bot from your voice channel
  * clear - Clears the queue
* Vote
  * pcreate <poll name> - Creates a poll with the specified name
  * pcurrent - Gets information about the current poll
  * poption <option name> - Creates a new poll option with the name specified
  * pstart - Starts the poll
  * pstop - Stops the poll
  * pvote <option> Vote for the option in the poll
* Stock Market
  * stock <ticker> - Gets information about the stock's prices

# Planned Features
* Voice/Music autoplay
* **IMPLEMENTING** Updated interface using embeds
* More card games w/ better interfaces
* Find more things to add :)
* Write a script to pull the newest release of this bot and restart the bot (for a Raspberry Pi)
