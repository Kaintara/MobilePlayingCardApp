import copy
from treesearch import mtcs
import random
import math

class GameEnvironment:
    def __init__(env):
        pass

    def softmax(env,xs, temp=0.7):
        m = max(xs)
        exps = [math.exp((x - m) / temp) for x in xs]
        s = sum(exps)
        return [e / s for e in exps]

    def determinization(env,state):
        threes = copy.deepcopy(state)
        public_cards = []
        if threes['hands'][1]:
            for card in threes['hands'][1]:
                public_cards.append(card)
        if threes['top_hands'][1]:
            for card in threes['top_hands'][1]:
                public_cards.append(card)
        if threes['top_hands'][0]:
            for card in threes['top_hands'][0]:
                public_cards.append(card)
        if threes['discard_pile']:
            for card in threes['discard_pile']:
                public_cards.append(card)   
        if threes['played_cards']:
            for card in threes['played_cards']:
                public_cards.append(card)
        unknown_cards = [c for c in threes['deck'] if c not in public_cards]
        if not threes["history"]:
            threes['hands'][1] = []
            for _ in range(0,3):
                card = unknown_cards.pop()
                threes['hands'][1].append(card)
            threes['bottom_hands'][1] = []
            for _ in range(0,3):
                card = unknown_cards.pop()
                threes['bottom_hands'][1].append(card)
            threes['bottom_hands'][0] = []
            for _ in range(0,3):
                card = unknown_cards.pop()
                threes['bottom_hands'][0].append(card)
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
            for _ in range(len(state['bottom_hands'][1])):
                card1 = unknown_cards.pop()
                threes["bottom_hands"][1].append(card1)
            threes['bottom_hands'][0] = []
            for _ in range(len(state['bottom_hands'][0])):
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
            Top_card = state['played_cards'][-1]
            if Top_card[0] == '2':
                for card in Hand:
                    Moves.append((player,card,"play"))
                return Moves
            for card in Hand:
                if card[0] == Top_card[0]:
                    Valid_Cards.append(card)
            temp_hand = Hand[:] + [Top_card]
            temp_hand.sort(key=lambda a: rank_order[a[0]])
            idx = temp_hand.index(Top_card) + 1
            if idx < len(temp_hand):
                Valid_Cards += temp_hand[idx:]
            for card in Valid_Cards:
                if card not in [m[1] for m in Moves]:  # Avoid duplicate moves
                    Moves.append((player,card,"play"))
            if not Moves:
                Moves.append((player,list(state['played_cards']),"pickup"))
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
                return env.apply_moves(state, (player,move[1],"play"))
            else:
                Card_rank = rank_order[move[1][0]]
                if Card_rank >= rank_order[Top_card[0]]:
                    return env.apply_moves(state, (player,move[1],"play"))
                else:
                    return env.apply_moves(state, (player, list(state["played_cards"]), "pickup"))
        elif move[2] == "play":
            played_rank = move[1][0]
            Hands = [state['hands'][player],state["bottom_hands"][player],state["top_hands"][player]]
            if played_rank in ('1','2'):
                state["played_cards"].append(move[1])
                for cards in Hands:
                    if move[1] in cards:
                        cards.remove(move[1])
            else:
                played_now = []
                Hand = []
                if state['hands'][player]:
                    Hand = state['hands'][player]
                elif state['top_hands'][player]:
                    Hand = state['top_hands'][player]
                elif state['bottom_hands'][player]:
                    Hand = state['bottom_hands'][player]
                else:
                    Hand = []

                for card in Hand[:]:
                    if card[0] == played_rank:
                        Hand.remove(card)
                        state["played_cards"].append(card)
                        played_now.append(card)
                state['history'][-1] = (player,played_now,'play')
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
                    while len(state['hands'][player]) < 3 and state['shuffled_deck']:
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
        if env.is_terminal(state):
            return 100 if state['winner'] == 1 else -100
        cards_left = len(state['hands'][1]) + len(state['top_hands'][1]) + len(state['bottom_hands'][1])
        cards_left2 = len(state['hands'][0]) + len(state['top_hands'][0]) + len(state['bottom_hands'][0])
        if state['turn'] == 0:
            return cards_left2
        return -cards_left
    
    def rollout_policy(env,moves,state):
        if len(moves) == 1:
            return moves[0]
        else:
            rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
            #scores = []
            best_move = moves[0]
            for move in moves:
                player, card, action = move
                if action == 'pickup':
                    continue
                elif action == 'play':
                    rank = card[0]
                    best_move_rank = best_move[1][0]
                    if rank_order[rank] < rank_order[best_move_rank[0]]:
                        best_move = move
                '''
                score = 0.0
                if action == 'pickup':
                    score -= 10
                elif action == 'play':
                    score += 10
                    rank = card[0]
                    score -= rank_order[rank] * 0.5
                    if rank == '2':
                        score -= 2
                    if rank == '1':
                        score -= 3
                elif action == 'try':
                    score += random.uniform(-1, 1)
                if state['another']:
                    score += 0.5
                scores.append(score)
            probs = env.softmax(scores)
            return random.choices(moves, probs)[0]
            '''
            return best_move

    def is_terminal(env,state):
        if not state['bottom_hands'][0]:
                state['winner'] = 0
                return True
        elif not state['bottom_hands'][1]:
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
state = threes_end_game = {
    'name': 'threes',
    'deck': ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD',
             'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS',
             'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC',
             'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH'],
    
    'shuffled_deck': [],
    
    'rank_order': {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15},
    
    'hands': [
        ['7H', '8H'],            # Player 0 - low hand count
        ['6C']                   # Player 1 - obvious move: play 6C (matches top card, and only has 1 card left!)
    ],
    
    'discard_pile': ['2H', '3C', '4D', '5S', '7D', '8D'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0, 'Easy'),
    'winner': None,
    
    'bottom_hands': [
        ['2C', '3H'],            # Player 0
        ['1H']                   # Player 1
    ],
    
    'top_hands': [
        ['5C'],                  # Player 0
        []                       # Player 1 (empty)
    ],
    
    'another': False,
    'played_cards': ['3D', '4D', '5D', '6D'],  # Run of 3-4-5-6 (top card is 6D)
    
    'history': [
        (0, '3D', 'play'),
        (1, '4D', 'play'),
        (0, '5D', 'play'),
        (1, '6D', 'play'),
        (0, ['3D', '4D', '5D', '6D'], 'pickup'),
        (1, '1H', 'play'),
        (0, '7H', 'play'),
    ]
}


#print(genv.determinization(state))
#print(genv.get_reward(genv.determinization(state)))
#print(genv.get_vaild_moves(state))
#print(genv.rollout_policy(genv.get_vaild_moves(state),state))
'''
lst = []
for _ in range(100):
    choice = mtcs(state,genv,0.5,True)
    lst.append(choice)
    print(choice)

counts = lst.count((1, '6C', 'play'))
print(f'Picks Best Move: {counts}%')
'''