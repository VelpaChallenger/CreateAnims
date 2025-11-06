class EntryReturn:

    def __init__(self, createanims):
        self.createanims = createanims

    def chr_entry(self, event=None): #chr is reserved keyword and should not matter in this context but I still feel more comfortable, if not technically then aesthetically when I see chr_entry.
        chr_entry_value = self.createanims.chr_entry.get()
        if int(chr_entry_value) % 2 == 1: #Validation 4: number must be even. Though for this, it will have to be on enter, there's no other way to know the input is finished.
            self.createanims.chr_entry.configure(highlightcolor="red", highlightbackground="red")
            self.createanims.chr_info_text.configure(text="CHR Bank must be an even number.", fg="red")
            return False
        self.createanims.chr_entry.configure(highlightcolor="white", highlightbackground="white")
        self.createanims.chr_info_text.configure(text="")
        new_chr_bank = int(chr_entry_value)
        self.createanims.current_chr_bank = new_chr_bank
        character = self.createanims.characters[self.createanims.current_character]
        character.frames[self.createanims.current_frame].metadata.chr_bank = new_chr_bank
        character_chr = character.chrs.get(new_chr_bank, None)
        if character_chr is None:
            self.createanims.chr_info_text.configure(text="Empty for current character. Please make sure the CHR Bank really is empty in the ROM and not used by another character or for other purposes like stages.", fg="blue") #Blue so that you do see it.
            character.chrs[new_chr_bank] = [0x00] * 0x800 #empty_chr, removed variable. #Default_chr is an alternative name. All pixels will use 00. So, color black (by default color used for transparency).
            character.chr_palettes[new_chr_bank] = [0x00] * 0x10 #If no CHR, we assume no chr palette either. It should be that way. Right?
        self.createanims.refresh_UI()