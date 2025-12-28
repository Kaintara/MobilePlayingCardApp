from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale, Translate
from kivy.clock import Clock
from kivy.uix.image import Image

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonIcon, MDIconButton, MDButtonText
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogIcon, MDDialogContentContainer, MDDialogSupportingText

class SM(MDScreenManager):
    pass

class MainMenu(MDScreen):
    pass

class NewGame(MDScreen):
    pass

class MDThrees(MDScreen):
    pass

class MDRummy(MDScreen):
    pass

class MDMemory(MDScreen):
    pass

class Rules(MDScreen):
    pass

class MDShop(MDScreen):
    pass

class Stats(MDScreen):
    pass

class Settings(MDScreen):
    pass

class Pause(MDScreen):
    pass

class Shop_Dialog(MDDialog):
    def __init__(self, themecost, coins, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(
            MDDialogIcon(icon="emoticon-confused")
        )
        self.add_widget(
            MDDialogHeadlineText(
                text="Insufficient coins!",
                halign="center",
                font_style="cataway",
                role="medium",
            )
        )
        self.add_widget(
            MDDialogSupportingText(
                text=f"Unfortunately for you, this theme costs {themecost}.\nYou have {coins} coins.",
                halign="left",
                font_style="cataway",
                theme_font_size="Custom",
                font_size=dp(20),
            )
        )
        self.add_widget(
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    MDButtonIcon(icon="check"),
                    on_release=self.dismiss
                )
            )
        )

class Achievement_Dialog(MDDialog):
    def __init__(self, achievement, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MDDialogIcon(icon="account-circle"))
        self.add_widget(
            MDDialogHeadlineText(
                text=f"Achievement Unlocked! - {achievement[1]}",
                halign="center",
                font_style="cataway",
                role="medium",
            )
        )
        self.add_widget(
            MDDialogSupportingText(
                text=f"{achievement[2]}",
                halign="left",
                font_style="cataway",
                theme_font_size="Custom",
                font_size=dp(20),
            )
        )

class Reward_Dialog(MDDialog):
    def __init__(self, reward, app,**kwargs):
        super().__init__(**kwargs)
        if reward[1] == 0:
            self.add_widget(MDDialogIcon(icon="crown"))
            self.add_widget(
                MDDialogHeadlineText(
                    text="Game Over! You won!",
                    halign="center",
                    font_style="cataway",
                    role="medium",
                )
            )
        else:
            self.add_widget(MDDialogIcon(icon="skull-crossbones-outline"))
            self.add_widget(
                MDDialogHeadlineText(
                    text="Game Over! You lost...",
                    halign="center",
                    font_style="cataway",
                    role="medium",
                )
            )
        self.add_widget(
            MDDialogSupportingText(
                text=f"You gained {reward[0]} coins for your efforts!",
                halign="left",
                font_style="cataway",
                theme_font_size="Custom",
                font_size=dp(20),
            )
        )
        self.add_widget(
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Good Game!", font_style="cataway", role="small"),
                    MDButtonIcon(icon="check-outline"),
                    style="tonal",
                    pos_hint={"center_x": 0.5},
                    on_release=lambda x: self.go_to_menu(app)
                )
            )
        )
        self.auto_dismiss = False
    
    def go_to_menu(self, app, *args):
        self.dismiss()
        app.root.current = "Menu"

