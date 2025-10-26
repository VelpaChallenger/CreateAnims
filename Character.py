CHARACTER_PALETTE_FILEPATH = "sub_zero.pal"
CHARACTER_CHR_FILEPATH = "sub_zero.chr" #Only 2K for now.
CHARACTER_CHR_PALETTE_FILEPATH = "sub_zero.chr.pal"

class Character:

    def __init__(self, character_name):
        self.palette = self.get_palette("subzero")
        chr_ids = [0x9C] #When I add more characters, there'll be more and they'll be obtained after we parse the anim file.
        self.chr_palettes, self.chrs = self.get_chrs_and_palettes(character_name, chr_ids) #Whatever, the and makes it clear. Any other name to include both just doesn't make it clear.
        #self.chr_palettes = {}
        #self.chr_palette = self.get_chr_palette("subzero")
        #self.chr_palettes
        #self.chr_palettes.append(self.chr_palette) #For now, we'll do the loop eventually. Yes yes eventually you heard my word!
        #self.chrs = [] #And then you can access each chr_palette and chr by bank ID. Super awesome and easy to follow!
        #self.chr = self.get_chr("subzero")
        #self.chrs.append(self.chr) #Yes, I could have like a list of both chr and chr_palettes but here I prefer it this way, it feels clearer. Like the alternative would be self.banks or something and then per key (bank ID) 

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
        with open(CHARACTER_PALETTE_FILEPATH, "rb") as character_pal:
            palette = list(character_pal.read())
        return palette

    def get_chr_palette(self, name, chr_id): #When we include absolutely every CHR_PALETTE with its corresponding CHR (I used uppercase cause I wanted to), we can iterate over a loop and then append to a chr_palettes and character_chrs. Awesome.
        with open(CHARACTER_CHR_PALETTE_FILEPATH, "rb") as character_chr_pal:
            chr_palette = list(character_chr_pal.read())
        return chr_palette

    def get_chr(self, name, chr_id):
        with open(CHARACTER_CHR_FILEPATH, "rb") as character_chr:
            character_chr = list(character_chr.read())
        return character_chr #Added character cause otherwise chr, you know, reserved keyword.