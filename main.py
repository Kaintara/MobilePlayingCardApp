from ui import * 
from save import SaveData
from game import *
from shop import *


class MobilePlayingCardApp(MDApp):
    def __init__(self, **kwargs):
        self.sm_stack = []
        self.sfx = True
        self.ai_difficulty = "Beginner"
        self.timer = True
        self.score = True
        self.all_achievements = [
            (0,'The memory of a goldfish','Play your first game of Memory',lambda save : save.alldata['Games']['Stats']['Memory_Stats']['General_Stats']["games_played"] >= 1),
            (1,'Only Three?','Play your first game of Threes',lambda save : save.alldata['Games']['Stats']['Threes_Stats']['General_Stats']["games_played"] >= 1),
            (2,'Four and Three!','Play your first game of Rummy',lambda save : save.alldata['Games']['Stats']['Rummy_Stats']['General_Stats']["games_played"] >= 1),
            (3,'Better Luck Next Time!','Lose your first game of Rummy',lambda save : save.alldata['Games']["Previous_Games"]['Rummy'][-1]['winner'] == 1),
            (4,'If only you had a ten, huh?','Lose your first game of Threes',lambda save : save.alldata['Games']["Previous_Games"]['Threes'][-1]['winner'] == 1),
            (5,'FUMBLED!','Lose your first game of Memory',lambda save : save.alldata['Games']["Previous_Games"]['Memory'][-1]['winner'] == 1),
            (6,'Poker Player','Win your first game of Rummy',lambda save : save.alldata['Games']["Previous_Games"]['Rummy'][-1]['winner'] == 0),
            (7,'Uno Player','Win your first game of Three',lambda save : save.alldata['Games']["Previous_Games"]['Threes'][-1]['winner'] == 0),
            (8,'The memory of an elephant','Win your first game of Memory',lambda save : save.alldata['Games']["Previous_Games"]['Memory'][-1]['winner'] == 0),
        ]
        self.unlocked_achievements = []
        self.previous_games = {
            'threes' : [],
            'rummy' : [],
            'memory' : []
        }
        self.shop = None
        self.save = None
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
        AppShop = Shop()
        self.shop = AppShop
        AppSave = SaveData()
        self.save = AppSave
        savedata = self.save.load()
        G1 = savedata['Games']['Current_Games']['Threes']
        G2 = savedata['Games']['Current_Games']['Rummy']
        G3 = savedata['Games']['Current_Games']['Memory']
        self.threes = Threes('threes',G1['rank_order'],G1)
        self.rummy = Rummy('rummy',G2['value_map'],G2)
        self.memory = Memory('memory',G1['rank_order'],G3)
        self.save.update(self)
        Games = [G1,G2,G3]
        for x in Games:
            print(x)
        for game in Games:
            print(game['winner'])
            if not game['winner'] and game['history']:
                return "Resume Game"
            return "New Game"
        
    def left(self,Screen):
        Carou = self.get_widget("carou",Screen)
        if Screen == "Stats":
            pass
        Carou.load_previous()

    def right(self,Screen):
        Carou = self.get_widget("carou",Screen)
        if Screen == "Stats":
            pass
        Carou.load_next()

    def on_start(self):
        self.shop.filling_shop_inventory(self)
        Gird = self.get_widget("grid",'MDShop')
        Gird.add_widget(Playing_Card('AH'))
        return super().on_start()

if __name__ == "__main__":
    MobilePlayingCardApp().run()