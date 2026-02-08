from ui import * 
from save import SaveData
from game import *
from shop import *
from treesearch import *
from threesMTCS import GameEnvironmentT
from rummyMTCS import GameEnvironmentR
from memoryMTCS import GameEnvironmentM

class MobilePlayingCardApp(MDApp):
    def __init__(self, **kwargs):
        self.sm_stack = []
        self.sfx = True
        self.ai_difficulty = "Beginner"
        self.ai_difficulty_map = {
            "Beginner" : 0.15,
            "Easy" : 0.2,
            "Medium" : 0.25,
            "Hard" : 0.35,
            "Expert" : 0.5
        }
        self.timer = True
        self.score = True
        self.all_achievements = [
            (0,'The memory of a goldfish','Play your first game of memory',lambda save : save.alldata['Games']['Stats']['memory_Stats']['General_Stats']["games_played"] >= 1),
            (1,'Only Three?','Play your first game of threes',lambda save : save.alldata['Games']['Stats']['threes_Stats']['General_Stats']["games_played"] >= 1),
            (2,'Four and Three!','Play your first game of rummy',lambda save : save.alldata['Games']['Stats']['rummy_Stats']['General_Stats']["games_played"] >= 1),
            (3,'Better Luck Next Time!','Lose your first game of rummy',lambda save : bool(save.alldata['Games']["Previous_Games"]['rummy']) and save.alldata['Games']["Previous_Games"]['rummy'][-1]['winner'] == 1),
            (4,'If only you had a ten, huh?','Lose your first game of threes',lambda save : bool(save.alldata['Games']["Previous_Games"]['threes']) and save.alldata['Games']["Previous_Games"]['threes'][-1]['winner'] == 1),
            (5,'FUMBLED!','Lose your first game of memory',lambda save : bool(save.alldata['Games']["Previous_Games"]['memory']) and save.alldata['Games']["Previous_Games"]['memory'][-1]['winner'] == 0),
            (6,'Poker Player','Win your first game of rummy',lambda save : bool(save.alldata['Games']["Previous_Games"]['rummy']) and save.alldata['Games']["Previous_Games"]['rummy'][-1]['winner'] == 0),
            (7,'Uno Player','Win your first game of Three',lambda save : bool(save.alldata['Games']["Previous_Games"]['threes']) and save.alldata['Games']["Previous_Games"]['threes'][-1]['winner'] == 0),
            (8,'The memory of an elephant','Win your first game of memory',lambda save : bool(save.alldata['Games']["Previous_Games"]['memory']) and save.alldata['Games']["Previous_Games"]['memory'][-1]['winner'] == 0),
        ]
        self.unlocked_achievements = []
        self.previous_games = {
            'threes' : [],
            'rummy' : [],
            'memory' : []
        }
        AppShop = Shop()
        self.shop = AppShop
        self.shop.set_all_themes()
        AppSave = SaveData()
        self.save = AppSave
        self.threes = None
        self.rummy = None
        self.memory = None
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.theme_style_switch_animation_duration = 0.4
        Window.set_icon(("icon.png"))
        LabelBase.register(
            name="cataway",
            fn_regular="assets/Catways.ttf",
        )
        self.theme_cls.font_styles["cataway"] = {
            "large" : {
                "line-height": 1.64,
                "font-name": "cataway",
                "font-size": sp(50),
            },
            "medium": {
                "line-height": 1.2,
                "font-name": "cataway",
                "font-size": sp(20),
            },
            "small": {
                "line-height": 1.44,
                "font-name": "cataway",
                "font-size": sp(36),
            },
        }
        #Assigning Screens to Screen Manager
        sm = SM()
        sm.add_widget(MainMenu(name="Menu"))
        sm.add_widget(NewGame(name="NewGame"))
        sm.add_widget(MDThrees(name="MDThrees"))
        sm.add_widget(MDRummy(name="MDRummy"))
        sm.add_widget(MDMemory(name="MDMemory"))
        sm.add_widget(Rules(name="Rules"))
        sm.add_widget(Settings(name="Settings"))
        sm.add_widget(MDShop(name="MDShop"))
        sm.add_widget(Stats(name="Stats"))
        sm.current = "Menu"
        return sm
    
    #Methods for UI
    def get_widget(self, widget, screen):
        return self.root.get_screen(screen).ids[widget]

    def back(self): #Back button
        sm = self.root
        if self.sm_stack[0] == sm.current:
            self.sm_stack.remove(sm.current)
            sm.current = self.sm_stack[0]
        elif sm.previous:
            sm.current = self.sm_stack[0]
        else:
            sm.current = "Menu"

    def sm_stacky(self,widget): #Stores order of screens visited for back button
        if widget in self.sm_stack:
            self.sm_stack.remove(widget)
            self.sm_stack.insert(0, widget)
        else:
            self.sm_stack.insert(0, widget)
    
    def resume_game_check(self):
        savedata = self.save.load()
        G1 = savedata['Games']['Current_Games']['threes']
        G2 = savedata['Games']['Current_Games']['rummy']
        G3 = savedata['Games']['Current_Games']['memory']
        self.threes = threes('threes',G1["rank_order"],G1)
        self.rummy = rummy('rummy',G2['value_map'],G2)
        self.memory = memory('memory',G1["rank_order"],G3)
        Games = [G1,G2,G3]
        for game in Games:
            print(game['winner'],game['history'][-1] if game['history'] else "No History")
            if game['winner'] is None and game['history']:
                return "Resume Game"
        return "New Game"
        
    def get_difficulty(self):
        Carou = self.get_widget("carou","Settings")
        difficulty = Carou.current_slide.text
        if difficulty == "Beginner":
            return "Beginner"
        elif difficulty == "Easy":
            return "Easy"
        elif difficulty == "Medium":
            return "Medium"
        elif difficulty == "Hard":
            return "Hard"
        elif difficulty == "Expert":
            return "Expert"

    def calc_all_time_stats(self):
        self.save.load()
        stats = self.save.alldata["Games"]["Stats"]
        fav_game = None
        fav_game_count = 0
        total_time = 0
        total_wins = 0
        total_games = 0
        best_time = None
        for game, game_stats in stats.items():
            gen = game_stats["General_Stats"]
            if gen["games_played"] > fav_game_count:
                fav_game = game
            total_games += gen["games_played"]
            if best_time is None or gen["best_time"] < best_time:
                best_time = gen["best_time"]
            total_time += gen["total_time"]
            total_wins += gen["wins"]
        if fav_game == "rummy_Stats":
            fav_game = "Rummy"
        elif fav_game == "threes_Stats":
            fav_game = "Threes"
        elif fav_game == "memory_Stats":
            fav_game = "Memory"
        wl_ratio = round(total_wins / total_games, 2) if total_games else 0
        if not best_time:
            best_time = 0
        return {
            "Fav_Game": fav_game or "-",
            "Wins" : total_wins,
            "Best_Time": self.s_to_mmss(best_time),
            "WLRatio" : wl_ratio,
            "Total_Time": self.s_to_mmss(total_time),
            "Total_Games": total_games
        }
    
    def fill_carou(self,content,extra_content):
        scroll_box = self.get_widget('stats',"Stats")
        scroll_box.padding = sp(30)
        scroll_box.clear_widgets()
        if content == "All_Time Stats":
            stats = self.calc_all_time_stats()
            scroll_box.add_widget(Text(text=f"Favourite Game: {stats["Fav_Game"]}"))
            scroll_box.add_widget(Text(text=f"Best Time ~ {stats["Best_Time"]}"))
            scroll_box.add_widget(Text(text=f"Wins: {stats["Wins"]}"))
            scroll_box.add_widget(Text(text=f"W/L Ratio: {stats["WLRatio"]}"))
            scroll_box.add_widget(Text(text=f"Total Time ~ {stats["Total_Time"]}"))
            scroll_box.add_widget(Text(text=f"Total Games: {stats["Total_Games"]}"))
        elif content == "Achievements":
            scroll_box.padding = sp(100)
            for x in self.all_achievements:
                scroll_box.add_widget(Achievement_Container(x))
        elif content == "Threes":
            self.save.load()
            if extra_content == "Overview":
                stats = self.save.alldata["Games"]["Stats"]["threes_Stats"]["General_Stats"]
                scroll_box.add_widget(Text(text=f"Times Won With a 3: {stats["won_with_3"]}"))
                scroll_box.add_widget(Text(text=f"Games Played: {stats["games_played"]}"))
                scroll_box.add_widget(Text(text=f"Total Amount of Pickups: {stats["amount_of_pickups"]}"))
                scroll_box.add_widget(Text(text=f"Best Time ~ {stats["best_time"]}"))
                scroll_box.add_widget(Text(text=f"Wins: {stats["wins"]}"))
                scroll_box.add_widget(Text(text=f"W/L Ratio: {stats["win_lose_ratio"]}"))
                scroll_box.add_widget(Text(text=f"Total Time ~ {stats["total_time"]}"))
                scroll_box.add_widget(Text(text=f"Last Played: {stats["last_played"]}"))
            else:
                stats = self.save.alldata["Games"]["Stats"]["threes_Stats"][extra_content]
                scroll_box.add_widget(Text(text=f"Games Played: {stats["games_played"]}"))
                scroll_box.add_widget(Text(text=f"Wins: {stats["wins"]}"))
                scroll_box.add_widget(Text(text=f"Best Time ~ {stats["best_time"]}"))
                scroll_box.add_widget(Text(text=f"Last Played: {stats["last_played"]}"))
        elif content == "Rummy":
            self.save.load()
            if extra_content == "Overview":
                stats = self.save.alldata["Games"]["Stats"]["rummy_Stats"]["General_Stats"]
                scroll_box.add_widget(Text(text=f"Games Played: {stats["games_played"]}"))
                scroll_box.add_widget(Text(text=f"Best Time ~ {stats["best_time"]}"))
                scroll_box.add_widget(Text(text=f"Wins: {stats["wins"]}"))
                scroll_box.add_widget(Text(text=f"W/L Ratio: {stats["win_lose_ratio"]}"))
                scroll_box.add_widget(Text(text=f"Total Time ~ {stats["total_time"]}"))
                scroll_box.add_widget(Text(text=f"Last Played: {stats["last_played"]}"))
            else:
                stats = self.save.alldata["Games"]["Stats"]["rummy_Stats"][extra_content]
                scroll_box.add_widget(Text(text=f"Games Played: {stats["games_played"]}"))
                scroll_box.add_widget(Text(text=f"Wins: {stats["wins"]}"))
                scroll_box.add_widget(Text(text=f"Best Time ~ {stats["best_time"]}"))
                scroll_box.add_widget(Text(text=f"Last Played: {stats["last_played"]}"))
        elif content == "Memory":
            self.save.load()
            if extra_content == "Overview":
                stats = self.save.alldata["Games"]["Stats"]["memory_Stats"]["General_Stats"]
                scroll_box.add_widget(Text(text=f"Most Pairs: {stats["most_pairs"]}"))
                scroll_box.add_widget(Text(text=f"Total Pairs: {stats["all_pairs"]}"))
                scroll_box.add_widget(Text(text=f"Games Played: {stats["games_played"]}"))
                scroll_box.add_widget(Text(text=f"Best Time ~ {stats["best_time"]}"))
                scroll_box.add_widget(Text(text=f"Wins: {stats["wins"]}"))
                scroll_box.add_widget(Text(text=f"W/L Ratio: {stats["win_lose_ratio"]}"))
                scroll_box.add_widget(Text(text=f"Total Time ~ {stats["total_time"]}"))
                scroll_box.add_widget(Text(text=f"Last Played: {stats["last_played"]}"))
            else:
                stats = self.save.alldata["Games"]["Stats"]["memory_Stats"][extra_content]
                scroll_box.add_widget(Text(text=f"Most Pairs: {stats["most_pairs"]}"))
                scroll_box.add_widget(Text(text=f"Games Played: {stats["games_played"]}"))
                scroll_box.add_widget(Text(text=f"Wins: {stats["wins"]}"))
                scroll_box.add_widget(Text(text=f"Best Time ~ {stats["best_time"]}"))
                scroll_box.add_widget(Text(text=f"Last Played: {stats["last_played"]}"))

    def determine_contents(self,content):
        extra = "Overview"
        conditionalcarou = self.get_widget("conditionalcarou","Stats")
        if content == "All_Time Stats" or content == "Achievements":
            conditionalcarou.clear_widgets()
            conditionalcarou.add_widget(Text(text="N/A"))
            bl = self.get_widget("bottom_left","Stats")
            br = self.get_widget("bottom_right","Stats")
            bl.disabled = True
            br.disabled = True
        elif content == "Threes" or content == "Rummy" or content == "Memory":
            conditionalcarou.clear_widgets()
            conditionalcarou.add_widget(Text(text="Overview"))
            conditionalcarou.add_widget(Text(text="Beginner"))
            conditionalcarou.add_widget(Text(text="Easy"))
            conditionalcarou.add_widget(Text(text="Normal"))
            conditionalcarou.add_widget(Text(text="Hard"))
            conditionalcarou.add_widget(Text(text="Expert"))
            bl = self.get_widget("bottom_left","Stats")
            br = self.get_widget("bottom_right","Stats")
            bl.disabled = False
            br.disabled = False
        elif content in ["Beginner","Easy","Normal","Hard","Expert","Overview"]:
            extra = content
            content = self.get_widget('carou','Stats').current_slide.text
        self.fill_carou(content,extra)

    def left(self,Screen):
        if Screen == "Con_Stats":
            ID = 'conditionalcarou'
            screen = "Stats"
        else:
            ID = "carou"
            screen = Screen
        Carou = self.get_widget(ID,screen)
        Carou.load_previous()
        if Screen == "Stats" or Screen == "Con_Stats":
            content = Carou.previous_slide.text
            self.determine_contents(content)
        
    def right(self,Screen):
        if Screen == "Con_Stats":
            ID = 'conditionalcarou'
            screen = "Stats"
        else:
            ID = "carou"
            screen = Screen
        Carou = self.get_widget(ID,screen)
        Carou.load_next()
        if Screen == "Stats" or Screen == "Con_Stats":
            content = Carou.next_slide.text
            self.determine_contents(content)

    def set_up_shop(self):
        self.shop.filling_shop_inventory(self)
        Grid = self.get_widget("grid",'MDShop')

    def s_to_mmss(self,total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_game(self,game):
        if game == "threes":
            timer = self.get_widget('timer','MDThrees')
            timer.text = self.s_to_mmss(self.threes.time_elapsed)
            for i in range(3):
                Ai_hand = self.get_widget(f'ai_hand{i + 1}', 'MDThrees')
                Ai_hand.clear_widgets()
                hand = self.get_widget(f'hand{i + 1}', 'MDThrees')
                hand.clear_widgets()
            for i in range(len(self.threes.bottom_hands[1])):
                Ai_hand = self.get_widget(f'ai_hand{i + 1}', 'MDThrees')
                Ai_hand.add_widget(Display_Card(self.threes.bottom_hands[1][i], 'back'))
            for i in range(len(self.threes.top_hands[1])):
                Ai_hand = self.get_widget(f'ai_hand{i + 1}', 'MDThrees')
                card = Display_Card(self.threes.top_hands[1][i], 'front')
                card.pos_hint = {"center_x": 0.6, "center_y": 0.5}
                Ai_hand.add_widget(card)
            deck = self.get_widget('deck', 'MDThrees')
            deck.clear_widgets()
            if self.threes.played_cards:
                deck.add_widget(Playing_Card(self.threes.played_cards[-1],'threes','front'))
            if self.threes.shuffled_deck:
                card = Display_Card(self.threes.shuffled_deck[-1],'back')
                card.pos_hint = {"center_x": 1.5, "center_y": 0.5}
                deck.add_widget(card)
            for i in range(len(self.threes.bottom_hands[0])):
                hand = self.get_widget(f'hand{i + 1}', 'MDThrees')
                hand.add_widget(Playing_Card(self.threes.bottom_hands[0][i], 'threes','back'))
            for i in range(len(self.threes.top_hands[0])):
                hand = self.get_widget(f'hand{i + 1}', 'MDThrees')
                card = Playing_Card(self.threes.top_hands[0][i],'threes','front')
                card.pos_hint = {"center_x": 0.6, "center_y": 0.5}
                hand.add_widget(card)
            hand = self.get_widget('hand', 'MDThrees')
            hand.clear_widgets()
            if self.threes.hands[0]:
                self.threes.hands[0].sort(key=lambda card: self.threes.rank_order[card[:-1]], reverse=True)
            for card in self.threes.hands[0]:
                hand.add_widget(Playing_Card(card,'threes','front'))
        elif game == "rummy":
            timer = self.get_widget('timer','MDRummy')
            timer.text = self.s_to_mmss(self.rummy.time_elapsed)
            for i in range(8):
                Ai_hand = self.get_widget(f'ai_hand{i + 1}', 'MDRummy')
                Ai_hand.clear_widgets()
                if i < len(self.rummy.hands[1]):
                    Ai_hand.add_widget(Display_Card(self.rummy.hands[1][i], 'back'))
            deck = self.get_widget('deck', 'MDRummy')
            deck.clear_widgets()
            if self.rummy.discard_pile:
                deck.add_widget(Playing_Card(self.rummy.discard_pile[-1],'rummy','front'))
            if self.rummy.shuffled_deck:
                card = Playing_Card(self.rummy.shuffled_deck[-1],'rummy','back')
                card.pos_hint = {"center_x": 1.5, "center_y": 0.5}
                deck.add_widget(card)
            for i in range(8):
                hand = self.get_widget(f'hand{i + 1}', 'MDRummy')
                hand.clear_widgets()
            for i in range(len(self.rummy.hands[0])):
                hand = self.get_widget(f'hand{i + 1}', 'MDRummy')
                hand.add_widget(Playing_Card(self.rummy.hands[0][i], 'rummy','front'))
        elif game == "memory":
            timer = self.get_widget('timer','MDMemory')
            timer.text = self.s_to_mmss(self.memory.time_elapsed)
            hand = self.get_widget('hand', 'MDMemory')
            hand.clear_widgets()
            for card in self.memory.hands[0]:
                hand.add_widget(Display_Card(card,'front'))
            Ai_hand = self.get_widget('ai_hand', 'MDMemory')
            Ai_hand.clear_widgets()
            for card in self.memory.hands[1]:
                Ai_hand.add_widget(Display_Card(card,'front'))
            for y in range(9):
                for x in range(6):
                    hand = self.get_widget(f'hand{y}{x}', 'MDMemory')
                    hand.clear_widgets()
                    if not self.memory.card_array[y][x]:
                        continue
                    else:
                        hand = self.get_widget(f'hand{y}{x}', 'MDMemory')
                        if (self.memory.first_selected_card[0] == y and self.memory.first_selected_card[1] == x):
                            hand.add_widget(Playing_Card(self.memory.card_array[y][x], 'memory', 'front'))
                        else:
                            hand.add_widget(Playing_Card(self.memory.card_array[y][x],'memory','back'))

    def next_turn(self,game):
        self.update_game(game)
        if game == 'threes':
            self.threes.selected_card = "" 
            self.threes.update_game_state()
            if self.threes.turn == 1:
                move = m_mtcs(self.threes.state,GameEnvironmentT(),self.threes.difficulty[0])
                moves = self.threes.get_valid_moves()
                if all(m[2] == 'try' for m in moves):
                    move = random.choice(moves)
                print(f"Move{move}")
                print(self.threes.hands[1])
                self.threes.apply_move(move)
                self.threes.update_game_state()
                self.threes.turn = self.threes.next_vaild_player(self.threes.turn,self.save)
                print(f"Turn: {self.threes.turn}")
                self.save.quick_save(self)
                if self.threes.turn is None:
                    print('Line 351 main.py reached')
                    self.threes.end_game(self)
                elif self.threes.turn == 1:
                    Clock.schedule_once(lambda dt: self.next_turn('threes'), 0.5)
                self.update_game(game)
        elif game == 'rummy':
            self.rummy.selected_card = "" 
            self.rummy.update_game_state()
            if self.rummy.turn == 1:
                move = m_mtcs(self.rummy.state,GameEnvironmentR(),self.threes.difficulty[0])
                print(f"Move{move}")
                self.rummy.apply_move(move)
                self.rummy.update_game_state()
                self.rummy.turn = self.rummy.next_vaild_player(self.rummy.turn)
                print(f"Turn: {self.rummy.turn}")
                self.save.quick_save(self)
                if self.rummy.turn is None:
                    print('Line 308 main.py reached')
                    self.rummy.end_game(self)
                else:
                    Clock.schedule_once(lambda dt: self.next_turn('rummy'), 0.5)
        elif game == 'memory':
            self.memory.selected_card = "" 
            self.memory.update_game_state()
            print("Turn: ",self.memory.turn)
            if self.memory.turn == 1:
                move = m_mtcs(self.memory.state,GameEnvironmentM(),self.memory.difficulty[0])
                print("Move: ",move)
                self.memory.apply_move(move,self)
                self.memory.update_game_state()
                if self.memory.state['history']:
                    if self.memory.state['history'][-1][0] == "Missed" or self.memory.state['history'][-1][0] == "Matched":
                        y = self.memory.state['history'][-1][3][0]
                        x = self.memory.state['history'][-1][3][1]
                        card_container = self.get_widget(f'hand{y}{x}','MDMemory')
                        card = card_container.children[0]
                        card.img.source = self.shop.get_theme(self.shop.equipped).asset_dict[card.suit_rank]
                self.save.quick_save(self)
                if self.memory.is_game_over():
                    print('Game OVERRE')
                else:
                    Clock.schedule_once(lambda dt: self.next_turn('memory'), 2.0)

    def new_game(self,game):
        if game == "threes":
            self.threes = threes("threes",rank_order = {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,
'5': 5,'4': 4,'3': 3,'2': 15},
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
        'history': []})
            self.threes.difficulty = (self.ai_difficulty_map[self.get_difficulty()],self.get_difficulty())
            self.threes.shuffle_cards()
            self.threes.distribute_cards()
            self.threes.update_game_state()
            self.update_game(game)
            print(f"Threes State: {self.threes.state}")
            self.threes.turn = random.randint(0,1)
            self.next_turn(game)
        elif game == "rummy":
            self.rummy = rummy('rummy',{'A': 1,'K': 13,'Q': 12,'J': 11,'1': 10,'9': 9,'8': 8,'7': 7,'6': 6,
'5': 5,'4': 4,'3': 3,'2': 2},{'name' : "rummy",
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
        'history': []})
            self.rummy.difficulty = (self.ai_difficulty_map[self.get_difficulty()],self.get_difficulty())
            self.rummy.shuffle_cards()
            self.rummy.turn = random.randint(0,1)
            self.rummy.distribute_cards()
            self.rummy.update_game_state()
            print(f"Rummy State: {self.rummy.state}")
            self.update_game(game)
            self.next_turn(game)
        elif game == "memory":
            self.memory = memory("memory",'rank',{'name' : "memory",
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
        'history': []})
            self.memory.difficulty = (self.ai_difficulty_map[self.get_difficulty()],self.get_difficulty())
            self.memory.shuffle_cards()
            self.memory.distribute_cards()
            self.memory.update_game_state()
            self.update_game(game)
            self.memory.turn = random.randint(0,1)
            print(f"Memory State: {self.memory.state}")
            self.next_turn(game)
    
    def resume_game(self,game):
        self.save.update(self)
        self.update_game(game)
        if game == "threes" and self.threes.state['history'] and self.threes.winner is None:
            if self.threes.is_game_over():
                self.threes.end_game(self)
            if self.threes.turn == 1:
                Clock.schedule_once(lambda dt: self.next_turn('threes'), 0.5)
        elif game == "rummy" and self.rummy.state['history'] and self.rummy.winner is None:
            if self.rummy.is_game_over():
                self.rummy.end_game(self)
            if self.rummy.turn == 1:
                Clock.schedule_once(lambda dt: self.next_turn('rummy'), 0.5)
        elif game == "memory" and self.memory.state['history'] and self.memory.winner is None:
            if self.memory.is_game_over():
                self.memory.end_game(self)
            if self.memory.turn == 1:
                Clock.schedule_once(lambda dt: self.next_turn('memory'), 0.5)
        else:
            self.new_game(game)
    def start_game(self,game):
        if self.resume_game_check() == "Resume Game":
            print(game)
            self.resume_game(game)
        elif game == "threes":
            self.new_game("threes")
        elif game == "rummy":
            self.new_game("rummy")
        elif game == "memory":
            self.new_game("memory")

    def on_start(self):
        self.save.update(self)
        self.determine_contents("All_Time Stats")

if __name__ == "__main__":
    MobilePlayingCardApp().run()
