import random
import subprocess
import sys




def subseq_length(stream):
    stream_it = iter(stream)
    next = stream_it.next()
    start=0
    cursor=0
    for card in stream_it:
        cursor += 1
        (prev,next) = (next, card)
        if (next<prev):
            yield (start, cursor)
            start = cursor
    yield (start, cursor + 1)

def score_stream(stream):
    score = 0
    for (start,end) in subseq_length(stream):
        score += GameState.SCORES[end-start]
    return score

class GameState:

    SCORES = [0, 0, 1, 3, 5, 7, 9, 11, 15, 20, 25, 30, 35, 40, 50, 60, 70, 85, 100, 150, 300]

    def __init__(self,):
        self.stream = [None] * 20       # State of the stream. Empty slots have the value None.
        self.turn = 0                   # Turn number
        self.cards = range(1,11) + range(11,20)*2 + range(20,31) # Remaining cards
        self.current_card = None        # The card to put on the board at this turn.

    def start_turn(self,):
        card = random.choice(self.cards)
        self.cards.remove(card)
        self.current_card = card

    def apply(self,move):
        self.stream[move] = self.current_card
        self.turn += 1

    def is_finished(self,):
        return self.turn == 20

    def score(self,):
        return score_stream(self.stream)

class Player:
    
    def move(self, game_state):
        raise NotImplementedError()

class Match:

    def __init__(self, player):
        self.player = player
        self.game_state = GameState()

    def run(self,):
        while not self.game_state.is_finished():
            self.game_state.start_turn()
            move = self.player.move(self.game_state)
            #print move
            self.game_state.apply(move)
        return self.game_state.score()

class PipePlayer:

    def __init__(self, cmd=None):
        if len(cmd) > 0:
            self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=sys.stderr)
            self.cout = self.process.stdin
            self.cin = self.process.stdout
        else:
            self.cin = sys.stdin
            self.cout = sys.stdout

    def prompt(self, msg):
        self.cout.write(msg + "\n")
        self.cout.flush()
        return self.cin.readline()
        
    def move(self, game_state):
        info = ":".join([
            " ".join(str(val or -1) for val in game_state.stream),
            " ".join(map(str,game_state.cards)),
            str(game_state.current_card)
        ])
        return int(self.prompt(info))

def player_from_argv(argv):
    if len(argv) > 0:
        if argv[0] == "-p":
            return PipePlayer(argv[1:])
        if argv[0] == "-m":
            return __import__(*argv[1:])
    return None

def help():
    print """
    You may either run your player as a python module:
      - python streams.py -m <your_python_module_name>
        e.g. python streams.py -m simple_player

    ... or as an external process.
      - python streams.py 

    """

def main(argv):
    NB_RUNS = 1000
    score = 0
    player = player_from_argv(argv)
    if player == None:
        help()
    else:
        for i in range(NB_RUNS):
            run_score = Match(player).run()
            print run_score
            score += run_score 
    print score / float(NB_RUNS)

if __name__ == "__main__":
    main(sys.argv[1:])