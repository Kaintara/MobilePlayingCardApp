from save import SaveData
        
class FakeApp:
    def __init__(self):
        self.sm_stack = True
        self.sfx = True
        self.ai_difficulty = "Hard"
        self.timer = True
        self.score = 999
        self.unlocked_achivements = ["Hello World!"]

        self.previous_games = {
            'Threes': {
                'winner': 0,
                'history': [(0, "3D", "play")],
                'difficulty': (0, "Beginner"),
                'time': 10
            },
            'Rummy': {
                'winner': 0,
                'history': [],
                'difficulty': (0, "Easy"),
                'time': 50
            },
            'Memory': {
                'winner': 1,
                'history': [],
                'difficulty': (0, "Normal"),
                'time': 30
            }
        }

class FakeShop:
    def __init__(self):
        self.equipped = "Cool Skin"
        self.unlocked_inventory = ["Cool Skin", "Basic Skin"]
        self.coin_count = 1234

class FakeGameState:
    def __init__(self, name):
        self.state = f"{name} current state"


def test_savedata():
    Save = SaveData()
    app = FakeApp()
    shop = FakeShop()
    threes = FakeGameState("Threes")
    rummy  = FakeGameState("Rummy")
    memory = FakeGameState("Memory")
    Save.savedata(app, threes, rummy, memory, shop)
    print("\n===== SHOP DATA =====")
    print(Save.alldata['Shop'])
    print("\n===== APP DATA =====")
    print(Save.alldata['App'])
    print("\n===== PREVIOUS GAMES =====")
    print(Save.alldata['Games']['Previous_Games'])
    print("\n===== CURRENT GAMES =====")
    print(Save.alldata['Games']['Current_Games'])
    print("\n===== STATS =====")
    print(Save.alldata['Games']['Stats'])
    Save.load()

test_savedata()

'''
    def cards_left(env,state,player):
        rank_order = {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}
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
        Suits = [Hearts,Clubs,Clubs,Diamonds]
        for suit in Suits:
            if env.find_run(suit):
                Runs = env.find_run(suit)
                for card in Runs:
                    if card in Temp_hand:
                        Temp_hand.remove(card)
        if env.find_set(Temp_hand):
            Sets = env.find_set(Temp_hand)
            for card in Sets:
                if card in Temp_hand:
                    Temp_hand.remove(card)
        if not Temp_hand:
            return 0
        else:
            return len(Temp_hand)
    '''
