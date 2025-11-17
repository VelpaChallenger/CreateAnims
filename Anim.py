import os
from PIL import Image, ImageTk

from tkinter import messagebox

INITIAL_X_FRAME = 375 #To know from where to start col by col, row by row. The cells.
INITIAL_Y_FRAME = 200

def func_AnimImage_on_left_click(createanims, anim_index, event=None): #A wrapper to go around memory leak issues with Tkinter.
    anim_image_object = createanims.anim_images[anim_index]
    anim_image_object.on_left_click(event)

def func_AnimImage_on_right_click(createanims, anim_index, event=None): #Idem
    anim_image_object = createanims.anim_images[anim_index]
    anim_image_object.on_right_click(event)

def func_AnimImage_on_double_right_click(createanims, anim_index, event=None): #Idem
    anim_image_object = createanims.anim_images[anim_index]
    anim_image_object.on_double_right_click(event)

class Frame:
    
    def __init__(self, frame_bytes):
        self.metadata = FrameMetaData(frame_bytes)
        self.tiles = frame_bytes[6:] #The tiles that give shape to the frame.

class FrameMetaData: #To make it clear that it's not the frame itself.

    def __init__(self, frame_bytes):
        self.x_length = frame_bytes[0]
        self.y_length = frame_bytes[1]
        self.x_offset = (frame_bytes[2] & 0x7F) * (1 if (frame_bytes[2] & 0x80) else -1) #Fun fact: the code is there, but there's no negative X! (that is, there's not any 0x80) At least for characters. There probably is for projectiles. #For flipped, can add + and the same logic. -8 or 0. #Also yes, it's inverted between y offset and x offset. Go ask HT. #Don't get me wrong, it's still opposite. But, I put - y_offset instead of + y_offset to make it closer to what the code does. Who knows? Maybe whatever tool they were using at the time (we're talking the 90s) was doing operations like these, and the consequences of their inner workings are relevant even today, 30+ years later.
        self.chr_bank = frame_bytes[3]
        self.y_offset = (frame_bytes[4] & 0x1F) * (1 if (frame_bytes[4] & 0x20) else -1) #I don't usually use ternary in Python but here it is pretty convenient.
        self.special_palette_id = 0 #Unused, but we may give it an use later on.

class CharacterAnim: #Yeah I know. Maybe it was better to say AnimUtils from the beginning. Meh. This works.

    def __init__(self, anim_bytes):
        self.physics_id = anim_bytes[0]
        self.frame_ids = anim_bytes[1:] #Similar logic to Frame. We split it so that it's easier to handle and name. Nothing else.

class AnimImage: #Yes, this is what I was talking about before. I'm pretty sure it would be technically impossible or just too messy to have these images be exactly the same as TileImages. But either way, we do need them to be different so that the same actions like clicking and stuff make different things.

    def __init__(self, createanims, anim_canvas, tile_image_object, anim_image, anim_index, tile_palette_group, tile_label, pre_tkimg, final_img):
        self.createanims = createanims
        self.anim_canvas = anim_canvas
        self.tile_image_object = tile_image_object
        self.anim_image = anim_image #Beware, it's not the image object itself. It's the ID of the image which we'll use to make changes and stuff. Very much same as PalRectangle and ColorPickerRectangle.
        self.anim_index = anim_index #Same as cell_id.
        self.tile_palette_group = tile_palette_group
        self.tile_label = tile_label
        self.pre_tkimg = pre_tkimg #This is the image as in img.putpalette. It's before we do the conversion from PIL image to Tkinter image. So, pre_tkimg. Useful for transparency when drawing anim.
        self.final_img = final_img #This is the final, processed img, like the ImageTk image. It's only being saved to protect it from the gc. Meanie.
        self.anim_canvas.tag_bind(self.anim_image, "<Button-1>", lambda event: func_AnimImage_on_left_click(createanims, anim_index, event))
        self.anim_canvas.tag_bind(self.anim_image, "<Button-3>", lambda event: func_AnimImage_on_right_click(createanims, anim_index, event))
        self.anim_canvas.tag_bind(self.anim_image, "<Double-Button-3>", lambda event: func_AnimImage_on_double_right_click(createanims, anim_index, event))

    def on_left_click(self, event=None):
        self.select()
        if self.createanims.current_chr_tile_index is not None: #If there is some tile in the CHR window selected.
            frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id] #It could be a good idea to add a get_frame(). But you know, that's what most people do. I only do it if it's convenient. Here, this is just way clearer.
            frame.tiles[self.anim_index] = self.createanims.current_chr_tile_index
            self.createanims.anim.refresh()

    def on_right_click(self, event=None):
        self.select()
        if self.tile_image_object is not None: #It could be the empty one, in which case, don't do anything, just select in Anim.
            self.tile_image_object.select()
            self.tile_image_object.update_tile_label()

    def on_double_right_click(self, event=None):
        frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id]
        frame.tiles[self.anim_index] = 0xFF
        self.createanims.anim.refresh()

    def select(self):
        x, y = self.anim_canvas.coords(self.anim_image)
        if self.createanims.current_anim_image_rectangle is None: #Again, similar approach to PalRectangle and ColorPickerRectangle. Though this time I add a suffix _rectangle to make it clear that we're making a rectangle around the tile image. Wonderful awesome.
            self.createanims.current_anim_image_rectangle = self.anim_canvas.create_rectangle(x, y, x+15, y+15, width=1, outline="white") #Let's give white a try. Maybe after you're reading this it's a different color.
            self.createanims.current_anim_image_inner_rectangle = self.anim_canvas.create_rectangle(x+1, y+1, x+14, y+14, width=1, outline="black") #Actually inner, what I meant to say. #Outer, it's going to help for white tiles to be clearly visibly selected as well.
            self.createanims.current_anim_image_outer_rectangle = self.anim_canvas.create_rectangle(x-1, y-1, x+16, y+16, width=1, outline="black") #And now outer, helps a lot too.
        else:
            self.anim_canvas.moveto(self.createanims.current_anim_image_rectangle, x-1, y-1) #Nothing to move if it doesn't exist. So that's why the if.
            self.anim_canvas.moveto(self.createanims.current_anim_image_inner_rectangle, x, y)
            self.anim_canvas.moveto(self.createanims.current_anim_image_outer_rectangle, x-2, y-2)

