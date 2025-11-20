import math
import copy
import random
from treesearch import Node

class GameEnvironment:
    def __init__(env):
        pass

    def determinization(env,state):
        threes = copy.deepcopy(state)
        public_cards = []
        if threes['hands'][1]:
            for card in threes['hands'][1]:
                public_cards.append(card)
        if threes['top_hands'][1]:
            for card in threes['hands'][1]:
                public_cards.append(card)
        if threes['top_hands'][0]:
            for card in threes['hands'][1]:
                public_cards.append(card)
        if threes['discard_pile']:
            for card in threes['hands'][1]:
                public_cards.append(card)   
        if threes['played_cards']:
            for card in threes['hands'][1]:
                public_cards.append(card)
        unknown_cards = threes['deck']
        for card in unknown_cards:
            if card in public_cards:
                unknown_cards.remove(card)
        if not threes["history"]:
            Hands = [threes['hands'][1], threes['bottom_hands'][1], threes['bottom_hands'][0]]
            for hand in Hands:
                hand = []
                for _ in range(0,3):
                    card = unknown_cards.pop()
                    hand.append(card)
            threes['shuffled_deck'] = unknown_cards
        else:
            Player_hand = []
            if threes['history'][-1][2] == 'pickup' and threes['history'][-1][0] == 0:
                for card in threes['history'][-1][1]:
                    if card in unknown_cards:
                        Player_hand.append(card)
            while len(threes['hands'][0]) != len(Player_hand):
                Player_hand.append(unknown_cards.pop())
            threes['bottom_hands'][1] = []
            threes['bottom_hands'][0] = []
            for _ in range(0,3):
                card1 = unknown_cards.pop()
                threes["bottom_hands"][1].append(card1)
                card2 = unknown_cards.pop()
                threes["bottom_hands"][0].append(card2)
            threes['shuffled_deck'] = unknown_cards
            threes['hands'][0] = Player_hand
        return threes
    
    def sort_cards(env,state):
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        state['hands'][0].sort(key=(lambda a : rank_order[a[0]]))
        state['hands'][1].sort(key=(lambda a : rank_order[a[0]]))
    
    def get_vaild_moves(env,state):
        player = 1 - state['turn']
        Moves = []
        Valid_Cards = []
        if state['hands'][player]:
            Hand = state['hands'][player]
        elif state['top_hands'][player]:
            Hand = state['top_hands'][player]
        else:
            Hand = state['bottom_hands'][player]
            for card in Hand:
                Moves.append((player,card,"try"))
            return Moves
        if state['played_cards']:
            Moves.append((player,state['played_cards'],"pickup"))
            Top_card = state['played_cards'][-1]
            if Top_card[0] == '2':
                for card in Hand:
                    Moves.append((player,card,"play"))
                    return Moves
            for card in Hand:
                if Top_card[0] == card[0]:
                    Valid_Cards.append(Top_card)
                    break
            Hand.append(Top_card)
            env.sort_cards(state)
            Index = Hand.index(Top_card) + 1
            Valid_Cards += Hand[Index:]
            for card in Valid_Cards:
                Moves.append((player,card,"play"))
        else:
            for card in Hand:
                Moves.append((player,card,"play"))
        return Moves
    
    def apply_moves(env,state,move):
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        state["history"].append(move)
        player = move[0]
        if state["played_cards"]:
            Top_card = state["played_cards"][-1]
        else:
            Top_card = '2H'
        if move[2] == "try":
            if Top_card[0] == '2':
                state["played_cards"].append(move[1])
                state["bottom_hands"][player].remove(move[1])
            else:
                Card_rank = rank_order[move[1][0]]
                if Card_rank >= rank_order[Top_card[0]]:
                    state["played_cards"].append(move[1])
                    state["bottom_hands"][player].remove(move[1])
                else:
                    env.apply_moves(state, (player, state["played_cards"], "pickup"))
                    return
        elif move[2] == "play":
            state["played_cards"].append(move[1])
            Hands = [state['hands'][player],state["bottom_hands"][player],state["top_hands"][player]]
            for cards in Hands:
                if move[1] in cards:
                    cards.remove(move[1])
            four = False
            if len(state["played_cards"]) > 3:
                for i in range(1,5):
                    if i == 1:
                        rank = state["played_cards"][-i][0]
                    else:
                        temp = rank
                        rank = state["played_cards"][-i][0]
                        if temp == rank:
                            four = True
                        else:
                            four = False
                            break
            if four == True or move[1][0] == '1':
                state['discard_pile'] += state["played_cards"]
                state["played_cards"] = []
                state['another'] = True
            if state['shuffled_deck'] and state['hands'][player]:
                while state['shuffled_deck']:
                    while len(state['hands'][player]) < 3:
                        card = state['shuffled_deck'].pop()
                        state['hands'][player].append(card)
                    break
        elif move[2] == "pickup":
            if state["played_cards"]:
                for card in state["played_cards"]:
                    state['hands'][player].append(card)
            state["played_cards"] = []
        if not state.get('another', False):
            state['turn'] = 1 - state['turn']
        else:
            state['another'] = False
        return state
    
    def get_reward(env,state):
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        Hand = []
        Bot_Hand = []
        for i in range(0,2):
            if state['hands'][i]:
                Hand = state['hands'][i]
            elif state['top_hands'][i]:
                Hand = state['top_hands'][i]
            else:
                Hand = state['bottom_hands'][i]
            if i == 1:
                Bot_Hand = Hand
        reward = 0
        difference = (len(Hand) - len(Bot_Hand)) * 2
        card_value = max([rank_order[card[0]] for card in Bot_Hand])
        card_difference = min([rank_order[card[0]] for card in Bot_Hand]) - max([rank_order[card[0]] for card in Hand])
        if len(Bot_Hand) < 3:
            reward += 5
        return reward + difference + card_value + card_difference

    def is_terminal(env,state):
        for player in [0, 1]:
            if (not state['hands'][player] and not state['top_hands'][player] and not state['bottom_hands'][player]):
                return True
        return False

