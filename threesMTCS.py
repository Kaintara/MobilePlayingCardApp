import copy
from treesearch_mcts import mtcs

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
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        player = state['turn']
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
            Moves.append((player,list(state['played_cards']),"pickup"))
            Top_card = state['played_cards'][-1]
            if Top_card[0] == '2':
                for card in Hand:
                    Moves.append((player,card,"play"))
                    return Moves
            for card in Hand:
                if Top_card[0] == card[0]:
                    Valid_Cards.append(Top_card)
                    break
            temp_hand = Hand[:] + [Top_card]
            temp_hand.sort(key=lambda a: rank_order[a[0]])
            for card in Hand:
                if card[0] == Top_card[0]:
                    Valid_Cards.append(card)
            idx = temp_hand.index(Top_card) + 1
            if idx < len(temp_hand):
                Valid_Cards += temp_hand[idx:]
            for card in Valid_Cards:
                Moves.append((player,card,"play"))
        else:
            for card in Hand:
                Moves.append((player,card,"play"))
        return Moves
    
    def apply_moves(env,og_state,move):
        state = copy.deepcopy(og_state)
        if not move:
            if env.is_terminal(state):
                return state
            state['turn'] = env.next_valid_player(state)
            return state
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        payload = move[1]
        if isinstance(payload, list):
            payload_for_history = list(payload)
        else:
            payload_for_history = payload
        state["history"].append((move[0], payload_for_history, move[2]))
        player = move[0]
        if state["played_cards"]:
            Top_card = state["played_cards"][-1]
        else:
            Top_card = '2H'
        if move[2] == "try":
            if Top_card[0] == '2':
                env.apply_moves(state, (player,move[1],"play"))
            else:
                Card_rank = rank_order[move[1][0]]
                if Card_rank >= rank_order[Top_card[0]]:
                    env.apply_moves(state, (player,move[1],"play"))
                else:
                    env.apply_moves(state, (player, list(state["played_cards"]), "pickup"))
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
                snapshot = list(state["played_cards"])
                for card in snapshot:
                    if card not in state['hands'][player]:
                        state['hands'][player].append(card)
             state["played_cards"] = []
        if env.is_terminal(state):
            return state
        else:
            if state['another'] == True:
                state['another'] = False
            if state['turn'] == 1:
                state['turn'] = 0
            else:
                state['turn'] = 1
        return state
    
    def get_reward(env,state):
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        Hand = []
        Bot_Hand = []
        player = 1
        for i in range(0,2):
            if state['hands'][i]:
                Hand = state['hands'][i]
            elif state['top_hands'][i]:
                Hand = state['top_hands'][i]
            else:
                Hand = state['bottom_hands'][i]
            if i == 1:
                Bot_Hand = Hand
        if env.is_terminal(state):
            return 1000 if state['winner'] == player else -1000
        reward = 0
        reward -= len(Bot_Hand) * 4
        if state['history'] and state['history'][-1][2] == "pickup":
            reward -= 20
        if len(state['played_cards']) == 0 and state['history']:
            if state['history'][-1][2] == "play":
                reward += 12
        if state.get('another', False):
            reward += 5
        difference = (len(Hand)-3) * 2
        card_difference = min([rank_order[card[0]] for card in Bot_Hand]) - max([rank_order[card[0]] for card in Bot_Hand])
        return reward + difference + card_difference

    def is_terminal(env,state):
        for player in [0, 1]:
            if (not state['hands'][player] and not state['top_hands'][player] and not state['bottom_hands'][player]):
                if not state['bottom_hands'][0]:
                    state['winner'] = 0
                else:
                    state['winner'] = 1
                return True
        return False
    
    def next_valid_player(env,state):
        if env.is_terminal(state):
            return
        else:
            if state['another'] == True:
                state['another'] = False
                return state['turn']
            if state['turn'] == 1:
                return 0
            else:
                return 1

genv = GameEnvironment()
state = {'name': 'threes', 'deck': ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD', 'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC', 'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH'], 'shuffled_deck': ['4C', 'AD', '8D', 'AS', '7C', 'KC', '2S', '7D', 'QH', '3C', '5S', 'AC', '6H', '8C', '5H', '4D', '1C', '9D', '1S', 'QS', 'KD', 'QD', '6D', '5D', 'JC', '9C', '3D', '4H', '9H', 'JD'], 'rank_order': {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '1': 16, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 15}, 'hands': [['7H', 'JS', 'KH'], ['1D', '7S', '8H']], 'discard_pile': [], 'selected_card': '', 'turn': 1, 'time_elapsed': 0, 'difficulty': (0, 'Easy'), 'winner': None, 'bottom_hands': [['2C', '3H', '8S'], ['1H', '2D', 'AH']], 'top_hands': [['5C', '6C', '6S'], ['JH', '4S', '3S']], 'another': False, 'played_cards': ['QC', 'KS', '2H', '9S'], 'history': [(0, 'KS', 'play'), (1, 'KH', 'play'), (0, ['KS', 'KH'], 'pickup'), (1, 'QC', 'play'), (0, 'KS', 'play'), (1, '2H', 'play'), (0, '9S', 'play')]}

print(genv.determinization(state))
print(genv.get_reward(genv.determinization(state)))

print(mtcs(state,genv,100,2))