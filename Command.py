from tkinter import filedialog
import os

from Anim import Frame

class Command:

    def __init__(self, createanims):
        self.createanims = createanims

    def save_palette(self):
        initial_directory = self.createanims.palette_directory
        if self.createanims.palette_directory is None:
            initial_directory = os.getcwd()
        pal_filename = filedialog.asksaveasfilename(
            defaultextension=".pal",
            filetypes=[("Palette files", ".pal"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Save palette",
            parent=self.createanims.root
        )
        if not pal_filename: #Then save was aborted.
            return
        self.createanims.palette_directory = os.path.dirname(pal_filename) #Directory where the file selected is.
        with open(pal_filename, "wb") as pal_file:
            pal_file.write(bytearray(self.createanims.characters[self.createanims.current_character].palette))

    def save_chr_palette(self):
        initial_directory = self.createanims.chr_palette_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        chr_pal_filename = filedialog.asksaveasfilename(
            defaultextension=".pal",
            filetypes=[("CHR Palette files", ".chr.pal"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Save CHR palette",
            parent=self.createanims.root
        )
        if not chr_pal_filename: #Then save was aborted.
            return
        self.createanims.chr_palette_directory = os.path.dirname(chr_pal_filename) #Directory where the file selected is.
        with open(chr_pal_filename, "wb") as chr_pal_file:
            chr_pal_file.write(bytearray(self.createanims.characters[self.createanims.current_character].chr_palettes[self.createanims.current_chr_bank]))

    def save_frame(self):
        initial_directory = self.createanims.frames_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        frame_filename = filedialog.asksaveasfilename(
            defaultextension=".frame",
            filetypes=[("Frame files", ".frame"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Save frame",
            parent=self.createanims.root
        )
        if not frame_filename: #Then save was aborted.
            return
        self.createanims.frames_directory = os.path.dirname(frame_filename) #Directory where the file selected is.
        with open(frame_filename, "wb") as frame_file:
            frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame]
            metadata = frame.metadata
            frame_file.write(bytearray([metadata.x_length, metadata.y_length, metadata.x_offset, metadata.chr_bank, metadata.y_offset, 0x0])) #Metadata first.
            frame_file.write(bytearray(frame.tiles)) #And now the tiles.

    def toggle_anim_transparency(self, event=None): #When it's called from keyboard shortcut, event is sent. So we need event=None, we won't use it anyways.
        self.createanims.anim.transparency ^= 1 #Let's make it a literal toggle.
        self.createanims.anim.refresh() #But, as usual, a refresh also.

    def toggle_draw_frame_rectangle(self, event=None): #When it's called from keyboard shortcut, event is sent. So we need event=None, we won't use it anyways.
        self.createanims.anim.draw_frame_rectangle ^= 1 #Let's make it a literal toggle.
        self.createanims.anim.refresh() #But, as usual, a refresh also.

    def toggle_draw_empty_cells(self, event=None):
        self.createanims.anim.draw_empty_cells ^= 1
        self.createanims.anim.refresh()

    def import_palette(self):
        initial_directory = self.createanims.palette_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        pal_filename = filedialog.askopenfilename(
            defaultextension=".pal",
            filetypes=[("Palette files", ".pal"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Import palette",
            parent=self.createanims.root
        )
        if not pal_filename:
            return
        self.createanims.palette_directory = os.path.dirname(pal_filename)
        with open(pal_filename, "rb") as pal_file:
            character = self.createanims.characters[self.createanims.current_character]
            character.palette = list(pal_file.read())
        self.createanims.refresh_UI()

    def import_chr(self):
        initial_directory = self.createanims.chr_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        chr_filename = filedialog.askopenfilename(
            defaultextension=".chr",
            filetypes=[("CHR files", ".chr"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Import CHR",
            parent=self.createanims.root
        )
        if not chr_filename:
            return
        self.createanims.chr_directory = os.path.dirname(chr_filename)
        with open(chr_filename, "rb") as chr_file:
            character = self.createanims.characters[self.createanims.current_character]
            character.chrs[self.createanims.current_chr_bank] = list(chr_file.read())
        self.createanims.refresh_UI()

    def import_chr_palette(self):
        initial_directory = self.createanims.chr_palette_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        chr_pal_filename = filedialog.askopenfilename(
            defaultextension=".chr.pal",
            filetypes=[("CHR Palette files", ".chr.pal"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Import CHR palette",
            parent=self.createanims.root
        )
        if not chr_pal_filename:
            return
        self.createanims.chr_palette_directory = os.path.dirname(chr_pal_filename)
        with open(chr_pal_filename, "rb") as chr_pal_file:
            character = self.createanims.characters[self.createanims.current_character]
            character.chr_palettes[self.createanims.current_chr_bank] = list(chr_pal_file.read())
        self.createanims.refresh_UI()

    def import_frame(self):
        initial_directory = self.createanims.frames_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        frame_filename = filedialog.askopenfilename(
            defaultextension=".frame",
            filetypes=[("Frame files", ".frame"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Import frame",
            parent=self.createanims.root
        )
        if not frame_filename: #Then save was aborted.
            return
        self.createanims.frames_directory = os.path.dirname(frame_filename) #Directory where the file selected is.
        with open(frame_filename, "rb") as frame_file:
            character = self.createanims.characters[self.createanims.current_character]
            frame = Frame(list(frame_file.read()))
            character.frames[self.createanims.current_frame] = frame
        self.createanims.refresh_UI()