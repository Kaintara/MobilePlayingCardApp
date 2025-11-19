import random

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

class Threes(Game):
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

    def get_valid_moves(threes,player):
        Moves = []
        Valid_Cards = []
        if threes.hands[player]:
            Hand = threes.hands[player]
        elif threes.top_hands[player]:
            Hand = threes.hands[player]
        else:
            Hand = threes.bottom_hands[player]
            for card in Hand:
                Moves.append((player,card,"try"))
            return Moves
        if threes.played_cards:
            Moves.append((player,threes.played_cards,"pickup"))
            Top_card = threes.played_cards[-1]
            if Top_card[0] == '2':
                for card in Hand:
                    Moves.append((player,card,"play"))
                    return Moves
            for card in Hand:
                if Top_card[0] == card[0]:
                    Valid_Cards.append(Top_card)
                    break
            Hand.append(Top_card)
            threes.sort_cards()
            Index = Hand.index(Top_card) + 1
            Valid_Cards += Hand[Index:]
            for card in Valid_Cards:
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

    def end_game(threes,savedata):
        pass
       # savedata.save()
       # reward = threes.get_reward(shop)
       # Dialog = Reward_Dialog(reward)
       # Dialog.open()

    def next_vaild_player(threes,player,savedata):
        if threes.is_game_over():
            threes.end_game(savedata)
        else:
            if threes.another == True:
                threes.another = False
                return player
            if player == 1:
                return 0
            else:
                return 1
    
    def apply_move(threes,player,move):
        if not move:
            if threes.is_game_over():
                threes.end_game()
                return
            else:
                threes.turn = threes.next_vaild_player()
                return
        
        threes.state["history"].append(move)
        if threes.played_cards:
            Top_card = threes.played_cards[-1]
        else:
            Top_card = '2H'
        if move[2] == "try":
            if Top_card[0] == '2':
                threes.played_cards.append(move[1])
                threes.bottom_hands[player].remove(move[1])
            else:
                Card_rank = threes.rank_order[move[1][0]]
                if Card_rank >= threes.rank_order[Top_card[0]]:
                    threes.played_cards.append(move[1])
                    threes.bottom_hands[player].remove(move[1])
                else:
                    threes.apply_move(player,(player,threes.played_cards,"pickup"))
                    return
        elif move[2] == "play":
            threes.played_cards.append(move[1])
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
            if threes.shuffled_deck and threes.hands[player] and len(threes.hands[player]) < 3:
                while len(threes.hands[player]) != 3 or threes.shuffled_deck:
                    card = threes.shuffled_deck.pop()
                    threes.hands[player].append(card)
            Hands = [threes.hands[player],threes.bottom_hands[player],threes.top_hands[player]]
            for cards in Hands:
                if move[1] in cards:
                    cards.remove(move[1])
        elif move[2] == "pickup":
            threes.hands[player] += threes.played_cards[:-1]
            threes.played_cards = []

    def unlocked_achievements(threes,savedata):
        pass

    def get_reward(threes,shop):
        shop.coin_count += (threes.difficulty[0]*5)
        amount_earned += threes.difficulty[0]*5
        Unlocked_achievement = threes.unlocked_achievements()
        if Unlocked_achievement:
            shop.coin_count += 5*len(Unlocked_achievement)
            amount_earned += 5*len(Unlocked_achievement)
        if threes.winner == 0:
            shop.coin_count += (30 + threes.difficulty[0]*5)
            amount_earned += (30 + threes.difficulty[0]*5)
        else:
            shop.coin_count += 10
            amount_earned += 10
        return (amount_earned, Unlocked_achievement)
    
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
        threes.state['history'] = threes.state['history']

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

threes = Threes("threes",rank_order,state)

class Rummy(Game):
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
        Suits = [Hearts,Clubs,Clubs,Diamonds]
        for suit in Suits:
            if rummy.find_run(suit):
                Runs = rummy.find_run(suit)
                Sorted_hand += Runs
                for card in Runs:
                    Temp_hand.remove(card)
        if rummy.find_set(Temp_hand):
            Sets = rummy.find_run(Temp_hand)
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

    def get_valid_moves(rummy,player):
        Moves = []
        Hand_len = len(rummy.hands[player])
        if Hand_len == 7 and len(rummy.state['history']) > 1:
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

    def end_game(rummy,savedata):
        pass
       # savedata.save()
       # reward = threes.get_reward(shop)
       # Dialog = Reward_Dialog(reward)
       # Dialog.open()

    def next_vaild_player(rummy,player,savedata):
        if rummy.is_game_over():
            rummy.end_game(savedata)
        else:
            if rummy.state['history']:
                if rummy.state['history'][-1][0] == player and rummy.state['history'][-1][2] == 'draw':
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
        
    def apply_move(rummy,player,move):
        if not move:
            if rummy.is_game_over():
                rummy.end_game()
                return
            else:
                rummy.turn = rummy.next_vaild_player(player,'savedata')
                return
        rummy.state["history"].append(move)
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

    def unlocked_achievements(rummy,savedata):
        pass

    def get_reward(rummy,shop):
        shop.coin_count += (rummy.difficulty[0]*5)
        amount_earned += rummy.difficulty[0]*5
        Unlocked_achievement = rummy.unlocked_achievements()
        if Unlocked_achievement:
            shop.coin_count += 5*len(Unlocked_achievement)
            amount_earned += 5*len(Unlocked_achievement)
        if rummy.winner == 0:
            shop.coin_count += (30 + rummy.difficulty[0]*5)
            amount_earned += (30 + rummy.difficulty[0]*5)
        else:
            shop.coin_count += 10
            amount_earned += 10
        return (amount_earned, Unlocked_achievement)
    
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

