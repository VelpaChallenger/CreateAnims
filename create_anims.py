import os

from CreateAnims import *
from Character import *
#random commit

def load_game_anims(createanims): #Another idea was to have a call to this in init_state, which makes sense considering we're initializing values. But then I would sort of have a circular dependency. I would have to put that stuff in yet another file, and I kinda like it here in the main file, so to speak. So that's why I ended up doing this way. It still makes sense: all the data has to go to createanims.
    get_physics(createanims) #Could use return but... meh, this will do.
    characters_name_list = os.listdir(createanims.root_dir)
    createanims.characters_dict = {}
    character_ID = 0
    for character_name in characters_name_list:
        if character_name == "physics": #Not a character actually!
            continue
        character = Character(createanims.root_dir, character_name)
        createanims.characters.append(character)
        createanims.characters_dict[character.name] = character_ID #Whatever, I just don't like the idea of having to linear search to get the character ID when saving changes, and adding it in the affected_file, it feels like a lot more of trouble than this feels. Also it might help for the feature where IDs can change? Or maybe not, in those cases I'll probably iterate over that list rather than the directories. And then search physics the same way I do now.
        character_ID += 1 #Autoincremental, yes.
    createanims.current_anim = 0x00 #Nah we need everything, whatever. Maybe current_frame no but at that point meh. Comment back to where it was, now in load_new_character_value, was in anim. #And yes, you're absolutely right. This already includes setting all the current_anim, current... oh wait, current_anim is the one we do need. Alright. #This will make the refresh to last saved simpler. Thing is, what if you added new character, new frame and such and now you load back with those values, error, because they don't exist. So, we return to values we know that exist. Might add some errors though if you try to load a folder with missing stuff and such, but it will be the same code so it will validate on both startup and then refresh.
    createanims.current_frame = 0x00
    createanims.current_frame_id = 0x01
    createanims.anim.load_new_character_value(0)

def get_physics(createanims): #Yup. This will happen here. #Also yeah, CreateAnims can run without physics. I was going to add get_physics_if_any but, considering I may extend this to other kind of elements... for now I'll leave it as it is.
    physics_path = f"{createanims.root_dir}/physics"
    if not os.path.isdir(physics_path): #No or trickery this time around.
        return
    physics_name_list = os.listdir(physics_path)
    physics_ids = [int(physics_filename.split(".physics")[0][-3:]) for physics_filename in physics_name_list] #As always, careful about .bak files and stuff. Will add this to docs.
    for physics_id in physics_ids:
        with open(f"{physics_path}/physics_{physics_id:03d}.physics", "rb") as physics_file:
            physics = list(physics_file.read()) #In this case, we won't use an object. This will do.
        createanims.physics_list.append(physics)

def main():
    createanims = CreateAnims()
    createanims.root_dir = "../characters"
    load_game_anims(createanims)
    createanims.root.mainloop()

if __name__ == "__main__": #Who would have thought! We will need this after all. I mean again, it's either that, or we create a new file helpers or something like that, and then we import from there and... no this, I don't like but I like that other even less. Let's go with this.
    main()