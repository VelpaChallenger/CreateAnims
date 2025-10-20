#aka Editor as others might know it. But I like CreateAnims.

from tkinter import Tk

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

    def init_anim_window(self):
        self.root.title("Create Anims") #Sometimes dreams come true! Believe in them!
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{INITIAL_X}+{INITIAL_Y}") #It's how my mind sees things. It's the initial, you might drag the window around and stuff. #Window x/y could be alternative name.