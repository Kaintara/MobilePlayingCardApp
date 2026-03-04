#Imports
import copy
from treesearch import m_mtcs, Node
import random
import math

class GameEnvironmentT:
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
        threes = copy.deepcopy(state) #Makes a copy of the game state
        public_cards = []
        #Checks all hands that are public to the AI and adds the visable cards to the public_cards list
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
        unknown_cards = [c for c in threes['deck'] if c not in public_cards] #Compiles a list of all the cards the AI is not aware of
        if not threes["history"]: #Checks if there is any previous game history
            #Randomly assigns cards to the unknown hands if there is no history available
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
            if threes['history'][-1][2] == 'pickup' and threes['history'][-1][0] == 0: #Checks if most recent move was a pickup by the opposing player
                for card in threes['history'][-1][1]: #Iterates through picked up cards in history and adds them to the opposing player's determined hand
                    if card in unknown_cards:
                        Player_hand.append(card)
            threes['bottom_hands'][1] = []
            #Randomly determines the rest of the unknown cards to the opposing player, to both player's bottom hands and lastly the deck
            for _ in range(len(state['bottom_hands'][1])):
                #if unknown_cards:
                    card1 = unknown_cards.pop()
                    threes["bottom_hands"][1].append(card1)
            threes['bottom_hands'][0] = []
            for _ in range(len(state['bottom_hands'][0])):
                #if unknown_cards:
                    card2 = unknown_cards.pop()
                    threes["bottom_hands"][0].append(card2)
            for _ in range(len(threes['hands'][0]) - len(Player_hand)):
                #if unknown_cards:
                    Player_hand.append(unknown_cards.pop())
            threes['shuffled_deck'] = unknown_cards
            threes['hands'][0] = Player_hand
        return threes
    
    def sort_cards(env,state): #Uses the rank_order dictionary as a key to sort each players hand
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        state['hands'][0].sort(key=(lambda a : rank_order[a[0]]))
        state['hands'][1].sort(key=(lambda a : rank_order[a[0]]))
    
    def get_vaild_moves(env,state):
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        player = state['turn']
        Moves = []
        Valid_Cards = []
        #Checks which hand the player is currently using
        if state['hands'][player]:
            Hand = state['hands'][player]
        elif state['top_hands'][player]:
            Hand = state['top_hands'][player]
        else: #If the unseen hand is being used only vaild moves are trying those cards so these moves are returned
            Hand = state['bottom_hands'][player]
            for card in Hand:
                Moves.append((player,card,"try"))
            return Moves
        if state['played_cards']: #Checks if there are cards in the middle that can be picked up
            Top_card = state['played_cards'][-1] #Finds the most recently played card which the player needs to beat
            if Top_card[0] == '2': #Checks if the top card is 2 if it is the player can beat it with any card so returns a play move for every card
                for card in Hand:
                    Moves.append((player,card,"play"))
                return Moves
            for card in Hand: #Iterates through each card
                if card[0] == Top_card[0]: #Checks if the top card has the same rank as the card in hand, if so then that card is added to the vaild card list
                    Valid_Cards.append(card)
            temp_hand = Hand[:] + [Top_card]
            temp_hand.sort(key=lambda a: rank_order[a[0]])
            idx = temp_hand.index(Top_card) + 1
            if idx < len(temp_hand):
                Valid_Cards += temp_hand[idx:]
            for card in Valid_Cards: #Iterates through all vaild cards and adds a play move for each card
                if card not in [m[1] for m in Moves]: #Checks the cards' rank has not already been added to the vaild moves
                    Moves.append((player,card,"play"))
            if not Moves:
                Moves.append((player,list(state['played_cards']),"pickup")) #Adds the pickup move to the list of vaild moves
        else:
            for card in Hand:
                Moves.append((player,card,"play"))
        return Moves
    
    def apply_moves(env,og_state,move):
        state = copy.deepcopy(og_state) #Makes a copy of the game state
        if not move: #Checks if the move exists 
            if env.is_terminal(state): #Checks if the game is over
                return state
            state['turn'] = env.next_valid_player(state) #Changes turn to the next vaild player
            return state
        rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
        cards = move[1]
        if isinstance(cards, list): #Checks if the second part of the move tuple contains a list of cards or not
            card_list = list(cards) #Make a copy of the list
        else:
           card_list = cards
        state["history"].append((move[0], card_list, move[2])) #Adds move to history
        player = move[0]
        if state["played_cards"]: #Checks if there are cards in the middle that can be picked up
            Top_card = state["played_cards"][-1]
        else:
            Top_card = '2H' #If no card in the middle sets to 2H to use to compare so that all moves are vaild
        if move[2] == "try":
            if Top_card[0] == '2':
                return env.apply_moves(state, (player,move[1],"play"))
            else: #Checks that the attempted card is higher then previously played card if not the player pickups otherwise the move is applied
                Card_rank = rank_order[move[1][0]]
                if Card_rank >= rank_order[Top_card[0]]:
                    return env.apply_moves(state, (player,move[1],"play"))
                else:
                    return env.apply_moves(state, (player, list(state["played_cards"]), "pickup"))
        elif move[2] == "play":
            played_rank = move[1][0]
            Hands = [state['hands'][player],state["bottom_hands"][player],state["top_hands"][player]]
            if played_rank in ('1','2'): #If the card is a 10 or a 2 only the card selected is played and removed from the player's hand
                state["played_cards"].append(move[1])
                for cards in Hands:
                    if move[1] in cards:
                        cards.remove(move[1])
            else:
                played_now = []
                Hand = []
                #Iterates through Hands to find which hand is being used
                if state['hands'][player]:
                    Hand = state['hands'][player]
                elif state['top_hands'][player]:
                    Hand = state['top_hands'][player]
                elif state['bottom_hands'][player]:
                    Hand = state['bottom_hands'][player]
                else:
                    Hand = []
                for card in Hand[:]: #Plays all cards with the same rank as the one selected and removes them from the players hand
                    if card[0] == played_rank:
                        Hand.remove(card)
                        state["played_cards"].append(card)
                        played_now.append(card)
                state['history'][-1] = (player,played_now,'play') #Updates the history such that all played cards are reflected in it
            four = False
            if len(state["played_cards"]) > 3: #Checks if four of the same rank has been placed
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
            if four == True or move[1][0] == '1': #If four of the same cards or a 10 is placed the cards in the middle are 'burnt' - put into the discard pile and the player gets another turn
                state['discard_pile'] += state["played_cards"]
                state["played_cards"] = []
                state['another'] = True
            if state['shuffled_deck'] and state['hands'][player]: #Adds cards to the player's hand such that they have at least three cards until the deck is gone.
                while state['shuffled_deck']:
                    while len(state['hands'][player]) < 3 and state['shuffled_deck']:
                        card = state['shuffled_deck'].pop()
                        state['hands'][player].append(card)
                    break
        elif move[2] == "pickup": #Gives all the cards that have been played to the player which needs to pick up
             if state["played_cards"]:
                played_cards = list(state["played_cards"])
                for card in played_cards:
                    if card not in state['hands'][player]:
                        state['hands'][player].append(card)
             state["played_cards"] = []
        if env.is_terminal(state): #Checks if the game is over
            return state
        else:
            if state['another'] == True: #Checks if the player gets another turn and returns the player if they do
                state['another'] = False #Sets it so the player doesn't get another turn next turn
            else: #Changes player's turn from 1 to 0 or 0 to 1
                if state['turn'] == 1:
                    state['turn'] = 0
                else:
                    state['turn'] = 1
        return state
    
    def get_reward(env,state):
        if env.is_terminal(state): #Checks if the game is over
            return 100 if state['winner'] == 1 else -100 #Returns 100 if the AI wins otherwise -100
        #Calculates how many cards the players has left
        cards_left = len(state['hands'][1]) + len(state['top_hands'][1]) + len(state['bottom_hands'][1]) 
        cards_left2 = len(state['hands'][0]) + len(state['top_hands'][0]) + len(state['bottom_hands'][0])
        if state['turn'] == 0: #Checks if it is the AI's turn or not
            return cards_left2 #Returns postive if it is not the AI's turn
        return -cards_left #Returns negative if it is the AI's turn
    
    def rollout_policy(env,moves,state):
        if len(moves) == 1: #Checks if there is more than one move available 
            return moves[0]
        else:
            rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15}
            best_move = moves[0]
            for move in moves: #Iterates through each move 
                player, card, action = move
                if action == 'pickup': #Checks if the move is a pickup one is so skips over the pickup move
                    continue 
                elif action == 'play': #Checks if the move is a play move
                    rank = card[0]
                    best_move_rank = best_move[1][0]
                    if rank_order[rank] < rank_order[best_move_rank[0]]: #Compares the rank of the stored best move and the current iteration's move, the lowest rank is chosen as the best move
                        best_move = move
            return best_move

    def is_terminal(env,state):
        #Checks if any player has finished their last cards, if they do then they win otherwise False is returned
        if not state['bottom_hands'][0]: 
                state['winner'] = 0
                return True
        elif not state['bottom_hands'][1]:
                state['winner'] = 1
                return True
        return False
    
    def next_valid_player(env,state):
        if env.is_terminal(state): #Checks if the game is over
            return
        else:
            if state['another'] == True: #Checks if the player gets another turn and returns the player if they do
                state['another'] = False #Sets it so the player doesn't get another turn next turn
                return state['turn']
            if state['turn'] == 1: #Changes player's turn from 1 to 0 or 0 to 1
                return 0
            else:
                return 1
            