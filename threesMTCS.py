import math
import copy
import random

class GameEnvironment:
    def __init__(env):
        pass

    def determinization(env,state):
        threes = copy.deepcopy(state)
        public_cards = []
        if threes.state['hands'][1]:
            for x in threes.state['hands'][1]:
                public_cards.append(x)
        if threes.state['top_hands'][1]:
            for x in threes.state['hands'][1]:
                public_cards.append(x)
        if threes.state['top_hands'][0]:
            for x in threes.state['hands'][1]:
                public_cards.append(x)
        if threes.state['discard_pile'][1]:
            for x in threes.state['hands'][1]:
                public_cards.append(x)   
        if threes.state['played_cards'][1]:
            for x in threes.state['hands'][1]:
                public_cards.append(x)     