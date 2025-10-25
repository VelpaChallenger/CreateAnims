from tkinter import filedialog
import os

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
            pal_file.write(bytearray(self.createanims.characters_palettes[self.createanims.current_character]))