rummy = Rummy("rummy",{'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,
'5': 5,'4': 4,'3': 3,'2': 2},state)


class Memory(Game):
    def __init__(memory, name, rank_order, state):
        super().__init__(name, rank_order, state)
        memory.state = state
        memory.deck = ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH","BJ","RJ"]
        memory.first_selected_card = ('y','x','card')
        memory.second_selected_card = ('y','x','card')
        memory.selected_first_card = False
        memory.card_array = [['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','','']]

    def distribute_cards(memory):
        for y in range(0,9):
            for x in range(0,6):
                card = memory.shuffled_deck.pop()
                memory.card_array[y][x] = card

    def get_valid_moves(memory,player):
        Moves = []
        for y, row in enumerate(memory.card_array):
            for x, card in enumerate(row):
                if card:
                    Moves.append((player,(y,x,card),"pick"))
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

    def end_game(memory,savedata):
        pass
       # savedata.save()
       # reward = threes.get_reward(shop)
       # Dialog = Reward_Dialog(reward)
       # Dialog.open()

    def next_vaild_player(memory,player,savedata):
        if memory.is_game_over():
            memory.end_game(savedata)
        else:
            if memory.state['history']:
                if memory.state['history'][-1][3] == "Matched":
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
        
    def apply_move(memory,player,move):
        if not move:
            if memory.is_game_over():
                memory.end_game()
                return
            else:
                memory.turn = memory.next_vaild_player(player,'savedata')
                return
        memory.state["history"].append(move)
        if memory.selected_first_card == False:
            memory.first_selected_card = move[1]
            memory.selected_first_card = True
        else:
            memory.second_selected_card = move[1]
            memory.selected_first_card = False
            first = memory.first_selected_card
            second = memory.second_selected_card
            if first[2][0] == second[2][0]:
                suit1 = first[2][1]
                suit2 = second[2][1]
                if (suit1 in ['D','H'] and suit2 in ['D','H']) or (suit1 in ['C','S'] and suit2 in ['C','S']):
                    memory.card_array[first[0]][first[1]] = None
                    memory.card_array[second[0]][second[1]] = None
                    memory.state["history"].append((player,first,second,"Matched"))
                    memory.hands[player].append(first[2])
                    memory.hands[player].append(second[2])
                else:
                    memory.state["history"].append((player,first,second,"Missed"))
                memory.first_selected_card = ('y','x','card')
                memory.second_selected_card = ('y','x','card')
            else:
                memory.state["history"].append((player,(memory.first_selected_card,memory.second_selected_card),"NotMatched"))

    def unlocked_achievements(rummy,savedata):
        pass

    def get_reward(rummy,shop):
        shop.coin_count += (rummy.difficulty[0]*5)
        amount_earned += rummy.difficulty[0]*5
        Unlocked_achievement = rummy.unlocked_achievements()
        if Unlocked_achievement:
            shop.coin_count += 5*len(Unlocked_achievement)
            amount_earned += 5*len(Unlocked_achievement)
        if rummy.winner == 0:
            shop.coin_count += (30 + rummy.difficulty[0]*5)
            amount_earned += (30 + rummy.difficulty[0]*5)
        else:
            shop.coin_count += 10
            amount_earned += 10
        return (amount_earned, Unlocked_achievement)
    
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



threes.shuffle_cards()
threes.distribute_cards()
public_cards = []
if threes['hands'][1]:
    for x in threes['hands'][1]:
        public_cards.append(x)
if threes['top_hands'][0]:
    public_cards.append(threes['top_hands'][0])



if threes['top_hands'][1]:
    public_cards.append(threes['top_hands'][1])
if threes['top_hands'][0]:
    public_cards.append(threes['top_hands'][0])
if threes['discard_pile']:
    public_cards.append(threes['discard_pile'])
if threes['played_cards']:
    public_cards.append(threes['played_cards'])
print(public_cards)