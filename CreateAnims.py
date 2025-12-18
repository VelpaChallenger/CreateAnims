#aka Editor as others might know it. But I like CreateAnims.

import tkinter
from tkinter import Tk, ttk, font
import traceback
import sys

from TileUtils import *
from Command import *
from EntryReturn import *
from Anim import *
from CreateAnimsButton import *
from UndoRedo import *
from FileFormatValidator import *

FONT = ("TkDefaultFont", 16)

WIDTH = 872
HEIGHT = 620
INITIAL_X = 500
INITIAL_Y = 200

PHYSICS_WIDTH = 430
PHYSICS_HEIGHT = 310
PHYSICS_INITIAL_X = 600
PHYSICS_INITIAL_Y = 250

CREATEANIMS_VERSION_DATE = "Local test"
CREATEANIMS_VERSION = "v1.0.6" #The third one means pre-release. Not meant to be used in production but maybe you want it to test some stuff and things like that. Mostly meant for before v1.0.
COMMIT_ID = "Local test"

class CreateAnims:

    def __init__(self):
        self.init_state()
        self.init_anim_window()

    def init_state(self):
        self.tile_utils = TileUtils(self)
        self.command = Command(self)
        self.entry_return = EntryReturn(self)
        self.anim = Anim(self)
        self.button = CreateAnimsButton(self)
        self.undo_redo = UndoRedo(self)
        self.file_format_validator = FileFormatValidator(self)
        self.characters = []
        self.current_pal_rectangle = None
        self.current_character_pal_index = None #Similarly, we'll need it for the relationship/associations between a PalRectangle and a ColorPickerRectangle.
        self.current_color_picker_rectangle = None
        self.current_tile_image_rectangle = None
        self.current_tile_image_multiple_tiles_rectangle = None #Maybe we can use this instead of the bool?
        self.current_chr_tile_index = None #We will need it to update anim's image.
        self.current_anim_image_rectangle = None
        self.characters_directory = None
        self.palette_directory = None
        self.chr_directory = None
        self.chr_palette_directory = None
        self.frames_directory = None
        self.anims_directory = None
        self.physics_directory = None
        self.png_img = []
        self.in_play_anim = False
        self.in_physics_window = False
        self.in_exception = False
        #self.tile_image_multiple_tiles_rectangle_bool = False
        self.physics_list = []
        self.current_palette_info_text = ""

    def init_anim_window(self):
        self.root = Tk() #Yes, this makes more sense when I think about it. And will make things smoother for the loading bar.
        self.root.title("Create Anims") #Sometimes dreams come true! Believe in them!
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{INITIAL_X}+{INITIAL_Y}") #It's how my mind sees things. It's the initial, you might drag the window around and stuff. #Window x/y could be alternative name.
        self.make_styles()

        frame_stage = tkinter.Frame(self.root, border=0) #Scenario also. But I like more stage. It's where the action happens.
        frame_stage.grid(row=0, column=0, columnspan=3, sticky="w")
        self.anim_canvas = tkinter.Canvas(frame_stage, width=WIDTH, height=256, bg="#E0E0E0", borderwidth=0, highlightthickness=0)
        self.anim_canvas.grid(row=0, column=0)

        frame_palette = tkinter.Frame(self.root, border=0)
        frame_palette.grid(row=1, column=0, rowspan=3, sticky="nw")
        self.pal_label = tkinter.Label(frame_palette, text="Palette:", anchor="w", font=FONT)
        self.pal_label.grid(row=0, column=0, sticky="w")
        self.character_palette_canvas = tkinter.Canvas(frame_palette, width=256, height=32, bg="#808080", borderwidth=0, highlightthickness=0)
        self.character_palette_canvas.grid(row=1, column=0)
        self.color_picker_canvas = tkinter.Canvas(frame_palette, width=256, height=64, bg="#808080", borderwidth=0, highlightthickness=0)
        self.color_picker_canvas.grid(row=2, column=0, pady=30)
        self.create_color_picker()
        self.palette_info = tkinter.LabelFrame(frame_palette, text="PALETTE INFO", bd=2, width=150, height=160)
        self.palette_info.grid(row=0, column=1, rowspan=3, padx=15, sticky="nw")
        self.palette_info_text = tkinter.Label(self.palette_info, text="", justify="left", wraplength=142)
        self.palette_info_text.place(x=5, y=5)

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
        self.chr_canvas = tkinter.Canvas(frame_chr, width=256, height=128, bg="#808080", borderwidth=0, highlightthickness=0)
        self.chr_canvas.grid(row=1, column=0)
        self.tile_label = tkinter.Label(frame_chr, text="Tile: 00 / 00", anchor="w", font=FONT)
        self.tile_label.grid(row=2, column=0, sticky="w")
        self.chr_info = tkinter.LabelFrame(frame_chr, text="CHR INFO", bd=2, width=150, height=160)
        self.chr_info.grid(row=0, column=1, rowspan=3, padx=15, sticky="nw")
        self.chr_info_text = tkinter.Label(self.chr_info, text="", justify="left", wraplength=142)
        self.chr_info_text.place(x=5, y=5)

        self.menu_bar = tkinter.Menu(self.root)
        file_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open Characters Directory", command=self.command.open_characters_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Save palette", command=self.command.save_palette)
        file_menu.add_command(label="Save CHR", command=self.command.save_chr)
        file_menu.add_command(label="Save CHR palette", command=self.command.save_chr_palette)
        file_menu.add_command(labe="Save frame", command=self.command.save_frame)
        file_menu.add_command(label="Save anim", command=self.command.save_anim)
        file_menu.add_command(label="Save physics", command=self.command.save_physics)
        file_menu.add_separator()
        file_menu.add_command(label="Save changes", command=self.undo_redo.tracer)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_x)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.edit_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo_redo.undo, accelerator="Ctrl+Z", state="disabled")
        self.edit_menu.add_command(label="Redo", command=self.undo_redo.redo, accelerator="Ctrl+Y", state="disabled")
        self.edit_menu.add_command(label="Switch UndoRedo branch", command=self.undo_redo.switch_branch_undo_redo, accelerator="Ctrl+Shift+Z", state="disabled")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Clear all selections", command=self.command.clear_all_selections, accelerator="Ctrl+D")
        self.edit_menu.add_command(label="Refresh to Last Saved", command=self.command.refresh_to_last_saved, accelerator="Ctrl+R")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        anim_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        anim_menu.add_command(label="Toggle transparency", command=self.command.toggle_anim_transparency, accelerator="Shift+T") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("<Shift-T>", self.command.toggle_anim_transparency)
        anim_menu.add_command(label="Toggle rectangle around frame", command=self.command.toggle_draw_frame_rectangle, accelerator="r") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("r", self.command.toggle_draw_frame_rectangle)
        anim_menu.add_command(label="Toggle draw empty cells", command=self.command.toggle_draw_empty_cells, accelerator="e") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("e", self.command.toggle_draw_empty_cells)
        self.menu_bar.add_cascade(label="Anim", menu=anim_menu)
        tools_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Log History", command=self.init_log_history_window, accelerator="Ctrl+L")
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu) #Yes, usually keyboard shortcuts go here also but, whatever.
        import_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        import_menu.add_command(label="Palette", command=self.command.import_palette)
        import_menu.add_command(label="CHR", command=self.command.import_chr)
        import_menu.add_command(label="CHR Palette", command=self.command.import_chr_palette)
        import_menu.add_command(label="Frame", command=self.command.import_frame)
        import_menu.add_command(label="Anim", command=self.command.import_anim)
        import_menu.add_command(label="Physics", command=self.command.import_physics)
        self.menu_bar.add_cascade(label="Import", menu=import_menu)
        help_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.init_about_window)
        help_menu.add_command(label="Docs", command=self.command.open_docs_in_browser)
        help_menu.add_separator()
        help_menu.add_command(label="Check for Updates", command=self.command.check_for_updates)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=self.menu_bar)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=3, sticky="nsew")

        frame_command_base = tkinter.Frame(self.root, border=0) #It makes me feel like I'm at my base!
        frame_command_base.grid(row=5, column=0, columnspan=3, sticky="nw") #Has to be same as anim_stage. Will use as a container for all sub-frames. Including sub-sub frames.

        frame_all_anim_field = tkinter.Frame(frame_command_base, border=0)
        frame_all_anim_field.pack(side="left")

        frame_anim_field = tkinter.Frame(frame_all_anim_field, border=0) #Let's call these fields rather than entries.
        frame_anim_field.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.anim_label = tkinter.Label(frame_anim_field, text="Anim:", anchor="w", font=FONT, width=9)
        self.anim_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_anim_entry), "%P")
        self.anim_entry = tkinter.Entry(frame_anim_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.anim_entry.bind("<Return>", self.entry_return.anim_entry)
        self.anim_entry.pack(side="left")
        self.anim_left_arrow = ttk.Button(frame_anim_field, text="", style="Left.TButton", command=self.button.anim_left_arrow_button)
        self.anim_left_arrow.pack(side="left", padx=(5, 2))
        self.anim_right_arrow = ttk.Button(frame_anim_field, text="", style="Right.TButton", command=self.button.anim_right_arrow_button)
        self.anim_right_arrow.pack(side="left")

        frame_field = tkinter.Frame(frame_all_anim_field, border=0)
        frame_field.grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        self.frame_label = tkinter.Label(frame_field, text="Frame:", anchor="w", font=FONT, width=9)
        self.frame_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_frame_entry), "%P")
        self.frame_entry = tkinter.Entry(frame_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.frame_entry.bind("<Return>", self.entry_return.frame_entry)
        self.frame_entry.pack(side="left")
        self.frame_left_arrow = ttk.Button(frame_field, text="", style="Left.TButton", command=self.button.frame_left_arrow_button)
        self.frame_left_arrow.pack(side="left", padx=(5, 2))
        self.frame_right_arrow = ttk.Button(frame_field, text="", style="Right.TButton", command=self.button.frame_right_arrow_button)
        self.frame_right_arrow.pack(side="left")

        frame_id_field = tkinter.Frame(frame_all_anim_field, border=0)
        frame_id_field.grid(row=7, column=0, sticky="nw", padx=5, pady=5)
        self.frame_id_label = tkinter.Label(frame_id_field, text="Frame ID:", anchor="w", font=FONT, width=9)
        self.frame_id_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_frame_id_entry), "%P")
        self.frame_id_entry = tkinter.Entry(frame_id_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.frame_id_entry.bind("<Return>", self.entry_return.frame_id_entry)
        self.frame_id_entry.pack(side="left")
        self.frame_id_left_arrow = ttk.Button(frame_id_field, text="", style="Left.TButton", command=self.button.frame_id_left_arrow_button)
        self.frame_id_left_arrow.pack(side="left", padx=(5, 2))
        self.frame_id_right_arrow = ttk.Button(frame_id_field, text="", style="Right.TButton", command=self.button.frame_id_right_arrow_button)
        self.frame_id_right_arrow.pack(side="left")

        physics_id_field = tkinter.Frame(frame_all_anim_field, border=0)
        physics_id_field.grid(row=8, column=0, sticky="nw", padx=5, pady=5)
        self.physics_id_label = tkinter.Label(physics_id_field, text="Physics ID:", anchor="w", font=FONT, width=9)
        self.physics_id_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_physics_id_entry), "%P")
        self.physics_id_entry = tkinter.Entry(physics_id_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.physics_id_entry.bind("<Return>", self.entry_return.physics_id_entry)
        self.physics_id_entry.pack(side="left")
        self.physics_id_left_arrow = ttk.Button(physics_id_field, text="", style="Left.TButton", command=self.button.physics_id_left_arrow_button)
        self.physics_id_left_arrow.pack(side="left", padx=(5, 2))
        self.physics_id_right_arrow = ttk.Button(physics_id_field, text="", style="Right.TButton", command=self.button.physics_id_right_arrow_button)
        self.physics_id_right_arrow.pack(side="left")

        frame_dimensions = tkinter.Frame(frame_command_base) #Dimensions because it's what makes me think of. Width, height, X and Y offsets will be here.
        frame_dimensions.pack(side="left", anchor="nw")

        frame_x_offset_field = tkinter.Frame(frame_dimensions)
        frame_x_offset_field.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.x_offset_label = tkinter.Label(frame_x_offset_field, text="X Offset:", anchor="w", font=FONT, width=9)
        self.x_offset_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_x_offset_entry), "%P")
        self.x_offset_entry = tkinter.Entry(frame_x_offset_field, width=4, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.x_offset_entry.bind("<Return>", self.entry_return.x_offset_entry)
        self.x_offset_entry.pack(side="left")
        self.x_offset_left_arrow = ttk.Button(frame_x_offset_field, text="", style="Left.TButton", command=self.button.x_offset_left_arrow_button)
        self.x_offset_left_arrow.pack(side="left", padx=(5, 2))
        self.x_offset_right_arrow = ttk.Button(frame_x_offset_field, text="", style="Right.TButton", command=self.button.x_offset_right_arrow_button)
        self.x_offset_right_arrow.pack(side="left")

        frame_y_offset_field = tkinter.Frame(frame_dimensions)
        frame_y_offset_field.grid(row=6, column=0, sticky="nw", padx=5, pady=5)
        self.y_offset_label = tkinter.Label(frame_y_offset_field, text="Y Offset:", anchor="w", font=FONT, width=9)
        self.y_offset_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_y_offset_entry), "%P")
        self.y_offset_entry = tkinter.Entry(frame_y_offset_field, width=4, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.y_offset_entry.bind("<Return>", self.entry_return.y_offset_entry)
        self.y_offset_entry.pack(side="left")
        self.y_offset_left_arrow = ttk.Button(frame_y_offset_field, text="", style="Left.TButton", command=self.button.y_offset_left_arrow_button)
        self.y_offset_left_arrow.pack(side="left", padx=(5, 2))
        self.y_offset_right_arrow = ttk.Button(frame_y_offset_field, text="", style="Right.TButton", command=self.button.y_offset_right_arrow_button)
        self.y_offset_right_arrow.pack(side="left")

        frame_width_field = tkinter.Frame(frame_dimensions)
        frame_width_field.grid(row=7, column=0, sticky="nw", padx=5, pady=5)
        self.width_label = tkinter.Label(frame_width_field, text="Width:", anchor="w", font=FONT, width=9)
        self.width_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_width_entry), "%P")
        self.width_entry = tkinter.Entry(frame_width_field, width=4, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.width_entry.bind("<Return>", self.entry_return.width_entry)
        self.width_entry.pack(side="left")
        self.width_left_arrow = ttk.Button(frame_width_field, text="", style="Left.TButton", command=self.button.width_left_arrow_button)
        self.width_left_arrow.pack(side="left", padx=(5, 2))
        self.width_right_arrow = ttk.Button(frame_width_field, text="", style="Right.TButton", command=self.button.width_right_arrow_button)
        self.width_right_arrow.pack(side="left")

        frame_height_field = tkinter.Frame(frame_dimensions)
        frame_height_field.grid(row=8, column=0, sticky="nw", padx=5, pady=5)
        self.height_label = tkinter.Label(frame_height_field, text="Height:", anchor="w", font=FONT, width=9)
        self.height_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_height_entry), "%P")
        self.height_entry = tkinter.Entry(frame_height_field, width=4, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.height_entry.bind("<Return>", self.entry_return.height_entry)
        self.height_entry.pack(side="left")
        self.height_left_arrow = ttk.Button(frame_height_field, text="", style="Left.TButton", command=self.button.height_left_arrow_button)
        self.height_left_arrow.pack(side="left", padx=(5, 2))
        self.height_right_arrow = ttk.Button(frame_height_field, text="", style="Right.TButton", command=self.button.height_right_arrow_button)
        self.height_right_arrow.pack(side="left")

        frame_character = tkinter.Frame(frame_command_base)
        frame_character.pack(side="left", anchor="nw")

        frame_character_field = tkinter.Frame(frame_character)
        frame_character_field.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.character_label = tkinter.Label(frame_character_field, text="Character:", anchor="w", font=FONT, width=9)
        self.character_label.pack(side="left")
        vcmd = (self.root.register(self.anim.validate_character_entry), "%P")
        self.character_entry = tkinter.Entry(frame_character_field, width=3, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.character_entry.bind("<Return>", self.entry_return.character_entry)
        self.character_entry.pack(side="left")
        self.character_left_arrow = ttk.Button(frame_character_field, text="", style="Left.TButton", command=self.button.character_left_arrow_button)
        self.character_left_arrow.pack(side="left", padx=(5, 2))
        self.character_right_arrow = ttk.Button(frame_character_field, text="", style="Right.TButton", command=self.button.character_right_arrow_button)
        self.character_right_arrow.pack(side="left")

        separator = ttk.Separator(frame_command_base, orient='vertical')
        separator.pack(side="left", anchor="nw", fill="both")

        frame_anim_player = tkinter.Frame(frame_command_base) #Anim player, I like the sound of that! Then play_anim for the button itself. Or maybe button will be here in this frame.
        frame_anim_player.pack(side="left")

        self.play_anim_button = ttk.Button(frame_anim_player, text="Play Anim", command=self.button.play_anim_button, takefocus=0)
        self.play_anim_button.pack(side="top", padx=(5, 2), pady=(5, 5))
        self.stop_anim_button = ttk.Button(frame_anim_player, text="Stop Anim", command=self.button.stop_anim_button, takefocus=0, state="disabled") #Only one can be active at a time.
        self.stop_anim_button.pack(side="top", padx=(5, 2), pady=(5, 5))
        self.edit_physics_button = ttk.Button(frame_anim_player, text="Edit Physics", command=self.button.edit_physics_button, takefocus=0)
        self.edit_physics_button.pack(side="top", padx=(5, 2), pady=(5, 5))

        self.root.bind_all("<Button-1>", self.bind_all_focus)

        self.root.bind("<Control-z>", self.undo_redo.undo)
        self.root.bind("<Control-y>", self.undo_redo.redo)
        self.root.bind("<Control-Z>", self.undo_redo.switch_branch_undo_redo) #What? Control-Z? Don't you mean Control-Shift-z? Actually yes. But Shift-z means Z, so if you put Control-shift-z, it won't work.
        self.root.bind("<Control-s>", self.undo_redo.tracer)
        self.root.bind("<Control-l>", self.init_log_history_window)
        self.root.bind("<Control-r>", self.command.refresh_to_last_saved)
        self.root.bind("<Control-d>", self.command.clear_all_selections)

        self.root.protocol("WM_DELETE_WINDOW", self.on_x)

        self.root.report_callback_exception = self.self_destruct

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

    def bind_all_focus(self, event=None): #Goodbyte lambda.
        if type(event.widget) == ttk.Button or type(event.widget) == str: #Well I didn't really want to but, we've come this far, we already have no more lambda. Whatever. The gist of it is that when you left click on anything, this triggers, due to bind_all, and it includes labels. Physics labels, they get destroyed before this runs. When that happens, they become strings, for whatever tkinter internal reason. So, focus_set() fails. At that point we just don't care anymore.
            return #Those don't play under the same rule, those use takefocus=0.
        event.widget.focus_set()

    def create_color_picker(self): #Its own function 'cause, it does have some complexity. #Also, it could be in TileUtils but... it's initialization still. So I'll go this route.
        from TileUtils import SYSTEM_PALETTE, ColorPickerRectangle #Let's borrow it for a bit.
        self.color_picker_rectangles = []
        pal_index = 0x0 #We'll start from zero, all the way to the end.
        initial_y = -16 #The trick of starting with a negative so that it works also the first iteration. Great awesome.
        for row in range(4):
            initial_x = 0
            initial_y += 16
            for col in range(16):
                rgb_triplet = SYSTEM_PALETTE[pal_index]
                r, g, b = rgb_triplet[0], rgb_triplet[1], rgb_triplet[2]
                rgb = f"#{r:02X}{g:02X}{b:02X}"
                color_picker_rectangle = self.color_picker_canvas.create_rectangle(initial_x, initial_y, initial_x + 16, initial_y + 16, fill=rgb, outline=rgb, width=1)
                self.color_picker_rectangles.append(ColorPickerRectangle(self, self.color_picker_canvas, color_picker_rectangle, pal_index, rgb, self.pal_label))
                initial_x += 16
                pal_index += 1

    def init_physics_window(self): #Probably will have a destroy as well? In case of Ok/Cancel.
        self.in_physics_window = True #We will use it after all!
        self.physics_window = tkinter.Toplevel(self.root)
        self.physics_window.title("Create Anims Physics Manager") #Sometimes dreams come true! Believe in them!
        self.physics_window.geometry(f"{PHYSICS_WIDTH}x{PHYSICS_HEIGHT}+{PHYSICS_INITIAL_X}+{PHYSICS_INITIAL_Y}")
        self.root.attributes('-disabled', 1)
        self.physics_window.transient(self.root) # set to be on top of the main window
        self.physics_window.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        self.physics_window.focus_force()
        self.physics_window.bind("<Control-z>", self.undo_redo.undo)
        self.physics_window.bind("<Control-y>", self.undo_redo.redo)
        self.physics_window.bind("<Control-Z>", self.undo_redo.switch_branch_undo_redo)
        self.physics_window.protocol("WM_DELETE_WINDOW", self.on_physics_window_x)

        self.physics_graphics_canvas = tkinter.Canvas(self.physics_window, bd=0, highlightthickness=0, bg="white", width=256, height=100)
        self.physics_graphics_canvas.pack(side="top", fill="both", expand=True)
        self.physics_graphics_canvas.create_line(0, 180, 500, 180, fill="black")
        self.physics_graphics_canvas.create_line(215, 0, 215, 180, fill="black")

        self.physics_canvas = tkinter.Canvas(self.physics_window, bd=0, highlightthickness=0, height=25) #scrollregion=(0,0,500,500), width=100, height=50) #Exact measures will be determined later. This is the predetermined stuff.
        self.physics_canvas.pack(side="top", fill="both", expand=True)
        self.frame_physics = tkinter.Frame(self.physics_canvas, border=0)
        self.frame_physics.bind("<Configure>", lambda event: self.physics_canvas.configure(scrollregion=self.physics_canvas.bbox('all'))) #Let's please verify that this bind doesn't mess up memory.
        self.physics_canvas.create_window((0, 0), window=self.frame_physics, anchor="nw")
        hbar = tkinter.Scrollbar(self.physics_window, orient="horizontal", command=self.physics_canvas.xview)
        self.physics_canvas.configure(xscrollcommand=hbar.set) #One will always have a configure. canvas needs hbar for the scrollcommand. hbar needs the canvas for the command.
        hbar.pack(side="top", fill="x")
        self.anim.fill_physics_grid() #Changed my mind. The creation itself will happen here, then here we'll fill the values. #Physics grid is not predetermined. So, Anim will take things from here. CreateAnims has more to do with UI init stuff. The more low level stuff if you will.
        self.root.wait_window(self.physics_window)
        self.in_physics_window = False
        self.root.attributes('-disabled', 0)
        self.root.focus_force()

    def on_physics_window_x(self): #Specifically, the X button was pressed. Let's consider this an UndoRedo too.
        self.undo_redo.undo_redo([self.init_physics_window], [self.destroy_physics_window])

    def destroy_physics_window(self): #Won't do anything if it's already destroyed (aka i.e. when X button was pressed.).
        self.physics_window.destroy() #Puff! Gone! (used for Undo)

    def init_physics_dialog(self, frame_index): #Technically a window, but yeah, a dialog.
        self.disable_undo_redo()
        self.physics_dialog = tkinter.Toplevel(self.root)
        self.physics_dialog.title(f"Update X and Y Physics for Frame {frame_index:02d}")
        self.physics_dialog.geometry(f"300x100+665+300") #Whatever.
        self.physics_window.attributes('-disabled', 1)
        self.physics_dialog.transient(self.physics_window)
        self.physics_dialog.grab_set()
        self.physics_dialog.focus_force()

        self.physics_dialog_x_frame = tkinter.Frame(self.physics_dialog, border=0)
        self.physics_dialog_x_frame.pack(anchor="nw")
        self.physics_dialog_x_label = tkinter.Label(self.physics_dialog_x_frame, text="X:")
        self.physics_dialog_x_label.pack(side="left")
        vcmd = (self.physics_dialog.register(self.anim.validate_physics_dialog_x_entry), "%P")
        self.physics_dialog_x_entry = tkinter.Entry(self.physics_dialog_x_frame, width=4, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.physics_dialog_x_entry.bind("<Return>", self.entry_return.physics_dialog_x_entry)
        self.physics_dialog_x_entry.pack(side="left")

        self.physics_dialog_y_frame = tkinter.Frame(self.physics_dialog, border=0)
        self.physics_dialog_y_frame.pack(anchor="nw")
        self.physics_dialog_y_label = tkinter.Label(self.physics_dialog_y_frame, text="Y:")
        self.physics_dialog_y_label.pack(side="left")
        vcmd = (self.physics_dialog.register(self.anim.validate_physics_dialog_y_entry), "%P") #There's actually a problem for that. Which is, if you enter invalid value for Y, X entry is still highlighted. So, they do have to be different. #For Y, the function will be the same. A bit confusing maybe for future me, but please read this!
        self.physics_dialog_y_entry = tkinter.Entry(self.physics_dialog_y_frame, width=4, font=FONT, validate="key", validatecommand=vcmd, highlightcolor="white", highlightbackground="white", highlightthickness=1)
        self.physics_dialog_y_entry.bind("<Return>", self.entry_return.physics_dialog_x_entry)
        self.physics_dialog_y_entry.pack(side="left", pady=(5, 5))

        physics = self.physics_list[self.current_physics_id] #Ah, what a refresher. I don't have to type so much createanims here.
        x_physics = self.anim.calculate_physics(physics[2*frame_index]) #Same as always. #Here too we need to convert. But that's why we have calculate_physics. We can call it from there directly.
        y_physics = self.anim.calculate_physics(physics[(2*frame_index) + 1])
        self.physics_dialog_x_entry.insert(0, str(x_physics))
        self.physics_dialog_x_entry.select_range(0, "end")
        self.physics_dialog_x_entry.focus()
        self.physics_dialog_y_entry.insert(0, str(y_physics))
        self.physics_dialog_current_frame = frame_index #Will come in handy for EntryReturn. #Actually... let's do something a little different. Or... nah whatever.
        self.physics_window.wait_window(self.physics_dialog)
        self.undo_redo.decide_undo_redo_status() #Actually, only if they should be reenabled. Leave them at the state they should. Presumably, Undo should be enabled and Redo not, but, this logic will decide. #You can undo and redo again.
        if self.physics_window.winfo_exists(): #Might not exist anymore due to a destroy as part of exception handling.
            self.physics_window.attributes('-disabled', 0)
            self.physics_window.focus_force()

    def init_log_history_window(self, event=None):
        if self.in_play_anim:
            from tkinter import messagebox
            messagebox.showinfo(title="Cannot open Log History", message="You cannot open Log History while playing an anim.") #Cannot start.
            return #Could also silently not say anything, or use the potential, planned AnimInfo but that's for more Anim specific stuff so, I'll use messagebox for this.
        self.disable_undo_redo()
        self.log_history_window = tkinter.Toplevel(self.root)
        self.log_history_window.title(f"Log History")
        self.log_history_window.geometry(f"500x400+715+300") #Was going to be 400x400 but some texts don't fit in.
        self.root.attributes('-disabled', 1)
        self.log_history_window.transient(self.root)
        self.log_history_window.grab_set()
        self.log_history_window.focus_force()

        self.log_history_canvas_frame = tkinter.Frame(self.log_history_window, bd=0)
        self.log_history_canvas_frame.pack(anchor="nw")

        self.log_history_canvas_frame.bind_all("<MouseWheel>", lambda event: self.log_history_canvas.yview_scroll(int(-1*(event.delta/120)), "units")) #self.move_scrollbar)
        self.log_history_canvas_frame.bind_all("<Up>", lambda event: self.log_history_canvas.yview_scroll(-1, "units")) #self.move_scrollbar_up)
        self.log_history_canvas_frame.bind_all("<Down>", lambda event: self.log_history_canvas.yview_scroll(1, "units"))#self.move_scrollbar_down)

        log_history_canvas_height = 340 #Should always be this value and will use it several times so I'm defining it here.
        self.log_history_canvas = tkinter.Canvas(self.log_history_canvas_frame, bd=0, highlightthickness=0, height=log_history_canvas_height, width=480) #scrollregion=(0,0,500,500), width=100, height=50) #Exact measures will be determined later. This is the predetermined stuff.
        self.log_history_canvas.pack(side="left", fill="both", expand=True)
        self.frame_log_history = tkinter.Frame(self.log_history_canvas, border=0) #This one is the scrollable. log_history_frame is the LabelFrame.
        self.frame_log_history.bind("<Configure>", lambda event: self.log_history_canvas.configure(scrollregion=self.log_history_canvas.bbox('all'))) #Let's please verify that this bind doesn't mess up memory.
        self.log_history_canvas.create_window((0, 0), window=self.frame_log_history, anchor="nw")
        vbar = tkinter.Scrollbar(self.log_history_canvas_frame, orient="vertical", command=self.log_history_canvas.yview, takefocus=1)
        self.log_history_canvas.configure(yscrollcommand=vbar.set) #One will always have a configure. canvas needs hbar for the scrollcommand. hbar needs the canvas for the command.
        vbar.pack(side="left", fill="y")

        self.log_history_frame = tkinter.LabelFrame(self.frame_log_history, text="LOG HISTORY", bd=2, width=460)
        self.log_history_frame.pack(anchor="nw", padx=15)
        self.log_history_label = tkinter.Label(self.log_history_frame, text=self.undo_redo.log_history.rstrip(), justify="left", wraplength=440)
        self.log_history_label.place(x=5, y=5)
        self.log_history_window.update() #Updates log_history_label height (well everything but I care about height in this case).
        log_history_label_height = self.log_history_label.winfo_height() + 25 #25 seems like the right number to make all look cool.
        if log_history_label_height < log_history_canvas_height: #I don't usually put logic in CreateAnims but yes.
            log_history_label_height = log_history_canvas_height
        self.log_history_frame.configure(height=log_history_label_height) #So the frame will be as high as the frame. Excellent.

        self.log_history_command_base_container = tkinter.Frame(self.log_history_window, bd=0)
        self.log_history_command_base_container.pack(fill="both", expand=True) #We need a container for place logic to work the way we want and center things the way we want it.

        self.log_history_command_base = tkinter.Frame(self.log_history_command_base_container, bd=0)
        self.log_history_command_base.place(x=33, y=0, anchor="nw") #Default seems to be nw, but still, to be specific/explicit. Yes confirmed, nw is default.

        self.log_history_label_copy_ok = tkinter.Label(self.log_history_command_base, text="", width=16, justify="right", anchor="ne")
        self.log_history_label_copy_ok.pack(side="left")

        self.log_history_copy_button = ttk.Button(self.log_history_command_base, text="Copy", takefocus=0, command=self.copy_to_clipboard) #Copy log, copy to clipboard.
        self.log_history_copy_button.pack(side="left", padx=(8, 15), pady=15)
        self.log_history_OK_button = ttk.Button(self.log_history_command_base, text="OK", takefocus=0, command=self.log_history_window.destroy)
        self.log_history_OK_button.pack(side="left", padx=15, pady=15)

        self.root.wait_window(self.log_history_window)
        self.undo_redo.decide_undo_redo_status() #Actually, only if they should be reenabled. Leave them at the state they should. Presumably, Undo should be enabled and Redo not, but, this logic will decide. #You can undo and redo again.
        self.root.attributes('-disabled', 0)
        self.root.focus_force()

    def copy_to_clipboard(self):
        if not self.undo_redo.log_history.rstrip():
            self.log_history_label_copy_ok.configure(text="Nothing to copy (yet)", fg="red")
            return
        self.root.clipboard_clear() #Oops. Yes, first this to avoid copying a lot if Copy is pressed multiple times.
        self.root.clipboard_append(self.undo_redo.log_history.rstrip())
        self.log_history_label_copy_ok.configure(text="Copied!", fg="green")

    def init_save_changes_window(self):
        self.disable_undo_redo()
        self.save_changes_window = tkinter.Toplevel(self.root)
        self.save_changes_window.title(f"Save changes")
        self.save_changes_window.geometry(f"500x500+715+250")
        self.root.attributes('-disabled', 1)
        self.save_changes_window.transient(self.root)
        self.save_changes_window.grab_set()
        self.save_changes_window.focus_force()

        self.save_changes_label = tkinter.Label(self.save_changes_window, text="You are about to save the following changes:\n", anchor="nw", justify="left") #save_changes_text = f #And again, we'll move it somewhere else. #Changed my mind, let's encapsulate the logic here instead of in the label.
        self.save_changes_label.pack(anchor="nw")

        self.save_changes_canvas_frame = tkinter.Frame(self.save_changes_window, bd=0)
        self.save_changes_canvas_frame.pack(anchor="nw")

        self.save_changes_canvas_frame.bind("<Enter>", lambda event: self.bind_scroll(self.save_changes_canvas))
        self.save_changes_canvas_frame.bind("<Leave>", lambda event: self.unbind_scroll(self.save_changes_canvas))

        save_changes_canvas_height = 140 #Will be smaller for these scrolls than it is for Log History. #Should always be this value and will use it several times so I'm defining it here.
        self.save_changes_canvas = tkinter.Canvas(self.save_changes_canvas_frame, bd=0, highlightthickness=0, height=save_changes_canvas_height, width=480)
        self.save_changes_canvas.pack(side="left", fill="both", expand=True)
        self.frame_save_changes = tkinter.Frame(self.save_changes_canvas, border=0) #This one is the scrollable. save_changes_frame is the LabelFrame.
        self.frame_save_changes.bind("<Configure>", lambda event: self.save_changes_canvas.configure(scrollregion=self.save_changes_canvas.bbox('all'))) #Let's please verify that this bind doesn't mess up memory.
        self.save_changes_canvas.create_window((0, 0), window=self.frame_save_changes, anchor="nw")
        vbar = tkinter.Scrollbar(self.save_changes_canvas_frame, orient="vertical", command=self.save_changes_canvas.yview, takefocus=1)
        self.save_changes_canvas.configure(yscrollcommand=vbar.set) #One will always have a configure. canvas needs hbar for the scrollcommand. hbar needs the canvas for the command.
        vbar.pack(side="left", fill="y")

        self.save_changes_frame = tkinter.LabelFrame(self.frame_save_changes, text="", bd=2, width=460) #Changes to be saved. But I'd like to experiment with just a container. We know those are the changes to be saved, the label above says so.
        self.save_changes_frame.pack(anchor="nw", padx=15)
        self.save_changes_label = tkinter.Label(self.save_changes_frame, text="".join(self.undo_redo.trace).rstrip(), justify="left", wraplength=440)
        self.save_changes_label.place(x=5, y=5)
        self.save_changes_window.update() #Updates save_changes_label height (well everything but I care about height in this case).
        save_changes_label_height = self.save_changes_label.winfo_height() + 25 #25 seems like the right number to make all look cool.
        if save_changes_label_height < save_changes_canvas_height: #I don't usually put logic in CreateAnims but yes.
            save_changes_label_height = save_changes_canvas_height
        self.save_changes_frame.configure(height=save_changes_label_height) #So the frame will be as high as the frame. Excellent.

        self.save_changes_affected_files_label = tkinter.Label(self.save_changes_window, text="\nAffected files:\n", anchor="nw", justify="left")
        self.save_changes_affected_files_label.pack(anchor="nw")

        self.save_changes_affected_files_canvas_frame = tkinter.Frame(self.save_changes_window, bd=0)
        self.save_changes_affected_files_canvas_frame.pack(anchor="nw")

        self.save_changes_affected_files_canvas_frame.bind("<Enter>", lambda event: self.bind_scroll(self.save_changes_affected_files_canvas))
        self.save_changes_affected_files_canvas_frame.bind("<Leave>", lambda event: self.unbind_scroll(self.save_changes_affected_files_canvas))

        save_changes_affected_files_canvas_height = 140 #Will be smaller for these scrolls than it is for Log History. #Should always be this value and will use it several times so I'm defining it here.
        self.save_changes_affected_files_canvas = tkinter.Canvas(self.save_changes_affected_files_canvas_frame, bd=0, highlightthickness=0, height=save_changes_affected_files_canvas_height, width=480)
        self.save_changes_affected_files_canvas.pack(side="left", fill="both", expand=True)
        self.frame_save_changes_affected_files = tkinter.Frame(self.save_changes_affected_files_canvas, border=0) #This one is the scrollable. save_changes_affected_files_frame is the LabelFrame.
        self.frame_save_changes_affected_files.bind("<Configure>", lambda event: self.save_changes_affected_files_canvas.configure(scrollregion=self.save_changes_affected_files_canvas.bbox('all'))) #Let's please verify that this bind doesn't mess up memory.
        self.save_changes_affected_files_canvas.create_window((0, 0), window=self.frame_save_changes_affected_files, anchor="nw")
        vbar = tkinter.Scrollbar(self.save_changes_affected_files_canvas_frame, orient="vertical", command=self.save_changes_affected_files_canvas.yview, takefocus=1)
        self.save_changes_affected_files_canvas.configure(yscrollcommand=vbar.set) #One will always have a configure. canvas needs hbar for the scrollcommand. hbar needs the canvas for the command.
        vbar.pack(side="left", fill="y")

        self.save_changes_affected_files_frame = tkinter.LabelFrame(self.frame_save_changes_affected_files, text="", bd=2, width=460) #Changes to be saved. But I'd like to experiment with just a container. We know those are the changes to be saved, the label above says so.
        self.save_changes_affected_files_frame.pack(anchor="nw", padx=15)
        self.save_changes_affected_files_label = tkinter.Label(self.save_changes_affected_files_frame, text="".join(sorted(list(set(self.undo_redo.affected_files)))).rstrip(), justify="left", wraplength=440)
        self.save_changes_affected_files_label.place(x=5, y=5)
        self.save_changes_window.update() #Updates save_changes_affected_files_label height (well everything but I care about height in this case).
        save_changes_affected_files_label_height = self.save_changes_affected_files_label.winfo_height() + 25 #25 seems like the right number to make all look cool.
        if save_changes_affected_files_label_height < save_changes_affected_files_canvas_height: #I don't usually put logic in CreateAnims but yes.
            save_changes_affected_files_label_height = save_changes_affected_files_canvas_height
        self.save_changes_affected_files_frame.configure(height=save_changes_affected_files_label_height) #So the frame will be as high as the frame. Excellent.

        self.save_changes_confirmation_label = tkinter.Label(self.save_changes_window, text="\nFiles will be overwritten. Do you wish to continue?", anchor="nw", justify="left") #save_changes_text = f #And again, we'll move it somewhere else. #Changed my mind, let's encapsulate the logic here instead of in the label.
        self.save_changes_confirmation_label.pack(anchor="nw")

        self.save_changes_command_base = tkinter.Frame(self.save_changes_window, bd=0)
        self.save_changes_command_base.pack()

        self.save_changes_yes_button = ttk.Button(self.save_changes_command_base, text="Yes", takefocus=0, command=self.command.save_changes) #Copy log, copy to clipboard.
        self.save_changes_yes_button.pack(side="left", padx=(8, 15), pady=15)
        self.save_changes_no_button = ttk.Button(self.save_changes_command_base, text="No", takefocus=0, command=self.save_changes_window.destroy)
        self.save_changes_no_button.pack(side="left", padx=15, pady=15)

        self.root.wait_window(self.save_changes_window)
        self.undo_redo.decide_undo_redo_status() #Actually, only if they should be reenabled. Leave them at the state they should. Presumably, Undo should be enabled and Redo not, but, this logic will decide. #You can undo and redo again.
        self.root.attributes('-disabled', 0)
        self.root.focus_force()

    def init_about_window(self):
        self.disable_undo_redo()
        self.about_window = tkinter.Toplevel(self.root)
        self.about_window.title(f"About CreateAnims")
        self.about_window.geometry(f"500x400+715+300")
        self.root.attributes('-disabled', 1)
        self.about_window.transient(self.root)
        self.about_window.grab_set()
        self.about_window.focus_force()

        self.about_title = tkinter.Label(self.about_window, text="CreateAnims VelpaChallenger") #My idea is once I have the icon, to put the date below the icon.
        self.about_title.pack()
        self.about_version = tkinter.Label(self.about_window, text=f"Version: {CREATEANIMS_VERSION} {CREATEANIMS_VERSION_DATE}", anchor="nw") #Okay, let's put it here, the date.
        self.about_version.pack(anchor="nw", pady=(120, 0))
        self.about_commit_frame = tkinter.Frame(self.about_window, bd=0)
        self.about_commit_frame.pack(anchor="nw")
        self.about_commit_text = tkinter.Label(self.about_commit_frame, text=f"Commit:", anchor="nw", padx=0)
        self.about_commit_text.pack(side="left")
        self.about_commit_id = tkinter.Label(self.about_commit_frame, text=f"{COMMIT_ID}", anchor="nw", fg="blue", cursor="hand2", padx=0)
        hyperlink_font = font.Font(self.about_commit_id, self.about_commit_id.cget('font'))
        hyperlink_font.configure(underline=True)
        self.about_commit_id.configure(font=hyperlink_font)
        commit_url = f"https://github.com/VelpaChallenger/Create-Anims/commit/{COMMIT_ID}" #Technically you can use the short version as well but... well yeah whatever. Let's do use the short one.
        self.about_commit_id.bind("<Button-1>", lambda event: self.open_url_in_browser(commit_url)) #Might be good idea to have a general CreateAnims method to open URLs in the browser. In fact, I'll do just that.
        self.about_commit_id.pack(side="left")
        thanks_text = (
        "Thanks to the following people for their contributions in one way or another!\n\n" #My personality, with exclamation and all. #Be it testing, suggestions, moral support, giving the idea etc. etc.
        "\t-Rkk\n"
        "\t-drax01"
        )
        self.about_thanks = tkinter.Label(self.about_window, text=thanks_text, anchor="nw", justify="left")
        self.about_thanks.pack(anchor="nw")
        description_text = "Originally intended for MK3 NES Arkade Edition, but written with the intention of being extended to other games to make creating animations easier and smoother.\nAs always, suggestions, bug reports recommendations ideas comments etc. etc. are more than welcome!"
        self.about_description = tkinter.Label(self.about_window, text=description_text, anchor="nw", justify="left", wraplength=500)
        self.about_description.pack(anchor="nw", pady=(30, 0))
        self.about_ok = ttk.Button(self.about_window, text="OK", takefocus=0, command=self.about_window.destroy)
        self.about_ok.pack(pady=(10, 0))

        self.root.wait_window(self.about_window)
        self.undo_redo.decide_undo_redo_status() #Actually, only if they should be reenabled. Leave them at the state they should. Presumably, Undo should be enabled and Redo not, but, this logic will decide. #You can undo and redo again.
        self.root.attributes('-disabled', 0)
        self.root.focus_force()

    def bind_scroll(self, canvas): #Not sure if we actually need the canvas, I think widget.bind_all and widget.unbind_all are the literal same to root.bind_all and root.unbind_all, but even if that, it makes it clear.
        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units")) #On second thought... I think I'm creating a function for this. Hmmmmmmm...
        canvas.bind_all("<Up>", lambda event: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Down>", lambda event: canvas.yview_scroll(1, "units"))

    def unbind_scroll(self, canvas):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Up>")
        canvas.unbind_all("<Down>")

    def disable_undo_redo(self): #Also, I understand it may be counterintuitive for this to be in CreateAnims but status to be in UndoRedo? But it makes sense to me. Here we're plain disabling for the init of a window which is part of CreateAnims.
        self.edit_menu.entryconfigure("Undo", state="disabled") #Ya know what, yes, I'll make it a method and I just call the method. #You cannot undo or redo anything here. Not until you enter your values or close the window without any ado.
        self.edit_menu.entryconfigure("Redo", state="disabled")
        self.edit_menu.entryconfigure("Switch UndoRedo branch", state="disabled")

    def open_url_in_browser(self, url):
        import webbrowser
        webbrowser.open(url, new=2)

    def refresh_UI(self): #This will be part of CreateAnims. All directly UI-related, idea is that it's here. Maybe not the technical like more specific code per se, but at least the highest layer.
        self.tile_utils.refresh_palette() #Changed my mind, will be part of a refresh/update UI.
        self.tile_utils.refresh_chr()
        self.anim.refresh()

    def close(self): #exit
        sys.exit(999)

    def on_x(self):
        if self.undo_redo.trace:
            self.root.bell()
            response = messagebox.askyesno(title="Do you really wish to exit?", message="You have pending unsaved changes. Do you really wish to exit?", default="no")
            if not response:
                return
        sys.exit(999)

    def self_destruct(self, *args):
        from tkinter import messagebox
        if self.in_exception:
            return #Let the main one take care of it. Don't keep spamming messageboxes and stuff. Happens particularly with tooltips like when hovering there's an error then you keep hovering it keeps going.
        self.in_exception = True #in_self_destruct.
        for widget in self.root.winfo_children(): #Physics Window might be open, or not, Physics Dialog might be open, Log History window, Trace, etc. etc... so with this code, we make sure that those windows are destroyed if they exist and CreateAnims can close. And go to sleep and rest.
            if isinstance(widget, tkinter.Toplevel):
                widget.attributes("-disabled", 1) #Block every window active. You're unable to do anything. It's unstable status. Just see the error. Take a screenshot if you want. And please, close it.
        error_message = "".join(traceback.format_exception(*args)) #*args here is arguably and maybe even the same as sys.exception(). #Changed order, do it here so that I don't even have to click on the messagebox, I can see the error right away when debugging in my computer. Beautiful.
        print(error_message, end="") #Yeah whatever. I was going to add a flag but this is fine. I think I can understand when I saw this in other contexts. It will work in my local, with the executable it just won't do anything. No errors exceptions anything.
        messagebox.showerror(title="Unhandled exception", message="Sorry, there was a problem while running CreateAnims. Please see crash_log.txt for details. (and please report the bug!)")
        crash_log = "crash_log.txt"
        with open(crash_log, "w") as crash_log_file:
            crash_log_file.write(error_message + "\nLog History:\n\n" + self.undo_redo.log_history.rstrip()) #Could use f-string but this is fine.
        for widget in self.root.winfo_children(): #Physics Window might be open, or not, Physics Dialog might be open, Log History window, Trace, etc. etc... so with this code, we make sure that those windows are destroyed if they exist and CreateAnims can close. And go to sleep and rest.
            if isinstance(widget, tkinter.Toplevel):
                widget.destroy()
        sys.exit(999)