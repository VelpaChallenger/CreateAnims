import os

from CreateAnims import *
from Character import *

def load_game_anims(createanims): #Another idea was to have a call to this in init_state, which makes sense considering we're initializing values. But then I would sort of have a circular dependency. I would have to put that stuff in yet another file, and I kinda like it here in the main file, so to speak. So that's why I ended up doing this way. It still makes sense: all the data has to go to createanims.
    characters_name_list = os.listdir(createanims.root_dir)
    for character_name in characters_name_list:
        character = Character(createanims, character_name)
        createanims.characters.append(character)

def main():
    createanims = CreateAnims()
    createanims.root_dir = "../characters"
    load_game_anims(createanims)
    createanims.current_character = 0 #ID-based.
    createanims.current_chr_bank = next(iter(createanims.characters[0].chrs)) #Though I don't really like having to use next and iter. But meh. To get first key. #More generic this way. Won't matter whoever is first character. #0x9C
    createanims.chr_entry.insert(0, str(createanims.current_chr_bank))
    createanims.current_anim = 0x00
    createanims.anim_entry.insert(0, str(createanims.current_anim))
    createanims.current_frame = 0x00
    createanims.frame_entry.insert(0, str(createanims.current_frame))
    createanims.current_frame_id = 0x01
    createanims.frame_id_entry.insert(0, str(createanims.current_frame_id))
    createanims.refresh_UI()
    createanims.root.mainloop()
main()