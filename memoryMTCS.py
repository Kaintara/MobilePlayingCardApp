import copy
import random
from treesearch import m_mtcs
import math

class GameEnvironmentM:
    def __init__(env):
        pass

    def softmax(env,scores, temp=0.7):
        maximum = max(scores) #Returns the highest score within the scores list
        exps = []
        for score in scores: #Iterates through each score
            exps.append(math.exp(math.exp((score - maximum) / temp))) #Calculates exponential vaule for each score
        total = sum(exps) #Sums all exponentials
        return [e / total for e in exps] #Normalises the values into probabilites that sum to 1 
    
    def convert_move(env,move,state):
        y = int(move[2][0])
        x = int(move[2][1])
        card = state['card_array'][y][x]
        print(state['card_array'][y][x])
        if not card:
            return random.choice(env.get_vaild_moves(state))
        else:
            if move[2] != state['card_array'][y][x]: #Checks if the move is vaild
                vaild_move = ('pick',1,(y,x,state['card_array'][y][x])) #Updates the choosen move so that the card is selected from the actual game state, such that it is vaild
                return vaild_move
            else:
                return move

    def determinization(env,state):
        memory = copy.deepcopy(state) #Makes a copy of the game state
        memory['deck'] = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory['card_array'] = [['' for _ in range(6)] for _ in range(9)]
        for y, row in enumerate(state.get('card_array', [])):
           for x, card in enumerate(row):
              if not card:
                    memory['card_array'][y][x] = 'Empty_Space'
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
                    # Clear matched cards from board so they can't be picked again
                    memory['card_array'][first[0]][first[1]] = None
                    memory['card_array'][second[0]][second[1]] = None
                    # Also remove from deck
                    if first[2] in memory['deck']:
                        memory['deck'].remove(first[2])
                    if second[2] in memory['deck']:
                       memory['deck'].remove(second[2])
        random.shuffle(memory['deck'])
        for _ in range(5):
            x = random.randint(0,5)
            y = random.randint(0,8)
            if not memory['card_array'][y][x] or memory['card_array'][y][x] == 'Empty_Space':
              if memory['deck']:
                memory['card_array'][y][x] = memory['deck'].pop()
        return memory
 
    def get_vaild_moves(env,state):
        player = state['turn']
        Moves = []
        for y, row in enumerate(state['card_array']):
            for x, card in enumerate(row):
                if card and card != 'Empty_Space':
                    if card == state.get('first_selected_card')[2]:
                            continue
                    else:
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
        if env.is_terminal(state):
            return 10 if state['winner'] == 1 else -10
        reward = len(state['hands'][1]) * 0.5
        return reward
    
    def rollout_policy(env,moves,state):
        scores = []
        first_pick = state.get('first_selected_card')
        for move in moves:
            action, player, cardpos = move
            score = 0.0
            if state['selected_first_card'] and first_pick != ('y','x','card'):
                if first_pick == cardpos:
                    score -= 10
                elif first_pick[2][0] == cardpos[2][0]:
                    suit1 = cardpos[2][1]
                    suit2 = first_pick[2][1]
                    is_joker_pair = (first_pick[2] in ('BJ','RJ') and cardpos[2] in ('BJ','RJ'))
                    same_color = (suit1 in ['D','H'] and suit2 in ['D','H']) or (suit1 in ['C','S'] and suit2 in ['C','S'])
                    if is_joker_pair or same_color:
                        score += 10
            else:
                if move in state['history']:
                    score -= 10
            scores.append(score)
        probs = env.softmax(scores)
        return random.choices(moves, probs)[0]

    def cards_undiscovered(env,state):
        count = 0
        memory = copy.deepcopy(state)
        memory['deck'] = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory['card_array'] = [['' for _ in range(6)] for _ in range(9)]
        for y, row in enumerate(state.get('card_array', [])):
           for x, card in enumerate(row):
              if not card:
                    memory['card_array'][y][x] = 'Empty_Space'
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



state = memory_early_game = {
    'name': "memory",
    
    'deck': [
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
        "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"
    ],
    
    'shuffled_deck': [],
    
    'hands': [
        ["8H", "9C"],     # Player 0 has 2 cards (1 match)
        ["7D", "JS"]      # Player 1 has 2 cards (1 match)
    ],
    
    'first_selected_card': ('y','x','card'),
    'second_selected_card': ('y','x','card'),
    'selected_first_card': False,
    
    # 9×6 board - Player 1 can see two matching cards (7H and 7C)
    'card_array': [
        ['',    '',    '9H',  '9C',  '',    'KS'],
        ['1D',  'QS',  '6H',  '',    'KD',  'JC'],
        ['3S',  '7S',  '',    'AD',  '8C',  '9S'],
        ['5S',  '1H',  'AS',  'RJ',  '8S',  ''],
        ['BJ',  '4H',  '',    'QH',  '3D',  'AC'],
        ['JD',  '',    '7H',  '4D',  'KC',  ''],
        ['QC',  '',    'AH',  '5H',  '5D',  ''],
        ['6S',  'JH',  '3C',  '7D',  '',    '6D'],
        ['6C',  '4C',  '2C',  '',    '9D',  '7C']  # 7C at (8,5)
    ],
    
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (-1, ""),
    'winner': None,
    
    'history': [
        # Player 0 revealed two non-matching cards
        ('pick', 1, (8,4,'9D')),
        ('pick', 1, (8,4,'9D')),
        ('Missed', 1, (0,2,'9H'), (2,5,'9S')),
        ('pick', 0, (0,2,'9H')),
        ('pick', 0, (0,3,'9C')),
        ('Missed', 0, (0,2,'9H'), (0,3,'9C'))     
    ]
}


#genv = GameEnvironmentM()
#move = genv.rollout_policy(genv.get_vaild_moves(genv.determinization(state)),genv.determinization(state))
#print(genv.convert_move(move,state))
#print(genv.determinization(state)
#print(genv.get_reward(genv.determinization(state)))
#print(genv.convert_move(((0,2,'4H')),state))

#move1= mtcs(state,genv,5,True)
#print(move1)
#state = genv.apply_moves(state,genv.convert_move(move1,state))
#print(state)
#move1= mtcs(state,genv,1,True)
#print(move1)


