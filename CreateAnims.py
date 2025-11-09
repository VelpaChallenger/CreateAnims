#aka Editor as others might know it. But I like CreateAnims.

import tkinter
from tkinter import Tk
from tkinter import ttk

from TileUtils import *
from Command import *
from EntryReturn import *
from Anim import *
from CreateAnimsButton import *

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
        self.entry_return = EntryReturn(self)
        self.anim = Anim(self)
        self.button = CreateAnimsButton(self)
        self.characters = []
        self.current_pal_rectangle = None
        self.current_color_picker_rectangle = None
        self.current_tile_image_rectangle = None
        self.current_chr_tile_index = None #We will need it to update anim's image.
        self.current_anim_image_rectangle = None
        self.palette_directory = None
        self.chr_directory = None
        self.chr_palette_directory = None
        self.frames_directory = None
        self.anims_directory = None

    def init_anim_window(self):
        self.root.title("Create Anims") #Sometimes dreams come true! Believe in them!
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{INITIAL_X}+{INITIAL_Y}") #It's how my mind sees things. It's the initial, you might drag the window around and stuff. #Window x/y could be alternative name.
        self.make_styles()

        frame_stage = tkinter.Frame(self.root, border=0) #Scenario also. But I like more stage. It's where the action happens.
        frame_stage.grid(row=0, column=0, columnspan=3, sticky="w")
        self.stage_canvas = tkinter.Canvas(frame_stage, width=860, height=256, bg="#E0E0E0", borderwidth=0, highlightthickness=0)
        self.stage_canvas.grid(row=0, column=0)
        self.anim_canvas = tkinter.Canvas(frame_stage, width=200, height=256, cursor="hand2", borderwidth=0, highlightthickness=0)
        self.anim_canvas.grid(row=0, column=0)

        frame_palette = tkinter.Frame(self.root, border=0)
        frame_palette.grid(row=1, column=0, rowspan=3, sticky="nw")
        self.pal_label = tkinter.Label(frame_palette, text="Palette:", anchor="w", font=FONT)
        self.pal_label.grid(row=0, column=0, sticky="w")
        self.character_palette_canvas = tkinter.Canvas(frame_palette, width=256, height=32, bg="#808080", cursor="hand2", borderwidth=0, highlightthickness=0)
        self.character_palette_canvas.grid(row=1, column=0)
        self.color_picker_canvas = tkinter.Canvas(frame_palette, width=256, height=69, bg="#808080", cursor="hand2", borderwidth=0, highlightthickness=0)
        self.color_picker_canvas.grid(row=2, column=0, pady=30)
        self.create_color_picker()

        frame_chr = tkinter.Frame(self.root, border=0)
        frame_chr.grid(row=1, column=1, rowspan=3, columnspan=2, sticky="nw")
        frame_chr_bank = tkinter.Frame(frame_chr, border=0)
        frame_chr_bank.grid(row=0, column=0, sticky="nw")
        self.chr_label = tkinter.Label(frame_chr_bank, text="CHR Bank:", anchor="w", font=FONT)
        self.chr_label.pack(side="left")
        vcmd = (self.root.register(self.tile_utils.validate_chr_bank), "%P")
        self.chr_entry = tkinter.Entry(frame_chr_bank, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.chr_entry.bind("<Return>", self.entry_return.chr_entry)
        self.chr_entry.pack(side="left")
        self.chr_left_arrow = ttk.Button(frame_chr_bank, text="", style="Left.TButton", command=self.button.chr_left_arrow_button)
        self.chr_left_arrow.pack(side="left", padx=(5, 2))
        self.chr_right_arrow = ttk.Button(frame_chr_bank, text="", style="Right.TButton", command=self.button.chr_right_arrow_button)
        self.chr_right_arrow.pack(side="left")
        self.chr_canvas = tkinter.Canvas(frame_chr, width=256, height=128, bg="#808080", cursor="hand2", borderwidth=0, highlightthickness=0)
        self.chr_canvas.grid(row=1, column=0)
        self.tile_label = tkinter.Label(frame_chr, text="Tile: 00 / 00", anchor="w", font=FONT)
        self.tile_label.grid(row=2, column=0, sticky="w")
        self.chr_info = tkinter.LabelFrame(frame_chr, text="CHR INFO", bd=2, width=150, height=160)
        self.chr_info.grid(row=0, column=1, rowspan=3, padx=15, sticky="nw")
        self.chr_info_text = tkinter.Label(self.chr_info, text="", justify="left", wraplength=142)
        self.chr_info_text.place(x=5, y=5)

        menu_bar = tkinter.Menu(self.root)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save palette", command=self.command.save_palette)
        file_menu.add_command(label="Save CHR palette", command=self.command.save_chr_palette)
        file_menu.add_command(labe="Save frame", command=self.command.save_frame)
        file_menu.add_command(label="Save anim", command=self.command.save_anim)
        menu_bar.add_cascade(label="File", menu=file_menu)
        anim_menu = tkinter.Menu(menu_bar, tearoff=0)
        anim_menu.add_command(label="Toggle transparency", command=self.command.toggle_anim_transparency, accelerator="Shift+T") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("<Shift-T>", self.command.toggle_anim_transparency)
        anim_menu.add_command(label="Toggle rectangle around frame", command=self.command.toggle_draw_frame_rectangle, accelerator="r") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("r", self.command.toggle_draw_frame_rectangle)
        anim_menu.add_command(label="Toggle draw empty cells", command=self.command.toggle_draw_empty_cells, accelerator="e") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("e", self.command.toggle_draw_empty_cells)
        menu_bar.add_cascade(label="Anim", menu=anim_menu)
        import_menu = tkinter.Menu(menu_bar, tearoff=0)
        import_menu.add_command(label="Palette", command=self.command.import_palette)
        import_menu.add_command(label="CHR", command=self.command.import_chr)
        import_menu.add_command(label="CHR Palette", command=self.command.import_chr_palette)
        import_menu.add_command(label="Frame", command=self.command.import_frame)
        import_menu.add_command(label="Anim", command=self.command.import_anim)
        menu_bar.add_cascade(label="Import", menu=import_menu)
        self.root.config(menu=menu_bar)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=3, sticky="nsew")

        frame_anim_field = tkinter.Frame(self.root, border=0) #Let's call these fields rather than entries.
        frame_anim_field.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.anim_label = tkinter.Label(frame_anim_field, text="Anim:", anchor="w", font=FONT, width=8)
        self.anim_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_anim_entry), "%P")
        self.anim_entry = tkinter.Entry(frame_anim_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.anim_entry.bind("<Return>", self.entry_return.anim_entry)
        self.anim_entry.pack(side="left")
        self.anim_left_arrow = ttk.Button(frame_anim_field, text="", style="Left.TButton", command=self.button.anim_left_arrow_button)
        self.anim_left_arrow.pack(side="left", padx=(5, 2))
        self.anim_right_arrow = ttk.Button(frame_anim_field, text="", style="Right.TButton", command=self.button.anim_right_arrow_button)
        self.anim_right_arrow.pack(side="left")

        frame_field = tkinter.Frame(self.root, border=0)
        frame_field.grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        self.frame_label = tkinter.Label(frame_field, text="Frame:", anchor="w", font=FONT, width=8)
        self.frame_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_frame_entry), "%P")
        self.frame_entry = tkinter.Entry(frame_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.frame_entry.bind("<Return>", self.entry_return.frame_entry)
        self.frame_entry.pack(side="left")
        self.frame_left_arrow = ttk.Button(frame_field, text="", style="Left.TButton", command=self.button.frame_left_arrow_button)
        self.frame_left_arrow.pack(side="left", padx=(5, 2))
        self.frame_right_arrow = ttk.Button(frame_field, text="", style="Right.TButton", command=self.button.frame_right_arrow_button)
        self.frame_right_arrow.pack(side="left")

        frame_id_field = tkinter.Frame(self.root, border=0)
        frame_id_field.grid(row=7, column=0, sticky="nw", padx=5, pady=5)
        self.frame_id_label = tkinter.Label(frame_id_field, text="Frame ID:", anchor="w", font=FONT, width=8)
        self.frame_id_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_frame_id_entry), "%P")
        self.frame_id_entry = tkinter.Entry(frame_id_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.frame_id_entry.bind("<Return>", self.entry_return.frame_id_entry)
        self.frame_id_entry.pack(side="left")
        self.frame_id_left_arrow = ttk.Button(frame_id_field, text="", style="Left.TButton", command=self.button.frame_id_left_arrow_button)
        self.frame_id_left_arrow.pack(side="left", padx=(5, 2))
        self.frame_id_right_arrow = ttk.Button(frame_id_field, text="", style="Right.TButton", command=self.button.frame_id_right_arrow_button)
        self.frame_id_right_arrow.pack(side="left")

        self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

    def make_styles(self):
        style = ttk.Style()
        style.layout(
            "Left.TButton", [
                ("Button.leftarrow", None),
                ("Button.label", None)
            ]
        )
        style.layout(
            "Right.TButton", [
                ("Button.rightarrow", None),
                ("Button.label", None)
            ]
        )
        style.configure("Left.TButton", font=('', '20'), width=2)
        style.configure("Right.TButton", font=('', '20'), width=2)

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