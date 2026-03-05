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
        card = state['card_array'][y][x] #Returns the card at the position of the move from the game state
        if not card: #Checks if the card exists, if not returns a random vaild move to avoid errors
            return random.choice(env.get_vaild_moves(state))
        else:
            if move[2] != state['card_array'][y][x]: #Checks if the move is vaild
                vaild_move = ('pick',1,(y,x,state['card_array'][y][x])) #Updates the choosen move so that the card is selected from the actual game state, such that it is vaild
                if vaild_move not in env.get_vaild_moves(state): #Checks that the move is vaild, if not returns a random vaild move
                    return random.choice(env.get_vaild_moves(state))
                return vaild_move
            else:
                return move

    def determinization(env,state):
        memory = copy.deepcopy(state) #Makes a copy of the game state
        memory['deck'] = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory['card_array'] = [['' for _ in range(6)] for _ in range(9)] #Makes an empty card array to fill in with the known cards from the game state and history
        #Iterates through the card array in the game state and fills cards already removed from card array with "Empty_Space" 
        for y, row in enumerate(state.get('card_array', [])):
           for x, card in enumerate(row):
              if not card:
                    memory['card_array'][y][x] = 'Empty_Space'
        if memory['history']: #Checks if there is any history to iterate through
            for move in memory['history']: #Interates through the history and fills in the card array with any cards that have been revealed and not removed from the game
                if move[0] == 'Missed':
                    first = move[2]
                    second = move[3]
                    #Add revealed cards back into card array
                    memory['card_array'][first[0]][first[1]] = first[2]
                    memory['card_array'][second[0]][second[1]] = second[2]
                    # Remove from deck
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
        for _ in range(5): #Randomly fills in some of the unknown spaces in the card array with cards from the deck to allow for some exploration using MCTS
            x = random.randint(0,5)
            y = random.randint(0,8)
            if not memory['card_array'][y][x] or memory['card_array'][y][x] == 'Empty_Space':
              if memory['deck']:
                memory['card_array'][y][x] = memory['deck'].pop()
        return memory
 
    def get_vaild_moves(env,state):
        player = state['turn']
        Moves = []
        for y, row in enumerate(state['card_array']): #Iterates through the card array in the game state 
            for x, card in enumerate(row):
                if card and card != 'Empty_Space': #Checks if there is a card at the position and that it is not an empty space
                    if card == state.get('first_selected_card')[2]: #Checks if the card hasn't already been selected as the first card and is not vaild
                            continue
                    else:
                        Moves.append(("pick",player,(y,x,card))) #Adds the move to pick the card at the position to the list of vaild moves
        return Moves
    
    def apply_moves(env,og_state,move):
        state = copy.deepcopy(og_state) #Makes a copy of the game state to apply the move to prevent modifying the original game state
        if not move: #Checks if there is a move to apply to prevent errors
            if env.is_terminal(state): #Checks if the game is over
                return state
            state['turn'] = env.next_valid_player(state) #If there is no move, simply pass the turn to the next player and return the updated game state
            return state
        player = state['turn']
        state['history'].append(move) #Adds the move to the game history
        if state['selected_first_card'] == False: #Checks if the first card has already been selected, if not selects the card from the move as the first card
            state['first_selected_card'] = move[2]
            state['selected_first_card'] = True
        else:
            #Sets card from move as second selected card and checks if the two selected cards are a match
            state['second_selected_card'] = move[2]
            state['selected_first_card'] = False
            first = state['first_selected_card']
            second = state['second_selected_card']
            if first[2][0] == second[2][0]: #Checks if the two selected cards have the same rank
                suit1 = first[2][1]
                suit2 = second[2][1]
                is_joker_pair = (first[2] in ('BJ','RJ') and second[2] in ('BJ','RJ'))
                same_color = (suit1 in ['D','H'] and suit2 in ['D','H']) or (suit1 in ['C','S'] and suit2 in ['C','S']) #Checks if the two selected cards have the same color
                if is_joker_pair or same_color: #Checks if cards are a match
                    #Remove matched cards from card array
                    state['card_array'][first[0]][first[1]] = None
                    state['card_array'][second[0]][second[1]] = None
                    #Adds matched cards to the player's hand and updates the game history
                    state["history"].append(("Matched",player,first,second))
                    state['hands'][player].append(first[2])
                    state['hands'][player].append(second[2])
                else: #Adds the missed move to play history and update player turn
                    state["history"].append(("Missed",player,first,second))
                    state['turn'] = 1 - state['turn']
            else: #Adds the missed move to play history and update player turn
                 state["history"].append(("Missed",player,first,second))
                 state['turn'] = 1 - state['turn']
            #Resets the selected cards
            state['first_selected_card'] = ('y','x','card')
            state['second_selected_card'] = ('y','x','card')
        return state
    
    def get_reward(env,state):
        if env.is_terminal(state): #Checks if the game is over and returns a reward of 10 for winning and -10 for losing
            return 10 if state['winner'] == 1 else -10
        reward = len(state['hands'][1]) * 0.5 #Adds a small reward for each card in the player's hand to encourage collecting cards
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
        for y,row in enumerate(state['card_array']): #Iterates through the card array in the game state to check if there are any cards left
            for x,card in enumerate(row):
                if card:
                    return False
        if len(state['hands'][1]) > len(state['hands'][0]): #Selects the winner based on who has more cards in their hand at the end of the game
            state['winner'] = 1
        else:
            state['winner'] = 0
        return True
    
    def next_valid_player(env,state): #Determines the next player to play
        player = state['turn'] 
        if env.is_terminal(state): #Checks if the game is over
            return
        else:
            return 1 - player


