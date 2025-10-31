#aka Editor as others might know it. But I like CreateAnims.

import tkinter
from tkinter import Tk

from TileUtils import *
from Command import *
from Anim import *

FONT = ("TkDefaultFont", 16)

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
        self.command = Command(self)
        self.anim = Anim(self)
        self.characters = []
        self.current_pal_rectangle = None
        self.current_color_picker_rectangle = None
        self.current_tile_image_rectangle = None
        self.current_anim_image_rectangle = None
        self.current_frame = None
        self.palette_directory = None
        self.chr_palette_directory = None

    def init_anim_window(self):
        self.root.title("Create Anims") #Sometimes dreams come true! Believe in them!
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{INITIAL_X}+{INITIAL_Y}") #It's how my mind sees things. It's the initial, you might drag the window around and stuff. #Window x/y could be alternative name.

        frame_stage = tkinter.Frame(self.root, border=0) #Scenario also. But I like more stage. It's where the action happens.
        frame_stage.grid(row=0, column=0, columnspan=2, sticky="w")
        self.stage_canvas = tkinter.Canvas(frame_stage, width=860, height=256, bg="#E0E0E0")
        self.stage_canvas.grid(row=0, column=0)
        self.anim_canvas = tkinter.Canvas(frame_stage, width=200, height=256, cursor="hand2")
        self.anim_canvas.grid(row=0, column=0)

        frame_palette = tkinter.Frame(self.root, border=0)
        frame_palette.grid(row=1, column=0, sticky="nw")
        self.pal_label = tkinter.Label(frame_palette, text="Palette:", anchor="w", font=FONT)
        self.pal_label.grid(row=0, column=0, sticky="w")
        self.character_palette_canvas = tkinter.Canvas(frame_palette, width=256, height=32, bg="#808080", cursor="hand2", borderwidth=0, highlightthickness=0)
        self.character_palette_canvas.grid(row=1, column=0)
        self.color_picker_canvas = tkinter.Canvas(frame_palette, width=256, height=69, bg="#808080", cursor="hand2", borderwidth=0, highlightthickness=0)
        self.color_picker_canvas.grid(row=2, column=0, pady=30)
        self.create_color_picker()

        frame_chr = tkinter.Frame(self.root, border=0)
        frame_chr.grid(row=1, column=1, sticky="nw")
        self.chr_label = tkinter.Label(frame_chr, text="CHR Bank: 9C", anchor="w", font=FONT)
        self.chr_label.grid(row=0, column=0, sticky="w")
        self.chr_canvas = tkinter.Canvas(frame_chr, width=256, height=128, bg="#808080", cursor="hand2", borderwidth=0, highlightthickness=0)
        self.chr_canvas.grid(row=1, column=0)
        self.tile_label = tkinter.Label(frame_chr, text="Tile: 00 / 00", anchor="w", font=FONT)
        self.tile_label.grid(row=2, column=0, sticky="w")

        menu_bar = tkinter.Menu(self.root)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save palette", command=self.command.save_palette)
        file_menu.add_command(label="Save CHR palette", command=self.command.save_chr_palette)
        menu_bar.add_cascade(label="File", menu=file_menu)
        anim_menu = tkinter.Menu(menu_bar, tearoff=0)
        anim_menu.add_command(label="Toggle transparency", command=self.command.toggle_anim_transparency, accelerator="Shift+T") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("<Shift-T>", self.command.toggle_anim_transparency)
        anim_menu.add_command(label="Toggle rectangle around frame", command=self.command.toggle_draw_frame_rectangle, accelerator="r") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("r", self.command.toggle_draw_frame_rectangle)
        menu_bar.add_cascade(label="Anim", menu=anim_menu)
        self.root.config(menu=menu_bar)

    def create_color_picker(self): #Its own function 'cause, it does have some complexity. #Also, it could be in TileUtils but... it's initialization still. So I'll go this route.
        from TileUtils import SYSTEM_PALETTE, ColorPickerRectangle #Let's borrow it for a bit.
        self.color_picker_rectangles = []
        pal_index = 0x0 #We'll start from zero, all the way to the end.
        initial_y = -16 #The trick of starting with a negative so that it works also the first iteration. Great awesome.
        for row in range(4):
            initial_x = 0
            initial_y += 17
            for col in range(16):
                rgb_triplet = SYSTEM_PALETTE[pal_index]
                r, g, b = rgb_triplet[0], rgb_triplet[1], rgb_triplet[2]
                rgb = f"#{r:02X}{g:02X}{b:02X}"
                color_picker_rectangle = self.color_picker_canvas.create_rectangle(initial_x, initial_y, initial_x + 15, initial_y + 16, fill=rgb, outline=rgb, width=1)
                self.color_picker_rectangles.append(ColorPickerRectangle(self, self.color_picker_canvas, color_picker_rectangle, pal_index, rgb, self.pal_label))
                initial_x += 16
                pal_index += 1

    def refresh_UI(self): #This will be part of CreateAnims. All directly UI-related, idea is that it's here. Maybe not the technical like more specific code per se, but at least the highest layer.
        self.tile_utils.refresh_palette() #Changed my mind, will be part of a refresh/update UI.
        self.tile_utils.refresh_chr()
        self.anim.refresh()