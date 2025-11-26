import copy
import random
from treesearch import mtcs

class GameEnvironment:
    def __init__(env):
        pass

    def determinization(env,state):
        memory = copy.deepcopy(state)
        memory['deck'] = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory['card_array'] = [['' for _ in range(6)] for _ in range(9)]
        for y, row in enumerate(state.get('card_array', [])):
           for x, card in enumerate(row):
              if not card:
                    memory['card_array'][y][x] = 'Blank'
        if memory['history']:
            for move in memory['history']:
                if move[0] == 'Missed':
                    first = move[2]
                    second = move[3]
                    memory['card_array'][first[0]][first[1]] = first[2]
                    memory['card_array'][second[0]][second[1]] = second[2]
                    if first[2] in memory['deck']:
                        memory['deck'].remove(first[2])
                    if second[2] in memory['deck']:
                       memory['deck'].remove(second[2])
                elif move[0] == 'Matched':
                    first = move[2]
                    second = move[3]
                    if first[2] in memory['deck']:
                        memory['deck'].remove(first[2])
                    if second[2] in memory['deck']:
                       memory['deck'].remove(second[2])
        random.shuffle(memory['deck'])
        for y in range(9):
            for x in range(6):
                if not memory['card_array'][y][x]:
                    if not memory['deck']:
                        raise ValueError("Deck exhausted while determinizing")
                    memory['card_array'][y][x] = memory['deck'].pop()
        return memory
 
    def get_vaild_moves(env,state):
        player = state['turn']
        Moves = []
        for y, row in enumerate(state['card_array']):
            for x, card in enumerate(row):
                if card and card != 'Blank':
                    Moves.append(("pick",player,(y,x,card)))
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
        if state['selected_first_card'] == False:
            state['first_selected_card'] = move[2]
            state['selected_first_card'] = True
        else:
            state['second_selected_card'] = move[2]
            state['selected_first_card'] = False
            first = state['first_selected_card']
            second = state['second_selected_card']
            if first[2][0] == second[2][0]:
                suit1 = first[2][1]
                suit2 = second[2][1]
                is_joker_pair = (first[2] in ('BJ','RJ') and second[2] in ('BJ','RJ'))
                same_color = (suit1 in ['D','H'] and suit2 in ['D','H']) or (suit1 in ['C','S'] and suit2 in ['C','S'])
                if is_joker_pair or same_color:
                    state['card_array'][first[0]][first[1]] = None
                    state['card_array'][second[0]][second[1]] = None
                    state["history"].append(("Matched",player,first,second))
                    state['hands'][player].append(first[2])
                    state['hands'][player].append(second[2])
                else:
                    state["history"].append(("Missed",player,first,second))
                    state['turn'] = 1 - state['turn']
            else:
                    state["history"].append(("Missed",player,first,second))
                    state['turn'] = 1 - state['turn']
            state['first_selected_card'] = ('y','x','card')
            state['second_selected_card'] = ('y','x','card')
        return state
    
    def get_reward(env,state):
        player = state['turn']
        if env.is_terminal(state):
            return 1000 if state['winner'] == player else -1000
        reward = len(state['hands'][1]) * 2
        return reward + env.cards_undiscovered(state)
    
    def cards_undiscovered(env,state):
        count = 0
        memory = copy.deepcopy(state)
        memory['deck'] = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory['card_array'] = [['' for _ in range(6)] for _ in range(9)]
        for y, row in enumerate(state.get('card_array', [])):
           for x, card in enumerate(row):
              if not card:
                    memory['card_array'][y][x] = 'Blank'
        if memory['history']:
            for move in memory['history']:
                if move[0] == 'Missed':
                    print(move)
                    first = move[2]
                    second = move[3]
                    memory['card_array'][first[0]][first[1]] = first[2]
                    memory['card_array'][second[0]][second[1]] = second[2]
                    if first[2] in memory['deck']:
                        memory['deck'].remove(first[2])
                    if second[2] in memory['deck']:
                       memory['deck'].remove(second[2])
                elif move[0] == 'Matched':
                    first = move[2]
                    second = move[3]
                    if first[2] in memory['deck']:
                        memory['deck'].remove(first[2])
                    if second[2] in memory['deck']:
                       memory['deck'].remove(second[2])
        random.shuffle(memory['deck'])
        for y in range(9):
            for x in range(6):
                if not memory['card_array'][y][x]:
                    count += -1
        return count/2

    def is_terminal(env,state):
        for y,row in enumerate(state['card_array']):
            for x,card in enumerate(row):
                if card:
                    return False
        if len(state['hands'][1]) > len(state['hands'][0]):
            state['winner'] = 1
        else:
            state['winner'] = 0
        return True
    
    def next_valid_player(env,state):
        player = state['turn'] 
        if env.is_terminal(state):
            return
        else:
            return 1 - player

genv = GameEnvironment()

state = {
    'name': "memory",

    'deck': [
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
        "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"
    ],

    'shuffled_deck': [],

    'hands': [
        ["8H", "9C"],     # Player 0 has 2 cards
        ["7D", "JS", "KS"]  # Player 1 has 3 cards
    ],

    'first_selected_card': ('y','x','card'),
    'second_selected_card': ('y','x','card'),
    'selected_first_card': False,

    # 9×6 board — '' means unknown/unflipped (your environment REQUIRES this format)
    'card_array': [
        ['7C','',  '9H','9C','',  'KS'],
        ['1D','QS','6H','',  'KD','JC'],
        ['3S','7S','',  'AD','8C','9S'],
        ['5S','1H','AS','RJ','8S',''],
        ['BJ','4H','',  'QH','3D','AC'],
        ['JD','',  '1S','4D','KC',''],
        ['QC','',  'AH','5H','5D',''],
        ['6S','JH','3C','7D','',  '6D'],
        ['6C','4C','2C','',  '9D','3H']
    ],

    'turn': 0,
    'time_elapsed': 0,
    'difficulty': (-1, ""),

    'winner': None,

    'history': [
        # Player 0 reveals 7C and KS → miss
        ('pick', 0, (0,0,'7C')),
        ('pick', 0, (0,5,'KS')),
        ('Missed', 0, (0,0,'7C'), (0,5,'KS')),

        # Player 1 reveals BJ and RJ → match
        ('pick', 1, (4,0,'BJ')),
        ('pick', 1, (3,3,'RJ')),
        ('Matched', 1, (4,0,'BJ'), (3,3,'RJ')),

        # Player 0 reveals 2C and JD → miss
        ('pick', 0, (8,2,'2C')),
        ('pick', 0, (5,0,'JD')),
        ('Missed', 0, (8,2,'2C'), (5,0,'JD'))
    ]
}

print(genv.determinization(state))
print(genv.get_reward(genv.determinization(state)))

print(mtcs(state,genv,50))