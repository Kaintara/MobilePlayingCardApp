from datetime import datetime
import json

class SaveData():
    def __init__(save):
        #Create a template for which all neccessary game data can be saved in
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
                    'threesStats' : {
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
                    'rummy_Stats' : {
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
                    'memory_Stats' : {
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
                    'threes' : [],
                    'rummy' : [],
                    'memory' : []
                },
                'Current_Games' :
                {'threes': {'name' : "threes",
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
                 'rummy': {'name' : "rummy",
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
                 'memory': {'name' : "memory",
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

    def calc_threes_stats(save):
        Game = save.alldata['Games']['Previous_Games']['threes'][-1] #Returns the game data of the most recent Threes game
        difficulty = Game['difficulty'][1]
        Difficulty_Stats = save.alldata['Games']['Stats']['threes_Stats'][difficulty]
        All_Stats = save.alldata['Games']['Stats']['threes_Stats']['General_Stats']
        #Adds one to the games played in the all time stats and the stats for that specfic difficulty 
        All_Stats["games_played"] += 1
        Difficulty_Stats["games_played"] += 1
        if Game['winner'] == 0: #Checks if the user won
            #Adds one the user's wins in the all time stats and the stats for that specfic difficulty
            All_Stats["wins"] += 1
            Difficulty_Stats["wins"] += 1
            threes = [(0,"3D","play"),(0,"3H","play"),(0,"3S","play"),(0,"3C","play")]
            if Game['history'][-1] in threes: #Checks if the user won with a 3
                #Adds won with a 3 to the game stats
                All_Stats["won_with_3"] += 1
        if All_Stats["games_played"] > 0: #Checks the user has played more than one game
            All_Stats["win_lose_ratio"] = f"{round((All_Stats['wins']/All_Stats['games_played'])*100, 2)}%" #Calculates the user's win rate
        for move in Game['history']: #Iterates through each move in the game
            if move[2] == 'pickup' and move[0] == 0: #Checks if the move is a pickup and it was the user's move
                All_Stats["amount_of_pickups"] += 1 #Increments the number of times the user picked up cards
        if Difficulty_Stats["best_time"] is None or Difficulty_Stats["best_time"] > Game['time']: #Checks if the player has a best time or their most recent time is lower then their recorded best time for that particular difficulty
            Difficulty_Stats["best_time"] = Game['time'] #Updates the best time
            if All_Stats["best_time"] is None or All_Stats["best_time"] > Game['time']: #Checks if the player has a best time or their most recent time is lower then their recorded best time over all games
                All_Stats["best_time"] = Game['time'] #Updates the best time
        All_Stats['total_time'] += Game['time'] #Updates the overall time the player has spent
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Gets the current time and formats it
        #Adds the current time to the relevant stats last played section
        All_Stats["last_played"] = now
        Difficulty_Stats["last_played"] = now

    def calc_rummy_stats(save):
        Game = save.alldata['Games']['Previous_Games']['rummy'][-1] #Returns the game data of the most recent rummy game
        difficulty = Game['difficulty'][1]
        Difficulty_Stats = save.alldata['Games']['Stats']['rummy_Stats'][difficulty]
        All_Stats = save.alldata['Games']['Stats']['rummy_Stats']['General_Stats']
        #Adds one to the games played in the all time stats and the stats for that specfic difficulty 
        All_Stats["games_played"] += 1
        Difficulty_Stats["games_played"] += 1
        if Game['winner'] == 0: #Checks if the user won
            #Adds one the user's wins in the all time stats and the stats for that specfic difficulty
            All_Stats["wins"] += 1
            Difficulty_Stats["wins"] += 1
        if All_Stats["games_played"] > 0: #Checks the user has played more than one game
            All_Stats["win_lose_ratio"] = f"{round((All_Stats['wins']/All_Stats['games_played'])*100, 2)}%" #Calculates user's win rate
        if Difficulty_Stats["best_time"] is None or Difficulty_Stats["best_time"] > Game['time']: #Checks if the player has a best time or their most recent time is lower then their recorded best time for that particular difficulty
            Difficulty_Stats["best_time"] = Game['time'] #Updates the best time
            if All_Stats["best_time"] is None or All_Stats["best_time"] > Game['time']: #Checks if the player has a best time or their most recent time is lower then their recorded best time over all games
                All_Stats["best_time"] = Game['time'] #Updates the best time
        All_Stats['total_time'] += Game['time'] #Updates the overall time the player has spent
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Gets the current time and formats it
        #Adds the current time to the relevant stats last played section
        All_Stats["last_played"] = now
        Difficulty_Stats["last_played"] = now

    def calc_memory_stats(save):
        Game = save.alldata['Games']['Previous_Games']['memory'][-1] #Returns the game data of the most recent memory game
        difficulty = Game['difficulty'][1]
        Difficulty_Stats = save.alldata['Games']['Stats']['memory_Stats'][difficulty]
        All_Stats = save.alldata['Games']['Stats']['memory_Stats']['General_Stats']
        #Adds one to the games played in the all time stats and the stats for that specfic difficulty 
        All_Stats["games_played"] += 1
        Difficulty_Stats["games_played"] += 1
        if Game['winner'] == 0: #Checks if the user has won
            #Adds one the user's wins in the all time stats and the stats for that specfic difficulty
            All_Stats["wins"] += 1
            Difficulty_Stats["wins"] += 1
        if All_Stats["games_played"] > 0: #Checks the user has played more than one game
            All_Stats["win_lose_ratio"] = f"{round((All_Stats['wins']/All_Stats['games_played'])*100, 2)}%" #Calculates the user's win rate
        pair_count = 0
        for move in Game['history']: #Iterates through each move in the game
            if move[1] == 0 and move[0] == "Matched": #Checks if the move was a match and it was the user's move
                pair_count += 1 #Increments the number of pair for that game
                All_Stats["all_pairs"] += 1 #Increments the number of pairs over all games
        if Difficulty_Stats["most_pairs"] < pair_count: #Checks if number pairs is greater than user's record for that difficulty
            Difficulty_Stats["most_pairs"] = pair_count #Updates pair count
            if All_Stats["most_pairs"] < pair_count: #Checks if number pairs is greater than user's record over all games
                All_Stats["most_pairs"] = pair_count #Updates pair count
        if Difficulty_Stats["best_time"] is None or Difficulty_Stats["best_time"] > Game['time']:  #Checks if the player has a best time or their most recent time is lower then their recorded best time for that particular difficulty
            Difficulty_Stats["best_time"] = Game['time'] #Updates the best time
            if All_Stats["best_time"] is None or All_Stats["best_time"] > Game['time']: #Checks if the player has a best time or their most recent time is lower then their recorded best time over all games
                All_Stats["best_time"] = Game['time'] #Updates the best time
        All_Stats['total_time'] += Game['time'] #Updates the overall time the player has spent
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Gets the current time and formats it
        #Adds the current time to the relevant stats last played section
        All_Stats["last_played"] = now
        Difficulty_Stats["last_played"] = now

    def savedata(save, app, threes, rummy, memory, shop):
        #Updates all the major changes in different classes to the save data dictionary
        save.alldata['Shop']['equipped'] = shop.equipped
        save.alldata['Shop']['unlocked_inventory'] = shop.unlocked_inventory
        save.alldata['Shop']['coin_count'] = shop.coin_count
        save.alldata['App']['sm_stack'] = app.sm_stack
        save.alldata['App']['sfx'] = app.sfx
        save.alldata['App']['ai_difficulty'] = app.ai_difficulty
        save.alldata['App']['timer'] = app.timer
        save.alldata['App']['score'] = app.score
        save.alldata['App']['unlocked_achievements'] = app.unlocked_achievements
        if app.previous_games['threes']: #Checks if a threes game was recently completed 
            last_game = app.previous_games['threes'][-1]
            save.alldata['Games']['Previous_Games']['threes'].append(last_game) #Adds game to the save data
            save.calc_threes_stats() #Updates the game stats based on this game
        if app.previous_games['rummy']: #Checks if a rummy game was recently completed 
            last_game = app.previous_games['rummy'][-1]
            save.alldata['Games']['Previous_Games']['rummy'].append(last_game) #Adds game to the save data
            save.calc_rummy_stats() #Updates the game stats based on this game
        if app.previous_games['memory']: #Checks if a memory game was recently completed 
            last_game = app.previous_games['memory'][-1]
            save.alldata['Games']['Previous_Games']['memory'].append(last_game) #Adds game to the save data
            save.calc_memory_stats() #Updates the game stats based on this game
        #Updates all the current game states in the savedata dictionary
        save.alldata['Games']['Current_Games']['threes'] = threes.state
        save.alldata['Games']['Current_Games']['rummy'] = rummy.state
        save.alldata['Games']['Current_Games']['memory'] = memory.state
        with open(r"MobilePlayingCardApp\player_data.json", "w") as f: #Opens player save file in write mode
            json.dump(save.alldata, f, indent=4) #Writes the save data to the save file as a JSON object

    def load(save):
        with open(r"MobilePlayingCardApp\player_data.json", "r") as f: #Opens player save file in read mode
            save.alldata = json.load(f) #Loads the save data and converts from a JSON object to a python dictionary
        return save.alldata
    
    def quick_save(save,app):
        #Updates minor changes to the game into the player's save data
        save.alldata['App']['timer'] = app.timer
        save.alldata['App']['sfx'] = app.sfx
        save.alldata['Shop']['equipped'] = app.shop.equipped
        save.alldata['Shop']['unlocked_inventory'] = app.shop.unlocked_inventory
        save.alldata['Shop']['coin_count'] = app.shop.coin_count
        save.alldata['Games']['Current_Games']['threes'] = app.threes.state
        save.alldata['Games']['Current_Games']['rummy'] = app.rummy.state
        save.alldata['Games']['Current_Games']['memory'] = app.memory.state
        with open(r"MobilePlayingCardApp\player_data.json", "w") as f: #Opens player save file in write mode
            json.dump(save.alldata, f, indent=4) #Writes the save data to the save file as a JSON object

    def load_game_states(save, app):
        save.load() #Loads the current save data
        #Updates all relevant attributes to match the given game states
        #Threes
        app.threes.state = save.alldata['Games']['Current_Games']['threes']
        app.threes.shuffled_deck = app.threes.state['shuffled_deck']
        app.threes.hands = app.threes.state['hands']
        app.threes.discard_pile = app.threes.state['discard_pile']
        app.threes.selected_card = app.threes.state['selected_card']
        app.threes.bottom_hands = app.threes.state['bottom_hands']
        app.threes.top_hands = app.threes.state['top_hands']
        app.threes.played_cards = app.threes.state['played_cards']
        app.threes.another = app.threes.state['another']
        app.threes.turn = app.threes.state['turn']
        app.threes.time_elapsed = app.threes.state['time_elapsed']
        app.threes.difficulty = app.threes.state['difficulty']
        #Rummy
        app.rummy.state = save.alldata['Games']['Current_Games']['rummy']
        app.threes.winner = app.threes.state['winner']
        app.rummy.shuffled_deck = app.rummy.state['shuffled_deck']  
        app.rummy.hands = app.rummy.state['hands'] 
        app.rummy.discard_pile = app.rummy.state['discard_pile']
        app.rummy.selected_card = app.rummy.state['selected_card']
        app.rummy.turn = app.rummy.state['turn']
        app.rummy.time_elapsed = app.rummy.state['time_elapsed']
        app.rummy.difficulty = app.rummy.state['difficulty']
        app.rummy.winner = app.rummy.state['winner']
        #Memory
        app.memory.state = save.alldata['Games']['Current_Games']['memory']
        app.memory.hands = app.memory.state['hands']
        app.memory.shuffled_deck = app.memory.state['shuffled_deck']
        app.memory.card_array = app.memory.state['card_array']
        app.memory.first_selected_card = app.memory.state['first_selected_card']
        app.memory.second_selected_card = app.memory.state['second_selected_card']
        app.memory.selected_first_card = app.memory.state['selected_first_card']
        app.memory.turn = app.memory.state['turn']
        app.memory.time_elapsed = app.memory.state['time_elapsed']
        app.memory.difficulty = app.memory.state['difficulty']
        app.memory.winner = app.memory.state['winner']
    
    def update(save, app):
        save.load() #Loads the current save data
        shop = app.shop
        #Updates all relevant attributes to match the given save data
        shop.equipped = save.alldata['Shop']['equipped']
        shop.unlocked_inventory = save.alldata['Shop']['unlocked_inventory']
        shop.coin_count = save.alldata['Shop']['coin_count']
        app.sm_stack = save.alldata['App']['sm_stack']
        app.sfx = save.alldata['App']['sfx']
        app.ai_difficulty = save.alldata['App']['ai_difficulty']
        app.timer = save.alldata['App']['timer']
        app.score = save.alldata['App']['score']
        app.unlocked_achievements = save.alldata['App']['unlocked_achievements']
        app.threes.state = save.alldata['Games']['Current_Games']['threes']
        app.rummy.state = save.alldata['Games']['Current_Games']['rummy']
        app.memory.state = save.alldata['Games']['Current_Games']['memory']
        #Updates all the current game states to match the save data
        save.load_game_states(app)


test_save = SaveData() #Initialises a save data object
print("SaveData class initialised:",test_save,"\nSave data template:",test_save.alldata)
