from datetime import datetime
import json

class SaveData():
    def __init__(save):
        save.alldata = {
            'Shop' : {'equipped' : 'Classic',
                     'unlocked_inventory' : ['Classic'],
                     'coin_count' : 0,
                       },
            'App' : {'sm_stack' : [],
                     'sfx': True,
                     'ai_difficulty' : "Beginner",
                     'timer': True,
                     'score' : True,
                     'unlocked_achievements' : []
                     },
            'Games' : {
                'Stats' : {
                    'Threes_Stats' : {
                        'General_Stats' : {
                        "games_played": 0,
                        "wins": 0,
                        "win_lose_ratio": 0,
                        "won_with_3": 0,
                        "amount_of_pickups": 0,
                        "best_time": None,
                        "total_time": 0,
                        "last_played": None
                        },  
                        'Beginner' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Easy' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Normal' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Hard' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Expert' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                    },
                    'Rummy_Stats' : {
                        'General_Stats' : {
                        "games_played": 0,
                        "wins": 0,
                        "win_lose_ratio": 0,
                        "best_time": None,
                        "total_time": 0,
                        "last_played": None
                        },
                        'Beginner' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Easy' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Normal' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Hard' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Expert' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": None,
                            "last_played": None
                        },
                    },
                    'Memory_Stats' : {
                        'General_Stats' : {
                        "games_played": 0,
                        "wins": 0,
                        "win_lose_ratio": 0,
                        "most_pairs": 0,
                        "all_pairs": 0,
                        "best_time": None,
                        "total_time": 0,
                        "last_played": None
                    },
                        'Beginner' : {
                            "games_played": 0,
                            "wins": 0,
                            "most_pairs": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Easy' : {
                            "games_played": 0,
                            "wins": 0,
                            "most_pairs": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Normal' : {
                            "games_played": 0,
                            "wins": 0,
                            "most_pairs": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Hard' : {
                            "games_played": 0,
                            "wins": 0,
                            "most_pairs": 0,
                            "best_time": None,
                            "last_played": None
                        },
                        'Expert' : {
                            "games_played": 0,
                            "wins": 0,
                            "most_pairs": 0,
                            "best_time": None,
                            "last_played": None
                        },
                    },
                },
                'Previous_Games' : {   #Format = {'winner': None,'history': [],'difficulty' : (-1,""), 'time':0}
                    'Threes' : [],
                    'Rummy' : [],
                    'Memory' : []
                },
                'Current_Games' :
                {'Threes': {'name' : "threes",
                            'deck' : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
                            'shuffled_deck' : [],
                            'rank_order' : {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15},
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
                            'history': []},
                 'Rummy': {'name' : "rummy",
                            'deck' : ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD","AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS","AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC","AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
                            'shuffled_deck' : [],
                            'value_map' : {'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2},
                            'hands' : [[],[]],
                            'discard_pile' : [],
                            'selected_card' : '',
                            'turn' : 0,
                            'time_elapsed' : 0,
                            'difficulty' : (-1,""),
                            'winner' : None,
                            'history': []},
                 'Memory': {'name' : "memory",
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
                            'history': []}}
            }
        }

    def calc_threes_stats(save):  #Format of previous games = {'winner': None,'history': [],'difficulty' : (-1,""), 'time':0}
        Game = save.alldata['Games']['Previous_Games']['Threes'][-1]
        difficulty = Game['difficulty'][1]
        Difficulty_Stats = save.alldata['Games']['Stats']['Threes_Stats'][difficulty]
        All_Stats = save.alldata['Games']['Stats']['Threes_Stats']['General_Stats']
        All_Stats["games_played"] += 1
        Difficulty_Stats["games_played"] += 1
        if Game['winner'] == 0:
            All_Stats["wins"] += 1
            Difficulty_Stats["wins"] += 1
            threes = [(0,"3D","play"),(0,"3H","play"),(0,"3S","play"),(0,"3C","play")]
            if Game['history'][-1] in threes:
                All_Stats["won_with_3"] += 1
        if All_Stats["games_played"] > 0:
            All_Stats["win_lose_ratio"] = f"{round((All_Stats['wins']/All_Stats['games_played'])*100, 2)}%"
        for move in Game['history']:
            if move[2] == 'pickup' and move[0] == 0:
                All_Stats["amount_of_pickups"] += 1
        if Difficulty_Stats["best_time"] is None or Difficulty_Stats["best_time"] > Game['time']:
            Difficulty_Stats["best_time"] = Game['time']
            if All_Stats["best_time"] is None or All_Stats["best_time"] > Game['time']:
                All_Stats["best_time"] = Game['time']
        All_Stats['total_time'] += Game['time']
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        All_Stats["last_played"] = now
        Difficulty_Stats["last_played"] = now

    def calc_rummy_stats(save):
        Game = save.alldata['Games']['Previous_Games']['Rummy'][-1]
        difficulty = Game['difficulty'][1]
        Difficulty_Stats = save.alldata['Games']['Stats']['Rummy_Stats'][difficulty]
        All_Stats = save.alldata['Games']['Stats']['Rummy_Stats']['General_Stats']
        All_Stats["games_played"] += 1
        Difficulty_Stats["games_played"] += 1
        if Game['winner'] == 0:
            All_Stats["wins"] += 1
            Difficulty_Stats["wins"] += 1
        if All_Stats["games_played"] > 0:
            All_Stats["win_lose_ratio"] = f"{round((All_Stats['wins']/All_Stats['games_played'])*100, 2)}%"
        if Difficulty_Stats["best_time"] is None or Difficulty_Stats["best_time"] > Game['time']:
            Difficulty_Stats["best_time"] = Game['time']
            if All_Stats["best_time"] is None or All_Stats["best_time"] > Game['time']:
                All_Stats["best_time"] = Game['time']
        All_Stats['total_time'] += Game['time']
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        All_Stats["last_played"] = now
        Difficulty_Stats["last_played"] = now

    def calc_memory_stats(save):
        Game = save.alldata['Games']['Previous_Games']['Memory'][-1]
        difficulty = Game['difficulty'][1]
        Difficulty_Stats = save.alldata['Games']['Stats']['Memory_Stats'][difficulty]
        All_Stats = save.alldata['Games']['Stats']['Memory_Stats']['General_Stats']
        All_Stats["games_played"] += 1
        Difficulty_Stats["games_played"] += 1
        if Game['winner'] == 0:
            All_Stats["wins"] += 1
            Difficulty_Stats["wins"] += 1
        if All_Stats["games_played"] > 0:
            All_Stats["win_lose_ratio"] = f"{round((All_Stats['wins']/All_Stats['games_played'])*100, 2)}%"
        pair_count = 0
        for move in Game['history']:
            if move[1] == 0 and move[0] == "Matched":
                pair_count += 1
                All_Stats["all_pairs"] += 1
        if Difficulty_Stats["most_pairs"] < pair_count:
            Difficulty_Stats["most_pairs"] = pair_count
            if All_Stats["most_pairs"] < pair_count:
                All_Stats["most_pairs"] = pair_count
        if Difficulty_Stats["best_time"] is None or Difficulty_Stats["best_time"] > Game['time']:
            Difficulty_Stats["best_time"] = Game['time']
            if All_Stats["best_time"] is None or All_Stats["best_time"] > Game['time']:
                All_Stats["best_time"] = Game['time']
        All_Stats['total_time'] += Game['time']
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        All_Stats["last_played"] = now
        Difficulty_Stats["last_played"] = now

    def savedata(save, app, threes, rummy, memory, shop):
        save.alldata['Shop']['equipped'] = shop.equipped
        save.alldata['Shop']['unlocked_inventory'] = shop.unlocked_inventory
        save.alldata['Shop']['coin_count'] = shop.coin_count
        save.alldata['App']['sm_stack'] = app.sm_stack
        save.alldata['App']['sfx'] = app.sfx
        save.alldata['App']['ai_difficulty'] = app.ai_difficulty
        save.alldata['App']['timer'] = app.timer
        save.alldata['App']['score'] = app.score
        save.alldata['App']['unlocked_achievements'] = app.unlocked_achievements
        if app.previous_games['Threes'] not in save.alldata['Games']['Previous_Games']['Threes'] and save.alldata['Games']['Previous_Games']['Threes']:
            save.alldata['Games']['Previous_Games']['Threes'].append(app.previous_games['Threes']) 
            save.calc_threes_stats()
        if app.previous_games['Rummy'] not in save.alldata['Games']['Previous_Games']['Rummy'] and save.alldata['Games']['Previous_Games']['Rummy']:
            save.alldata['Games']['Previous_Games']['Rummy'].append(app.previous_games['Rummy']) 
            save.calc_rummy_stats()
        if app.previous_games['Memory'] not in save.alldata['Games']['Previous_Games']['Memory'] and save.alldata['Games']['Previous_Games']['Memory']:
            save.alldata['Games']['Previous_Games']['Memory'].append(app.previous_games['Memory']) 
            save.calc_memory_stats()
        save.alldata['Games']['Current_Games']['Threes'] = threes.state
        save.alldata['Games']['Current_Games']['Rummy'] = rummy.state
        save.alldata['Games']['Current_Games']['Memory'] = memory.state
        with open(r"MobilePlayingCardApp\player_data.json", "w") as f:
            json.dump(save.alldata, f, indent=4)

    def load(save):
        with open(r"MobilePlayingCardApp\player_data.json", "r") as f:
            save.alldata = json.load(f)
        return save.alldata
    
    def update(save, app):
        shop = app.shop
        shop.equipped = save.alldata['Shop']['equipped']
        shop.unlocked_inventory = save.alldata['Shop']['unlocked_inventory']
        shop.coin_count = save.alldata['Shop']['coin_count']
        app.sm_stack = save.alldata['App']['sm_stack']
        app.sfx = save.alldata['App']['sfx']
        app.ai_difficulty = save.alldata['App']['ai_difficulty']
        app.timer = save.alldata['App']['timer']
        app.score = save.alldata['App']['score']
        app.unlocked_achievements = save.alldata['App']['unlocked_achievements']
        app.threes.state = save.alldata['Games']['Current_Games']['Threes']
        app.rummy.state = save.alldata['Games']['Current_Games']['Rummy']
        app.memory.state = save.alldata['Games']['Current_Games']['Memory']

    def test_all_stats(save):
        print("\n===== TESTING ALL STAT FUNCTIONS =====\n")
        fake_threes_game = {'winner': 0,'history': [(0,"3D","play"),(1,"7H","pickup"),(0,"3H","play")],'difficulty': (0,"Beginner"),'time': 42}
        save.alldata['Games']['Previous_Games']['Threes'].append(fake_threes_game)
        print("Running calc_threes_stats() ...")
        save.calc_threes_stats()
        print("Threes General Stats:", save.alldata['Games']['Stats']['Threes_Stats']['General_Stats'])
        print("Threes Beginner Stats:", save.alldata['Games']['Stats']['Threes_Stats']['Beginner'])
        print()
        fake_rummy_game = {'winner': 0,'history': [("Play","AD"),("Pickup","3H"),("Play","7C")],'difficulty': (0,"Easy"),'time': 55}
        save.alldata['Games']['Previous_Games']['Rummy'].append(fake_rummy_game)
        print("Running calc_rummy_stats() ...")
        save.calc_rummy_stats()
        print("Rummy General Stats:", save.alldata['Games']['Stats']['Rummy_Stats']['General_Stats'])
        print("Rummy Easy Stats:", save.alldata['Games']['Stats']['Rummy_Stats']['Easy'])
        print()
        fake_memory_game = {'winner': 0,'history': [("Matched", 0, ("5H","5H")),("Matched", 0, ("7C","7C")),("Flip",1,"2D")],'difficulty': (0,"Normal"),'time': 33}
        save.alldata['Games']['Previous_Games']['Memory'].append(fake_memory_game)
        print("Running calc_memory_stats() ...")
        save.calc_memory_stats()
        print("Memory General Stats:", save.alldata['Games']['Stats']['Memory_Stats']['General_Stats'])
        print("Memory Normal Stats:", save.alldata['Games']['Stats']['Memory_Stats']['Normal'])
        print()
        print("===== TEST COMPLETE =====\n")


