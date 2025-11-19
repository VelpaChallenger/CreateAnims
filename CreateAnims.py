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
HEIGHT = 620
INITIAL_X = 500
INITIAL_Y = 200

PHYSICS_WIDTH = 430
PHYSICS_HEIGHT = 310
PHYSICS_INITIAL_X = 600
PHYSICS_INITIAL_Y = 250

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
        self.physics_directory = None
        self.png_img = []
        self.in_play_anim = False
        self.physics_list = []

    def init_anim_window(self):
        self.root.title("Create Anims") #Sometimes dreams come true! Believe in them!
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{INITIAL_X}+{INITIAL_Y}") #It's how my mind sees things. It's the initial, you might drag the window around and stuff. #Window x/y could be alternative name.
        self.make_styles()

        frame_stage = tkinter.Frame(self.root, border=0) #Scenario also. But I like more stage. It's where the action happens.
        frame_stage.grid(row=0, column=0, columnspan=3, sticky="w")
        self.anim_canvas = tkinter.Canvas(frame_stage, width=860, height=256, bg="#E0E0E0", borderwidth=0, highlightthickness=0)
        self.anim_canvas.grid(row=0, column=0)

        frame_palette = tkinter.Frame(self.root, border=0)
        frame_palette.grid(row=1, column=0, rowspan=3, sticky="nw")
        self.pal_label = tkinter.Label(frame_palette, text="Palette:", anchor="w", font=FONT)
        self.pal_label.grid(row=0, column=0, sticky="w")
        self.character_palette_canvas = tkinter.Canvas(frame_palette, width=256, height=32, bg="#808080", borderwidth=0, highlightthickness=0)
        self.character_palette_canvas.grid(row=1, column=0)
        self.color_picker_canvas = tkinter.Canvas(frame_palette, width=256, height=69, bg="#808080", borderwidth=0, highlightthickness=0)
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
        file_menu.add_command(label="Save palette", command=self.command.save_palette)
        file_menu.add_command(label="Save CHR palette", command=self.command.save_chr_palette)
        file_menu.add_command(labe="Save frame", command=self.command.save_frame)
        file_menu.add_command(label="Save anim", command=self.command.save_anim)
        file_menu.add_command(label="Save physics", command=self.command.save_physics)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        anim_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        anim_menu.add_command(label="Toggle transparency", command=self.command.toggle_anim_transparency, accelerator="Shift+T") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("<Shift-T>", self.command.toggle_anim_transparency)
        anim_menu.add_command(label="Toggle rectangle around frame", command=self.command.toggle_draw_frame_rectangle, accelerator="r") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("r", self.command.toggle_draw_frame_rectangle)
        anim_menu.add_command(label="Toggle draw empty cells", command=self.command.toggle_draw_empty_cells, accelerator="e") #We'll add a little 'anim' in the name for me. Yay.
        self.root.bind("e", self.command.toggle_draw_empty_cells)
        self.menu_bar.add_cascade(label="Anim", menu=anim_menu)
        import_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        import_menu.add_command(label="Palette", command=self.command.import_palette)
        import_menu.add_command(label="CHR", command=self.command.import_chr)
        import_menu.add_command(label="CHR Palette", command=self.command.import_chr_palette)
        import_menu.add_command(label="Frame", command=self.command.import_frame)
        import_menu.add_command(label="Anim", command=self.command.import_anim)
        import_menu.add_command(label="Physics", command=self.command.import_physics)
        self.menu_bar.add_cascade(label="Import", menu=import_menu)
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
            initial_y += 17
            for col in range(16):
                rgb_triplet = SYSTEM_PALETTE[pal_index]
                r, g, b = rgb_triplet[0], rgb_triplet[1], rgb_triplet[2]
                rgb = f"#{r:02X}{g:02X}{b:02X}"
                color_picker_rectangle = self.color_picker_canvas.create_rectangle(initial_x, initial_y, initial_x + 15, initial_y + 16, fill=rgb, outline=rgb, width=1)
                self.color_picker_rectangles.append(ColorPickerRectangle(self, self.color_picker_canvas, color_picker_rectangle, pal_index, rgb, self.pal_label))
                initial_x += 16
                pal_index += 1

    def init_physics_window(self): #Probably will have a destroy as well? In case of Ok/Cancel.
        self.physics_window = tkinter.Toplevel(self.root)
        self.physics_window.title("Create Anims Physics Manager") #Sometimes dreams come true! Believe in them!
        self.physics_window.geometry(f"{PHYSICS_WIDTH}x{PHYSICS_HEIGHT}+{PHYSICS_INITIAL_X}+{PHYSICS_INITIAL_Y}")
        self.root.attributes('-disabled', 1)
        self.physics_window.transient(self.root) # set to be on top of the main window
        self.physics_window.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        self.physics_window.focus_force()

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
        self.root.wait_window(self.physics_window) # pause anything on the main window until this one closes
        self.root.attributes('-disabled', 0)
        self.root.focus_force()

    def init_physics_dialog(self, frame_index): #Technically a window, but yeah, a dialog.
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
        vcmd = (self.physics_dialog.register(self.anim.validate_physics_dialog_x_entry), "%P") #For Y, the function will be the same. A bit confusing maybe for future me, but please read this!
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
        self.physics_dialog_refresh = False #By default, but EntryReturn might set it to True.
        self.physics_window.wait_window(self.physics_dialog)
        self.physics_window.attributes('-disabled', 0)
        self.physics_window.focus_force()
        if self.physics_dialog_refresh:
            self.anim.fill_physics_grid()

    def refresh_UI(self): #This will be part of CreateAnims. All directly UI-related, idea is that it's here. Maybe not the technical like more specific code per se, but at least the highest layer.
        self.tile_utils.refresh_palette() #Changed my mind, will be part of a refresh/update UI.
        self.tile_utils.refresh_chr()
        self.anim.refresh()