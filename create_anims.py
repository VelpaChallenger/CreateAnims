from CreateAnims import *
from Character import *

#PATHS (here for now, all in one place)

character_bank = "bank_sub_zero_copy.asm"

def load_game_anims(createanims): #Another idea was to have a call to this in init_state, which makes sense considering we're initializing values. But then I would sort of have a circular dependency. I would have to put that stuff in yet another file, and I kinda like it here in the main file, so to speak. So that's why I ended up doing this way. It still makes sense: all the data has to go to createanims.
    character = Character("subzero") #load_character("subzero") #What character to load. It's a prefix of sorts that might be needed for every character to get the right files? But I need to change how that is displayed so that users won't see pure keys let's say, or these IDs.
    createanims.characters.append(character)

def main():
    createanims = CreateAnims()
    #createanims.chr_palette = get_chr_palette() #This is probably the only one that doesn't depend on which character is being loaded.
    load_game_anims(createanims)
    createanims.current_character = 0 #ID-based.
    createanims.current_chr_bank = next(iter(createanims.characters[0].chrs)) #Though I don't really like having to use next and iter. But meh. To get first key. #More generic this way. Won't matter whoever is first character. #0x9C
    createanims.refresh_UI()
    createanims.root.mainloop()
main()