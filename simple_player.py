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
        completed_stream = list(completed_stream)
        for (start, end) in subseq_length(completed_stream):
            if not all(stream[start:end]):
                yield (end-start, (c, start, end))
        cycle_future_cards.next() # shift future cards from 1.

def put_longest(stream, future_cards):
    (_, (c, start,end)) = max(try_shifts(stream, future_cards))
    shifted_future_cards = future_cards[c:] + future_cards[:c]
    offset = 0
    new_stream = copy(stream)
    for (i, slot) in enumerate(stream):
        if slot is None:
            if i < start:
                offset+=1
            elif i<end:
                new_stream[i] = shifted_future_cards.pop(offset)
    return (new_stream, sorted(shifted_future_cards))


def deterministic(stream, future_cards):
    while len(future_cards) > 0:
        (stream, future_cards) = put_longest(stream, future_cards)
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
