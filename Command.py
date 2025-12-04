from tkinter import filedialog
import os

from Anim import Frame, CharacterAnim

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

    def save_chr(self): #Let's add it after all. There's no CHR editor (for now), there might be one in the future but even if there isn't, you might want to import and then save that only.
        initial_directory = self.createanims.chr_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        chr_filename = filedialog.asksaveasfilename(
            defaultextension=".chr",
            filetypes=[("CHR files", ".chr"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Save CHR",
            parent=self.createanims.root
        )
        if not chr_filename: #Then save was aborted.
            return
        self.createanims.chr_directory = os.path.dirname(chr_filename) #Directory where the file selected is.
        with open(chr_filename, "wb") as chr_file:
            chr_file.write(bytearray(self.createanims.characters[self.createanims.current_character].chrs[self.createanims.current_chr_bank]))

    def save_chr_palette(self):
        initial_directory = self.createanims.chr_palette_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        chr_pal_filename = filedialog.asksaveasfilename(
            defaultextension=".chr.pal",
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
            frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id]
            metadata = frame.metadata
            x_offset_for_file = abs(metadata.x_offset) | (0x80 if metadata.x_offset > 0 else 0x00) #We do need to perform a conversion. It is convenient for editing, but then when we save the file, we do need to convert it back.
            y_offset_for_file = abs(metadata.y_offset) | (0x20 if metadata.y_offset > 0 else 0x00)
            frame_file.write(bytearray([metadata.x_length, metadata.y_length, x_offset_for_file, metadata.chr_bank, y_offset_for_file, 0x0])) #Metadata first.
            frame_file.write(bytearray(frame.tiles)) #And now the tiles.

    def save_anim(self):
        initial_directory = self.createanims.anims_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        anim_filename = filedialog.asksaveasfilename(
            defaultextension=".anim",
            filetypes=[("Anim files", ".anim"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Save anim",
            parent=self.createanims.root
        )
        if not anim_filename: #Then save was aborted.
            return
        self.createanims.anims_directory = os.path.dirname(anim_filename) #Directory where the file selected is.
        with open(anim_filename, "wb") as anim_file:
            anim = self.createanims.characters[self.createanims.current_character].anims[self.createanims.current_anim]
            anim_file.write(bytearray([anim.physics_id]))
            anim_file.write(bytearray(anim.frame_ids))

    def save_physics(self):
        initial_directory = self.createanims.physics_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        physics_filename = filedialog.asksaveasfilename(
            defaultextension=".physics",
            filetypes=[("Physics files", ".physics"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Save physics",
            parent=self.createanims.root
        )
        if not physics_filename: #Then save was aborted.
            return
        self.createanims.physics_directory = os.path.dirname(physics_filename) #Directory where the file selected is.
        with open(physics_filename, "wb") as physics_file:
            physics = self.createanims.physics_list[self.createanims.current_physics_id]
            physics_file.write(bytearray(physics))

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
            new_palette = list(pal_file.read())
        character = self.createanims.characters[self.createanims.current_character] #Let's do it here. Let's close the file.
        old_palette = character.palette[:] #Just in case, don't use the exact same list, use a copy. Oh, but to do same thing as with frame_tiles, let's do it... hmmmm... yeah I know, frame_tiles wasn't part of the update so... ok whatever this is ok.
        if old_palette == new_palette: #Same check as always or almost always, it matters in this case.
            return
        self.createanims.undo_redo.undo_redo([self.load_new_character_palette_imported_value, old_palette, "None"], [self.load_new_character_palette_imported_value, new_palette, pal_filename])

    def load_new_character_palette_imported_value(self, new_palette, imported_from_filename): #Similar to for index, but this loads the entire palette all at once. #And as always, value at the end to identify that this is part of UndoRedo.
        character = self.createanims.characters[self.createanims.current_character]
        character.palette = new_palette[:] #Same, if one changes, I don't want the other to change too.
        self.createanims.refresh_UI() #We always do that here inside the value. #This is the only exception, there's nothing affected by this. The hovers, the entries, a refresh_UI is enough to show updates.

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
            new_chr = list(chr_file.read())
        character = self.createanims.characters[self.createanims.current_character]
        old_chr = character.chrs[self.createanims.current_chr_bank][:]
        if old_chr == new_chr:
            return
        self.createanims.undo_redo.undo_redo([self.load_new_chr_imported_value, old_chr, "None"], [self.load_new_chr_imported_value, new_chr, chr_filename])

    def load_new_chr_imported_value(self, new_chr, imported_from_filename):
        character = self.createanims.characters[self.createanims.current_character]
        character.chrs[self.createanims.current_chr_bank] = new_chr[:]
        self.createanims.tile_utils.load_new_chr_bank_value(self.createanims.current_chr_bank) #Yes I do have to do it always. There are always checks I need to run when importing new stuff. Like clearing or leaving the entry in white if it was red also stuff like that all sorts of stuff.

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
            new_chr_palette = list(chr_pal_file.read())
        character = self.createanims.characters[self.createanims.current_character]
        old_chr_palette = character.chr_palettes[self.createanims.current_chr_bank][:]
        if old_chr_palette == new_chr_palette:
            return
        self.createanims.undo_redo.undo_redo([self.load_new_chr_palette_imported_value, old_chr_palette, "None"], [self.load_new_chr_palette_imported_value, new_chr_palette, chr_pal_filename])

    def load_new_chr_palette_imported_value(self, new_chr_palette, imported_from_filename):
        character = self.createanims.characters[self.createanims.current_character]
        character.chr_palettes[self.createanims.current_chr_bank] = new_chr_palette[:]
        self.createanims.tile_utils.load_new_chr_bank_value(self.createanims.current_chr_bank)

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
            new_frame_bytes = list(frame_file.read()) #Refactor to adapt to UndoRedo. I don't really like assigning to instances. We are referring to the same object in memory, it can cause lots of trouble.
        character = self.createanims.characters[self.createanims.current_character]
        old_frame = character.frames[self.createanims.current_frame_id]
        old_frame_bytes = old_frame.metadata.get_bytes() + old_frame.tiles #I could also like save an attribute old_frame_bytes or just frame_bytes in the Frame but, I want to save memory? lol it's just a couple of bytes but whatever.
        if old_frame_bytes == new_frame_bytes: #My, come to think of it, this is a huge huge advantage of doing it this way. This becomes super trivial to check. Whereas with instances checks, I will try just to satisfy my curiosity but I'm pretty sure it wouldn't work because the instances themselves aren't equal. Or maybe it's like lists? And it checks values themselves. Will check.
            return
        self.createanims.undo_redo.undo_redo([self.load_new_frame_imported_value, old_frame_bytes, "None"], [self.load_new_frame_imported_value, new_frame_bytes, frame_filename])

    def load_new_frame_imported_value(self, new_frame_bytes, imported_from_filename):
        character = self.createanims.characters[self.createanims.current_character]
        character.frames[self.createanims.current_frame_id] = Frame(new_frame_bytes) #At this point, the old Frame will be garbage collected and the memory freed.
        self.createanims.anim.load_new_frame_value(self.createanims.current_frame) #Same logic as anim. This was causing bugs in UndoRedo. This has to update CHR bank and a bunch of other stuff.

    def import_anim(self): #On second thought, maybe I'll let it be. Sometimes anim before frame, sometimes frame after anim.
        initial_directory = self.createanims.anims_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        anim_filename = filedialog.askopenfilename(
            defaultextension=".anim",
            filetypes=[("Anim files", ".anim"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Import anim",
            parent=self.createanims.root
        )
        if not anim_filename: #Then save was aborted.
            return
        self.createanims.anims_directory = os.path.dirname(anim_filename) #Directory where the file selected is.
        with open(anim_filename, "rb") as anim_file:
            new_anim_bytes = list(anim_file.read())
        character = self.createanims.characters[self.createanims.current_character]
        old_anim = character.anims[self.createanims.current_anim]
        old_anim_bytes = [old_anim.physics_id] + old_anim.frame_ids
        if old_anim_bytes == new_anim_bytes:
            return
        self.createanims.undo_redo.undo_redo([self.load_new_anim_imported_value, old_anim_bytes, "None"], [self.load_new_anim_imported_value, new_anim_bytes, anim_filename])

    def load_new_anim_imported_value(self, new_anim_bytes, imported_from_filename):
        character = self.createanims.characters[self.createanims.current_character]
        character.anims[self.createanims.current_anim] = CharacterAnim(new_anim_bytes)
        self.createanims.anim.load_new_anim_value(self.createanims.current_anim) #Ironic but yes. Load the same ID, so not new but, you will find changes when loading it. #self.createanims.current_frame_id = character.anims[self.createanims.current_anim].frame_ids[0] #Very important otherwise UI refresh won't draw it updated. (oh no, I just made the horizontal scrollbar of death appear!) Also no, no need to call load_new_anim here, though of course it would work. But I feel this is cleaner in this context. Nothing has to change except this. Even the arrow status will be fine as it is, as it is still the same ids. Huh wait. Yes I do need to call it. Thanks me for writing this. import_frame indeed doesn't need it because the change is only graphical, like, only the tiles will change.

    def import_physics(self):
        initial_directory = self.createanims.physics_directory
        if initial_directory is None:
            initial_directory = os.getcwd()
        physics_filename = filedialog.askopenfilename(
            defaultextension=".physics",
            filetypes=[("Physics files", ".physics"), ("All files", "*.*")],
            initialdir=initial_directory,
            title="Import physics",
            parent=self.createanims.root
        )
        if not physics_filename: #Then save was aborted. #Import was aborted. But you know copypaste.
            return
        self.createanims.physics_directory = os.path.dirname(physics_filename) #Directory where the file selected is.
        with open(physics_filename, "rb") as physics_file:
            new_physics = list(physics_file.read())
        old_physics = self.createanims.physics_list[self.createanims.current_physics_id]
        if old_physics == new_physics:
            return
        self.createanims.undo_redo.undo_redo([self.load_new_physics_imported_value, old_physics, "None"], [self.load_new_physics_imported_value, new_physics, physics_filename])

    def load_new_physics_imported_value(self, new_physics, imported_from_filename):
        self.createanims.physics_list[self.createanims.current_physics_id] = new_physics[:] #Analogous to chr_palette. Has to be copy otherwise when we modify them in Edit physics for example they'll both get modified. For frames and anims it's different because we don't use the bytes themselves, we use the attributes which were filled based on those bytes. Not the same.
        self.createanims.anim.load_new_physics_id_value(self.createanims.current_physics_id) #I was going to add a messagebox but... I think it'll be enough with the potential physics ID mismatch and if not, you can still use Edit physics, like, I don't want it to be too annoying, I know what it feels like. But if I'm asked to add it, I will. #Similar logic to why loading new anim when importing an anim. There are some updates that need to run. Like for example, if the new physics has a mismatch, that has to run. And has to set the flag.

    def save_changes(self):
        self.createanims.undo_redo.trace.clear()
        self.createanims.undo_redo.saved = True
        for affected_file in list(set(self.createanims.undo_redo.affected_files)):
            filename = affected_file[2:].rstrip() #Let's not forget the newline. #Remove the - used for displaying purposes.
            filename_split = filename.split("/") #This might be more friendly for performance?
            if filename_split[0] != "physics":
                file_type = filename_split[1] #Careful, if we ever write code that runs in Linux as well and MacOS and other operating systems, we might have to change this.
            else:
                file_type = filename_split[0]
            if filename[-7:] == "chr.pal": #Come to think of it, maybe I could have used file extension from the beginning and the logic was simplified. Whatever.
                file_type = "chr_pal"
            if file_type == "anims":
                with open(f"{self.createanims.root_dir}/{filename}", "wb") as anim_file: #Same as save_anim, could encapsulate in same function. Well actually no, there are many differences. And the with can maybe be moved to the top? But I kinda like it this way here. Not a difference with performance no, it will have to run either way.
                    character_name = filename_split[0]
                    character_ID = self.createanims.characters_dict[character_name] #And yes, I could use character but... again it's all on context?
                    anim_ID = int(affected_file.split(".")[0][-3:]) #Could also use offset but, split with period makes it easier to copypaste. And to read too. Alhough I liked more -1:-4, but yes, it has to be -4 for the behavior I want. Technically the way to say last 3 digits though. But yeah, I won't contradict. -1:-4 is the right way.
                    anim = self.createanims.characters[character_ID].anims[anim_ID]
                    anim_file.write(bytearray([anim.physics_id]))
                    anim_file.write(bytearray(anim.frame_ids))
            elif file_type == "frames":
                with open(f"{self.createanims.root_dir}/{filename}", "wb") as frame_file:
                    character_name = filename_split[0]
                    character_ID = self.createanims.characters_dict[character_name]
                    frame_ID = int(affected_file.split(".")[0][-3:])
                    frame = self.createanims.characters[character_ID].frames[frame_ID]
                    metadata = frame.metadata
                    x_offset_for_file = abs(metadata.x_offset) | (0x80 if metadata.x_offset > 0 else 0x00)
                    y_offset_for_file = abs(metadata.y_offset) | (0x20 if metadata.y_offset > 0 else 0x00)
                    frame_file.write(bytearray([metadata.x_length, metadata.y_length, x_offset_for_file, metadata.chr_bank, y_offset_for_file, 0x0])) #Metadata first.
                    frame_file.write(bytearray(frame.tiles)) #And now the tiles.
            elif file_type == "physics":
                with open(f"{self.createanims.root_dir}/{filename}", "wb") as physics_file:
                    physics_ID = int(affected_file.split(".")[0][-3:])
                    physics = self.createanims.physics_list[physics_ID]
                    physics_file.write(bytearray(physics))
            elif file_type == "pal":
                with open(f"{self.createanims.root_dir}/{filename}", "wb") as pal_file:
                    character_name = filename_split[0]
                    character_ID = self.createanims.characters_dict[character_name]
                    pal_file.write(bytearray(self.createanims.characters[character_ID].palette))
            elif file_type == "chr":
                with open(f"{self.createanims.root_dir}/{filename}", "wb") as chr_file:
                    character_name = filename_split[0]
                    character_ID = self.createanims.characters_dict[character_name]
                    chr_bank = int(affected_file.split(".")[0][-3:])
                    chr_file.write(bytearray(self.createanims.characters[character_ID].chrs[chr_bank]))
            elif file_type == "chr_pal":
                with open(f"{self.createanims.root_dir}/{filename}", "wb") as chr_pal_file:
                    character_name = filename_split[0]
                    character_ID = self.createanims.characters_dict[character_name]
                    chr_bank = int(affected_file.split(".")[0][-3:])
                    chr_pal_file.write(bytearray(self.createanims.characters[character_ID].chr_palettes[chr_bank]))
            else:
                raise ValueError(f"Could not find file_type for {affected_file}") #Yes, let's be explicit about it this time around, I wouldn't want the file_type to be skipped and just not saved or something.
        self.createanims.undo_redo.affected_files.clear() #Has to happen at the end. Otherwise the for loop will not run.
        self.createanims.save_changes_window.destroy() #For now this. Will then implement the full logic based on affected files and such.

    def open_docs_in_browser(self):
        import webbrowser
        readme_path = os.path.abspath("README.html")
        url = "file://" + readme_path
        webbrowser.open(url, new=2)

    def check_for_updates(self):
        import requests
        import webbrowser
        import json
        import re
        import subprocess
        from tkinter import messagebox

        try: #Yes, I could encapsulate this but whatever. If I ever do, will use CreateAnims which... I mean... it's like open_url, I consider it still part of CreateAnims' core.
            request_response = requests.get("https://api.github.com/repos/VelpaChallenger/CreateAnims/branches/main")
        except requests.exceptions.ConnectionError:
            messagebox.showerror(title="Unable to check for updates", message="Unable to check for updates. Please confirm you have an stable internet connection.") #I remember all the times I read stuff like this, what do you mean I don't have an STABLE internet connection, it's more stable than you are you...!! lol. Oh this is a comment right? Which means other people are gonna read it? I mean. Whatever.
            return
        commit_id_main = json.loads(request_response.text)["commit"]["sha"] #Found a super use case for json and parsing and such.
        try:
            request_response = requests.get(f"https://github.com/VelpaChallenger/Create-Anims/blob/{commit_id_main}/CreateAnims.py?raw=True") #Yes that's it. If you send main, it's going to use the cached version which might take long to update. But if you use the commit, it's going to be the latest right away. Exactly what we want. #Ohhh that might be it. I remember I saw something about the cache!
        except requests.exceptions.ConnectionError:
            messagebox.showerror(title="Unable to check for updates", message="Unable to check for updates. Please confirm you have an stable internet connection.")
            return
        CreateAnims_buf = request_response.text.split("\n") #Let's do it exactly the same way as forward, now backwards or... well you get what I mean.
        for i, line in enumerate(CreateAnims_buf):
            if line.strip().startswith("CREATEANIMS_VERSION_DATE"):
                break
        version_from_remote = re.findall('"(.*)"', CreateAnims_buf[i+1])[0]
        from CreateAnims import CREATEANIMS_VERSION
        if version_from_remote != CREATEANIMS_VERSION:
            if self.createanims.undo_redo.trace: #But wait! There might be unsaved changes.
                response = messagebox.askyesno(title="Update available but...", message="There's an update available, but you have unsaved changes. Do you still wish to download and restart with the updated version?")
            else:
                response = messagebox.askyesno(title="Update available!", message="There's an update available. Do you wish to download and restart with the updated version?")
            if response:
                subprocess.Popen("CreateAnimsUpdater.exe") #Again, Popen so that CreateAnims can gracefully close and CreateAnimsUpdater will take it from there.
                self.createanims.root.destroy()
                return
                #pass #Do the download. Well actually, call CreateAnimsUpdater.exe which will be included in the zip (and if it doesn't exist, raise another error) and then close this instance of Tkinter, like fully close it. Then CreateAnimsUpdater.exe will show the progress bar and when it ends, the new instance will be up and running. Awesome.
        else:
            messagebox.showinfo(title="Up to date!", message="You're already up-to-date! :) .")