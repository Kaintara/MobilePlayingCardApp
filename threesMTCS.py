import math
import copy
import random

class GameEnvironment:
    def __init__(env):
        pass

    def determinization(env,state):
        threes = copy.deepcopy(state)
        public_cards = threes['hands'][1] + threes['top_hands'][1] + threes['top_hands'][0] + threes['discard_pile'] + threes['played_cards']