genv = GameEnvironment()
state = {'name': 'threes', 'deck': ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD', 'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH'], 'shuffled_deck': ['3D', '7C', '2S', 'KD', 'QH', '2D', 'AC', '1D', '1C', 'JC', '9S', '6D', '9C', '6C', '5D', 'AD', 'QD', 'KS', '5S', '1H', '4C', '8S', 'JH', '8C', '4S', 'JD', 'AH', '5C', '7H', '4D', 'JS', '9D'], 'rank_order': {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '1': 16, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 15}, 'hands': [['6H', 'QS', '7S'], ['5H', '8D', 'QC']], 'discard_pile': [], 'selected_card': '', 'turn': 0, 'time_elapsed': 0, 'difficulty': (0, 'Easy'), 'winner': None, 'bottom_hands': [['7D', '6S', '4H'], ['KC', '1S', 'AS']], 'top_hands': [['9H', 'KH', '2C'], ['8H', '3H', '3S']], 'another': False, 'played_cards': ['QC', '2H', '3C'], 'history': [(0, 'QC', 'play'), (1, '2H', 'play'), (0, '3C', 'play')]}
print(genv.determinization(state))
print(genv.get_reward(genv.determinization(state)))

def one_level_mtcs(root_state,game_env,iterations):
    det_root = game_env.determinization(root_state)
    root_node = Node(det_root,None,None)
    root_node.all_moves = game_env.get_vaild_moves(root_node.state)
    for move in root_node.all_moves:
        child_state = game_env.apply_moves(det_root, move)
        child_node = Node(child_state, root_node, move)
        root_node.children.append(child_node)
        child_node.all_moves = []
    for _ in range(iterations):
            child = random.choice(root_node.children)
            if not child:
                continue
            sim_state = copy.deepcopy(child.state)
            final_state = child.simulations(sim_state,game_env) #Error is here! Test the Node classes first then come back to this.
            reward = game_env.get_reward(final_state)
            print("Reward:", reward)
            print("Move:", child.previous_move)
            print("Final State:", final_state)
            if not reward:
                child.value += 0
            else:
                child.value += reward
            child.visits += 1
    best = root_node.best_child(1.4)
    if best is None:
        return None
    return best.previous_move

print(one_level_mtcs(state,genv,30))
