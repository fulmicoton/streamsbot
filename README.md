Streamsbot
=============


This repo hosts an arbiter and a simple player for the board game called
[Streams](http://www.moonstergames.com/streams/) which rules are available
[here](https://dl.dropbox.com/u/3201764/STREAM_RULES%20FR%20US%20KR.pdf).





Rules
-------------



Your stream is a list of 20 slots, empty at the beginning of the game.

At each of the 20 turn, a card is taken out of deck of card. 
The deck consists of 40 cards, each showing a number between 1 and 30.
Numbers between 11 and 20 appears twice.

At each turn, the player is expected to put this card on one available
slot of his stream. 

At the end of the game, all of the slot of his stream are occupied.
The goal of the game is to produce long increasing sequences in the stream.
So if the stream shows 

```python
    [  9,  8, 21, 23,  3,  4,  5, 10, 12, 13, 
      13, 15, 19, 14, 18, 25, 26, 16, 11, 30   ]

```

In which we identify the increasing subsquences

```
    [  8, 21, 23 ]    :  length 3
    [  3,  4,  5, 10, 12, 13, 13, 15, 19 ] :  length 9
    [ 14, 18, 25, 26] :  length 4
    [ 11, 30 ] :  length 2
```

The number of points given for each subsequences is given by the following table :

```

 Length | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14| 15| 16| 17| 18| 19| 20
--------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+----
 Points | 1 | 3 | 5 | 7 | 9 | 11| 15| 20| 25| 30| 35| 40| 50| 60| 70| 85|100|150|300
```

So that the resulting score of our example is

```
    3 + 20 + 5 + 1 = 29 points

```



Writing a python bot
--------------------------

The arbiter can load bots as a python module.
In that case, just create a file with a move function.

```python
def  move(game_state):
    # ... your strategy here
    return computed_move
```

**game_state** here is an object with all the information describing the 
current state of the game.

Namingly 
```python

# a list with length 20 describing your stream. 
# Empty slots contains None
game_state.stream 

# The value of the card you need to place for this turn
game_state.current_card

# A sorted list with the cards which are still available
# in the deck. (One value might appear twice)
game_state.cards

```

You can then evaluate your algorithm with 

```
python streams.py -m <your-python-module-name>
```

For instance you may run the example via :

```
python streams.py -m simple_player
```




Writing a bot in whatever language
------------------------------------------------

You can actually write a bot in whatever language you want.
In this case, your bot will run in a process spawned
by the arbiter program.

At each turn, the arbiter will send your process the game state via 
stdin.

The game state is encoded on one line with three fields separated by a column.

The first field is a your stream state.
It is encoded as space-separated integers. Empty slots are 
encoded as -1.

The second field is a the list of cards remaining in the deck,
also encoded as space-separated integers.

The last field is the current card your are expected to put in your stream.

Your program is expected to put the 0-indexed position at which you want to put 
your card.

The bot can be run via 

```
python streams.py -p <your complete command-line>
```

For instance your can run a very simple example with :

```
python streams.py -p python example_pipe_player.py
```

You can also check out the format of the input and output
by conversing directly with the bot from your console 
by running 

```
python streams.py -p 
```
