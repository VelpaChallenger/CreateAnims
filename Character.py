from Anim import *

class Character:

    def __init__(self, createanims, character_name):
        self.name = character_name #Not sure if we'll need it but... maybe for display purposes? We could add a dictionary or something... anyways, don't want to include too much in this final commit before going back to main.
        self.createanims = createanims
        self.palette = self.get_palette(character_name)
        self.frames = self.get_frames(character_name, [0x00, 0x01])
        chr_ids = [self.frames[1].metadata.chr_bank] #When I add more characters, there'll be more and they'll be obtained after we parse the anim file.
        self.chr_palettes, self.chrs = self.get_chrs_and_palettes(character_name, chr_ids) #Whatever, the and makes it clear. Any other name to include both just doesn't make it clear.

    def get_chrs_and_palettes(self, name, chr_ids): #Yeah, after all we're kinda going to do the loop thing now, though not entirely but leaving the bases.
        chr_palettes = {}
        chrs = {}
        for chr_id in chr_ids:
            chr_palette = self.get_chr_palette(name, chr_id)
            chr_palettes[chr_id] = chr_palette
            character_chr = self.get_chr(name, chr_id)
            chrs[chr_id] = character_chr
        return chr_palettes, chrs

    def get_palette(self, name):
        with open(f"{self.createanims.root_dir}/{name}/pal/{name}_usual.pal", "rb") as character_pal:
            palette = list(character_pal.read())
        return palette

    def get_chr_palette(self, name, chr_id): #When we include absolutely every CHR_PALETTE with its corresponding CHR (I used uppercase cause I wanted to), we can iterate over a loop and then append to a chr_palettes and character_chrs. Awesome.
        with open(f"{self.createanims.root_dir}/{name}/chr/{name}_chr_pal_{chr_id:03d}.chr.pal", "rb") as character_chr_pal:
            chr_palette = list(character_chr_pal.read())
        return chr_palette

    def get_chr(self, name, chr_id):
        with open(f"{self.createanims.root_dir}/{name}/chr/{name}_chr_{chr_id:03d}.chr", "rb") as character_chr:
            character_chr = list(character_chr.read())
        return character_chr #Added character cause otherwise chr, you know, reserved keyword.

    def get_frames(self, name, frame_ids):
        frames = [] #This one will be 0-indexed. Frame 00, frame 01 etc.
        for frame_id in frame_ids: #Potentially range(frame_ids) or something of the sort.
            frame = self.get_frame(name, frame_id)
            frames.append(frame)
        return frames

    def get_frame(self, name, frame_id):
        with open(f"{self.createanims.root_dir}/{name}/frames/{name}_frame_{frame_id:02d}.frame", "rb") as character_frame:
            frame = Frame(list(character_frame.read()))
        return frame