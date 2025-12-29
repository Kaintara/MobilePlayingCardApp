import random
from ui import Achievement_Dialog, Reward_Dialog
from kivy.clock import Clock
from threesMTCS import genv
from treesearch import mtcs

class Game: 
    def __init__(game, name, rank_order,state):
        game.name = name
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

    def shuffle_cards(game):
        shuffled_deck = game.deck[:]
        random.shuffle(shuffled_deck)
        game.shuffled_deck = shuffled_deck

    def unlocked_achievements(game, app, savedata):
        unlocked = []
        already_unlocked = {a[0] for a in app.unlocked_achievements}

        for id, name, desc, condition in app.all_achievements:
            if id not in already_unlocked and condition(savedata):
                unlocked.append((id, name, desc, condition))
                app.unlocked_achievements.append((id, name, desc))

        return unlocked

    def display_achievements(game,achievement):
        Dialog = Achievement_Dialog(achievement)
        Dialog.open()
        Clock.schedule_once(lambda dt: Dialog.dismiss(), 5)
    
    def get_reward(game,shop,app,savedata):
        amount_earned = 0
        shop.coin_count += (game.difficulty[0]*5)
        amount_earned += game.difficulty[0]*5
        Unlocked_achievement = game.unlocked_achievements(app,savedata)
        total_delay = 0
        if Unlocked_achievement:
            shop.coin_count += 5*len(Unlocked_achievement)
            amount_earned += 5*len(Unlocked_achievement)
            for index, achievement in enumerate(Unlocked_achievement):
                delay = index * 5
                total_delay += delay
                Clock.schedule_once(lambda dt: game.display_achievements(achievement), delay) 
        if game.winner == 0:
            shop.coin_count += (30 + game.difficulty[0]*5)
            amount_earned += (30 + game.difficulty[0]*5)
        else:
            shop.coin_count += 10
            amount_earned += 10
        return (amount_earned, game.winner, total_delay)
    
    def end_game(game, app):
        print("Game Over!")
        completed_game = {
            'winner': game.winner,
            'history': game.state['history'],
            'difficulty' : game.difficulty,
            'time': game.time_elapsed
        }
        app.previous_games[game.name].append(completed_game)
        app.save.savedata(app, app.threes, app.rummy, app.memory, app.shop)
        reward = game.get_reward(app.shop,app,app.save)
        app.save.savedata(app, app.threes, app.rummy, app.memory, app.shop)
        for _ in range(3):
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
        Dialog = Reward_Dialog(reward,app)
        Clock.schedule_once(lambda dt: Dialog.open(), reward[2]) 

