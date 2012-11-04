import random
from collections import defaultdict
from copy import copy
from streams import score_stream, subseq_length
from itertools import cycle

T=10

def try_shifts(stream, future_cards):
    cycle_future_cards = cycle(future_cards)
    for c in range(len(future_cards)):
        completed_stream = (slot if slot is not None else cycle_future_cards.next() for slot in stream)
        for (start, end) in subseq_length(completed_stream):
            if not all(stream[start:end]):
                yield (end-start, (c, start, end))
        cycle_future_cards.next() # shift future cards from 1.

def put_longest(stream, future_cards):
    (_, (c, start,end)) = max(try_shifts(stream, future_cards))
    offset = c
    for (i, slot) in enumerate(stream):
        if slot is None:
            if i < start:
                offset+=1
            elif i<end:
                offset %= len(future_cards)
                stream[i] = future_cards.pop(offset)

def deterministic(stream, future_cards):
    stream = copy(stream)
    future_cards = copy(future_cards)
    while len(future_cards) > 0:
        put_longest(stream,future_cards)
    return score_stream(stream)

def move(game_state):
    stream = game_state.stream
    available_slots = [ slot for (slot, card) in enumerate(stream) if card is None]
    remaining_cards = game_state.cards
    trajectories = [ sorted(random.sample(remaining_cards, len(available_slots)-1)) for t in range(T) ]
    c = defaultdict(int)
    for slot in available_slots:
        stream_copy = copy(stream)
        stream_copy[slot] = game_state.current_card
        for trajectory in trajectories:
            c[slot] += deterministic(stream_copy, trajectory)
    return max([ (v,k) for (k,v) in c.items() ])[1]

