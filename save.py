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
                     'unlocked_achivements' : []
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
                        "best_time": 0,
                        "total_time": 0,
                        "last_played": None
                        },  
                        'Beginner' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Easy' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Normal' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Hard' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Expert' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                    },
                    'Rummy_Stats' : {
                        'General_Stats' : {
                        "games_played": 0,
                        "wins": 0,
                        "win_lose_ratio": 0,
                        "best_time": 0,
                        "total_time": 0,
                        "last_played": None
                        },
                        'Beginner' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Easy' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Normal' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Hard' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Expert' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                    },
                    'Memory_Stats' : {
                        'General_Stats' : {
                        "games_played": 0,
                        "wins": 0,
                        "win_lose_ratio": 0,
                        "best_pairs": 0,
                        "all_pairs": 0,
                        "best_time": 0,
                        "total_time": 0,
                        "last_played": None
                    },
                        'Beginner' : {
                            "games_played": 0,
                            "wins": 0,
                            "most"
                            "best_time": 0,
                            "last_played": None
                        },
                        'Easy' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Normal' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Hard' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                        'Expert' : {
                            "games_played": 0,
                            "wins": 0,
                            "best_time": 0,
                            "last_played": None
                        },
                    },
                },
                'Previous_Games' : {   #Format = {'winner': None,'history': {},'difficulty' : (-1,"")}
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

    def calc_threes_stats(save):
        Games = save.alldata['Games']['Previous_Games']['Threes']

    def calc_rummy_stats(save):
        pass

    def calc_memory_stats(save):
        pass

    def savedata(save, app, threes, rummy, memory, shop):
        save.alldata['Shop']['equipped'] = shop.equipped
        save.alldata['Shop']['unlocked_inventory'] = shop.unlocked_inventory
        save.alldata['Shop']['coin_count'] = shop.coin_count
        save.alldata['App']['sm_stack'] = app.sm_stack
        save.alldata['App']['sfx'] = app.sfx
        save.alldata['App']['ai_difficulty'] = app.ai_difficulty
        save.alldata['App']['timer'] = app.timer
        save.alldata['App']['score'] = app.score
        save.alldata['App']['unlocked_achivements'] = app.unlocked_achivements
        if app.previous_games['Threes'] not in save.alldata['Games']['Previous_Games']['Threes']:
            save.alldata['Games']['Previous_Games']['Threes'].append(app.previous_games['Threes']) 
        if app.previous_games['Rummy'] not in save.alldata['Games']['Previous_Games']['Rummy']:
            save.alldata['Games']['Previous_Games']['Rummy'].append(app.previous_games['Rummy']) 
        if app.previous_games['Memory'] not in save.alldata['Games']['Previous_Games']['Memory']:
            save.alldata['Games']['Previous_Games']['Memory'].append(app.previous_games['Memory']) 
        save.alldata['Games']['Stats']['Threes_Stats'] = save.calc_threes_stats()
        save.alldata['Games']['Stats']['Rummy_Stats'] = save.calc_rummy_stats()
        save.alldata['Games']['Stats']['Memory_Stats'] = save.calc_memory_stats()
        save.alldata['Current_Games']['Threes'] = threes.state
        save.alldata['Current_Games']['Rummy'] = rummy.state
        save.alldata['Current_Games']['Memory'] = memory.state


