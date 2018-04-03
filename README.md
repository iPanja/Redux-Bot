# Redux-Bot
A discord bot for a TSA competition, written in Python.

# Overview
Redux is a Discord bot created for the 2018 TSA Software Development competition. If you have any issues or requests, please open up an issue.

# Commands
### Prefix: $
* Appearance
  * ```updateBot <game>``` Sets the game that the bot is currently playing
* Blackjack
  * ```blackjack create``` sets up the game
  * ```blackjack hit``` Hit, add an additional card to your hand
  * ```blackjack stay ``` Stay, end your turn
* Games of Chance
  * ```flipcoin```
  * ```randcard```
  * ```randint (min, max)```
  * ```rolldie (sides)```
  * ```rolldice (sides)```
  * Raffle
    * ```rcreate (max players)``` Create a raffle (set the max amount of participants)
    * ```renter``` Enter the current raffle
    * ```rend``` End the raffle
* Dictionary
  * ```define <word>``` Gets the definition of a word from the Oxford Dictionary
  * ```urban <word>``` Gets the urban dictionary definition of the word
* Fornite
  * ```flookup <pc/xbox/ps4> <epic username>``` Gets the user's solo total kills, K/D, and time spent
  * ```fstats <weapon name>``` Gets the stats of the closest match of the weapon that you typed in
* Google
  * ```expand <url>``` Expands a goo.gl shortened link to get where it would redirect you to
  * ```shorten <url>``` Shortens a url into a goo.gl link
* Math
  * ```equation``` Sets the current math equation to be calculated, 4x must be 4*x
  * ```variable <var> <value>``` Sets the current value of the variable that is being used for the equation
  * ```solve``` Solves the equation using the variables specified if applicable
* Moderation
  * ```clean <amount>``` Deletes the x last messages in the channel the command was issued in
  * ```spam <message> <amount>``` Spams the message x times in the channel the command was issued in
* Music
  * **UNDER CONSTRUCTION**
  * ```summon``` Summons the bot to your voice channel
  * ```play <song url>``` Plays the current song, if one is already playing it will be added to the queue
  * ```set``` Plays the next song in the queue
  * ```skip``` Skips the current song
  * ```volume <volume>``` Sets the volume of the music player. Must be a value between 0 and 1.
  * ```disconnect``` Disconnects the bot from your voice channel
  * ```clear``` Clears the queue
* Vote
  * ```pcreate <poll name>``` Creates a poll with the specified name
  * ```pcurrent``` Gets information about the current poll
  * ```poption <option name>``` Creates a new poll option with the name specified
  * ```pstart``` Starts the poll
  * ```pstop``` Stops the poll
  * ```pvote <option>``` Vote for the option in the poll
* Stock Market
  * ```stock <ticker>``` Gets information about the stock's prices
* Weather
  * ```weather <city/zipcode>``` Gets the current weather information
* Reddit
  * ```rLatest <subreddit>``` Gets the newest post from the subreddit
  * ```rHottest <subreddit>``` Gets the hottest post from the subreddit
  * ```rWatch <subreddit>``` Waits for a new post in the subreddit, then displays it
  * ```aww``` Gets the hottest picture from /r/aww
* Connect 4
  * ```c4 new <@player> <@player>``` Creates a Connect 4 games between the players mentioned
  * ```c4 place <row>``` Drops a chip in the row
  * ```c4 remake``` Remakes the game
* Hangman
  * ```hangman new``` Creates a new Hangman game
  * ```hangman guess <letter>``` Guess a letter
  * ```hangman remake``` Remakes the game
* Tic Tac Toe
  * ```ttt new <@player> <@player>``` Creates a Tic Tac Toe game between the players mentioned
  * ```ttt place <position>``` Places your mark at the designated position
  * ```ttt remake``` Remakes the game
* Spyfall
  * ```spyfall new``` Creates a Spyfall game with the people in the voice channel of the command issuer
  * ```$spyfall vote <@Player>``` Places one vote on the Player you believe is the spy
  * ```$spyfall guess <location>``` As the spy, you can guess where you are (You only have 1 try).
  * ```$spyfall timesup``` To be run by the Game Master when the timer has ended
* Taboo
  * ```$taboo new``` Direct Messages a key word/phrase, and a blacklist of words/phrases they can not say.

# Planned Features
* **[x]** Updated interface using embeds
* **[x]** Connect 4
* **[x]** Reddit
* **[x]** ~~Setup on Heroku~~ Use Raspberry Pi
  * Run launcher.sh on startup to run the bot
* **[ ]** Poker
* **[ ]** Mobile App to control settings (mute players, etc)
  * iPhone - Expected to begin development on March 8
  * Android - To be announced
* **[ ]** Voice/Music autoplay
* **[ ]** Write a script to pull the newest release of this bot and restart the bot (for a Raspberry Pi ~~or Heroku~~)
* Find more things to add :)
