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

    def end_game(threes):
        print("Called end game")

    def next_vaild_player(threes):
        print("called nvp")
        return 1
    
    def apply_move(threes,player,move):
        if not move:
            if threes.is_game_over():
                threes.end_game()
                return
            else:
                threes.turn = threes.next_vaild_player()
                return
        print("Applying move:", move)
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
        'difficulty' : (0,"Easy"),
        'winner' : None,
        'bottom_hands' : [[],[]],
        'top_hands' : [[],[]],
        'played_cards' : [],
        'history': []}



threes = Threes("threes",rank_order,state)
Hands = [threes.hands,threes.bottom_hands,threes.top_hands]
threes.played_cards = ['5H','5D']
threes.hands = [['JS', 'KD', 'KS'], ['QH', 'JH', '3D']]
threes.apply_move(0,(0, 'KS', 'play'))
print(threes.state["history"])
print(threes.get_valid_moves(1))
threes.apply_move(1,(1, ['KS'], 'pickup'))
print(threes.state["history"])
print(threes.hands)

print(threes.is_game_over())
threes.hands = [[],[]]
threes.top_hands = [[],[]]
threes.bottom_hands = [['2H','3S'],[]]
print(threes.is_game_over())