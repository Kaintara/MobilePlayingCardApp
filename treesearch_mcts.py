import math
import time
import copy
import random


class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move  # move that lead to this state
        self.children = []
        self.untried_moves = None
        self.visits = 0
        self.value = 0.0

    def is_fully_expanded(self):
        return self.untried_moves is not None and len(self.untried_moves) == 0

    def best_child(self, c=1.4):
        # return child with highest UCT score
        best = None
        best_score = -float('inf')
        for child in self.children:
            if child.visits == 0:
                score = float('inf')
            else:
                exploit = child.value / child.visits
                explore = c * math.sqrt(math.log(self.visits + 1) / child.visits)
                score = exploit + explore
            if score > best_score:
                best_score = score
                best = child
        return best


# small helpers to be resilient to API name variants used in this repo
def _get_moves(env, state):
    if hasattr(env, 'get_vaild_moves'):
        return env.get_vaild_moves(state)
    if hasattr(env, 'get_valid_moves'):
        return env.get_valid_moves(state)
    # fallback: expect environment to provide a function
    raise AttributeError('Environment does not provide get_vaild_moves / get_valid_moves')


def _is_terminal(env, state):
    if hasattr(env, 'is_terminal'):
        return env.is_terminal(state)
    raise AttributeError('Environment does not provide is_terminal')


def _apply_move(env, state, move):
    if hasattr(env, 'apply_moves'):
        return env.apply_moves(state, move)
    raise AttributeError('Environment does not provide apply_moves')


def _determinize(env, state):
    if hasattr(env, 'determinization'):
        return env.determinization(state)
    return state


def _get_reward(env, state):
    if hasattr(env, 'get_reward'):
        return env.get_reward(state)
    raise AttributeError('Environment does not provide get_reward')


def _rollout_policy(moves):
    # default: uniform random; you can plug in heuristics here
    return random.choice(moves)


def mcts(root_state, game_env, time_limit=None, iterations=None, c=1.4, rollout_depth=200):
    """
    Time-limited or iteration-limited MCTS.

    Arguments:
    - root_state: the current (possibly partially observable) state
    - game_env: environment object providing methods used across repo
    - time_limit: seconds to run (float). If given, iterations is ignored.
    - iterations: number of simulations to run if time_limit is None.
    - c: UCT exploration constant
    - rollout_depth: max depth for rollouts

    Returns: best move (the child move with most visits), or None if no move.
    """
    # Determinize root if environment supports it (useful for partial information games)
    det_root = _determinize(game_env, root_state)
    # Optionally set the actor to the bot if needed (some code did set turn=1)
    # det_root['turn'] = 1  # do not force unless caller requires

    root = MCTSNode(det_root, parent=None, move=None)
    try:
        root.untried_moves = list(_get_moves(game_env, root.state))
    except AttributeError:
        root.untried_moves = []

    if not root.untried_moves:
        return None

    start_time = time.time()
    sims = 0

    def time_exceeded():
        return time_limit is not None and (time.time() - start_time) >= time_limit

    while True:
        if time_limit is None:
            if iterations is None:
                break
            if sims >= iterations:
                break
        else:
            if time_exceeded():
                break

        node = root
        path = [node]

        # Selection
        while not _is_terminal(game_env, node.state) and node.is_fully_expanded():
            node = node.best_child(c)
            if node is None:
                break
            path.append(node)

        # Expansion
        if not _is_terminal(game_env, node.state):
            if node.untried_moves is None:
                node.untried_moves = list(_get_moves(game_env, node.state))
            if node.untried_moves:
                move = node.untried_moves.pop(random.randrange(len(node.untried_moves)))
                child_state = _apply_move(game_env, node.state, move)
                child = MCTSNode(child_state, parent=node, move=move)
                # child untried_moves set lazily during selection/expansion
                node.children.append(child)
                node = child
                path.append(node)

        # Simulation / Rollout
        sim_state = copy.deepcopy(node.state)
        depth = 0
        while not _is_terminal(game_env, sim_state) and depth < rollout_depth:
            moves = _get_moves(game_env, sim_state)
            if not moves:
                break
            move = _rollout_policy(moves)
            sim_state = _apply_move(game_env, sim_state, move)
            depth += 1

        # Backpropagation
        try:
            reward = _get_reward(game_env, sim_state) or 0
        except Exception:
            reward = 0

        for n in path:
            n.visits += 1
            n.value += reward

        sims += 1

    # Choose the best child of root (by visits)
    best = None
    best_visits = -1
    for child in root.children:
        if child.visits > best_visits:
            best_visits = child.visits
            best = child

    if best is None:
        return None
    return best.move


# Small convenience wrapper for legacy code using mtcs name
def mtcs(root_state, game_env, iterations=100, time_limit=None):
    # if time_limit provided, iterations is ignored
    return mcts(root_state, game_env, time_limit=time_limit, iterations=iterations)
