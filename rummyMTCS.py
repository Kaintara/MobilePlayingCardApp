import copy
from treesearch import m_mtcs
import random
import math

class GameEnvironmentR:
    def __init__(env):
        pass
    
    def softmax(env,scores, temp=0.7):
        maximum = max(scores) #Returns the highest score within the scores list
        exps = []
        for score in scores: #Iterates through each score
            exps.append(math.exp(math.exp((score - maximum) / temp))) #Calculates exponential vaule for each score
        total = sum(exps) #Sums all exponentials
        return [e / total for e in exps] #Normalises the values into probabilites that sum to 1 

    def determinization(env,state):
        rummy = copy.deepcopy(state) #Makes a copy of the game state
        public_cards = []
        if rummy['hands']:
            if rummy['hands'][1]:
                for card in rummy['hands'][1]:
                    public_cards.append(card)
        if rummy['discard_pile']:
            for card in rummy['discard_pile']:
                public_cards.append(card)
        unknown_cards = rummy['deck']
        for card in unknown_cards:
            if card in public_cards:
                unknown_cards.remove(card)
        if not rummy["history"]:
            rummy['hands'][0] = []
            for _ in range(0,7):
                card = unknown_cards.pop()
                rummy['hands'][0].append(card)
        else:
            Player_hand = []
            for move in rummy['history']:
                if move[0] == 0 and move[1] != 'deck' and move[1] not in rummy['discard_pile'] and move[2] == 'draw':
                    Player_hand.append(move[1])
            while 7 != len(Player_hand):
                Player_hand.append(unknown_cards.pop())
            rummy['hands'][0] = Player_hand 
        rummy['shuffled_deck'] = unknown_cards
        return rummy
    
    def find_run(rummy,cards):
        rank_order = {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}
        runs = []
        if len(cards) >= 3:
            previous_value = rank_order[cards[0][0]]
            run_length = 0
            starting_index = ''
            for card in cards:
                value = rank_order[card[0]]
                if run_length == 0:
                        starting_index = cards.index(card)
                if value == previous_value:
                    run_length += 1
                elif value == (previous_value + 1):
                    run_length += 1
                    previous_value = value
                else:
                    run_length = 1
                    starting_index = cards.index(card)
                    previous_value = value
                if run_length == 3:
                    runs.append((3,starting_index))
                elif run_length == 4:
                    del runs[-1]
                    runs.append((4,starting_index))
            if runs:
                run_cards = []
                for run in runs:
                    run_cards += cards[run[1]:(run[0]+run[1])]
                return run_cards
        
    def find_set(rummy,cards):
        sets = []
        if len(cards) >= 3:
            set_length = 0
            starting_index = 0
            previous_rank = cards[0][0]
            for card in cards:
                if card[0] == previous_rank:
                    set_length += 1
                    previous_rank = card[0]
                else:
                    set_length = 1
                    starting_index = cards.index(card)
                    previous_rank = card[0]
                if set_length == 3:
                    sets.append((3,starting_index))
                elif set_length == 4:
                    del sets[-1]
                    sets.append((4,starting_index))
            if sets:
                set_cards = []
                for set in sets:
                    set_cards += cards[set[1]:(set[0]+set[1])]
                return set_cards
    
    def sort_cards(env,state,player):
        rank_order = {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}
        Sorted_hand = []
        Runs = []
        Sets = []
        Temp_hand = state['hands'][player][:]
        Temp_hand.sort(key=(lambda a : rank_order[a[0]]))
        Hearts = []
        Clubs = []
        Spades = []
        Diamonds = []
        for card in Temp_hand:
            if card.endswith('H'):
               Hearts.append(card)
            elif card.endswith('C'):
               Clubs.append(card)
            elif card.endswith('S'):
               Spades.append(card)
            elif card.endswith('D'):
               Diamonds.append(card)
        Suits = [Hearts,Clubs,Spades,Diamonds]
        for suit in Suits:
            if env.find_run(suit):
                Runs = env.find_run(suit)
                Sorted_hand += Runs
                for card in Runs:
                    if card in Temp_hand:
                        Temp_hand.remove(card)
        if env.find_set(Temp_hand):
            Sets = env.find_set(Temp_hand)
            Sorted_hand += Sets
            for card in Sets:
                if card in Temp_hand:
                        Temp_hand.remove(card)
        if not Temp_hand:
            return "GameOver"
        else:
            Temp_hand.sort(key=(lambda a : rank_order[a[0]]))
            Sorted_hand += Temp_hand
            state['hands'][player] = Sorted_hand
            return None

    def get_vaild_moves(env,state):
        player = state['turn']
        Moves = []
        Hand_len = len(state['hands'][player])
        if Hand_len == 7:
            if state['shuffled_deck']:
                Moves.append((player,"deck","draw"))
            if state['discard_pile']:
                Moves.append((player,state['discard_pile'][-1],"draw"))
            return Moves
        elif Hand_len == 8:
            for card in state['hands'][player]:
                Moves.append((player,card,"discard"))
            return Moves
        else:
            return Moves
    
    
    def apply_moves(env,og_state,move):
        state = copy.deepcopy(og_state)
        if not move:
            if env.is_terminal(state):
                return state
            state['turn'] = env.next_valid_player(state)
            return state
        player = state['turn']
        state['history'].append(move)
        if move[2] == "draw":
            if move[1] == "deck":
                Top_card = state['shuffled_deck'].pop()
                state['hands'][player].append(Top_card)
            else:
                Top_card = state['discard_pile'].pop()
                state['hands'][player].append(Top_card)
        elif move[2] == "discard":
            state['discard_pile'].append(move[1])
            state['hands'][player].remove(move[1])
            state['turn'] = 1 - state['turn']
        return state
    
    def get_reward(env,state):
        player = state['turn']
        if env.is_terminal(state):
            return 10 if state['winner'] == 1 else -10
        return 0
    
    def card_helps_meld(env, hand_, selected_card):
        rank_order = {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}
        Sorted_hand = []
        Runs = []
        Sets = []
        hand = hand_[:]
        hand.sort(key=(lambda a : rank_order[a[0]]))
        Hearts = []
        Clubs = []
        Spades = []
        Diamonds = []
        for card in hand:
            if card.endswith('H'):
               Hearts.append(card)
            elif card.endswith('C'):
               Clubs.append(card)
            elif card.endswith('S'):
               Spades.append(card)
            elif card.endswith('D'):
               Diamonds.append(card)
        Suits = [Hearts,Clubs,Spades,Diamonds]
        for suit in Suits:
            if env.find_run(suit):
                Runs = env.find_run(suit)
                Sorted_hand += Runs
                for card in Runs:
                    if card in hand:
                        hand.remove(card)
        if env.find_set(hand):
            Sets = env.find_set(hand)
            Sorted_hand += Sets
            for card in Sets:
                if card in hand:
                        hand.remove(card)
        if not Sorted_hand:
            rank_order = {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}
            rank = selected_card[0]
            suit = selected_card[1]
            value = rank_order[rank]
            same_rank = sum(1 for c in hand_ if c[0] == rank)
            if same_rank > 1:
                return True
            suit_cards = [c for c in hand_ if c[1] == suit]
            values = sorted(rank_order[c[0]] for c in suit_cards)
            return (value - 1 in values) or (value + 1 in values)
        elif not hand:
            if selected_card == Sorted_hand[-1]:
                return False
            return True
        else:
            if selected_card in Sorted_hand:
                return True
            return False
    
    def rollout_policy(env, moves, state):
        scored_moves = []
        for move in moves:
            player, card, action = move
            score = 0.0
            if action == 'draw':
                if card != 'deck' and env.card_helps_meld(state['hands'][player], card):
                    score += 10
                elif card == 'deck':
                    score += random.uniform(-2, 3)
            elif action == 'discard':
                if env.card_helps_meld(state['hands'][player], card):
                    score -= 10
                else:
                    score += 10
            scored_moves.append((score, move))
        scores = [s for s, _ in scored_moves]
        moves = [m for _, m in scored_moves]
        probs = env.softmax(scores, temp=0.2)
        return random.choices(moves, probs)[0]

    def is_terminal(env,state):
        if env.sort_cards(state,1) == 'GameOver':
            state['winner'] = 1
            return True
        elif env.sort_cards(state,0) == 'GameOver':
            state['winner'] = 0
            return True
        return False
    
    def next_valid_player(env,state):
        player = state['turn'] 
        if env.is_terminal(state):
            return
        else:
            if state['history']:
                if state['history'][-1][0] == player and state['history'][-1][2] == 'draw':
                    return player
                else:
                    if player == 1:
                        return 0
                    else:
                        return 1
            else:
                if player == 1:
                    return 0
                else:
                    return 1

