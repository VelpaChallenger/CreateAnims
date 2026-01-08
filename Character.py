import os

from Anim import *

class CreateAnimsFileFormatError(Exception): #CharacterFileFormatError.
    pass #The idea is to have a try-except this error to identify different kinds of errors.

class CreateAnimsFileNameError(Exception):
    pass

class Character:

    def __init__(self, root_dir, file_format_validator, character_name, loading_bar, loading_bar_label, character_text): #And I did create a FileFormatValidator. #And changed my mind in this too. Yes, I could create a Validator of sorts. Yes I could use static methods on Anim and also create classes for CHR and CHR PAL and PAL. But, none of these convince me. I don't follow what others do. I follow what suits me best. #Changed my mind. I know it's not perfect but whatever, every solution always have problems even if people hide them. If I let them as optional, I still need to check their Noneness. No, if the need ever arises, I will prefer reading this and then copypasting and manually removing those updates, or copypasting from a previous version etc. etc., many other solutions. I could even literally create another Character class altogether. #Not sure if I'll do again that of importing Character in a different context and whatnot but yeah, I'll use optional parameters for that.
        self.name = character_name #Yup! The time has come! I was about to add it, what a pleasant and happy surprise to see it was already added! Thanks past me! #Not sure if we'll need it but... maybe for display purposes? We could add a dictionary or something... anyways, don't want to include too much in this final commit before going back to main.
        self.root_dir = root_dir
        self.palette = self.get_palette(file_format_validator, character_name, loading_bar, loading_bar_label, character_text)
        self.frames = self.get_frames(file_format_validator, character_name, loading_bar, loading_bar_label, character_text) #Won't add the check while loading, added when navigating. #This order makes more sense. And plus, now I will be able to check the frames for the anims. Will add it after all. Can be a lot of trouble otherwise. And it does feel a bit inconsistent with the other checks.
        self.anims = self.get_anims(file_format_validator, character_name, loading_bar, loading_bar_label, character_text)
        self.chr_palettes, self.chrs = self.get_chrs_and_palettes(file_format_validator, character_name, loading_bar, loading_bar_label, character_text) #Whatever, the and makes it clear. Any other name to include both just doesn't make it clear.

    def get_chrs_and_palettes(self, file_format_validator, name, loading_bar, loading_bar_label, character_text): #Yeah, after all we're kinda going to do the loop thing now, though not entirely but leaving the bases.
        chr_directory = f"{self.root_dir}{os.sep}{name}{os.sep}chr"
        if not os.path.exists(chr_directory):
            raise CreateAnimsFileNameError(f"Invalid filename: Directory chr doesn't exist for character {name}.")
        chrs_filenames = os.listdir(chr_directory) #Don't ask me why here I use os.sep and in other places I use forward slash.
        if not chrs_filenames:
            raise CreateAnimsFileNameError(f"Invalid filename: Directory chr for character {name} is empty. Please add at least one .chr and .chr.pal file with the expected format (see docs for details, section internals).")
        found_chr_pal = False #This ends up being the simplest solution. Other solutions/alternatives involve peeking ahead or stuff like that.
        chr_palettes = {}
        chrs = {}
        total_chrs = len(chrs_filenames) #We'll make an exception here. Since they're different files, but part of the same, logical, unit you could say, we'll do it here.
        for i, chrs_filename in enumerate(chrs_filenames, start=1): #Notice the difference: filename vs filenameS. #And here yes, we'll use enumerate, since CHR and CHR PAL aren't expected to be ordered.
            chr_palette_split = chrs_filename.split(".", 1) #Important that we only split one time. Otherwise the check against chr will always return True and will not load any CHR. Still you get the total files validation, but it doesn't load. #We first need to check if there is something after the dot . to begin with. Maybe that's an impossible?
            if len(chr_palette_split) >= 2 and chr_palette_split[1] == "chr": #Avoid duplicates.
                continue
            loading_bar_label.configure(text=f"{character_text}. Loading CHR. {i}/{total_chrs}")
            if len(chr_palette_split) >= 2 and chr_palette_split[1] != "chr.pal":
                raise CreateAnimsFileNameError(f"Invalid filename: File {chrs_filename} doesn't have a .chr.pal extension.")
            if len(chr_palette_split[0]) < 3:
                raise CreateAnimsFileNameError(f"Invalid filename: File {chrs_filename} doesn't have a valid CHR ID. It has to be 3 digits long and be placed just before the file extension.")
            chr_id_string = chr_palette_split[0][-3:] #There'll always be at least one element for a split, even if no match. Though... nothing guarantees there'll be a last 3 elements. Urgh.
            if not chr_id_string.isdigit():  #Also, we can use isdigit here to avoid more... nesting? with try-except. Heh, kinda the same here actually but anyways. No negatives anyways, so isdigit is a bit more explicit in that sense.
                raise CreateAnimsFileNameError(f"Invalid filename: File {chrs_filename} doesn't have a valid CHR ID. It must contain only digits from 0 to 9.")
            chr_id = int(chr_id_string) #Now validated.
            is_new_chr_id = chr_palettes.get(chr_id, None)
            if is_new_chr_id is not None:
                raise CreateAnimsFileNameError(f"Invalid filename: File {chrs_filename} uses a CHR ID already loaded before.")
            chr_palette = self.get_chr_palette(name, chr_id) #All validations passed, hurray! Except, of course, now we have to check the file actually follows the complete format. We only validated the ID and the extension.
            if not file_format_validator.validate_chr_pal(chr_palette): #len(chr_palette) != 16: #I was going to use tile_utils and use same code for import, but then I'd need to pass createanims here. %$#% it.
                raise CreateAnimsFileFormatError(f"Invalid CHR PAL format for file {name}_chr_pal_{chr_id:03d}.chr.pal: CHR PAL is not exactly 16 bytes long. (1 byte per 8 tiles, 128 tiles per 2K CHR Bank, for a total of 16 bytes)")
            chr_palettes[chr_id] = chr_palette
            loading_bar['value'] += 1
            character_chr = self.get_chr(name, chr_id)
            if not file_format_validator.validate_chr(character_chr): #len(character_chr) != 2048:
                raise CreateAnimsFileFormatError(f"Invalid CHR format for file {name}_chr_{chr_id:03d}.chr: CHR is not exactly 2048 bytes long (2K). Each character uses 2K of the total 4K for sprites.")
            chrs[chr_id] = character_chr
            loading_bar['value'] += 1
            found_chr_pal = True
        if not found_chr_pal:
            raise CreateAnimsFileNameError(f"Invalid filename: Directory chr for character {name} is not empty, but it doesn't contain any .chr.pal files. Please add at least one .chr and .chr.pal file with the expected format (see docs for details, section internals).")
        return chr_palettes, chrs

    def get_palette(self, file_format_validator, name, loading_bar, loading_bar_label, character_text):
        palette_filename = f"{self.root_dir}/{name}/pal/{name}_usual.pal"
        if not os.path.exists(palette_filename):
            raise CreateAnimsFileNameError(f"Invalid filename: For character {name}, either directory pal doesn't exist or file {name}_usual.pal doesn't exist.")
        with open(palette_filename, "rb") as character_pal:
            loading_bar_label.configure(text=f"{character_text}. Loading palette.")
            palette = list(character_pal.read())
            if not file_format_validator.validate_palette_length(palette): #len(palette) != 8: #Do it before it is considered loaded.
                raise CreateAnimsFileFormatError(f"Invalid PAL format for file {name}_usual.pal: PAL is not exactly 8 bytes long. Each character uses 8 colors (2 groups) out of the 16 available colors (4 groups).")
            if not file_format_validator.validate_palette_values(palette):
                raise CreateAnimsFileFormatError(f"Invalid PAL format for file {name}_usual.pal: one or more bytes have a value higher than 0x3F.")
            loading_bar['value'] += 1
        return palette

    def get_chr_palette(self, name, chr_id): #When we include absolutely every CHR_PALETTE with its corresponding CHR (I used uppercase cause I wanted to), we can iterate over a loop and then append to a chr_palettes and character_chrs. Awesome.
        chr_palette_filename = f"{self.root_dir}/{name}/chr/{name}_chr_pal_{chr_id:03d}.chr.pal"
        if not os.path.exists(chr_palette_filename):
            raise CreateAnimsFileNameError(f"Invalid filename: File {chr_palette_filename} was not found. This can happen if one of the files doesn't follow the expected format (please see docs for details). Some hex editors also create .bak files on save, there shouldn't be any of those in the directory either.") #In reality, the way CHR ID validations work, I don't think it is entirely possible. But maybe.
        with open(chr_palette_filename, "rb") as character_chr_pal:
            chr_palette = list(character_chr_pal.read())
        return chr_palette

    def get_chr(self, name, chr_id):
        chr_filename = f"{self.root_dir}/{name}/chr/{name}_chr_{chr_id:03d}.chr"
        if not os.path.exists(chr_filename):
            raise CreateAnimsFileNameError(f"Invalid filename: File {chr_filename} was not found. This can happen if one of the files doesn't follow the expected format (please see docs for details). Some hex editors also create .bak files on save, there shouldn't be any of those in the directory either.") #In reality, the way CHR ID validations work, I don't think it is entirely possible. But maybe.")
        with open(chr_filename, "rb") as character_chr:
            character_chr = list(character_chr.read())
        return character_chr #Added character cause otherwise chr, you know, reserved keyword.

    def get_frames(self, file_format_validator, name, loading_bar, loading_bar_label, character_text):
        frames_directory = f"{self.root_dir}{os.sep}{name}{os.sep}frames"
        if not os.path.exists(frames_directory):
            raise CreateAnimsFileNameError(f"Invalid filename: Directory frames doesn't exist for character {name}.")
        frames_filenames = os.listdir(frames_directory) #Don't ask me why here I use os.sep and in other places I use forward slash.
        if not frames_filenames:
            raise CreateAnimsFileNameError(f"Invalid filename: Directory frames for character {name} is empty. Please add at least one .frame file with the expected format (see docs for details, section internals).")
        frames = [] #This one will be 0-indexed. Frame 00, frame 01 etc.
        total_frames = len(frames_filenames)
        for frame_id in range(total_frames): #And it happened. #Potentially range(frame_ids) or something of the sort.
            frame = self.get_frame(file_format_validator, name, frame_id, total_frames, loading_bar, loading_bar_label, character_text)
            frames.append(frame)
        return frames

    def get_frame(self, file_format_validator, name, frame_id, total_frames, loading_bar, loading_bar_label, character_text):
        frame_filename = f"{self.root_dir}/{name}/frames/{name}_frame_{frame_id:03d}.frame"
        if not os.path.exists(frame_filename):
            raise CreateAnimsFileNameError(f"Invalid filename: File {frame_filename} was not found. This can happen if one of the files doesn't follow the expected format (please see docs for details). Some hex editors also create .bak files on save, there shouldn't be any of those in the directory either.")
        with open(frame_filename, "rb") as character_frame:
            loading_bar_label.configure(text=f"{character_text}. Loading frames. {frame_id+1}/{total_frames}")
            frame_bytes = list(character_frame.read())
            self.validate_frame(file_format_validator, name, frame_id, frame_bytes)
            frame = Frame(file_format_validator, frame_bytes)
            loading_bar['value'] += 1
        return frame

    def validate_frame(self, file_format_validator, name, frame_id, frame_bytes):
        frame_filename = f"{name}_frame_{frame_id:03d}.frame"
        if not file_format_validator.validate_frame_minimum_bytes(frame_bytes):
            raise CreateAnimsFileFormatError(f"Invalid frame format for file {frame_filename}: frame is 6 or less bytes long. Please see format details in the docs (section Internals).")
        if not file_format_validator.validate_frame_total_tiles(frame_bytes):
            raise CreateAnimsFileFormatError(f"Invalid frame format for file {frame_filename}: amount of tiles in frame (from 7th byte onwards) doesn't match width*height (bytes 1 and 2). Please see format details in the docs (section Internals).")
        if not file_format_validator.validate_frame_width(frame_bytes):
            raise CreateAnimsFileFormatError(f"Invalid frame format for file {frame_filename}: width is larger than 60 or less than 1. Please see format details in the docs (section Internals).")
        if not file_format_validator.validate_frame_height(frame_bytes):
            raise CreateAnimsFileFormatError(f"Invalid frame format for file {frame_filename}: height is larger than 60 or less than 1. Please see format details in the docs (section Internals).")

    def get_anims(self, file_format_validator, name, loading_bar, loading_bar_label, character_text):
        anims_directory = f"{self.root_dir}{os.sep}{name}{os.sep}anims"
        if not os.path.exists(anims_directory):
            raise CreateAnimsFileNameError(f"Invalid filename: Directory anims doesn't exist for character {name}.")
        anims_filenames = os.listdir(anims_directory) #Don't ask me why here I use os.sep and in other places I use forward slash.
        if not anims_filenames:
            raise CreateAnimsFileNameError(f"Invalid filename: Directory anims for character {name} is empty. Please add at least one .anim file with the expected format (see docs for details, section internals).")
        anims = [] #This one will be 0-indexed too. Anim 00, Anim 01 etc. #Might change this soon enough because some anims don't have files, like I removed them, like anim 0xF I believe. Yeah just checked.
        total_anims = len(anims_filenames)
        for anim_id in range(total_anims): #Potentially range(frame_ids) or something of the sort.
            anim = self.get_anim(file_format_validator, name, anim_id, total_anims, loading_bar, loading_bar_label, character_text)
            anims.append(anim)
        return anims

    def get_anim(self, file_format_validator, name, anim_id, total_anims, loading_bar, loading_bar_label, character_text):
        anim_filename = f"{self.root_dir}/{name}/anims/{name}_anim_{anim_id:03d}.anim"
        if not os.path.exists(anim_filename):
            raise CreateAnimsFileNameError(f"Invalid filename: File {anim_filename} was not found. This can happen if one of the files doesn't follow the expected format (please see docs for details). Some hex editors also create .bak files on save, there shouldn't be any of those in the directory either.")
        with open(anim_filename, "rb") as character_anim:
            loading_bar_label.configure(text=f"{character_text}. Loading anims. {anim_id+1}/{total_anims}") #Again, +1 since we won't be using enumerate here. I don't feel like it. And I mean, I would have to pass that here too. For physics it's different because I don't have the IDs to begin with.
            anim_bytes = list(character_anim.read())
            if not file_format_validator.validate_anim(anim_bytes):
                raise CreateAnimsFileFormatError(f"Invalid anim format for file {name}_anim_{anim_id:03d}.anim: anim is less than 2 bytes long. Anim must be at least 2 bytes long: first byte is physics ID, second and onwards are the frames to use for the anim.")
            anim = CharacterAnim(anim_bytes)
            loading_bar['value'] += 1
        return anim