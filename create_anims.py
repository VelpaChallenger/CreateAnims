import os
import shutil
import threading

from CreateAnims import *
from Character import *

def load_game_anims(createanims, loading_default_directory=False): #Another idea was to have a call to this in init_state, which makes sense considering we're initializing values. But then I would sort of have a circular dependency. I would have to put that stuff in yet another file, and I kinda like it here in the main file, so to speak. So that's why I ended up doing this way. It still makes sense: all the data has to go to createanims.
    root = tkinter.Toplevel(createanims.root) #tkinter.Tk() #Copypasted from CreateAnimsUpdater. It will follow the same UI principle, minus with a few differences in logic on how to determine progress and all. Oh and the label will be different too of course.
    root.geometry(f"+800+450")
    root.wm_overrideredirect(True)

    if loading_default_directory:
        root.withdraw() #Doesn't have much of a point. It's just a couple of files and feels like a flashing when you start CreateAnims. So, withdraw in those cases.

    loading_bar_label = tkinter.Label(root, text="Initializing load_game_anims...", width=44, justify="left", anchor="nw") #text=f"Loading character {character_name}'s {file_type_display}") #Please wait...
    loading_bar_label.pack(pady=10, padx=(0, 10), anchor="nw")
    loading_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate', value=0, maximum=0)
    loading_bar.pack(pady=(0, 10), anchor="nw")
    thread_download_object = threading.Thread(target=thread_load_game_anims, args=(createanims, loading_bar, loading_bar_label, root)) #No need to use lambda here, can use args. And yes, root will be the load_game_anims UI for tracking progress.
    thread_download_object.start()

def thread_load_game_anims(createanims, loading_bar, loading_bar_label, root):
    try: #Yes, originally it was going to be just from get_physics and until root.after but, I do prefer it here, so that everything is caught.
        loading_bar['maximum'] = sum([len(files) for r, d, files in os.walk(createanims.root_dir) if "images" not in r]) #Exclude images which is used for play anim.
        get_physics(createanims, loading_bar, loading_bar_label) #Could use return but... meh, this will do.
        characters_name_list = [create_anims_dir for create_anims_dir in os.listdir(createanims.root_dir) if create_anims_dir != "physics"]
        if not characters_name_list:
            raise CreateAnimsFileNameError(f"Invalid filename: Characters directory doesn't contain any characters (only physics).")
        createanims.characters_dict = {}
        character_ID = 0
        total_characters = len(characters_name_list)
        for character_name in characters_name_list:
            character_text = f"Loading characters. {character_ID+1}/{total_characters} {character_name}" #No period here, will add later.
            loading_bar_label.configure(text=f"{character_text}") #In this case, we will do +1. Easier.
            character = Character(createanims.root_dir, createanims.file_format_validator, character_name, loading_bar, loading_bar_label, character_text)
            createanims.characters.append(character)
            createanims.characters_dict[character.name] = character_ID #Whatever, I just don't like the idea of having to linear search to get the character ID when saving changes, and adding it in the affected_file, it feels like a lot more of trouble than this feels. Also it might help for the feature where IDs can change? Or maybe not, in those cases I'll probably iterate over that list rather than the directories. And then search physics the same way I do now.
            character_ID += 1 #Autoincremental, yes.
        createanims.current_anim = 0x00 #Nah we need everything, whatever. Maybe current_frame no but at that point meh. Comment back to where it was, now in load_new_character_value, was in anim. #And yes, you're absolutely right. This already includes setting all the current_anim, current... oh wait, current_anim is the one we do need. Alright. #This will make the refresh to last saved simpler. Thing is, what if you added new character, new frame and such and now you load back with those values, error, because they don't exist. So, we return to values we know that exist. Might add some errors though if you try to load a folder with missing stuff and such, but it will be the same code so it will validate on both startup and then refresh.
        createanims.current_frame = 0x00
        createanims.current_frame_id = 0x01
        root.after(10, post_load, root, createanims, loading_bar) #My approach for destroying in main thread. I've seen other options like the classical and typical have main thread asking or polling about a flag, and then as soon as it sees it complete, it means the other thread finished, and then you keep doing your thing. But honestly, I find this a lot cleaner. So I'll do it this way, my own way or at least I haven't seen it.
    except CreateAnimsFileFormatError as exception_message:
        root.after(10, show_error_and_close, createanims, "File Format Error", exception_message)
        return
    except CreateAnimsFileNameError as exception_message:
        root.after(10, show_error_and_close, createanims, "File Name Error", exception_message)
        return
    except Exception as exception_message:
        root.after(10, show_error_and_close, createanims, "Unknown Exception", exception_message)
        return