class HandLayout(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(width=self.update_spacing, children=self.update_spacing)

    def update_spacing(self, *args):
        n = len(self.children)
        if n <= 1:
            self.spacing = 0
        else:
            required = n * dp(64)
            avail = self.width
            desired = (avail - required) / (n - 1)
            max_overlap = -dp(64) * 0.75   
            max_spread = dp(64) * 0.5 
            if desired < max_overlap:
                desired = max_overlap
            elif desired > max_spread:
                desired = max_spread
            self.spacing = desired

class Display_Card(MDCard):
    def __init__(self, suit_rank,face,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        app = MDApp.get_running_app()
        theme = None
        theme = app.shop.get_theme(app.shop.equipped)
        if face == 'front':
            img_src = theme.asset_dict[suit_rank]
        else:
            img_src = theme.back_img
        img = Image(source=img_src)    
        self.layout = RelativeLayout(
            size = ("64dp", "89dp")
        )
        self.layout.add_widget(img)
        self.add_widget(self.layout)

class Playing_Card(MDCard):
    def __init__(self,suit_rank,game,face,**kwargs):
        super().__init__(**kwargs)
        self.suit_rank = suit_rank
        self.selected = False
        self.game = game
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        app = MDApp.get_running_app()
        theme = None
        theme = app.shop.get_theme(app.shop.equipped)
        if face == 'front':
            img_src = theme.asset_dict[suit_rank]
        else:
            img_src = theme.back_img
        img = Image(source=img_src)
        self.layout = RelativeLayout(
            size = ("64dp", "89dp")
        )
        self.highlight = Image(
            source='MobilePlayingCardApp/assets/img/glow.png',
            size_hint=(1.2,1.2),
            opacity=0,
            pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.layout.add_widget(self.highlight)
        self.layout.add_widget(img)
        self.add_widget(self.layout)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            if self.game == 'threes':
                game = app.threes
                if game.turn == 0:
                    for move in game.get_valid_moves():
                        if self.suit_rank == move[1] or (move[2] == 'pickup' and self.suit_rank == game.played_cards[-1]):
                            if game.selected_card != self:
                                if game.selected_card:
                                    game.selected_card.highlight.opacity = 0
                                game.selected_card = self
                                self.selected = True
                                self.highlight.opacity = 1
                            else:
                                game.selected_card = ''
                                game.turn = game.next_vaild_player(game.turn,app.save)
                                print(game.turn)
                                if game.turn is not None:
                                    game.apply_move(move)
                                    game.update_game_state()
                                    app.save.quick_save(app)
                                    Clock.schedule_once(lambda dt: app.next_turn('threes'), 0.5)
                                else:
                                    print('Ending game from Playing_Card on_touch_down')
                                    game.end_game(app)
                            break
            elif self.game == 'rummy':
                game = app.rummy
                if game.turn == 0:
                    for move in game.get_valid_moves():
                        if self.suit_rank == move[1] or ((move[1] == 'deck' and self.suit_rank == game.shuffled_deck[-1])):
                            if game.selected_card != self:
                                if game.selected_card:
                                    game.selected_card.highlight.opacity = 0
                                game.selected_card = self
                                self.selected = True
                                self.highlight.opacity = 1
                            else:
                                game.selected_card = ''
                                game.turn = game.next_vaild_player(game.turn,app.save)
                                print(game.turn)
                                if game.turn is not None:
                                    print(move)
                                    print(game.hands[0])
                                    game.apply_move(move)
                                    game.update_game_state()
                                    app.save.quick_save(app)
                                    Clock.schedule_once(lambda dt: app.next_turn('rummy'), 0.5)
                                else:
                                    print('Ending game from Playing_Card on_touch_down')
                                    game.end_game(app)
                            break
        return super().on_touch_down(touch)
                                         


class Shop_Button(MDButton):
    def __init__(self, theme_obj, equipped=False, unlocked=False,**kwargs):
        super().__init__(**kwargs)
        price = theme_obj.cost
        self.theme_name = theme_obj.name
        self.size_hint = (1, None)
        self.height = dp(32)
        self.radius = [16]
        self.elevation = 0
        self.equipped = equipped
        self.unlocked = unlocked
        if equipped:
            self.md_bg_color = (0.75, 0.55, 0.55, 1)
            text = "Equipped"
            icon = "lock-open"
        elif unlocked:
            self.md_bg_color = (0.75, 0.55, 0.55, 1)
            text = "Equip"
            icon = "lock-open"
        else:
            self.md_bg_color = (0.6, 0.4, 0.4, 1)
            text = str(price)
            icon = "lock"
        self.add_widget(
            MDButtonText(
                text=text,
                halign="center",
                font_style="cataway",
                role="small"
            )
        )
        self.add_widget(
            MDIconButton(
                icon=icon,
                size_hint=(None, None),
                size=(dp(18), dp(18))
            )
        )
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            if not self.unlocked:
                app.shop.buy_theme(self.theme_name)
            else:
                app.shop.equip_theme(self.theme_name)
        return super().on_touch_down(touch)

class Shop_Card(MDCard):
    def __init__(self, theme_name, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = ("140dp", "210dp")
        self.radius = [24]
        self.elevation = 1
        self.padding = dp(10)
        self.md_bg_color = MDApp.get_running_app().theme_cls.surfaceColor

        front_src = theme_name.front_img
        back_src = theme_name.back_img

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            adaptive_height=True
        )

        card_stack = RelativeLayout(
            size_hint=(None, None),
            size=(dp(90), dp(130)),
            pos_hint={"center_x": 0.5}
            )
        
        card_back = Image(
            source=back_src,
            size_hint=(None, None),
            size=(dp(90), dp(130)),
            pos=(dp(20), dp(0))
            )
        card_back.size = (dp(86), dp(126))
        card_back.rotation = 2
        
        card_front = Image(
            source=front_src,
            size_hint=(None, None),
            size=(dp(75), dp(102)),
            pos=(0, 0)
            )
        
        card_stack.add_widget(card_back)
        card_stack.add_widget(card_front)
        
        button = Shop_Button(theme_name)

        layout.add_widget(card_stack)
        layout.add_widget(button)
        self.add_widget(layout)
