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
