import os

from Anim import *

class Character:

    def __init__(self, root_dir, character_name, loading_bar, loading_bar_label, character_text): #Changed my mind. I know it's not perfect but whatever, every solution always have problems even if people hide them. If I let them as optional, I still need to check their Noneness. No, if the need ever arises, I will prefer reading this and then copypasting and manually removing those updates, or copypasting from a previous version etc. etc., many other solutions. I could even literally create another Character class altogether. #Not sure if I'll do again that of importing Character in a different context and whatnot but yeah, I'll use optional parameters for that.
        self.name = character_name #Yup! The time has come! I was about to add it, what a pleasant and happy surprise to see it was already added! Thanks past me! #Not sure if we'll need it but... maybe for display purposes? We could add a dictionary or something... anyways, don't want to include too much in this final commit before going back to main.
        self.root_dir = root_dir
        self.palette = self.get_palette(character_name, loading_bar, loading_bar_label, character_text)
        self.anims = self.get_anims(character_name, self.get_anims_ids(character_name), loading_bar, loading_bar_label, character_text)
        self.frames = self.get_frames(character_name, self.get_frames_ids(character_name), loading_bar, loading_bar_label, character_text)
        chr_ids = self.get_chrs_ids(character_name) #When I add more characters, there'll be more and they'll be obtained after we parse the anim file.
        self.chr_palettes, self.chrs = self.get_chrs_and_palettes(character_name, chr_ids, loading_bar, loading_bar_label, character_text) #Whatever, the and makes it clear. Any other name to include both just doesn't make it clear.

    def get_chrs_ids(self, name):
        chrs_filenames=os.listdir(f"{self.root_dir}{os.sep}{name}{os.sep}chr") #Don't ask me why here I use os.sep and in other places I use forward slash.
        chrs_ids = [int(chr_filename.split(".chr.pal")[0][-3:]) for chr_filename in chrs_filenames if chr_filename[-4:] == ".pal"] #Let's use pal to get the IDs and avoid duplicates.
        return chrs_ids

    def get_chrs_and_palettes(self, name, chr_ids, loading_bar, loading_bar_label, character_text): #Yeah, after all we're kinda going to do the loop thing now, though not entirely but leaving the bases.
        chr_palettes = {}
        chrs = {}
        total_chrs = len(chr_ids) #We'll make an exception here. Since they're different files, but part of the same, logical, unit you could say, we'll do it here.
        for i, chr_id in enumerate(chr_ids, start=1): #And here yes, we'll use enumerate, since CHR and CHR PAL aren't expected to be ordered.
            loading_bar_label.configure(text=f"{character_text}. Loading CHR. {i}/{total_chrs}")
            chr_palette = self.get_chr_palette(name, chr_id)
            chr_palettes[chr_id] = chr_palette
            loading_bar['value'] += 1
            character_chr = self.get_chr(name, chr_id)
            chrs[chr_id] = character_chr
            loading_bar['value'] += 1
        return chr_palettes, chrs

    def get_palette(self, name, loading_bar, loading_bar_label, character_text):
        with open(f"{self.root_dir}/{name}/pal/{name}_usual.pal", "rb") as character_pal:
            loading_bar_label.configure(text=f"{character_text}. Loading palette.")
            palette = list(character_pal.read())
            loading_bar['value'] += 1
        return palette

    def get_chr_palette(self, name, chr_id): #When we include absolutely every CHR_PALETTE with its corresponding CHR (I used uppercase cause I wanted to), we can iterate over a loop and then append to a chr_palettes and character_chrs. Awesome.
        with open(f"{self.root_dir}/{name}/chr/{name}_chr_pal_{chr_id:03d}.chr.pal", "rb") as character_chr_pal:
            chr_palette = list(character_chr_pal.read())
        return chr_palette

    def get_chr(self, name, chr_id):
        with open(f"{self.root_dir}/{name}/chr/{name}_chr_{chr_id:03d}.chr", "rb") as character_chr:
            character_chr = list(character_chr.read())
        return character_chr #Added character cause otherwise chr, you know, reserved keyword.

    def get_frames_ids(self, name):
        frames_filenames=os.listdir(f"{self.root_dir}{os.sep}{name}{os.sep}frames") #Don't ask me why here I use os.sep and in other places I use forward slash.
        frames_ids = [int(frame_filename.split(".frame")[0][-3:]) for frame_filename in frames_filenames]
        return frames_ids

    def get_frames(self, name, frame_ids, loading_bar, loading_bar_label, character_text):
        frames = [] #This one will be 0-indexed. Frame 00, frame 01 etc.
        total_frames = len(frame_ids)
        for frame_id in frame_ids: #Potentially range(frame_ids) or something of the sort.
            frame = self.get_frame(name, frame_id, total_frames, loading_bar, loading_bar_label, character_text)
            frames.append(frame)
        return frames

    def get_frame(self, name, frame_id, total_frames, loading_bar, loading_bar_label, character_text):
        with open(f"{self.root_dir}/{name}/frames/{name}_frame_{frame_id:03d}.frame", "rb") as character_frame:
            loading_bar_label.configure(text=f"{character_text}. Loading frames. {frame_id+1}/{total_frames}")
            frame = Frame(list(character_frame.read()))
            loading_bar['value'] += 1
        return frame

    def get_anims_ids(self, name):
        anims_filenames=os.listdir(f"{self.root_dir}{os.sep}{name}{os.sep}anims") #Don't ask me why here I use os.sep and in other places I use forward slash.
        anims_ids = [int(anim_filename.split(".anim")[0][-3:]) for anim_filename in anims_filenames]
        return anims_ids

    def get_anims(self, name, anim_ids, loading_bar, loading_bar_label, character_text):
        anims = [] #This one will be 0-indexed too. Anim 00, Anim 01 etc. #Might change this soon enough because some anims don't have files, like I removed them, like anim 0xF I believe. Yeah just checked.
        total_anims = len(anim_ids)
        for anim_id in anim_ids: #Potentially range(frame_ids) or something of the sort.
            anim = self.get_anim(name, anim_id, total_anims, loading_bar, loading_bar_label, character_text)
            anims.append(anim)
        return anims

    def get_anim(self, name, anim_id, total_anims, loading_bar, loading_bar_label, character_text):
        with open(f"{self.root_dir}/{name}/anims/{name}_anim_{anim_id:03d}.anim", "rb") as character_anim:
            loading_bar_label.configure(text=f"{character_text}. Loading anims. {anim_id+1}/{total_anims}") #Again, +1 since we won't be using enumerate here. I don't feel like it. And I mean, I would have to pass that here too. For physics it's different because I don't have the IDs to begin with.
            anim = CharacterAnim(list(character_anim.read()))
            loading_bar['value'] += 1
        return anim