from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale, Translate
from kivy.clock import Clock

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