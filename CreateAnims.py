#aka Editor as others might know it. But I like CreateAnims.

import tkinter
from tkinter import Tk

from TileUtils import *

WIDTH = 860
HEIGHT = 600
INITIAL_X = 500
INITIAL_Y = 200

class CreateAnims:

    def __init__(self):
        self.init_state()
        self.init_anim_window()

    def init_state(self):
        self.root = Tk()
        self.tile_utils = TileUtils(self)
        self.characters_palettes = []

    def init_anim_window(self):
        self.root.title("Create Anims") #Sometimes dreams come true! Believe in them!
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{INITIAL_X}+{INITIAL_Y}") #It's how my mind sees things. It's the initial, you might drag the window around and stuff. #Window x/y could be alternative name.

        frame_left = tkinter.Frame(self.root, border=0)
        frame_left.grid(row=0, column=0)
        self.main_canvas = tkinter.Canvas(frame_left, width=256, height=256, bg="#E0E0E0")
        self.main_canvas.grid(row=2, column=0)
        self.palette_canvas = tkinter.Canvas(frame_left, width=256, height=32, bg="#808080", cursor="hand2")
        self.palette_canvas.grid(row=3, column=0)

    def refresh_UI(self): #This will be part of CreateAnims. All directly UI-related, idea is that it's here. Maybe not the technical like more specific code per se, but at least the highest layer.
        self.tile_utils.refresh_palette() #Changed my mind, will be part of a refresh/update UI.