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

class Shop_Dialog(MDDialog):
    def __init__(self, themecost, coins, **kwargs):
        # Build content container
        content = MDBoxLayout(orientation="vertical", spacing=dp(8), adaptive_height=True)
        content.add_widget(MDDialogIcon(icon="account-circle"))
        content.add_widget(
            MDDialogHeadlineText(
                text="Insufficient coins!",
                halign="center",
                font_style="cataway",
                role="medium",
            )
        )
        content.add_widget(
            MDDialogSupportingText(
                text=f"Unfortunately for you, this theme costs {themecost}.\nYou have {coins} coins.",
                halign="left",
                font_style="cataway",
                theme_font_size="Custom",
                font_size=dp(20),
            )
        )
        # Initialize parent dialog with custom content
        super().__init__(type="custom", content_cls=content, **kwargs)

class Achievement_Dialog(MDDialog):
    def __init__(self, achievement, **kwargs):
        # Build content container
        content = MDBoxLayout(orientation="vertical", spacing=dp(8), adaptive_height=True)
        content.add_widget(MDDialogIcon(icon="account-circle"))
        content.add_widget(
            MDDialogHeadlineText(
                text=f"Achievement Unlocked! - {achievement[1]}",
                halign="center",
                font_style="cataway",
                role="medium",
            )
        )
        content.add_widget(
            MDDialogSupportingText(
                text=f"{achievement[2]}",
                halign="left",
                font_style="cataway",
                theme_font_size="Custom",
                font_size=dp(20),
            )
        )
        # Initialize parent dialog with custom content
        super().__init__(type="custom", content_cls=content, **kwargs)

class Reward_Dialog(MDDialog):
    def __init__(self, reward, app,**kwargs):
        content = MDBoxLayout(orientation="vertical", spacing=dp(8), adaptive_height=True)
        if reward[1] == 0:
            content.add_widget(MDDialogIcon(icon="crown"))
            content.add_widget(
                MDDialogHeadlineText(
                    text="Game Over! You won!",
                    halign="center",
                    font_style="cataway",
                    role="medium",
                )
            )
        else:
            content.add_widget(MDDialogIcon(icon="check"))
            content.add_widget(
                MDDialogHeadlineText(
                    text="Game Over! You lost...",
                    halign="center",
                    font_style="cataway",
                    role="medium",
                )
            )
        content.add_widget(
            MDDialogSupportingText(
                text=f"You gained {reward[0]} coins for your efforts!",
                halign="left",
                font_style="cataway",
                theme_font_size="Custom",
                font_size=dp(20),
            )
        )
        content.add_widget(
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
        
        super().__init__(type="custom", content_cls=content, **kwargs)
        self.auto_dismiss = False
    
    def go_to_menu(self, app, *args):
        self.dismiss()
        app.root.current = "Menu"

class Playing_Card(MDCard):
    def __init__(self,suit_rank,**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None,None)
        self.size = ("64dp", "89dp")
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        app = MDApp.get_running_app()
        theme = None
        theme = app.shop.get_theme(app.shop.equipped)
        print("Works!")
        if app.shop.inventory:
            theme = app.shop.inventory[0]
            print(theme)
        # pick asset, fallback to a generic placeholder if missing
        if theme and getattr(theme, "asset_dict", None) and suit_rank in theme.asset_dict:
            img_src = theme.asset_dict[suit_rank]
        else:
            img_src = "assets/img/theme1/2_of_clubs.png"  # add a small placeholder image in assets
        img = Image(source=img_src)
        self.layout = RelativeLayout(
            size = ("64dp", "89dp")
        )
        #self.highlight = Image(
            #source='glow.png',
            #size_hint=(1.2,1.2),
            #opacity=0,
            #pos_hint={"center_x": 0.5, "center_y": 0.5}
       # )
       # self.layout.add_widget(self.highlight)
        self.layout.add_widget(img)
        self.add_widget(self.layout)

class Shop_Button(MDCard):
    def __init__(self, price="200", equipped=False, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1, None)
        self.height = dp(32)
        self.radius = [16]
        self.elevation = 0

        if equipped:
            self.md_bg_color = (0.75, 0.55, 0.55, 1)
            text = "Equipped"
            icon = "lock"
        else:
            self.md_bg_color = (0.6, 0.4, 0.4, 1)
            text = price
            icon = "lock"

        layout = MDBoxLayout(
            orientation="horizontal",
            padding=[dp(12), 0, dp(12), 0],
            spacing=dp(8)
        )

        layout.add_widget(
            MDLabel(
                text=text,
                halign="center",
                font_style="cataway",
                role="small"
            )
        )

        layout.add_widget(
            MDIconButton(
                icon=icon,
                size_hint=(None, None),
                size=(dp(18), dp(18))
            )
        )

        self.add_widget(layout)

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
        
        button = Shop_Button()

        layout.add_widget(card_stack)
        layout.add_widget(button)
        self.add_widget(layout)