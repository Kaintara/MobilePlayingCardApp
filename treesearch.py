import math
import copy
import random

class Node:
    def __init__(self, state, parent=None, previous_move=None):
        self.state = state
        self.parent = parent
        self.previous_move = previous_move
        self.children = []
        self.all_moves = None
        self.visits = 0
        self.value = 0.0

    def tried_all_moves(self):
        return self.all_moves is not None and len(self.all_moves) == 0
    
    def best_child(self,c_param=1.41):
        choices = []
        for child in self.children:
            if not self.children:
                return None
            if child.visits == 0:
                UCT = float('inf')
            else:
                UCT = (child.value / child.visits) + (c_param * math.sqrt(2 * math.log(self.visits + 1)/child.visits))
            choices.append(UCT)
        if not choices:
            return None
        return self.children[choices.index(max(choices))]
    
    def simulations(self,state,game_env,max_depth=200):
        s = copy.deepcopy(state)
        depth = 0
        while not game_env.is_terminal(s) and depth < max_depth:
            moves = game_env.get_vaild_moves(s)
            if not moves:
                break
            move = random.choice(moves)
            s = game_env.apply_moves(s, move)  # apply_moves returns a NEW state
            depth += 1
        return s