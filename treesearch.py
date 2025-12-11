import math
import copy
import random
import time

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
            print(move)
            s = game_env.apply_moves(s, move)
            depth += 1
        return s
    
def is_time_over(time_limit,time_elapsed):
    return time_limit is not None and (time.time() - time_elapsed) >= time_limit
    
def mtcs(root_state,game_env,time_limit):
    det_root = game_env.determinization(root_state)
    det_root['turn'] = 1
    root_node = Node(det_root,None,None)
    root_node.all_moves = game_env.get_vaild_moves(root_node.state)
    root_node.children = []
    time_elapsed = time.time()
    for move in root_node.all_moves:
        child_state = game_env.apply_moves(root_node.state, move)
        child_node = Node(child_state, root_node, move)
        root_node.children.append(child_node)
        child_node.all_moves = []
    if not root_node.children:
        return None
    for _ in range(iterations):
            child = random.choice(root_node.children)
            if not child:
                continue
            sim_state = copy.deepcopy(child.state)
            final_state = child.simulations(sim_state,game_env) 
            if final_state is None:
                continue
            reward = game_env.get_reward(final_state)
            print('Move:',child.previous_move)
            print('Reward',reward)
            child.value += (reward or 0)
            child.visits += 1
    best = root_node.best_child(1.4)
    if best is None:
        return None
    return best.previous_move