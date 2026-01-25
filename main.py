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
                "line-height": 1.52,
                "font-name": "cataway",
                "font-size": sp(45),
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
        sm.add_widget(Pause(name="Pause"))
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

    def determine_contents(self,content):
        conditionalcarou = self.get_widget("conditionalcarou","Stats")
        if content == "All_Time Stats" or content == "Achievements":
            conditionalcarou.clear_widgets()
            conditionalcarou.add_widget(MDLabel(text="N/A",font_style="cataway",role="small",halign="center",valign="center"))
            bl = self.get_widget("bottom_left","Stats")
            br = self.get_widget("bottom_right","Stats")
            bl.disabled = True
            br.disabled = True
        elif content == "Threes":
            conditionalcarou.clear_widgets()
            conditionalcarou.add_widget(MDLabel(text="N/A",font_style="cataway",role="small",halign="center",valign="center"))
            bl = self.get_widget("bottom_left","Stats")
            br = self.get_widget("bottom_right","Stats")
            bl.disabled = False
            br.disabled = False
        elif content == "Rummy":
            pass
        elif content == "Memory":
            pass

    def left(self,Screen):
        Carou = self.get_widget("carou",Screen)
        Carou.load_previous()
        if Screen == "Stats":
            content = Carou.current_slide.text
            self.determine_contents(content)
        

    def right(self,Screen):
        Carou = self.get_widget("carou",Screen)
        Carou.load_next()
        if Screen == "Stats":
            content = Carou.current_slide.text
            self.determine_contents(content)
        

    def on_start(self):
        pass

    def set_up_shop(self):
        self.shop.filling_shop_inventory(self)
        Grid = self.get_widget("grid",'MDShop')
        print("outputted card")

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
                if self.get_difficulty() == "Beginner":
                    move = m_mtcs(self.threes.state,GameEnvironmentT(),0.15)
                    moves = self.threes.get_valid_moves()
                    if all(m[2] == 'try' for m in moves):
                            move = random.choice(moves)
                    print(move)
                    self.threes.apply_move(move)
                    self.threes.update_game_state()
                elif self.get_difficulty() == "Easy":
                    move = m_mtcs(self.threes.state,GameEnvironmentT(),0.2)
                    moves = self.threes.get_valid_moves()
                    if all(m[2] == 'try' for m in moves):
                            move = random.choice(moves)
                    self.threes.apply_move(move)
                    self.threes.update_game_state()
                elif self.get_difficulty() == "Medium":
                    move = m_mtcs(self.threes.state,GameEnvironmentT(),0.25)
                    moves = self.threes.get_valid_moves()
                    if all(m[2] == 'try' for m in moves):
                            move = random.choice(moves)
                    self.threes.apply_move(move)
                    self.threes.update_game_state()
                elif self.get_difficulty() == "Hard":
                    move = m_mtcs(self.threes.state,GameEnvironmentT(),0.35)
                    moves = self.threes.get_valid_moves()
                    if all(m[2] == 'try' for m in moves):
                            move = random.choice(moves)
                    self.threes.apply_move(move)
                    self.threes.update_game_state()
                elif self.get_difficulty() == "Expert":
                    move = m_mtcs(self.threes.state,GameEnvironmentT(),0.5)
                    moves = self.threes.get_valid_moves()
                    if all(m[2] == 'try' for m in moves):
                            move = random.choice(moves)
                    self.threes.apply_move(move)
                    self.threes.update_game_state()
                self.threes.turn = self.threes.next_vaild_player(self.threes.turn,self.save)
                print(self.threes.turn)
                self.save.quick_save(self)
                if self.threes.turn is None:
                    print('Line 231 main.py reached')
                    self.threes.end_game(self)
                else:
                    Clock.schedule_once(lambda dt: self.next_turn('threes'), 0.5)
        elif game == 'rummy':
            self.rummy.selected_card = "" 
            self.rummy.update_game_state()
            if self.rummy.turn == 1:
                if self.get_difficulty() == "Beginner":
                    move = m_mtcs(self.rummy.state,GameEnvironmentR(),0.15)
                    print(move)
                    self.rummy.apply_move(move)
                    self.rummy.update_game_state()
                elif self.get_difficulty() == "Easy":
                    move = m_mtcs(self.rummy.state,GameEnvironmentR(),0.2)
                    self.rummy.apply_move(move)
                    self.rummy.update_game_state()
                elif self.get_difficulty() == "Medium":
                    move = m_mtcs(self.rummy.state,GameEnvironmentR(),0.25)
                    self.rummy.apply_move(move)
                    self.rummy.update_game_state()
                elif self.get_difficulty() == "Hard":
                    move = m_mtcs(self.rummy.state,GameEnvironmentR(),0.35)
                    self.rummy.apply_move(move)
                    self.rummy.update_game_state()
                elif self.get_difficulty() == "Expert":
                    move = m_mtcs(self.rummy.state,GameEnvironmentR(),0.5)
                    self.rummy.apply_move(move)
                    self.rummy.update_game_state()
                self.rummy.turn = self.rummy.next_vaild_player(self.rummy.turn)
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
                if self.get_difficulty() == "Beginner":
                    move = m_mtcs(self.memory.state,GameEnvironmentM(),0.15)
                    print("Move: ",move)
                    self.memory.apply_move(move,self)
                    self.memory.update_game_state()
                elif self.get_difficulty() == "Easy":
                    move = m_mtcs(self.memory.state,GameEnvironmentM(),0.2)
                    self.memory.apply_move(move,self)
                    self.memory.update_game_state()
                elif self.get_difficulty() == "Medium":
                    move = m_mtcs(self.memory.state,GameEnvironmentM(),0.25)
                    self.memory.apply_move(move,self)
                    self.memory.update_game_state()
                elif self.get_difficulty() == "Hard":
                    move = m_mtcs(self.memory.state,GameEnvironmentM(),0.35)
                    self.memory.apply_move(move,self)
                    self.memory.update_game_state()
                elif self.get_difficulty() == "Expert":
                    move = m_mtcs(self.memory.state,GameEnvironmentM(),0.5)
                    self.memory.apply_move(move,self)
                    self.memory.update_game_state()
                print(self.memory.state['history'])
                if self.memory.state['history']:
                    if self.memory.state['history'][-1][0] == "Missed":
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
            self.threes.shuffle_cards()
            self.threes.distribute_cards()
            self.threes.update_game_state()
            self.update_game(game)
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
            self.rummy.shuffle_cards()
            self.rummy.turn = random.randint(0,1)
            self.rummy.distribute_cards()
            self.rummy.update_game_state()
            print("Rummy State:")
            print(self.rummy.state)
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
            self.memory.shuffle_cards()
            self.memory.distribute_cards()
            self.memory.update_game_state()
            self.update_game(game)
            self.memory.turn = 1#random.randint(0,1)
            print(self.memory.turn)
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
            print("Resuming Rummy Game")
            print(self.rummy.is_game_over())
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