class threes(Game):
    def __init__(threes, name, rank_order, state):
        super().__init__(name, rank_order, state)
        threes.bottom_hands = [[],[]]
        threes.top_hands = [[],[]]
        threes.played_cards = []
        threes.another = False

    def distribute_cards(threes):
        Hands = [threes.hands,threes.bottom_hands,threes.top_hands]
        for hand in Hands:
            for i in range(0,6):
                if (i % 2) == 0:
                    card = threes.shuffled_deck.pop()
                    hand[0].append(card)
                else:
                    card = threes.shuffled_deck.pop()
                    hand[1].append(card)

    def sort_cards(threes):
        threes.hands[0].sort(key=(lambda a : threes.rank_order[a[0]]))
        threes.hands[1].sort(key=(lambda a : threes.rank_order[a[0]]))

    def get_valid_moves(threes):
        player = threes.turn
        Moves = []
        Valid_Cards = []
        if threes.hands[player]:
            Hand = threes.hands[player]
        elif threes.top_hands[player]:
            Hand = threes.top_hands[player]
        else:
            Hand = threes.bottom_hands[player]
            for card in Hand:
                Moves.append((player,card,"try"))   
            return Moves
        if threes.played_cards:
            Moves.append((player,threes.played_cards[:],"pickup"))
            Top_card = threes.played_cards[-1]
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
        else:
            for card in Hand:
                Moves.append((player,card,"play"))
        return Moves
    
    def is_game_over(threes):
        Player_hands = []
        Ai_hands = []
        Player_hands += threes.hands[0]
        Player_hands += threes.top_hands[0]
        Player_hands += threes.bottom_hands[0]
        Ai_hands += threes.hands[1]
        Ai_hands += threes.top_hands[1]
        Ai_hands += threes.bottom_hands[1]
        if not Player_hands:
            threes.winner = 0
            return True
        if not Ai_hands:
            threes.winner = 1
            return True
        return False

    def next_vaild_player(threes,player,savedata):
        if threes.is_game_over():
            return None
        else:
            if threes.another == True:
                threes.another = False
                return player
            if player == 1:
                return 0
            else:
                return 1
    
    def apply_move(threes,move):
        player = move[0]
        if not move:
            if threes.is_game_over():
                #threes.end_game()
                return
            else:
                threes.turn = threes.next_vaild_player(threes.turn, 'savedata')
                return
        threes.state["history"].append(move)
        if threes.played_cards:
            Top_card = threes.played_cards[-1]
        else:
            Top_card = '2H'
        if move[2] == "try":
            if Top_card[0] == '2':
                threes.apply_move((player,move[1],"play"))
            else:
                Card_rank = threes.rank_order[move[1][0]]
                if Card_rank >= threes.rank_order[Top_card[0]]:
                    threes.apply_move((player,move[1],"play"))
                else:
                    threes.apply_move((player,threes.played_cards,"pickup"))
                    return
        elif move[2] == "play":
            Hands = [threes.hands[player],threes.bottom_hands[player],threes.top_hands[player]]
            played_rank = move[1][0]
            if played_rank in ('1','2'):
                threes.played_cards.append(move[1])
                for cards in Hands:
                    if move[1] in cards:
                        cards.remove(move[1])
            else:
                played_now = []
                Hand = []
                if threes.hands[player]:
                    Hand = threes.hands[player]
                elif threes.top_hands[player]:
                    Hand = threes.top_hands[player]
                else:
                    Hand = threes.bottom_hands[player]
                for card in Hand[:]:
                    if card[0] == played_rank:
                        Hand.remove(card)
                        threes.played_cards.append(card)
                        played_now.append(card)
                if len(played_now) > 1:
                    threes.state['history'][-1] = (player,played_now,'play')
            four = False
            if len(threes.played_cards) > 3:
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
            if four == True or move[1][0] == '1':
                threes.discard_pile += threes.played_cards
                threes.played_cards = []
                threes.another = True
            if threes.shuffled_deck and threes.hands[player]:
                while threes.shuffled_deck:
                    while len(threes.hands[player]) < 3:
                        card = threes.shuffled_deck.pop()
                        threes.hands[player].append(card)
                    break
        elif move[2] == "pickup":
            if threes.played_cards:
                for card in threes.played_cards:
                    if card not in threes.hands[player]:
                        threes.hands[player].append(card)
            threes.played_cards = []
    
    def update_game_state(threes):
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

    def test_run(threes):
        threes.shuffle_cards()
        threes.distribute_cards()
        threes.turn = 0
        while not threes.is_game_over():
            if threes.turn == 1:
                chosen_move = mtcs(threes.state, genv, 0.3, True)
            else:
                moves = threes.get_valid_moves()
                # No moves at all – skip or break the game
                if not moves:
                    threes.turn = threes.next_vaild_player(threes.turn, 'save')
                    print("No valid moves – skipping turn")
                    continue
                # Filter moves
                play_moves = [m for m in moves if m[2] != "pickup"]
                pickup_moves = [m for m in moves if m[2] == "pickup"]
                # Decide which move to apply
                if play_moves:
                    # Choose the first non-pickup move
                    chosen_move = play_moves[0]
                else:
                    # Only pickup available
                    chosen_move = pickup_moves[0]
            # Apply the chosen move
            threes.apply_move(chosen_move)
            print("HANDS:", threes.hands)
            print("CARDS LEFT:", threes.state['bottom_hands'])
            print("DECK:", threes.shuffled_deck)
            threes.update_game_state()
            print("HISTORY:",threes.state['history'][-1])
            threes.turn = threes.next_vaild_player(threes.turn, 'save')
            #input()
        print("game over")

rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,
'5': 5,'4': 4,'3': 3,'2': 15}

state = {'name' : "threes",
        'deck' : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
        'shuffled_deck' : [],
        'rank_order' : {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,
'5': 5,'4': 4,'3': 3,'2': 15},
        'hands' : [[],[]],
        'discard_pile' : [],
        'selected_card' : '',
        'turn' : 0,
        'time_elapsed' : 0,
        'difficulty' : (-1,""),
        'winner' : None,
        'bottom_hands' : [[],[]],
        'top_hands' : [[],[]],
        'another' : False,
        'played_cards' : [],
        'history': []}

'''
threes_game = threes("threes",rank_order,state)
counts = 0
for _ in range(3):
    threes_game.test_run()
    counts += 1 if threes_game.winner == 1 else 0
    # reset
    threes_game.shuffled_deck = []
    threes_game.hands = [[],[]]
    threes_game.bottom_hands = [[],[]]
    threes_game.top_hands = [[],[]]
    threes_game.turn = 0
    threes_game.winner = None
    threes_game.history = []
    threes_game.state = state

print(f"threes AI wins {counts*33}%")
'''

class rummy(Game):
    def __init__(rummy, name, rank_order, state):
        super().__init__(name, rank_order, state)
        rummy.value_map = rank_order

    def distribute_cards(rummy):
        Start = 0 + rummy.turn
        End = 15 + rummy.turn
        Hands = rummy.hands
        for i in range(Start,End):
            if (i % 2) == 0:
                card = rummy.shuffled_deck.pop()
                Hands[0].append(card)
            else:
                card = rummy.shuffled_deck.pop()
                Hands[1].append(card)

    def find_run(rummy,cards):
        runs = []
        if len(cards) >= 3:
            previous_value = rummy.rank_order[cards[0][0]]
            run_length = 0
            starting_index = ''
            for card in cards:
                value = rummy.rank_order[card[0]]
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

    def sort_cards(rummy,player):
        Sorted_hand = []
        Runs = []
        Sets = []
        Temp_hand = rummy.hands[player][:]
        Temp_hand.sort(key=(lambda a : rummy.rank_order[a[0]]))
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
            if rummy.find_run(suit):
                Runs = rummy.find_run(suit)
                Sorted_hand += Runs
                print(Runs)
                for card in Runs:
                    print(card)
                    print(Temp_hand)
                    Temp_hand.remove(card)
        if rummy.find_set(Temp_hand):
            Sets = rummy.find_set(Temp_hand)
            Sorted_hand += Sets
            for card in Sets:
                Temp_hand.remove(card)
        if not Temp_hand:
            return "GameOver"
        else:
            Temp_hand.sort(key=(lambda a : rummy.rank_order[a[0]]))
            Sorted_hand += Temp_hand
            rummy.hands[player] = Sorted_hand
            return None

    def get_valid_moves(rummy):
        player = rummy.turn
        Moves = []
        Hand_len = len(rummy.hands[player])
        if Hand_len == 7:
            if rummy.shuffled_deck:
                Moves.append((player,"deck","draw"))
            if rummy.discard_pile:
                Moves.append((player,rummy.discard_pile[-1],"draw"))
            return Moves
        elif Hand_len == 8:
            for card in rummy.hands[player]:
                Moves.append((player,card,"discard"))
            return Moves
        else:
            return Moves
    
    def is_game_over(rummy):
        if rummy.sort_cards(1) == 'GameOver':
            rummy.winner = 1
            return True
        elif rummy.sort_cards(0) == 'GameOver':
            rummy.winner = 0
            return True
        return False
    
    def next_vaild_player(rummy,player,savedata):
        player = rummy.turn
        if rummy.is_game_over():
            return None

        history = rummy.state['history']

        if not history:
            print("Starting Player:", player)
            return player

        first_player, _, _ = history[0]

        if len(history) == 1:
            print("next player after first move", 1 - first_player)
            return 1 - first_player
        elif len(history) >= 2:
            last_player, _, last_action = history[-1]
            if last_action == 'discard':
                return 1 - last_player
            else:
                return last_player
        
    def apply_move(rummy,move):
        player = move[0]
        if not move:
            if rummy.is_game_over():
                rummy.end_game()
                return
            else:
                rummy.turn = rummy.next_vaild_player(player,'savedata')
                return
        rummy.state['history'].append(move)
        if move[2] == "draw":
            if move[1] == "deck":
                Top_card = rummy.shuffled_deck.pop()
                rummy.hands[player].append(Top_card)
            else:
                Top_card = rummy.discard_pile.pop()
                rummy.hands[player].append(Top_card)
        elif move[2] == "discard":
            rummy.discard_pile.append(move[1])
            rummy.hands[player].remove(move[1])
            print(rummy.turn)
            rummy.turn = 1 - rummy.turn
    
    def update_game_state(rummy):
        rummy.state['shuffled_deck'] = rummy.shuffled_deck
        rummy.state['hands'] = rummy.hands
        rummy.state['discard_pile'] = rummy.discard_pile
        rummy.state['selected_card'] = rummy.selected_card
        rummy.state['turn'] = rummy.turn
        rummy.state['time_elapsed'] = rummy.time_elapsed
        rummy.state['difficulty'] = rummy.difficulty
        rummy.state['winner'] = rummy.winner

    def test_run(rummy):
        rummy.shuffle_cards()
        rummy.distribute_cards()
        rummy.turn = 0
        while not rummy.is_game_over():
            moves = rummy.get_valid_moves(rummy.turn)
            if not moves:
                rummy.turn = rummy.next_vaild_player(rummy.turn, 'save')
                print("No valid moves – skipping turn")
                continue
            mo = [m for m in enumerate(moves)]
            print(mo)
            rummy.apply_move(moves[int(input())])
            print("HANDS:", rummy.hands)
            print("HISTORY:", rummy.state['history'])
            print("DECK:", rummy.shuffled_deck)
            rummy.update_game_state()
            print(rummy.turn)
        print("game over")
    