def post_load(root, createanims, loading_bar):
    if loading_bar['value'] != loading_bar['maximum']: #I need to do this here, in main thread, to be able to exit gracefully.
        tkinter.messagebox.showerror(title="Critical Error! Anims Mismatch", message=f"An error has occurred. The amount of total files {loading_bar['maximum']} found in the characters directory doesn't match the amount of loaded files {loading_bar['value']}. This can result in several inconsistencies, confusions and data corruption. Please review the characters folder and verify there aren't any additional non-CreateAnims related files (keep in mind images folder isn't considered for the final count). One possible reason for this issue is .bak files generated by hex editors when saving changes.") #Assets mismatch.
        createanims.close() #Maybe could call it exit too? Could do it here too but, yeah I really don't want to import sys just because of this.
    root.destroy()
    createanims.anim.load_new_character_value(0) #Let's do this here, in main thread.
    createanims.root.deiconify() #Let's hope it works. #It does! Also, for when you Refresh to Last Saved, this doesn't do anything. Now I'm thankful that there aren't errors or anything for things that you might expect an error for. Though, maybe that would still be better and I could try-except, but in any case, no, it doesn't throw any error. It just doesn't do anything if the window is already displaying.

def show_error_and_close(createanims, exception_type, exception_message):
    tkinter.messagebox.showerror(title=f"Critical Error! {exception_type}", message=f"An error of type {exception_type} has occurred. Details: {exception_message}")
    createanims.close()

def get_physics(createanims, loading_bar, loading_bar_label): #Yup. This will happen here. #Also yeah, CreateAnims can run without physics. I was going to add get_physics_if_any but, considering I may extend this to other kind of elements... for now I'll leave it as it is.
    physics_path = f"{createanims.root_dir}/physics"
    if not os.path.isdir(physics_path): #No or trickery this time around. #To avoid confusions specially for future me: this can be safely removed, the only reason why I don't is because at some point, I miiiight make it such that you can still use CreateAnims without physics. But that will imply quite a few checks here and there so, I'm not including it in the release I'm planning for before 2025 end. You, future me, or future reader, will have the blessing to know what happened. But for me, I leave this note.
        raise CreateAnimsFileNameError(f"Invalid filename: Directory physics does not exist in Characters directory.")
    physics_ids = os.listdir(physics_path)
    total_physics = len(physics_ids)
    for i in range(total_physics):
        physics_filename = f"{physics_path}/physics_{i:03d}.physics"
        if not os.path.exists(physics_filename):
            raise CreateAnimsFileNameError(f"Invalid filename: File {physics_filename} was not found. This can happen if one of the files doesn't follow the expected format (please see docs for details). Some hex editors also create .bak files on save, there shouldn't be any of those in the directory either.")
        with open(physics_filename, "rb") as physics_file:
            loading_bar_label.configure(text=f"Loading physics. {i+1}/{total_physics}") #Back to i+1. Makes it easier on the filename check. #i + 1 because i starts at zero. Although... there, updated start to 1. Doesn't have anything to do with the iteration itself so, awesome.
            physics = list(physics_file.read()) #In this case, we won't use an object. This will do.
            if not createanims.file_format_validator.validate_physics_parity(physics):
                raise CreateAnimsFileFormatError(f"Invalid physics format for file physics_{i:03d}.physics: total amount of bytes is not an odd number. For every frame, there's relative X and Y values to add to the current position. The physics terminator is 0x80, for a total of an odd number (2*n + 1).")
            if not createanims.file_format_validator.validate_physics_terminator(physics):
                raise CreateAnimsFileFormatError(f"Invalid physics format for file physics_{i:03d}.physics: terminator is not 0x80. Terminator 0x80 indicates the physics must end at that point and restart to state 0x00.")
            loading_bar['value'] += 1
        createanims.physics_list.append(physics)

