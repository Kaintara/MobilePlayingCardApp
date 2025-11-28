from ui import *

class MobilePlayingCardApp(MDApp):
    def __init__(self, **kwargs):
        self.sm_stack = []
        self.sfx = True
        self.ai_difficulty = "Beginner"
        self.timer = True
        self.score = True
        self.all_achievements = [('Achieve1','The first acheivement!','Open the Game'),('SUPER LUCKY!','Win rummy without playing...','History = None'),('Title Drop?','Win a game of threes with a three.','Last move in History is the (0,3somth,play)')]
        self.unlocked_achivements = []
        self.previous_games = {
            'Threes' : [],
            'Rummy' : [],
            'Memory' : []
        }
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.theme_style_switch_animation_duration = 0.4
        Window.set_icon(("icon.png"))
        LabelBase.register(
            name="cataway",
            fn_regular="Catways.ttf",
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
        sm.add_widget(Threes(name="Threes"))
        sm.add_widget(Rummy(name="Rummy"))
        sm.add_widget(Memory(name="Memory"))
        sm.add_widget(Rules(name="Rules"))
        sm.add_widget(Settings(name="Settings"))
        sm.add_widget(Shop(name="Shop"))
        sm.add_widget(Stats(name="Stats"))
        sm.current = "Menu"
        return sm
    
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

    def on_start(self):
        return super().on_start()