class PhysicsLabel:

    def __init__(self, createanims, label, frame_index):
        self.createanims = createanims
        self.frame_index = frame_index
        self.label = label
        self.label.bind("<Button-3>", self.on_right_click)
        self.label.bind("<Shift-Button-3>", self.on_shift_right_click)
        self.label.bind("<Shift-Button-1>", self.on_shift_left_click)

    def on_right_click(self, event=None):
        physics = self.createanims.physics_list[self.createanims.current_physics_id]
        physics.pop(2*self.frame_index) #And that's it.
        physics.pop(2*self.frame_index) #Well two times to account also for the Y. And yeah, everything gets shifted when doing pop so this works.
        self.createanims.anim.fill_physics_grid() #Kinda like a refresh, but for physics.

    def on_shift_right_click(self, event=None):
        physics = self.createanims.physics_list[self.createanims.current_physics_id]
        if (len(physics) // 2) == 60:
            self.createanims.physics_window.attributes('-disabled', 1)
            messagebox.showinfo(title="Too many frames", message="The anim may be long, but I still have to put a limit to it. Anyways, if you do need more frames, let me know!")
            self.createanims.physics_window.attributes('-disabled', 0)
            self.createanims.physics_window.focus_force()
            return
        physics.insert((2*self.frame_index) + 2, 0x00) #You may think this won't work when inserting at the end, but it does. Why? Because, 2*self.frame_index returns the x of the last physics. And that's the key. Exactly +2 after that, there's the 0x80. So you're inserting where 0x80 is, pushing 0x80.
        physics.insert((2*self.frame_index) + 2, 0x00)
        self.createanims.anim.fill_physics_grid()

    def on_shift_left_click(self, event=None):
        self.createanims.init_physics_dialog(self.frame_index)

class Anim: #Yes this could be AnimUtils. Or maybe FrameUtils, come to think of it. #Similar structure to TileUtils. You have the main class, which then uses data from other classes to do its stuff.

    def __init__(self, createanims):
        self.createanims = createanims
        self.transparency = 1 #Default value. #Yes, let's leave this as part of Anim. It will still be accessible from CreateAnims, Command etc. etc.
        self.draw_frame_rectangle = 1 #I know I know. I'm mixing Frame and Anim quite a lot. Oh well. We'll survive. I think.
        self.draw_empty_cells = 1
        self.frame_rectangle = None #No ID, will be created later if option is turned on.
        self.play_physics = True #By default, but may be turned False if for example the frames don't match. Alternatively, raise a warning/make it configurable whether to raise a warning.

    def refresh(self):
        if self.createanims.current_anim_image_rectangle is not None:
            self.store_anim_image_rectangle_coords() #We need to do it this way cause, once we hit delete, there's no turning back. But at the same time, we need to regenerate everything once it's been deleted. So, yeah.
        self.createanims.anim_canvas.delete("all") #Yeah, we will delete everything just in case just like TileUtils. And well, not 'just in case', without this, tag bind Button-1, then Shift+T, and second time it doesn't work anymore. Probably due to these references not letting the changes go through or something of the sort.
        self.createanims.anim_images = []
        frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id]
        initial_y = INITIAL_Y_FRAME - (frame.metadata.y_offset*2) - (16*frame.metadata.y_length) - 16 #Has to happen at this point, where we now have access to the frame metadata. Also *2 because if y offset is 5, that means 10 pixels away in our system.
        cell_id = 0 #Let's call it this way, probably the most accurate. tile_id could be confused with the tile_id stored in the cell, frame_tile_id would be another candidate to refer to the tile_id stored in the frame, but mixing frame and tile can be a bit confusing as with row and tile in the same name (I did it for TileUtils).
        for row in range(frame.metadata.y_length):
            initial_x = INITIAL_X_FRAME + (frame.metadata.x_offset*2)
            initial_y += 16
            for col in range(frame.metadata.x_length):
                tile_id = frame.tiles[cell_id]
                if tile_id != 0xFF: #So 0x7F is still a valid tile. So, we need to do it before & 0x7F.
                    tile_image_object = self.createanims.tiles_images[tile_id & 0x7F] #Let's move it here to have cleaner checks. #We only care about bits 0-6. Actually I think I was going to run a script to fix that for all frames. But meanwhile we can do this. The idea is to remove the and #$7F in the code, I think it's still there for now.
                    pre_tkimg = tile_image_object.pre_tkimg
                    self.decide_transparency_anim_image(pre_tkimg, self.transparency)
                    final_img = ImageTk.PhotoImage(pre_tkimg.resize((16, 16))) #So yes, actually different images with same base, but still different.
                    anim_image = self.createanims.anim_canvas.create_image(initial_x, initial_y, anchor="nw", image=final_img) #Thanks past me. Issue solved. #WARNING! Potential memory issue here. I'm never deleting this anim_image with each refresh. Not a problem after doing many many tests but... it does make me curious that it seemed to be a problem with the CHR canvas. Or maybe that one was getting slower for different reasons. Could be. Still taking note of that here in case it comes handy later.
                    self.createanims.anim_images.append(AnimImage(self.createanims, self.createanims.anim_canvas, tile_image_object, anim_image, cell_id, tile_image_object.tile_palette_group, self.createanims.tile_label, pre_tkimg, final_img))
                else: #We will draw something, but not an image. A rectangle. A blue rectangle.
                    pixels = [0x00] * 64 #Fully transparent. This works as a fill.
                    img = Image.frombytes("P", (8, 8), bytes(pixels))
                    tile_palette = [0x00] * 12 #Like, just whatever. We won't use them.
                    img.putpalette(tile_palette)
                    pre_tkimg = img
                    img.info['transparency'] = 0 #Always transparent in this case, nothing to decide.
                    final_img = ImageTk.PhotoImage(pre_tkimg.resize((16, 16)))
                    anim_image = self.createanims.anim_canvas.create_image(initial_x, initial_y, anchor="nw", image=final_img)
                    if self.draw_empty_cells:
                        anim_empty_rectangle = self.createanims.anim_canvas.create_rectangle(initial_x, initial_y, initial_x + 15, initial_y + 15, width=1, outline="blue") #Alt name anim_empty_image, but I like more rectangle because, even though it's taking the place of what could be an image, it is a rectangle.
                    self.createanims.anim_images.append(AnimImage(self.createanims, self.createanims.anim_canvas, None, anim_image, cell_id, None, self.createanims.tile_label, pre_tkimg, final_img)) #We could also create an empty image but... I think I prefer the rectangle idea. Let's see how it goes.
                initial_x += 16
                cell_id += 1
        if self.frame_rectangle is not None:
            self.createanims.anim_canvas.delete(self.frame_rectangle)
        if self.draw_frame_rectangle:
            self.frame_rectangle = self.createanims.anim_canvas.create_rectangle(INITIAL_X_FRAME + (frame.metadata.x_offset*2), INITIAL_Y_FRAME - (frame.metadata.y_offset*2) - (16*frame.metadata.y_length), INITIAL_X_FRAME + (frame.metadata.x_offset*2) + 16*frame.metadata.x_length, INITIAL_Y_FRAME - (frame.metadata.y_offset*2), outline="red", width=2)
        if self.createanims.current_anim_image_rectangle is not None: #I guess you're right. I mean no, you are right. I could handle the selections inside Anim, inside TileUtils and so on and so forth instead of CreateAnims. Although, I like that selections, which are something more global, are part of CreateAnims.
            self.regenerate_anim_image_rectangles() #Delete, and add again with previous cords.

    def decide_transparency_anim_image(self, pre_tkimg, transparency):
        if transparency: #Updated logic. #One of those cases where I prefer == 0 rather than using not.
            pre_tkimg.info['transparency'] = 0
        else: #Yeah now it should be 1, it's a toggle. #Should be None, but I'll interpret any other value the same way. Seems cleaner than elif and then else or just leaving the elif or showing some msg...
            pre_tkimg.info.pop('transparency', None) #No errors if the key doesn't exist.

    def store_anim_image_rectangle_coords(self):
        self.x1, self.y1, self.x2, self.y2 = self.createanims.anim_canvas.coords(self.createanims.current_anim_image_rectangle)
        self.x1_inner, self.y1_inner, self.x2_inner, self.y2_inner = self.createanims.anim_canvas.coords(self.createanims.current_anim_image_inner_rectangle)
        self.x1_outer, self.y1_outer, self.x2_outer, self.y2_outer = self.createanims.anim_canvas.coords(self.createanims.current_anim_image_outer_rectangle)

    def regenerate_anim_image_rectangles(self): #Yes, regenerate. For anims, and well could replicate for CHR as well, it's nice to still keep the selection.
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        self.createanims.current_anim_image_rectangle = self.createanims.anim_canvas.create_rectangle(x1, y1, x2, y2, width=1, outline="white")
        x1, y1, x2, y2 = self.x1_inner, self.y1_inner, self.x2_inner, self.y2_inner
        self.createanims.current_anim_image_inner_rectangle = self.createanims.anim_canvas.create_rectangle(x1, y1, x2, y2, width=1, outline="black")
        x1, y1, x2, y2 = self.x1_outer, self.y1_outer, self.x2_outer, self.y2_outer
        self.createanims.current_anim_image_outer_rectangle = self.createanims.anim_canvas.create_rectangle(x1, y1, x2, y2, width=1, outline="black")

    def validate_anim_entry(self, new_value):
        if not new_value: #Empty value is always welcome.
            self.createanims.anim_entry.configure(highlightcolor="white", highlightbackground="white")
            return True
        try: #Validation 1: value must be an integer, 0 or positive.
            int(new_value)
        except ValueError:
            self.createanims.anim_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        character = self.createanims.characters[self.createanims.current_character]
        if int(new_value) > len(character.anims) - 1: #Validation 2: value must not be greater than the maximum amount of anims for the current character.
            self.createanims.anim_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if new_value.startswith("0") and len(new_value) > 1: #Validation 3: if number starts with 0, it cannot have more than just 1 digit.
            self.createanims.anim_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        self.createanims.anim_entry.configure(highlightcolor="white", highlightbackground="white")
        return True

    def validate_frame_entry(self, new_value):
        if not new_value: #Empty value is always welcome.
            self.createanims.frame_entry.configure(highlightcolor="white", highlightbackground="white")
            return True
        try: #Validation 1: value must be an integer, 0 or positive.
            int(new_value)
        except ValueError:
            self.createanims.frame_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        anim = self.createanims.characters[self.createanims.current_character].anims[self.createanims.current_anim]
        if int(new_value) > len(anim.frame_ids) - 1: #Validation 2: value must not be greater than the maximum amount of frames for the current anim of the current character.
            self.createanims.frame_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if new_value.startswith("0") and len(new_value) > 1: #Validation 3: if number starts with 0, it cannot have more than just 1 digit.
            self.createanims.frame_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        self.createanims.frame_entry.configure(highlightcolor="white", highlightbackground="white")
        return True

    def validate_frame_id_entry(self, new_value):
        if not new_value: #Empty value is always welcome.
            self.createanims.frame_id_entry.configure(highlightcolor="white", highlightbackground="white")
            return True
        try: #Validation 1: value must be an integer, 0 or positive.
            int(new_value)
        except ValueError:
            self.createanims.frame_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        character = self.createanims.characters[self.createanims.current_character]
        if int(new_value) > len(character.frames) - 1: #Validation 2: value must not be greater than the maximum amount of frames for the current character.
            self.createanims.frame_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if new_value.startswith("0") and len(new_value) > 1: #Validation 3: if number starts with 0, it cannot have more than just 1 digit.
            self.createanims.frame_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        self.createanims.frame_id_entry.configure(highlightcolor="white", highlightbackground="white")
        return True

    def validate_physics_id_entry(self, new_value):
        if not new_value: #Empty value is always welcome.
            self.createanims.physics_id_entry.configure(highlightcolor="white", highlightbackground="white")
            return True
        try: #Validation 1: value must be an integer, 0 or positive.
            int(new_value)
        except ValueError:
            self.createanims.physics_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if int(new_value) > len(self.createanims.physics_list) - 1: #Validation 2: value must not be greater than the maximum amount of physics available.
            self.createanims.physics_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if new_value.startswith("0") and len(new_value) > 1: #Validation 3: if number starts with 0, it cannot have more than just 1 digit.
            self.createanims.physics_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        self.createanims.physics_id_entry.configure(highlightcolor="white", highlightbackground="white")
        return True

    def validate_physics_dialog_x_entry(self, new_value):
        if not new_value: #Empty value is always welcome.
            self.createanims.physics_dialog_x_entry.configure(highlightcolor="white", highlightbackground="white")
            return True
        if (new_value.startswith("-") and len(new_value) > 1) or not new_value.startswith("-"): #This time we admit negatives. This is why, while duplicated a lot, I like having different validations for each entry. #If we're just typing the -, leave it be. Skip it.
            try: #Validation 1: value must be an integer number, including zero and negative.
                new_value_int = int(new_value) #Ah but come to think of it, if it has a - and then a number, the int does work. So this logic can be simplified to just one try block. #Everything that comes afterwards must be a number. #If starts with "-" and has length 1, don't do any validation at all here.
                if new_value.startswith("-") and new_value_int == 0: #Don't do that. You'll break the tool. Stop trolling the tool.
                    self.createanims.physics_dialog.attributes('-disabled', 1) #Disabled until you do read the message and reflect on your conduct.
                    messagebox.showerror(title="Don't troll the tool", message=f"Don't troll the tool, I worked so hard on it you know. Besides, {new_value} is not even a number! lol *quickly google searches* Ok it seems to be considered a number in some areas of computing, but not here! lol") #Don't troll CreateAnims, to make it feel closer. For now the tool, I like the sound of it too.
                    self.createanims.physics_dialog.attributes('-disabled', 0)
                    self.createanims.physics_dialog.focus_force()
                    return False
            except ValueError:
                self.createanims.physics_dialog_x_entry.configure(highlightcolor="red", highlightbackground="red")
                return False
        if (new_value.startswith("-") and len(new_value) > 1 and int(new_value) < -128) or (not new_value.startswith("-") and int(new_value) > 127): #Validation 2: value must not be greater than the admitted by the engine.
            self.createanims.physics_dialog_x_entry.configure(highlightcolor="red", highlightbackground="red")
            self.createanims.physics_dialog.attributes('-disabled', 1)
            messagebox.showwarning(title="What a big number!", message="That's a big number you're trying to enter there. Are you trying to teleport? Well maybe actually. Or maybe you're just trying to troll the tool. Anyways, I would say you go for a different approach though. MK3 at least does not support positives greater than 127 and negatives lesser than -128. Also, even if you enter say, 32... that's pretty high, it won't look very smooth. But well, maybe it's what you want. I won't stop you there :) .")
            self.createanims.physics_dialog.attributes('-disabled', 0)
            self.createanims.physics_dialog.focus_force()
            return False
        if new_value.startswith("0") and len(new_value) > 1: #Validation 3: if number starts with 0, it cannot have more than just 1 digit.
            self.createanims.physics_dialog_x_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        self.createanims.physics_dialog_x_entry.configure(highlightcolor="white", highlightbackground="white")
        return True

    def validate_character_entry(self, new_value):
        if not new_value: #Empty value is always welcome.
            self.createanims.character_entry.configure(highlightcolor="white", highlightbackground="white")
            return True
        try: #Validation 1: value must be an integer, 0 or positive.
            int(new_value)
        except ValueError:
            self.createanims.character_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if int(new_value) > len(self.createanims.characters) - 1: #Validation 2: value must not be greater than the maximum amount of characters.
            self.createanims.character_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        if new_value.startswith("0") and len(new_value) > 1: #Validation 3: if number starts with 0, it cannot have more than just 1 digit.
            self.createanims.character_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        self.createanims.character_entry.configure(highlightcolor="white", highlightbackground="white")
        return True

    def load_new_physics_id(self, new_physics_id):
        self.createanims.physics_id_entry.configure(highlightcolor="white", highlightbackground="white")
        self.createanims.current_physics_id = new_physics_id
        self.createanims.physics_id_entry.delete(0, "end")
        self.createanims.physics_id_entry.insert(0, str(new_physics_id))
        anim = self.createanims.characters[self.createanims.current_character].anims[self.createanims.current_anim]
        anim.physics_id = new_physics_id #This is important because there can be two sources. Maybe we loaded a new anim, in which case this will leave it exactly as intended because, here the new_physics_id is the anim physics_id, but if we changed it via the physics ID entry, then it needs to be updated with the new value. And yes, same happens with CHR bank when we load_frame_id.
        self.decide_arrow_buttons_status(new_physics_id, len(self.createanims.physics_list) - 1, self.createanims.physics_id_left_arrow, self.createanims.physics_id_right_arrow) #And nothing else in this case. It's like loading a CHR in a way. Though it's even more different in that an update in physics ID does not require an UI refresh. It will only change the field, and then what happens when you click on Play Anim.
        self.play_physics = True #Assume always possible unless stated (validated) otherwise.
        if len(self.createanims.physics_list[self.createanims.current_physics_id]) // 2 != len(anim.frame_ids):
            self.play_physics = False
            if not self.createanims.in_play_anim: #Don't show it when restarting due to Stop Anim.
                messagebox.showwarning(title="Physics ID Mismatch", message=f"Warning: Anim {self.createanims.current_anim:02d} has {len(anim.frame_ids)} frame(s) but assigned physics ID {self.createanims.current_physics_id:02d} has {len(self.createanims.physics_list[self.createanims.current_physics_id]) // 2} pair(s). Please consider updating either one of them. If you leave it as it is, you might see inconsistencies in the ROM.\nOnce you're done with your changes, consider reloading the physics ID. If this dialog no longer appears, the issue has been solved :) . Yay!")

    def load_new_character(self, new_character, new_frame=0):
        self.createanims.character_entry.configure(highlightcolor="white", highlightbackground="white")
        self.createanims.current_character = new_character
        self.createanims.character_entry.delete(0, "end")
        self.createanims.character_entry.insert(0, str(new_character))
        self.decide_arrow_buttons_status(new_character, len(self.createanims.characters) - 1, self.createanims.character_left_arrow, self.createanims.character_right_arrow)
        self.load_new_anim(self.createanims.current_anim, new_frame) #We preserve anim. I find it useful if you want to compare how the same anim looks from one character to the other. Frame cannot really be preserved or... oh wait. It can. Every anim... or... oh no. No it can't. Some anims will definitely have same amount of frames. But not necessarily.

    def load_new_anim(self, new_anim, new_frame=0):
        self.createanims.anim_entry.configure(highlightcolor="white", highlightbackground="white")
        self.createanims.current_anim = new_anim
        self.createanims.anim_entry.delete(0, "end")
        self.createanims.anim_entry.insert(0, str(new_anim))
        character = self.createanims.characters[self.createanims.current_character]
        self.decide_arrow_buttons_status(new_anim, len(character.anims) - 1, self.createanims.anim_left_arrow, self.createanims.anim_right_arrow)
        self.load_new_physics_id(character.anims[self.createanims.current_anim].physics_id)
        self.load_new_frame(new_frame, refresh_UI_flag=False) #We always start at the first frame of the anim. #But can be changed/adjusted. Very useful to keep editing the same frame after stop anim.
        self.createanims.refresh_UI() #Potencial refactor: let load_new_chr_bank do the UI refresh. So don't pass flag anymore. And make sure to decide arrow status and stuff before loading new CHR bank. In theory, it shouldn't affect anything, if load runs last.

    def load_new_frame(self, new_frame, refresh_UI_flag=True):
        self.createanims.frame_entry.configure(highlightcolor="white", highlightbackground="white")
        self.createanims.current_frame = new_frame
        self.createanims.frame_entry.delete(0, "end")
        self.createanims.frame_entry.insert(0, str(new_frame))
        self.createanims.current_frame = new_frame
        character = self.createanims.characters[self.createanims.current_character]
        frame_id = character.anims[self.createanims.current_anim].frame_ids[self.createanims.current_frame]
        if frame_id != self.createanims.current_frame_id: #Clear it only if they're actually different. Also has to happen here before load_new_frame_id overwrites it.
            self.createanims.current_anim_image_rectangle = None
        self.load_new_frame_id(frame_id, refresh_UI_flag=False)
        self.decide_arrow_buttons_status(new_frame, len(character.anims[self.createanims.current_anim].frame_ids) - 1, self.createanims.frame_left_arrow, self.createanims.frame_right_arrow)
        if refresh_UI_flag:
            self.createanims.refresh_UI()

    def load_new_frame_id(self, new_frame_id, refresh_UI_flag=True):
        self.createanims.frame_id_entry.configure(highlightcolor="white", highlightbackground="white")
        self.createanims.current_frame_id = new_frame_id
        self.createanims.frame_id_entry.delete(0, "end")
        self.createanims.frame_id_entry.insert(0, str(new_frame_id))
        character = self.createanims.characters[self.createanims.current_character]
        character.anims[self.createanims.current_anim].frame_ids[self.createanims.current_frame] = new_frame_id
        self.createanims.current_frame_id = new_frame_id
        frame = character.frames[new_frame_id]
        self.createanims.tile_utils.load_new_chr_bank(frame.metadata.chr_bank, refresh_UI_flag=False)
        self.decide_arrow_buttons_status(new_frame_id, len(character.frames) - 1, self.createanims.frame_id_left_arrow, self.createanims.frame_id_right_arrow)
        self.createanims.current_anim_image_rectangle = None
        if refresh_UI_flag:
            self.createanims.refresh_UI()

    def decide_arrow_buttons_status(self, new_value, upper_boundary, left_arrow, right_arrow): #I was a bit hesitant to create two or rather to think of making two but... makes more sense. They are conceptually different. #Also yes let's make it more generic in this case.
        if new_value == 0:
            left_arrow.configure(state="disabled")
        else:
            left_arrow.configure(state="normal")
        if new_value == upper_boundary:
            right_arrow.configure(state="disabled")
        else:
            right_arrow.configure(state="normal")

    def disable_all(self):
        self.createanims.anim_entry.configure(state="disabled")
        self.createanims.anim_left_arrow.configure(state="disabled")
        self.createanims.anim_right_arrow.configure(state="disabled")
        self.createanims.frame_entry.configure(state="disabled")
        self.createanims.frame_left_arrow.configure(state="disabled")
        self.createanims.frame_right_arrow.configure(state="disabled")
        self.createanims.frame_id_entry.configure(state="disabled")
        self.createanims.frame_id_left_arrow.configure(state="disabled")
        self.createanims.frame_id_right_arrow.configure(state="disabled")
        self.createanims.physics_id_entry.configure(state="disabled")
        self.createanims.physics_id_left_arrow.configure(state="disabled")
        self.createanims.physics_id_right_arrow.configure(state="disabled")
        self.createanims.character_entry.configure(state="disabled")
        self.createanims.character_left_arrow.configure(state="disabled")
        self.createanims.character_right_arrow.configure(state="disabled")
        self.createanims.edit_physics_button.configure(state="disabled")
        self.createanims.menu_bar.entryconfigure("File", state="disabled")
        self.createanims.menu_bar.entryconfigure("Anim", state="disabled")
        self.createanims.menu_bar.entryconfigure("Import", state="disabled")

    def enable_all(self):
        self.createanims.anim_entry.configure(state="normal")
        self.createanims.anim_left_arrow.configure(state="normal")
        self.createanims.anim_right_arrow.configure(state="normal")
        self.createanims.frame_entry.configure(state="normal")
        self.createanims.frame_left_arrow.configure(state="normal")
        self.createanims.frame_right_arrow.configure(state="normal")
        self.createanims.frame_id_entry.configure(state="normal")
        self.createanims.frame_id_left_arrow.configure(state="normal")
        self.createanims.frame_id_right_arrow.configure(state="normal")
        self.createanims.physics_id_entry.configure(state="normal")
        self.createanims.physics_id_left_arrow.configure(state="normal")
        self.createanims.physics_id_right_arrow.configure(state="normal")
        self.createanims.character_entry.configure(state="normal")
        self.createanims.character_left_arrow.configure(state="normal")
        self.createanims.character_right_arrow.configure(state="normal")
        self.createanims.edit_physics_button.configure(state="normal")
        self.createanims.menu_bar.entryconfigure("File", state="normal")
        self.createanims.menu_bar.entryconfigure("Anim", state="normal")
        self.createanims.menu_bar.entryconfigure("Import", state="normal")

    def play_anim(self, event=None): #The one that runs over and over. Then the init code runs only once. Alternative is to create StringVar and then trace and pass this. But you still get two functions. I like more this.
        import tkinter
        if not self.createanims.in_play_anim:
            return #And the chain stops.
        if self.play_physics:
            physics = self.createanims.physics_list[self.createanims.current_physics_id]
            x_physics = 2*self.calculate_physics(physics[2*self.createanims.current_frame])
            y_physics = 2*self.calculate_physics(physics[(2*self.createanims.current_frame) + 1])
            self.createanims.physics_initial_x += x_physics
            self.createanims.physics_initial_y += y_physics
        self.createanims.png_img.clear()
        character = self.createanims.characters[self.createanims.current_character]
        frame_id = character.anims[self.createanims.current_anim].frame_ids[self.createanims.current_frame]
        img = tkinter.PhotoImage(file=f"{self.createanims.root_dir}/{character.name}/images/{character.name}_frame_{frame_id:03d}.png") #(self.createanims.tiles_images[0].pre_tkimg.resize((16, 16)))
        self.createanims.png_img.append(img) #Say no to garbage collection of PhotoImage.
        frame = character.frames[frame_id]
        self.createanims.play_anim_label.place(x=375+(frame.metadata.x_offset*2) + self.createanims.physics_initial_x, y=200 - (frame.metadata.y_offset*2) - (16*frame.metadata.y_length) + self.createanims.physics_initial_y)
        self.createanims.play_anim_label.configure(image=img)
        if self.createanims.current_frame == len(character.anims[self.createanims.current_anim].frame_ids) - 1:
            self.createanims.current_frame = 0
            if not self.check_physics_boundaries(self.createanims.physics_initial_x, self.createanims.physics_initial_y): #Otherwise, don't restart. I like more the look of it.
                self.restart_physics() #Let's encapsulate it here. Will make it easier to not have the restart values in many places.
        else:
            self.createanims.current_frame += 1
        self.createanims.root.after(47, self.play_anim) #I think 47 is the magical number. Looks really, really good.

    def generate_png_from_anim_frames(self, character):
        from generate_anim_images import refresh_chr, generate_png
        for frame_id in character.anims[self.createanims.current_anim].frame_ids:
            frame = character.frames[frame_id]
            current_chr_bank = frame.metadata.chr_bank
            refresh_chr(character, current_chr_bank)
            png = generate_png(frame)
            png_path = f"{self.createanims.root_dir}/{character.name}/images"
            os.path.isdir(png_path) or os.makedirs(png_path) #This time I feel like explaining, so or shortcircuits, which means, this is an indirect if. If the path exists, nothing else to do. If it doesn't, then make the dir.
            png.save(f"{png_path}/{character.name}_frame_{frame_id:03d}.png", "PNG")

    def fill_physics_grid(self):
        import tkinter #Well no can do. This specifically will need it.
        self.createanims.physics_graphics_canvas.delete('PhysicsPoint') #There you go! Will use, but for graphics_canvas. #Huh wait, this will delete the window as well right? So it's going to mess the window as well? #Method could be called refresh_physics.
        for label in self.createanims.frame_physics.winfo_children():
            label.destroy() #Yay! This works!
        label = tkinter.Label(self.createanims.frame_physics, text="Coordinate")
        label.grid(row=0, column=0)
        label = tkinter.Label(self.createanims.frame_physics, text="X")
        label.grid(row=1, column=0, sticky="nsew")
        label = tkinter.Label(self.createanims.frame_physics, text="Y")
        label.grid(row=2, column=0, sticky="nsew")
        current_x = 0 #Exact same logic as play_anim
        current_y = 0
        physics = self.createanims.physics_list[self.createanims.current_physics_id]
        if len(physics) == 1: #Then there's only an 0x80 left. Not possible. Every physics needs to have at least 1 pair.
            physics.insert(0, 0x00)
            physics.insert(0, 0x00)
            self.createanims.physics_window.attributes('-disabled', 1)
            messagebox.showinfo(title="Physics Automatic Addition", message=f"Physics ID {self.createanims.current_physics_id} was found to be empty (just an $80 byte). This means the physics is UNUSED. You can use it, but it must have at least one pair of X and Y 00. Therefore, those were added automatically. You will not find them in the original binary.")
            self.createanims.physics_window.attributes('-disabled', 0)
            self.createanims.physics_window.focus_force()
        for n in range(len(physics) // 2):
            label = tkinter.Label(self.createanims.frame_physics, text=f"{n:02d}")
            PhysicsLabel(self.createanims, label, n)
            label.grid(row=0, column=n+1, padx=(2, 2))
            aux_current_x = current_x
            x_physics = self.calculate_physics(physics[2*n])
            current_x += x_physics #No *2 in this case. Helps with not making drawings too big, but the general idea should still be there.
            x_label = tkinter.Label(self.createanims.frame_physics, text=f"{x_physics:02d}")
            x_label.grid(row=1, column=n+1)
            aux_current_y = current_y
            y_physics = self.calculate_physics(physics[(2*n) + 1])
            current_y += y_physics
            y_label = tkinter.Label(self.createanims.frame_physics, text=f"{y_physics:02d}")
            y_label.grid(row=2, column=n+1)
            self.createanims.physics_graphics_canvas.create_oval(215 + current_x, 180 + current_y, 215 + current_x, 180 + current_y, width=5, outline="red", tag="PhysicsPoint")
            self.createanims.physics_graphics_canvas.create_line(215 + aux_current_x, 180 + aux_current_y, 215 + current_x, 180 + current_y, fill="green", tag="PhysicsPoint") #Technically not point per se, but will make things easier.

    def calculate_physics(self, value): #Ok no, turns out it's different logic. But still, similar. #Very much the same as calculate_fine_pitch (parse_mml). I was going to do the whole toggle XOR thing and then -1 but, this will do.
        if value >= 0x80:
            return - (0x100 - value) #Yeah it's different because in calculate_fine_pitch, it has to give you the negative number still in 6502 format, like, 0xFD for example, but here I want the raw number, I want the -3 for example.
        else:
            return value

    def check_physics_boundaries(self, x, y):
        return (
            x >= -399 and #Remember: we're checking the initial_x here. Not the total position. Uhhhh... maybe not such a good idea. But for now it'll do.
            y >= 0 and
            x <= 399 and
            y <= 256
        )

    def restart_physics(self):
        self.createanims.physics_initial_x = 0 #-100 #Also yes, these could be members/fields of Anim. Key word "could".
        self.createanims.physics_initial_y = 0 #100