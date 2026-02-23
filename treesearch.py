import math
import copy
import random
import time

class Node:
    def __init__(self, state, parent=None, previous_move=None): #Initialising attributes for the node objects
        self.state = state
        self.parent = parent
        self.previous_move = previous_move
        self.children = []
        self.untried_moves = None
        self.visits = 0
        self.value = 0.0
        self.depth = 0 if parent is None else parent.depth + 1 #Sets the depth of the object to be one plus the parent's node depth unless it is the root node

    def tried_all_moves(self): #Checks all moves in untried moves list have been attempted
        return self.untried_moves is not None and len(self.untried_moves) == 0
    
    def best_child(self,c_param=1.5):
        choices = []
        if not self.children: #Vaildates that the node has children
            return None
        for child in self.children: #Iterates through the nodes children
            if child.visits == 0: #Checks the child has visits
                UCT = 0
            else:
                UCT = (child.value / child.visits) + (c_param * math.sqrt(2 * math.log(self.visits + 1)/child.visits)) #Calculates the child's upper confidence bound vaule
            choices.append(UCT)
        if not choices: #Vaildates that there are choices available
            return None
        return self.children[choices.index(max(choices))] #Returns the index of the child which returned the highest UCT
    
    def simulations(self,state,game_env,max_depth=50):
        s = copy.deepcopy(state) #Makes a copy of the given game state
        depth = 0
        while not game_env.is_terminal(s) and depth < max_depth: #Creates a loop which will end once the state of the game reaches terminal or the max-depth is reached
            moves = game_env.get_vaild_moves(s) #Returns vaild moves
            if not moves: #Checks that a move exists, end the loop if not
                break
            move = game_env.rollout_policy(moves,s) #Determines the best move 
            s = game_env.apply_moves(s, move) #Applys the move to the game state
            depth += 1 #Increments the depth of simulation
        return s
    
def is_time_over(time_limit,time_elapsed): #Checks if the time elapsed is less then the time limit set
    return time_limit is not None and (time.time() - time_elapsed) >= time_limit
    
def m_mtcs(root_state,game_env,time_limit):
    det_root = game_env.determinization(root_state) #Determinizes the game state to fill in unknown information
    #Selects a random move if the card array is empty
    if root_state['name'] == "memory" and det_root['card_array'] == [['' for _ in range(6)] for _ in range(9)]: 
        moves = game_env.get_vaild_moves(root_state)
        random_move = random.choice(moves)
        return random_move  
    #Sets roots node turn to the AI's turn
    det_root['turn'] = 1
    root_node = Node(det_root,None,None) #Creates root node object
    root_node.untried_moves = game_env.get_vaild_moves(root_node.state) #
    time_elapsed = time.time()
    start_time = time.time()
    iterations = 0
    while not is_time_over(time_limit,time_elapsed) or root_node.untried_moves: #Loops through code until all moves have been tried or the time limit has been met
        node = root_node
        path = [root_node]
        #Selection
        while (node.depth < 2 and node.tried_all_moves() and node.children): #Loops through the nodes children until all moves have been tried
            node = node.best_child()
            if node is None:
                break
            path.append(node)        
        # If selection returned None (no children), skip this iteration
        if node is None:
            #iterations += 1
            continue
        #Expansion
        if node.depth < 2:
            if node.untried_moves is None:
                node.untried_moves = game_env.get_vaild_moves(node.state)
            if node.untried_moves:
                move = node.untried_moves.pop(random.randrange(len(node.untried_moves)))
                child_state = game_env.apply_moves(node.state, move)
                child_node = Node(child_state, node, move)
                node.children.append(child_node)
                node = child_node
                path.append(node)
        #Simulation
            sim_state = copy.deepcopy(node.state)
            final_state = node.simulations(sim_state,game_env,20) 
        #Backpropagation
            if final_state is None:
                reward = 0
            else:
                reward = game_env.get_reward(final_state)
            for nodes in path:
                nodes.visits += 1
                nodes.value += reward
        #iterations += 1

    total_time = time.time() - start_time #Calculates total time elapsed
    
    '''
    if debug:
        print(f"MCTS debug: iterations={iterations}, elapsed={total_time:.3f}s, root_turn={det_root.get('turn')}")
        untried = len(root_node.untried_moves) if root_node.untried_moves else 0
        explored = len(root_node.children)
        print(f"Root node: {untried} untried moves, {explored} explored children (total moves: {untried + explored})")
        if root_node.children:
            # show stats sorted by visits
            stats = []
            for c in root_node.children:
                avg = (c.value / c.visits) if c.visits else float('nan')
                stats.append((c.previous_move, c.visits, avg))
            stats.sort(key=lambda x: x[1], reverse=True)
            print("Root children stats (move, visits, avg_value):")
            for m, v, a in stats:
                print(f"  {m} -> visits={v}, avg={a}")
    '''

    best = root_node.best_child(1.4)
    if best is None: #Checks if there is a best move selected if not just picks a random move
        moves = game_env.get_vaild_moves(root_state)
        random_move = random.choice(moves)
        return random_move
    return best.previous_move