state = {'name' : "rummy",
        'deck' : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
        'shuffled_deck' : [],
        'value_map' : {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,
'5': 5,'4': 4,'3': 3,'2': 2},
        'hands' : [[],[]],
        'discard_pile' : [],
        'selected_card' : '',
        'turn' : 0,
        'time_elapsed' : 0,
        'difficulty' : (-1,""),
        'winner' : None,
        'history': []}

#rummy = rummy("rummy",{'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2},state)

#rummy.test_run()

class memory(Game):
    def __init__(memory, name, rank_order, state):
        super().__init__(name, rank_order, state)
        memory.state = state
        memory.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory.first_selected_card = ('y','x','card')
        memory.second_selected_card = ('y','x','card')
        memory.selected_first_card = False
        memory.card_array = [[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]]

    def distribute_cards(memory):
        for y in range(0,9):
            for x in range(0,6):
                card = memory.shuffled_deck.pop()
                memory.card_array[y][x] = card

    def get_valid_moves(memory):
        player = memory.turn
        Moves = []
        for y, row in enumerate(memory.card_array):
            for x, card in enumerate(row):
                # Skip empty slots (None) and already-matched cards
                if card is not None and card != '':
                    if memory.first_selected_card[2] != 'card':  # First card has been picked
                        if card == memory.first_selected_card[2]:
                            continue  # Can't pick the same card twice
                        else:
                            Moves.append(("pick",player,(y,x,card)))
                    else:
                        # First card not yet picked, any valid card works
                        Moves.append(("pick",player,(y,x,card)))
        return Moves
    
    def is_game_over(memory):
        for y,row in enumerate(memory.card_array):
            for x,card in enumerate(row):
                if card:
                    return False
        if len(memory.hands[1]) > len(memory.hands[0]):
            memory.winner = 1
        else:
            memory.winner = 0
        return True

    def next_vaild_player(memory,player,savedata):
        if memory.is_game_over():
            memory.end_game(savedata)
        else:
            if memory.state['history']:
                if memory.state['history'][-1][0] == "Matched":
                    return player
                elif memory.state['history'][-1][0] == "Missed":
                    if player == 1:
                        return 0
                    else:
                        return 1
                elif memory.state['history'][-1][0] == "pick":
                    return player
            else:
                return player
        
    def apply_move(memory,move):
        player = memory.turn
        if not move:
            if memory.is_game_over():
                memory.end_game()
                return
            else:
                memory.turn = memory.next_vaild_player(player,'savedata')
                return
        memory.state["history"].append(move)
        if memory.selected_first_card == False:
            memory.first_selected_card = move[2]
            memory.selected_first_card = True
        else:
            memory.second_selected_card = move[2]
            memory.selected_first_card = False
            first = memory.first_selected_card
            second = memory.second_selected_card
            is_joker_pair = (first[2] in ('BJ', 'RJ') and second[2] in ('BJ', 'RJ'))
            if is_joker_pair or first[2][0] == second[2][0]:
                if not is_joker_pair:
                    suit1 = first[2][1]
                    suit2 = second[2][1]
                    same_color = (suit1 in ['D','H'] and suit2 in ['D','H']) or (suit1 in ['C','S'] and suit2 in ['C','S'])
                    match_condition = same_color
                else:
                    match_condition = True
                if match_condition:
                    memory.card_array[first[0]][first[1]] = None
                    memory.card_array[second[0]][second[1]] = None
                    memory.state["history"].append(("Matched",player,first,second))
                    memory.hands[player].append(first[2])
                    memory.hands[player].append(second[2])
                else:
                    memory.state["history"].append(("Missed",player,first,second))
            else:
                memory.state["history"].append(("Missed",player,first,second))
            memory.first_selected_card = ('y','x','card')
            memory.second_selected_card = ('y','x','card')

    def update_game_state(memory):
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

    def test_run(memory):
        memory.shuffle_cards()
        memory.distribute_cards()
        memory.turn = 0
        while not memory.is_game_over():
            moves = memory.get_valid_moves(memory.turn)
            if not moves:
                memory.turn = memory.next_vaild_player(memory.turn, 'save')
                print("No valid moves – skipping turn")
                continue
            if memory.turn == 1:
                chosen_move = mtcs(memory.state,genv,0.5,True)
            else:
                chosen_move = random.choice(moves)
            memory.apply_move(chosen_move)
            print("PAIRS:", memory.hands)
            print("HISTORY:", memory.state['history'][-1])
            print("CARD ARRAY:", memory.card_array)
            memory.update_game_state()
        print("game over")
        return memory.winner
    
'''
state = {'name' : "memory",
        'deck' : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
        'shuffled_deck' : [],
        'hands' : [[],[]],
        'first_selected_card' : ('y','x','card'),
        'second_selected_card' : ('y','x','card'),
        'selected_first_card' : False,
        'card_array' : [['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','','']],
        'turn' : 0,
        'time_elapsed' : 0,
        'difficulty' : (-1,""),
        'winner' : None,
        'history': []}

memory = memory('memory','rank',state)
counts = 0
for _ in range(5):
    counts += memory.test_run()
    memory.shuffled_deck = []
    memory.hands = [[],[]]
    memory.turn = 0
    memory.winner = None
    memory.history = []
    memory.state = state
print(f"Wins {counts*20}%")

'''

