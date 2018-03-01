.. Redux documentation master file, created by
   sphinx-quickstart on Wed Feb 28 22:40:25 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _section-api:

API
=================================

.. toctree::
   :maxdepth: 2

.. _section-api-Dictionary:

Dictionary
------------

    **$define <word>**
        Arguments: (string) word - Can be more than one word
        Gets the definition of the word from the Oxford Dictionary

.. _section-api-Urban:

Urban
-----------

    **$urban <word>**
        Arguments: (string) word - Can be more than one word
        Gets the Urban dictionary definition of the word.

.. _section-api-Fortnite:

Fortnite
-----------

    **$flookup <platform> <epic username>**
        Arguments: (string) Platform - xbox/ps4/pc. (string) Epic Username
        Grabs mainly the solo stats of the player.

    **$fstats <weapon name>**
        Arguments: (string) weapon name
        Finds the closest matching weapon name and displays it's stats.

.. _section-api-Google:

Google
-------------

    **$expand <url>**
        Arguments: (string) url
        Expands a goo.gl shortened link to get where it would redirect you to

    **$shorten <url>**
        Arguments: (string) url
        Shortens a url into a goo.gl link

.. _section-api-Stocks:

Stocks
-------------

    **$stock <ticker symbol>**
        Arguments: (string) Ticker Symbol
        Gets information about the stock's prices

.. _section-api-Reddit:

Reddit
-------------

    **$rLatest <subreddit>**
        Arguments: (string) subreddit name
        Gets the newest post from the subreddit

    **$rHottest <subreddit>**
        Arguments: (string) subreddit name
        Gets the hottest post from the subreddit

    **$rWatch <subreddit>**
        Arguments: (string) subreddit name
        Waits for a new post in the subreddit, then displays it

    **$aww**
        Gets the hottest picture from /r/aww

.. _section-api-Weather:

Weather
-------------

    **$weather <city/zipcode>**
        Arguments: (string/int) city or zipcode
        Gets the current weather information