genv = GameEnvironmentR()



state = rummy_mid_game = {
    'name': 'rummy',
    'deck': ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
             "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
             "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
             "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
    
    'shuffled_deck': ['4C','AD','8D','AS','7C','KC','2S','7D','QH','3C','5S','AC','6H'],
    
    'value_map': {'A':1,'K':13,'Q':12,'J':11,'1':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2},
    
    'hands': [
        # PLAYER 0 (about to draw: has 7 cards)
        ['4H','5H','4D','2D','2S','8C','4C'],
        
        # PLAYER 1 (in discard phase: has 8 cards - obvious best move: discard QH!)
        ['3H','6S','6D','6C','9H','QS','1S','KS']
    ],
    
    'discard_pile': ['5C','7D','2C'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0,'Easy'),
    'winner': None,
    
    'history': [
        (1,'KC','discard'),
        (0,'7D','draw'),
        (0,'7D','discard'),
        (1,'2C','draw'),
        (0,'4C','draw'),
    ]
}

#print(genv.determinization(state))
#print(genv.get_reward(genv.determinization(state)))

#print(mtcs(state,genv,0.5))
#print(genv.rollout_policy(genv.get_vaild_moves(state),state))
'''
lst = []
for _ in range(100):
    choice = m_mtcs(state,genv,0.5)
    lst.append(choice)
    print(choice)
    print(genv.card_helps_meld(state['hands'][1],choice[1]))

counts = lst.count((1, '9H', 'discard'))
counts2 = lst.count((1, '3H', 'discard'))
print(f'Picks Best Move: {counts+counts2}%')
'''