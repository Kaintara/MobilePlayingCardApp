import random
from ui import Achievement_Dialog, Reward_Dialog, MDApp, SoundLoader
from kivy.clock import Clock

class Game: #Main Game Class
    def __init__(game, name, rank_order,state):
        game.name = name #Sets an id for each game
        game.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"]
        game.shuffled_deck = []
        game.rank_order = rank_order
        game.hands = [[],[]]
        game.discard_pile = []
        game.selected_card = ''
        game.turn = 0
        game.state = state
        game.time_elapsed = 0
        game.difficulty = (0,"Easy")
        game.winner = None
        game.timer_event = None
        #Loads in sounds that to be accessed later
        game.win_noise = SoundLoader.load('assets/sound/win_noise.mp3') 
        game.lose_noise = SoundLoader.load('assets/sound/lose_noise.mp3')
        game.achievement_noise = SoundLoader.load('assets/sound/iykyk.mp3')

    def shuffle_cards(game):
        shuffled_deck = game.deck[:] #Makes a copy of the deck
        random.shuffle(shuffled_deck) #Shuffles the deck
        game.shuffled_deck = shuffled_deck

    def unlocked_achievements(game, app, savedata): #Checks for any unlocked achievements and returns a list of them
        unlocked = []
        already_unlocked = {a[0] for a in app.unlocked_achievements} #Creates a dictionary of already unlocked achievements
        for id, name, desc, condition in app.all_achievements: #Iterates through each possible achievement
            if id not in already_unlocked and condition(savedata): #Checks achievement condition has been met and it has not already been unlocked
                unlocked.append((id, name, desc, condition)) #Adds achievement to list of unlocked to be returned
                app.unlocked_achievements.append((id, name, desc)) #Adds achievement to list of unlocked to be saved
        return unlocked

    def display_achievements(game,achievement):
        Dialog = Achievement_Dialog(achievement) #Creates an achievement Dialog with achievement passed through
        game.achievement_noise.play() #Plays the achievement noise
        Dialog.open() #Displays the Dialog
        Clock.schedule_once(lambda dt: Dialog.dismiss(), 5) #Schedules an auto close of the dialog after five seconds
    
    def get_reward(game,shop,app,savedata):
        amount_earned = 0
        #Adds five times the game's difficulty to coin total and recorded amount earned
        shop.coin_count += (game.difficulty[0]*5) 
        amount_earned += game.difficulty[0]*5 
        Unlocked_achievement = game.unlocked_achievements(app,savedata) #Saves all unlocked achievements
        total_delay = 0
        if Unlocked_achievement: #Checks if achievements have been unlocked
        #Adds five times the amount of unlocked achievements to coin total and recorded amount earned
            shop.coin_count += 5*len(Unlocked_achievement)
            amount_earned += 5*len(Unlocked_achievement)
            for index, achievement in enumerate(Unlocked_achievement): #Iterates through each all unlocked achievements to calculate delay to display Achievement Dialogs and the reward dialog
                delay = (index+1) * 2
                total_delay += delay
                Clock.schedule_once(lambda dt, achieve=achievement: game.display_achievements(achieve), delay) 
        if game.winner == 0: #Checks if the player won
            Clock.schedule_once(lambda dt: game.win_noise.play(), total_delay) #Plays winner noise with the Reward Dialog
            #Adds 30 plus five times the game's difficulty to coin total and recorded amount earned
            shop.coin_count += (30 + game.difficulty[0]*5)
            amount_earned += (30 + game.difficulty[0]*5)
        else:
            Clock.schedule_once(lambda dt: game.lose_noise.play(), total_delay) #Plays loser noise with the Reward Dialog
            #Adds 10 to coin total and recorded amount earned
            shop.coin_count += 10
            amount_earned += 10
        return (amount_earned, game.winner, total_delay)
    
    def end_game(game, app):
        game.stop_timer()
        #Formats the data of the completed game
        completed_game = {
            'winner': game.winner,
            'history': game.state['history'],
            'difficulty' : game.difficulty,
            'time': game.time_elapsed
        }
        app.previous_games[game.name].append(completed_game) #Adds game to list of completed games
        reward = game.get_reward(app.shop,app,app.save) #Returns the game reward and displays achievements if any have been unlocked
        #Resets all of the game's attributes for the next game
        if game.name == "threes":
            app.threes.shuffled_deck = []
            app.threes.hands = [[],[]]
            app.threes.bottom_hands = [[],[]]
            app.threes.top_hands = [[],[]]
            app.threes.turn = 0
            app.threes.winner = None
            app.threes.state = {"name" : "threes",
                            "deck" : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
                            "shuffled_deck" : [],
                            "rank_order" : {"A": 14,"K": 13,"Q": 12,"J": 11,"1": 16,"9": 9,"8": 8,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 15},
                            "hands" : [[],[]],
                            "discard_pile" : [],
                            "selected_card" : "",
                            "turn" : 0,
                            "time_elapsed" : 0,
                            "difficulty" : [-1,""],
                            "winner" : None,
                            "bottom_hands" : [[],[]],
                            "top_hands" : [[],[]],
                            "another" : False,
                            "played_cards" : [],
                            "history": []}
            app.threes.discard_pile = []
            app.threes.played_cards = []
        elif game.name == "rummy":
            app.rummy.shuffled_deck = []
            app.rummy.hands = [[],[]]
            app.rummy.turn = 0
            app.rummy.winner = None
            app.rummy.state = {"name" : "rummy",
                            "deck" : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
                            "shuffled_deck" : [],
                            "value_map" : {"A": 1,"K": 13,"Q": 12,"J": 11,"1": 10,"9": 9,"8": 8,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 2},
                            "hands" : [[],[]],
                            "discard_pile" : [],
                            "selected_card" : "",
                            "turn" : 0,
                            "time_elapsed" : 0,
                            "difficulty" : [-1,""],
                            "winner" : None,
                            "history": []}
            app.rummy.discard_pile = []
        elif game.name == "memory":
            app.memory.shuffled_deck = []
            app.memory.hands = [[],[]]
            app.memory.turn = 0
            app.memory.winner = None
            app.memory.state = {"name" : "memory",
                            "deck" : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
                            "shuffled_deck" : [],
                            "hands" : [[],[]],
                            "first_selected_card" : ["y","x","card"],
                            "second_selected_card" : ["y","x","card"],
                            "selected_first_card" : False,
                            "card_array" : [["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""]],
                            "turn" : 0,
                            "time_elapsed" : 0,
                            "difficulty" : [-1,""],
                            "winner" : None,
                            "history": []}
            app.memory.card_array = [["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""]]
        app.save.savedata(app, app.threes, app.rummy, app.memory, app.shop) #Saves the entire game's data
        Dialog = Reward_Dialog(reward,app) #Creates a Reward Dialog
        Clock.schedule_once(lambda dt: Dialog.open(), (reward[2]+1)) #Schedules the display of the reward dialog based on returned delay

    def update_timer(game,dt):
        game.time_elapsed += dt #Adds change of time to the time elapsed
        app = MDApp.get_running_app() #Returns the App class
        app.update_timer(game.name) #Updates the UI with the new time
        #print(game.time_elapsed)
        #print("time has been updated")
        
    def start_timer(game):
        if not game.timer_event: #Checks that there is no current timer running already
            print("started timer")
            game.timer_event = Clock.schedule_interval(lambda dt: game.update_timer(dt),1) #Schedules an repeat-event which calls game.update_timer every second

    def stop_timer(game):
        if game.timer_event: #Checks there is a timer currently running
            game.timer_event.cancel() #Cancels the clock schedule interval event
            game.timer_event = None #Removes the timer event so that start_timer acknowledges there is no timer running
        print("timer has been stopped")

class threes(Game): #Threes Game Class
    def __init__(threes, name, rank_order, state):
        super().__init__(name, rank_order, state) #Sets all the attributes as done in the Parent Game Class
        #Adds addtional neccessary attributes
        threes.bottom_hands = [[],[]]
        threes.top_hands = [[],[]]
        threes.played_cards = []
        threes.another = False

    def distribute_cards(threes):
        Hands = [threes.hands,threes.bottom_hands,threes.top_hands] #Makes a list of each type of hand
        for hand in Hands: #Iterates through each hand
            for i in range(0,6): #Iterates from 0 to 5
            #If i is divisable by 2 cards are dealt to first player, else they are dealt to the second player
                if (i % 2) == 0: 
                    card = threes.shuffled_deck.pop()
                    hand[0].append(card)
                else:
                    card = threes.shuffled_deck.pop()
                    hand[1].append(card)

    def sort_cards(threes): #Uses the rank_order dictionary as a key to sort each players main hand
        threes.hands[0].sort(key=(lambda a : threes.rank_order[a[0]]))
        threes.hands[1].sort(key=(lambda a : threes.rank_order[a[0]]))

    def get_valid_moves(threes): #Returns all valid moves
        player = threes.turn 
        Moves = []
        Valid_Cards = []
        #Checks which hand the player is currently using
        if threes.hands[player]:
            Hand = threes.hands[player]
        elif threes.top_hands[player]:
            Hand = threes.top_hands[player]
        else:
            Hand = threes.bottom_hands[player]
            #If the unseen hand is being used only vaild moves are trying those cards so these moves are returned
            for card in Hand:
                Moves.append((player,card,"try"))   
            return Moves
        if threes.played_cards: #Checks if there are cards in the middle that can be picked up
            Moves.append((player,threes.played_cards[:],"pickup")) #Adds the pickup move to the list of vaild moves
            Top_card = threes.played_cards[-1] #Finds the most recently played card which the player needs to beat
            if Top_card[0] == '2': #Checks if the top card is 2 if it is the player can beat it with any card so returns a play move for every card
                for card in Hand:
                    Moves.append((player,card,"play"))
                return Moves
            for card in Hand: #Iterates through each card
                if card[0] == Top_card[0]: #Checks if the top card has the same rank as the card in hand, if so then that card is added to the vaild card list
                    Valid_Cards.append(card)
            temp_hand = Hand[:] + [Top_card]
            temp_hand.sort(key=lambda a: threes.rank_order[a[0]])
            idx = temp_hand.index(Top_card) + 1
            if idx < len(temp_hand):
                Valid_Cards += temp_hand[idx:]
            for card in Valid_Cards: #Iterates through all vaild cards and adds a play move for each card
                if card not in [m[1] for m in Moves]: #Checks the cards' rank has not already been added to the vaild moves
                    Moves.append((player,card,"play"))
        else:
            #As there is no card to beat all moves are vaild so iterates through player's hand and adds a play move for each card
            for card in Hand:
                Moves.append((player,card,"play"))
        return Moves
    
    def is_game_over(threes):
        Player_hands = []
        Ai_hands = []
        #Adds cards to the respective player's hand
        Player_hands += threes.hands[0]
        Player_hands += threes.top_hands[0]
        Player_hands += threes.bottom_hands[0]
        Ai_hands += threes.hands[1]
        Ai_hands += threes.top_hands[1]
        Ai_hands += threes.bottom_hands[1]
        #Checks if any player has no cards, if they do then they win otherwise False is returned
        if not Player_hands:
            threes.winner = 0
            return True
        if not Ai_hands:
            threes.winner = 1
            return True
        return False

    def next_vaild_player(threes,player,savedata):
        if threes.is_game_over(): #Checks if the game is over
            return None
        else:
            if threes.another == True: #Checks if the player gets another turn and returns the player if they do
                threes.another = False #Sets it so the player doesn't get another turn next turn
                return player
            #Changes player's turn from 1 to 0 or 0 to 1
            if player == 1:
                return 0
            else:
                return 1
    
    def apply_move(threes,move):
        player = move[0]
        if not move: #Checks if the move exists 
            if threes.is_game_over(): #Checks if the game is over
                return
            else:
                threes.turn = threes.next_vaild_player(threes.turn, 'savedata') #Changes turn to the next vaild player
                return
        threes.state["history"].append(move) #Adds move to history
        if threes.played_cards: #Checks if there are cards in the middle that can be picked up
            Top_card = threes.played_cards[-1]
        else:
            Top_card = '2H' #If no card in the middle sets to 2H to use to compare so that all moves are vaild
        if move[2] == "try":
            if Top_card[0] == '2':
                threes.apply_move((player,move[1],"play"))
            else: #Checks that the attempted card is higher then previously played card if not the player pickups otherwise the move is applied
                Card_rank = threes.rank_order[move[1][0]]
                if Card_rank >= threes.rank_order[Top_card[0]]:
                    threes.apply_move((player,move[1],"play"))
                else:
                    threes.apply_move((player,threes.played_cards,"pickup"))
                    return
        elif move[2] == "play":
            Hands = [threes.hands[player],threes.bottom_hands[player],threes.top_hands[player]]
            played_rank = move[1][0]
            if played_rank in ('1','2'): #If the card is a 10 or a 2 only the card selected is played and removed from the player's hand
                threes.played_cards.append(move[1])
                for cards in Hands:
                    if move[1] in cards:
                        cards.remove(move[1])
            else:
                played_now = []
                Hand = []
                #Iterates through Hands to find which hand is being used
                if threes.hands[player]:
                    Hand = threes.hands[player]
                elif threes.top_hands[player]:
                    Hand = threes.top_hands[player]
                else:
                    Hand = threes.bottom_hands[player]
                for card in Hand[:]: #Plays all cards with the same rank as the one selected and removes them from the players hand
                    if card[0] == played_rank:
                        Hand.remove(card)
                        threes.played_cards.append(card)
                        played_now.append(card)
                if len(played_now) > 1: #Updates the history such that all played cards are reflected in it
                    threes.state['history'][-1] = (player,played_now,'play')
            four = False
            if len(threes.played_cards) > 3: #Checks if four of the same rank has been placed
                for i in range(1,5):
                    if i == 1:
                        rank = threes.played_cards[-i][0]
                    else:
                        temp = rank
                        rank = threes.played_cards[-i][0]
                        if temp == rank:
                            four = True
                        else:
                            four = False
                            break
            if four == True or move[1][0] == '1': #If four of the same cards or a 10 is placed the cards in the middle are 'burnt' - put into the discard pile and the player gets another turn
                threes.discard_pile += threes.played_cards
                threes.played_cards = []
                threes.another = True
            if threes.shuffled_deck and threes.hands[player]: #Adds cards to the player's hand such that they have at least three cards until the deck is gone.
                while threes.shuffled_deck:
                    while len(threes.hands[player]) < 3:
                        card = threes.shuffled_deck.pop()
                        threes.hands[player].append(card)
                    break
        elif move[2] == "pickup": #Gives all the cards that have been played to the player which needs to pick up
            if threes.played_cards:
                for card in threes.played_cards:
                    if card not in threes.hands[player]:
                        threes.hands[player].append(card)
            threes.played_cards = []
    
    def update_game_state(threes): #Updates the game state
        threes.state['selected_card'] = threes.selected_card
        threes.state['shuffled_deck'] = threes.shuffled_deck
        threes.state['hands'] = threes.hands
        threes.state['bottom_hands'] = threes.bottom_hands
        threes.state['top_hands'] = threes.top_hands
        threes.state['played_cards'] = threes.played_cards  
        threes.state['discard_pile'] = threes.discard_pile
        threes.state['another'] = threes.another
        threes.state['turn'] = threes.turn
        threes.state['time_elapsed'] = threes.time_elapsed
        threes.state['difficulty'] = threes.difficulty
        threes.state['winner'] = threes.winner

class rummy(Game): #Rummy Game Class
    def __init__(rummy, name, rank_order, state):
        super().__init__(name, rank_order, state) #Sets all the attributes as done in the Parent Game Class
        #Adds addtional neccessary attributes
        rummy.value_map = rank_order

    def distribute_cards(rummy):
        Start = 0 + rummy.turn
        End = 15 + rummy.turn
        Hands = rummy.hands
        for i in range(Start,End): #Ensures the starting player is dealt 8 cards and the other 7
            #If i is divisable by 2 cards are dealt to first player, else they are dealt to the second player
            if (i % 2) == 0:
                card = rummy.shuffled_deck.pop()
                Hands[0].append(card)
            else:
                card = rummy.shuffled_deck.pop()
                Hands[1].append(card)

    def find_run(rummy,cards):
        runs = []
        if len(cards) >= 3: #Checks cards are long enough to be a run
            previous_value = rummy.rank_order[cards[0][0]]
            run_length = 0
            starting_index = ''
            for card in cards: #Iterates through cards to find a run
                value = rummy.rank_order[card[0]]
                if run_length == 0: #Stores starting postion of the run
                    starting_index = cards.index(card)
                if value == previous_value: #Adds one to run length if card is the starting card
                    run_length += 1
                elif value == (previous_value + 1): #Adds one to run length if card is exactly one above the previous
                    run_length += 1
                    previous_value = value
                else: #Resets run if not consecutive
                    run_length = 1
                    starting_index = cards.index(card)
                    previous_value = value
                if run_length == 3: #Stores run it reaches required length
                    runs.append((3,starting_index))
                elif run_length == 4: #Stores run it increases in length
                    del runs[-1]
                    runs.append((4,starting_index))
            if runs: #Returns cards in the run if a run is present
                run_cards = []
                for run in runs:
                    run_cards += cards[run[1]:(run[0]+run[1])]
                return run_cards
        
    def find_set(rummy,cards):
        sets = []
        if len(cards) >= 3: #Checks cards are long enough to be a set
            set_length = 0
            starting_index = 0
            previous_rank = cards[0][0]
            for card in cards: #Iterates through cards to find a set
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

    def sort_cards(rummy,player):
        Sorted_hand = []
        Runs = []
        Sets = []
        Temp_hand = rummy.hands[player][:]
        Temp_hand.sort(key=(lambda a : rummy.rank_order[a[0]])) #Sorts cards in order of rank
        Hearts = []
        Clubs = []
        Spades = []
        Diamonds = []
        for card in Temp_hand: #Sorts cards into suits 
            if card.endswith('H'):
               Hearts.append(card)
            elif card.endswith('C'):
               Clubs.append(card)
            elif card.endswith('S'):
               Spades.append(card)
            elif card.endswith('D'):
               Diamonds.append(card)
        Suits = [Hearts,Clubs,Spades,Diamonds]
        for suit in Suits: #Iterates through each suit
            if rummy.find_run(suit): #Adds the runs to the sorted hand one is found
                Runs = rummy.find_run(suit)
                Sorted_hand += Runs
                for card in Runs:
                    Temp_hand.remove(card)
        if rummy.find_set(Temp_hand): #Adds the sets to the sorted hand one is found
            Sets = rummy.find_set(Temp_hand)
            Sorted_hand += Sets
            for card in Sets:
                Temp_hand.remove(card)
        if not Temp_hand: #If there is no cards left, it means the player has met the win requirements
            return "GameOver"
        else: #Returns the sorted hand
            Temp_hand.sort(key=(lambda a : rummy.rank_order[a[0]]))
            Sorted_hand += Temp_hand
            rummy.hands[player] = Sorted_hand
            return None

    def get_valid_moves(rummy):
        player = rummy.turn
        Moves = []
        Hand_len = len(rummy.hands[player])
        #Checks whether or not the player has 7 or 8 cards
        if Hand_len == 7: #if 7 it returns draw moves
            if rummy.shuffled_deck:
                Moves.append((player,"deck","draw"))
            if rummy.discard_pile:
                Moves.append((player,rummy.discard_pile[-1],"draw"))
            return Moves
        elif Hand_len == 8: # if 8 it returns discard moves
            for card in rummy.hands[player]:
                Moves.append((player,card,"discard"))
            return Moves
        else: #Returns [] if player has invaild amount of cards
            return Moves
    
    def is_game_over(rummy):
        #Checks if and which player that causes sort_cards returns 'GameOver' else returns False
        if rummy.sort_cards(1) == 'GameOver':
            rummy.winner = 1
            return True
        elif rummy.sort_cards(0) == 'GameOver':
            rummy.winner = 0
            return True
        return False
    
    def next_vaild_player(rummy,player):
        player = rummy.turn
        if rummy.is_game_over(): #Checks if the game is over
            return None
        else:
            if rummy.state['history']:
                last_move = rummy.state['history'][-1]
                #Switches turn if the last move was a discard otherwise they get another turn
                if last_move[2] == "draw":
                    return player
                elif last_move[2] == "discard":
                    if player == 1:
                        return 0
                    else:
                        return 1
                else: #Ensures swap of turn if last move was invalid
                    if player == 1:
                        return 0
                    else:
                        return 1
            else: #Ensures that the first player is swapped after their discard move
                if player == 1:
                    return 0
                else:
                    return 1
        
    def apply_move(rummy,move):
        player = move[0]
        if not move: #Checks if the move exists 
            if rummy.is_game_over(): #Checks if the game is over
                rummy.end_game()
                return
            else: #Changes turn to the next vaild player if no vaild move is possible
                rummy.turn = rummy.next_vaild_player(player,'savedata')
                return
        rummy.state['history'].append(move) #Adds move to history
        if move[2] == "draw": #Adds card to the player's hand and removes it from the source of where they selected it
            if move[1] == "deck":
                Top_card = rummy.shuffled_deck.pop()
                rummy.hands[player].append(Top_card)
            else:
                Top_card = rummy.discard_pile.pop()
                rummy.hands[player].append(Top_card)
        elif move[2] == "discard": #Removes card from player's hand and adds it to the discard pile
            rummy.discard_pile.append(move[1])
            rummy.hands[player].remove(move[1])
    
    def update_game_state(rummy): #Updates the game state
        rummy.state['shuffled_deck'] = rummy.shuffled_deck
        rummy.state['hands'] = rummy.hands
        rummy.state['discard_pile'] = rummy.discard_pile
        rummy.state['selected_card'] = rummy.selected_card
        rummy.state['turn'] = rummy.turn
        rummy.state['time_elapsed'] = rummy.time_elapsed
        rummy.state['difficulty'] = rummy.difficulty
        rummy.state['winner'] = rummy.winner


class memory(Game): #Memory Game Class
    def __init__(memory, name, rank_order, state):
        super().__init__(name, rank_order, state) #Sets all the attributes as done in the Parent Game Class
        #Adds addtional neccessary attributes
        memory.state = state
        memory.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory.first_selected_card = ('y','x','card')
        memory.second_selected_card = ('y','x','card')
        memory.selected_first_card = False
        memory.card_array = [[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]]

    def distribute_cards(memory): #Iterates through the card array and assigns card to each spot in it
        for y in range(0,9):
            for x in range(0,6):
                card = memory.shuffled_deck.pop()
                memory.card_array[y][x] = card

    def get_valid_moves(memory):
        player = memory.turn
        Moves = []
        for y, row in enumerate(memory.card_array): #Iterates through the card array
            for x, card in enumerate(row):
                if card is not None and card != '': #Checks if card exists 
                    if memory.first_selected_card[2] != 'card': #Checks if a first card has been selected
                        if card == memory.first_selected_card[2]:
                            continue
                        else:
                            Moves.append(("pick",player,(y,x,card))) #Adds move if card exists in array and is not the same card as first selected
                    else:
                        Moves.append(("pick",player,(y,x,card))) #Adds move if card exists in array
        return Moves
    
    def is_game_over(memory):
        #Iterates through card array to check it is empty
        for y,row in enumerate(memory.card_array):
            for x,card in enumerate(row):
                if card: #If card array is not empty return False as game is not over
                    return False
        #Sets the winner as the player with the most pairs
        if len(memory.hands[1]) > len(memory.hands[0]):
            memory.winner = 1
        else:
            memory.winner = 0
        return True

    def next_vaild_player(memory,player,app): #Write in NEA
        if memory.is_game_over(): #Checks if the game is over
            memory.end_game(app) #Ends game is game is over
        else:
            if memory.state['history']: #Checks if game has previous history
                if memory.state['history'][-1][0] == "Matched": #Gives player another turn if they matched cards
                    return player
                elif memory.state['history'][-1][0] == "Missed": #Changes turns if player did not successful match
                    if player == 1:
                        return 0
                    else:
                        return 1
                elif memory.state['history'][-1][0] == "pick": #Gives player another turn to pick a second card
                    return player
            else:
                return player #Assumes game has started due to no history so gives the player another turn
        
    def apply_move(memory,move,app):
        player = memory.turn
        if not move: #Checks if a move exists
            if memory.is_game_over() or len(memory.hands[0]) + len(memory.hands[1]) == 52: #Checks if the game is over
                memory.end_game(app) #Ends the game
                return
            else:
                memory.turn = memory.next_vaild_player(player,app) #Changes turn to the next vaild player
                return
        memory.state["history"].append(move) #Adds move to history
        if memory.selected_first_card == False: #Checks if the player has already selected a card
            memory.first_selected_card = move[2] #Stores the first selected card
            memory.selected_first_card = True #Sets selecting the first card to true
        else:
            memory.second_selected_card = move[2] #Stores the second selected card
            memory.selected_first_card = False #Resets the player selecting their first card
            first = memory.first_selected_card
            second = memory.second_selected_card
            is_joker_pair = (first[2] in ('BJ', 'RJ') and second[2] in ('BJ', 'RJ')) #Sets conditon for matching the jokers
            if is_joker_pair or first[2][0] == second[2][0]: #Checks if jokers have been paired or the ranks of selected cards are the same
                if not is_joker_pair: #Checks if the cards are the joker pair
                    suit1 = first[2][1]
                    suit2 = second[2][1]
                    match_condition = (suit1 in ['D','H'] and suit2 in ['D','H']) or (suit1 in ['C','S'] and suit2 in ['C','S']) #Determines if cards have the same colour
                else:
                    match_condition = True
                if match_condition: #Checks whether or not the cards have been matched
                    #Removes matched cards from the card array
                    memory.card_array[first[0]][first[1]] = None
                    memory.card_array[second[0]][second[1]] = None
                    memory.state["history"].append(("Matched",player,first,second)) #Adds the matched move to play history
                    #Adds matched cards to the player's hand
                    memory.hands[player].append(first[2])
                    memory.hands[player].append(second[2])
                else:
                    memory.state["history"].append(("Missed",player,first,second)) #Adds the missed move to play history
            else:
                memory.state["history"].append(("Missed",player,first,second)) #Adds the missed move to play history
            #Resets the player's selected cards
            memory.first_selected_card = ('y','x','card')
            memory.second_selected_card = ('y','x','card')
            memory.turn = memory.next_vaild_player(player,app) #Changes turns to the next player

    def update_game_state(memory): #Updates the Game state
        memory.state['shuffled_deck'] = memory.shuffled_deck
        memory.state['hands'] = memory.hands
        memory.state['first_selected_card'] = memory.first_selected_card
        memory.state['second_selected_card'] = memory.second_selected_card
        memory.state['selected_first_card'] = memory.selected_first_card
        memory.state['card_array'] = memory.card_array
        memory.state['turn'] = memory.turn
        memory.state['time_elapsed'] = memory.time_elapsed
        memory.state['difficulty'] = memory.difficulty
        memory.state['winner'] = memory.winner

