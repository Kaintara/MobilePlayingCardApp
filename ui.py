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
        # defensive: app.shop or equipped theme may be None during startup
        theme = None
        if getattr(app, "shop", None):
            try:
                theme = app.shop.get_theme(app.shop.equipped)
            except Exception:
                theme = None
        # fallback to first available theme
        if theme is None and getattr(app, "shop", None) and app.shop.inventory:
            theme = app.shop.inventory[0]
        # pick asset, fallback to a generic placeholder if missing
        if theme and getattr(theme, "asset_dict", None) and suit_rank in theme.asset_dict:
            img_src = theme.asset_dict[suit_rank]
        else:
            img_src = "assets/img/default_card.png"  # add a small placeholder image in assets
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