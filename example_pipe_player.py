import sys
from collections import namedtuple

GameState = namedtuple("GameState", "stream remaining_cards current_card")

def read_int_list(s):
    return [ int(card) if card != "-1" else None for card in s.split(" ") ]

def move(game_state):
    stream = game_state.stream
    for (slot, card) in enumerate(stream):
        if card is None:
            return slot
    raise "Not slot available anymore."

def read_gamestate(line):
    (stream, remaining, current_card) = line.split(":")
    return GameState(
        stream=read_int_list(stream),
        remaining_cards=read_int_list(remaining),
        current_card=int(current_card)
    )

while True:
    try:
        line = sys.stdin.readline()
        game_state = read_gamestate(line)
        current_move = move(game_state)
        print current_move
        sys.stdout.flush()
    except:
        pass

