from PIL import Image, ImageTk

INITIAL_X_FRAME = 50 #To know from where to start col by col, row by row. The cells.
INITIAL_Y_FRAME = 36

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
        self.x_offset = frame_bytes[2]
        self.chr_bank = frame_bytes[3]
        self.y_offset = (frame_bytes[4] & 0xF) * (-1 if (frame_bytes[4] & 0x10) else 1) #I don't usually use ternary in Python but here it is pretty convenient.
        self.special_palette_id = 0 #Unused, but we may give it an use later on.

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
            frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame] #It could be a good idea to add a get_frame(). But you know, that's what most people do. I only do it if it's convenient. Here, this is just way clearer.
            frame.tiles[self.anim_index] = self.createanims.current_chr_tile_index
            self.createanims.anim.refresh()

    def on_right_click(self, event=None):
        self.select()
        if self.tile_image_object is not None: #It could be the empty one, in which case, don't do anything, just select in Anim.
            self.tile_image_object.select()
            self.tile_image_object.update_tile_label()

    def on_double_right_click(self, event=None):
        frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame]
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

class Anim: #Yes this could be AnimUtils. Or maybe FrameUtils, come to think of it. #Similar structure to TileUtils. You have the main class, which then uses data from other classes to do its stuff.

    def __init__(self, createanims):
        self.createanims = createanims
        self.transparency = 1 #Default value. #Yes, let's leave this as part of Anim. It will still be accessible from CreateAnims, Command etc. etc.
        self.draw_frame_rectangle = 1 #I know I know. I'm mixing Frame and Anim quite a lot. Oh well. We'll survive. I think.
        self.draw_empty_cells = 1
        self.frame_rectangle = None #No ID, will be created later if option is turned on.

    def refresh(self):
        if self.createanims.current_anim_image_rectangle is not None:
            self.store_anim_image_rectangle_coords() #We need to do it this way cause, once we hit delete, there's no turning back. But at the same time, we need to regenerate everything once it's been deleted. So, yeah.
        self.createanims.anim_canvas.delete("all") #Yeah, we will delete everything just in case just like TileUtils. And well, not 'just in case', without this, tag bind Button-1, then Shift+T, and second time it doesn't work anymore. Probably due to these references not letting the changes go through or something of the sort.
        initial_y = INITIAL_Y_FRAME - 16
        self.createanims.anim_images = []
        frame = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame]
        cell_id = 0 #Let's call it this way, probably the most accurate. tile_id could be confused with the tile_id stored in the cell, frame_tile_id would be another candidate to refer to the tile_id stored in the frame, but mixing frame and tile can be a bit confusing as with row and tile in the same name (I did it for TileUtils).
        for row in range(frame.metadata.y_length):
            initial_x = INITIAL_X_FRAME
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
            self.frame_rectangle = self.createanims.anim_canvas.create_rectangle(INITIAL_X_FRAME, INITIAL_Y_FRAME, INITIAL_X_FRAME + 16*frame.metadata.x_length, INITIAL_Y_FRAME + 16*frame.metadata.y_length, outline="red", width=2)
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
        return True

    def validate_frame_entry(self, new_value):
        return True

    def validate_frame_id_entry(self, new_value):
        return True