def create_default_directory(root_dir): #Ah no wait, actually no, this is when the program first starts, no cb yet. Well in that case yeah whatever, just don't start lol. Or... #This might throw an exception if you think of opening some file here, but that can happen always, but yeah even if it happens, at this point we already have the tkinter self_destruct cb in place so, all good.
    try:
        if os.path.exists(root_dir):
            shutil.rmtree(root_dir) #Start from scratch.
        os.makedirs(root_dir)
        physics_directory = os.path.join(root_dir, "physics")
        os.makedirs(physics_directory)
        default_physics_bytes = bytearray([0x00, 0x00, 0x80])
        default_physics_filename = os.path.join(physics_directory, "physics_000.physics")
        with open(default_physics_filename, "wb") as default_physics_file:
            default_physics_file.write(default_physics_bytes)
        character_x_directory = os.path.join(root_dir, "character_x") #The Character X! Has about 9999HP, 9999MP, the Ultimate attack never seen before... !! ... ok yeah.
        os.makedirs(character_x_directory)
        character_x_anims_directory = os.path.join(character_x_directory, "anims")
        os.makedirs(character_x_anims_directory) #I know, I could have used join from the beginning, it's the whole point and it's abstracted there, but whatever.
        default_anims_bytes = bytearray([0x00, 0x00])
        default_anims_filename = os.path.join(character_x_anims_directory, "character_x_anim_000.anim") #Yes, there can be underscore in the name.
        with open(default_anims_filename, "wb") as default_anims_file:
            default_anims_file.write(default_anims_bytes)
        character_x_chr_directory = os.path.join(character_x_directory, "chr")
        os.makedirs(character_x_chr_directory)
        default_chr_bytes = bytearray([0x00] * 0x800) #Same as TileUtils code for new CHR.
        default_chr_filename = os.path.join(character_x_chr_directory, "character_x_chr_000.chr")
        with open(default_chr_filename, "wb") as default_chr_file:
            default_chr_file.write(default_chr_bytes)
        default_chr_pal_bytes = bytearray([0x00] * 0x10) #Also same as TileUtils.
        default_chr_pal_filename = os.path.join(character_x_chr_directory, "character_x_chr_pal_000.chr.pal")
        with open(default_chr_pal_filename, "wb") as default_chr_pal_file:
            default_chr_pal_file.write(default_chr_pal_bytes)
        character_x_frames_directory = os.path.join(character_x_directory, "frames")
        os.makedirs(character_x_frames_directory)
        default_frames_bytes = bytearray([0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0xFF])
        default_frames_filename = os.path.join(character_x_frames_directory, "character_x_frame_000.frame")
        with open(default_frames_filename, "wb") as default_frames_file:
            default_frames_file.write(default_frames_bytes)
        character_x_pal_directory = os.path.join(character_x_directory, "pal")
        os.makedirs(character_x_pal_directory)
        default_pal_bytes = bytearray([0x0E, 0x01, 0x02, 0x03, 0x0E, 0x04, 0x05, 0x08])
        default_pal_filename = os.path.join(character_x_pal_directory, "character_x_usual.pal")
        with open(default_pal_filename, "wb") as default_pal_file:
            default_pal_file.write(default_pal_bytes)
    except PermissionError as exception_message:
        tkinter.messagebox.showerror(title="Error creating default directory", message=f"CreateAnims could not create default directory. This can happen if you first let CreateAnims create it (or you created it yourself) and then opened it with some process and why am I even bothering explaining? If you triggered this error, you most likely wanted to make it appear. Anyways! And no, I'm not moving it to a less visible place :p . Programs should be standalone! All in one single place!\n\nHere are the exception details: {exception_message}.") #This does work, actually!
        sys.exit(999) #Just directly end, no problems here.
    except Exception as exception_message:
        tkinter.messagebox.showerror(title="Unknown error creating default directory", message=f"CreateAnims could not create default directory due to an unknown exception. Here are the details: {exception_message}.")
        sys.exit(999)

def main():
    createanims = CreateAnims()
    createanims.root_dir = "CreateAnims_DefaultCharacters" #"../characters"
    create_default_directory(createanims.root_dir)
    createanims.root.withdraw() #I was going to say, for the default don't load anything but turns out it's a lot more complicated lol so yeah, do load even if it's just one character with the bare minimum. Simplifies things not just a lot, but quite, quite a lot.
    load_game_anims(createanims, loading_default_directory=True)
    createanims.root.mainloop()

if __name__ == "__main__": #Who would have thought! We will need this after all. I mean again, it's either that, or we create a new file helpers or something like that, and then we import from there and... no this, I don't like but I like that other even less. Let's go with this.
    main()