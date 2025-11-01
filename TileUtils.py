from PIL import Image, ImageTk

SYSTEM_PALETTE = [
	[116, 116, 116],
	[36, 24, 140],
	[0, 0, 168],
	[68, 0, 156],
	[140, 0, 116],
	[168, 0, 16],
	[164, 0, 0],
	[124, 8, 0],
	[64, 44, 0],
	[0, 68, 0],
	[0, 80, 0],
	[0, 60, 20],
	[24, 60, 92],
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
	[188, 188, 188],
	[0, 112, 236],
	[32, 56, 236],
	[128, 0, 240],
	[188, 0, 188],
	[228, 0, 88],
	[216, 40, 0],
	[200, 76, 12],
	[136, 112, 0],
	[0, 148, 0],
	[0, 168, 0],
	[0, 144, 56],
	[0, 128, 136],
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
	[252, 252, 252],
	[60, 188, 252],
	[92, 148, 252],
	[204, 136, 252],
	[244, 120, 252],
	[252, 116, 180],
	[252, 116, 96],
	[252, 152, 56],
	[240, 188, 60],
	[128, 208, 16],
	[76, 220, 72],
	[88, 248, 152],
	[0, 232, 216],
	[120, 120, 120],
	[0, 0, 0],
	[0, 0, 0],
	[252, 252, 252],
	[168, 228, 252],
	[196, 212, 252],
	[212, 200, 252],
	[252, 196, 252],
	[252, 196, 216],
	[252, 188, 176],
	[252, 216, 168],
	[252, 228, 160],
	[224, 252, 160],
	[168, 240, 188],
	[176, 252, 204],
	[156, 252, 240],
	[196, 196, 196],
	[0, 0, 0],
	[0, 0, 0],
]

class PalRectangle: #I usually don't do this, but whatever. The main is TileUtils.

    def __init__(self, createanims, palette_canvas, pal_rectangle, character_pal_index, pal, pal_label):
        self.createanims = createanims
        self.palette_canvas = palette_canvas
        self.pal_rectangle = pal_rectangle #This is actually a literal int. Pretty cool. #Alternative name pal_rectangle_id to make it clear it's a literal int/ID.
        self.character_pal_index = character_pal_index #This will be used to know what value to update such that now when refresh_palette runs, it will display updated palette.
        self.pal = pal
        self.pal_label = pal_label
        self.palette_canvas.tag_bind(self.pal_rectangle, "<Enter>", self.on_enter)
        self.palette_canvas.tag_bind(self.pal_rectangle, "<Button-1>", self.on_left_click)

    def on_enter(self, event=None):
        self.pal_label.config(text=f"Palette: {self.pal:02X}")

    def on_left_click(self, event=None):
        if self.createanims.current_pal_rectangle is not None:
            current_rgb = self.palette_canvas.itemcget(self.createanims.current_pal_rectangle, "fill")
            self.palette_canvas.itemconfig(self.createanims.current_pal_rectangle, outline=current_rgb) #Outline "" doesn't really work. It leaves some borders.
        self.palette_canvas.itemconfig(self.pal_rectangle, outline="red")
        self.createanims.current_pal_rectangle = self.pal_rectangle
        self.select_color_picker_rectangle(self.pal) #When a pal rectangle is selected, its corresponding color picker rectangle is selected too. Relatively easy to do thanks to the fact color picker is ordered and fixed!

    def select_color_picker_rectangle(self, pal):
        color_picker_rectangle_object = self.createanims.color_picker_rectangles[pal] #Object to clarify/set that it's not just the ID.
        if self.createanims.current_color_picker_rectangle is not None:
            current_rgb = color_picker_rectangle_object.color_picker_canvas.itemcget(self.createanims.current_color_picker_rectangle, "fill")
            color_picker_rectangle_object.color_picker_canvas.itemconfig(self.createanims.current_color_picker_rectangle, outline=current_rgb)
        color_picker_rectangle_object.color_picker_canvas.itemconfig(color_picker_rectangle_object.color_picker_rectangle, outline="blue") #Might be worth it to create a function that retrieves the selection color based on pal.
        self.createanims.current_color_picker_rectangle = color_picker_rectangle_object.color_picker_rectangle

class ColorPickerRectangle: #So like PalRectangle, but rectangles used for the color picker.

    def __init__(self, createanims, color_picker_canvas, color_picker_rectangle, pal, rgb, pal_label):
        self.createanims = createanims
        self.color_picker_canvas = color_picker_canvas
        self.color_picker_rectangle = color_picker_rectangle
        self.pal = pal
        self.rgb = rgb #We will use it after all, just for something else.
        self.pal_label = pal_label
        self.color_picker_canvas.tag_bind(self.color_picker_rectangle, "<Button-1>", self.on_left_click)

    def on_left_click(self, event=None):
        if self.createanims.current_color_picker_rectangle is not None:
            current_rgb = self.color_picker_canvas.itemcget(self.createanims.current_color_picker_rectangle, "fill")
            self.color_picker_canvas.itemconfig(self.createanims.current_color_picker_rectangle, outline=current_rgb) #Outline "" doesn't really work. It leaves some borders. (copypasted)
        self.color_picker_canvas.itemconfig(self.color_picker_rectangle, outline="blue")
        self.createanims.current_color_picker_rectangle = self.color_picker_rectangle
        self.update_pal_rectangle()
        self.createanims.tile_utils.refresh_chr()
        self.createanims.anim.refresh()

    def update_pal_rectangle(self):
        if self.createanims.current_pal_rectangle is None:
            return #Nothing to do then. This logic only applies if there is a pal rectangle selected.
        pal_rectangle_object = self.createanims.pal_rectangles[self.createanims.current_pal_rectangle]
        character_palette = self.createanims.characters[self.createanims.current_character].palette
        character_palette[pal_rectangle_object.character_pal_index] = self.pal #Now the character palette is updated and will be picked by refresh_palette.
        pal_rectangle_object.palette_canvas.itemconfig(pal_rectangle_object.pal_rectangle, fill=self.rgb)
        self.pal_label.config(text=f"Palette: {self.pal:02X}") #Technically not the pal_rectangle itself but I mean, still logically part of the same update. Same unit.

class TileImage:

    def __init__(self, createanims, chr_canvas, tile_image, tile_index, tile_palette_group, tile_label, pre_tkimg, final_img):
        self.createanims = createanims
        self.chr_canvas = chr_canvas
        self.tile_image = tile_image #Beware, it's not the image object itself. It's the ID of the image which we'll use to make changes and stuff. Very much same as PalRectangle and ColorPickerRectangle.
        self.tile_index = tile_index
        self.tile_palette_group = tile_palette_group
        self.tile_label = tile_label
        self.pre_tkimg = pre_tkimg #This is the image as in img.putpalette. It's before we do the conversion from PIL image to Tkinter image. So, pre_tkimg. Useful for transparency when drawing anim.
        self.final_img = final_img #This is the final, processed img, like the ImageTk image. It's only being saved to protect it from the gc. Meanie.
        self.chr_canvas.tag_bind(self.tile_image, "<Enter>", self.on_enter)
        self.chr_canvas.tag_bind(self.tile_image, "<Button-1>", self.on_left_click)
        self.chr_canvas.tag_bind(self.tile_image, "<Double-Button-1>", self.on_double_left_click)
        self.chr_canvas.tag_bind(self.tile_image, "<B3-Motion>", self.on_right_click_motion)
        self.chr_canvas.tag_bind(self.tile_image, "<ButtonRelease-3>", self.on_right_click_release)
        self.in_motion = False

    def on_enter(self, event=None):
        self.tile_label.config(text=f"Tile: {self.tile_index:02X} / {self.tile_palette_group:02X}")

    def on_left_click(self, event=None):
        x, y = self.chr_canvas.coords(self.tile_image)
        if self.createanims.current_tile_image_rectangle is None: #Again, similar approach to PalRectangle and ColorPickerRectangle. Though this time I add a suffix _rectangle to make it clear that we're making a rectangle around the tile image. Wonderful awesome.
            self.createanims.current_tile_image_rectangle = self.chr_canvas.create_rectangle(x, y, x+15, y+15, width=1, outline="white") #Let's give white a try. Maybe after you're reading this it's a different color.
            self.createanims.current_tile_image_inner_rectangle = self.chr_canvas.create_rectangle(x+1, y+1, x+14, y+14, width=1, outline="black") #Actually inner, what I meant to say. #Outer, it's going to help for white tiles to be clearly visibly selected as well.
            self.createanims.current_tile_image_outer_rectangle = self.chr_canvas.create_rectangle(x-1, y-1, x+16, y+16, width=1, outline="black") #And now outer, helps a lot too.
        else:
            self.chr_canvas.moveto(self.createanims.current_tile_image_rectangle, x-1, y-1) #Nothing to move if it doesn't exist. So that's why the if.
            self.chr_canvas.moveto(self.createanims.current_tile_image_inner_rectangle, x, y)
            self.chr_canvas.moveto(self.createanims.current_tile_image_outer_rectangle, x-2, y-2)

    def on_double_left_click(self, event=None):
        initial_x, initial_y = self.chr_canvas.coords(self.tile_image) #We could also cache this but uh, yeah. Let's get them here before we delete the image (also yeah, if I stored it, I would have to update it with every move... not fun).
        self.createanims.tile_utils.delete_tile_image_rectangles()
        chr_palette = self.createanims.characters[self.createanims.current_character].chr_palettes[self.createanims.current_chr_bank] #It has a bit of everything from refresh_chr. But has to be different because on the one hand, I only want just one image updated. And on the other, it'd just get messy to have everything under the same function.
        tile_palette_row = self.tile_index // 8 #We can also do >> 3 which is same as the lsr we see in the code but I mean whatever.
        tile_palette_row_tile = self.tile_index % 8
        chr_palette[tile_palette_row] ^= 1 << tile_palette_row_tile #Here's the gist of it, the magic. #The opposite. Also, yes, it seems like a lot of trouble for just one not but the alternative is to catch (cache) it or something which... meh.
        character_chr = self.createanims.characters[self.createanims.current_character].chrs[self.createanims.current_chr_bank]
        pixels = self.createanims.tile_utils.get_pixels(self.tile_index, character_chr)
        img = Image.frombytes("P", (8, 8), bytes(pixels))
        tile_palette_group, tile_palette = self.createanims.tile_utils.get_tile_palette(self.tile_index, chr_palette) #Let's change the name. tile_palette. It's more accurate. #Exactly. As we have CHR and pixels. We also have chr_palette and pixels_palette. Beautiful.
        img.putpalette(tile_palette) #Though, it'll always be the rgb of the group 0 or 1 palette so, in a way, it could be called even pal_rectangle.
        self.pre_tkimg = img
        final_img = ImageTk.PhotoImage(img.resize((16, 16)))
        self.tile_image = self.createanims.chr_canvas.create_image(initial_x, initial_y, anchor="nw", image=final_img)
        self.final_img = final_img #And again, we need to keep the reference.
        self.chr_canvas.tag_bind(self.tile_image, "<Enter>", self.on_enter) #Maybe... it would be better to just create a new TileImage altogether.
        self.chr_canvas.tag_bind(self.tile_image, "<Button-1>", self.on_left_click)
        self.chr_canvas.tag_bind(self.tile_image, "<Double-Button-1>", self.on_double_left_click)
        self.chr_canvas.tag_bind(self.tile_image, "<B3-Motion>", self.on_right_click_motion)
        self.chr_canvas.tag_bind(self.tile_image, "<ButtonRelease-3>", self.on_right_click_release)
        x, y = initial_x, initial_y
        self.createanims.current_tile_image_rectangle = self.chr_canvas.create_rectangle(x, y, x+15, y+15, width=1, outline="white") #Let's give white a try. Maybe after you're reading this it's a different color.
        self.createanims.current_tile_image_inner_rectangle = self.chr_canvas.create_rectangle(x+1, y+1, x+14, y+14, width=1, outline="black") #Actually inner, what I meant to say. #Outer, it's going to help for white tiles to be clearly visibly selected as well.
        self.createanims.current_tile_image_outer_rectangle = self.chr_canvas.create_rectangle(x-1, y-1, x+16, y+16, width=1, outline="black")
        self.tile_palette_group = tile_palette_group
        self.createanims.anim.refresh()

    def on_right_click_motion(self, event): #Not None anymore cause now I'm gonna use it.
        if not self.verify_motion_coordinates(event.x, event.y): #You're right, I have to do this here. As a guard, and with original event.x and event.y values. #You cannot trigger motion outside the boundaries. Let's verify that.
            return
        tile_row = event.y // 16
        tile_col = event.x // 16 #We only care about the integer part. >> 4 achieves same but, again this is more explicit for me.
        tile_selected = tile_row*0x10 + tile_col
        tile_image = self.createanims.tiles_images[tile_selected]
        tile_image.on_enter() #Update labels.
        if tile_image.in_motion or self.createanims.current_tile_image_rectangle is None: #Cannot do if there is no selection. #No, we're leaving it this way. Cool to know which ones we already updated. Then the rectangle won't move. And we'll be able to see last updated. #But in this case, maybe we can still update the Tile / CHR Palette labels and move the rectangles/selector.
            return
        tile_image.in_motion = True
        tile_image.on_double_left_click() #So beautiful. Because event=None, it just works. And we're being explicit that we want the exact same thing to happen.

    def verify_motion_coordinates(self, x, y):
        return (
            x >= 0 and #Both have to be positive (i.e., don't go too much to the left or too much up).
            y >= 0 and
            x < 256 and #Actually, those have to be < and not <=. At that point, the result gives a tile out of range. I think this is still correct either way though, as I'm pretty sure last one is pixels 112 to 127 and 240 to 255. #Each image is 16 pixels wide, canvas is 256 pixels wide.
            y < 128 #Same, now for y. So with this we cover all 4 corners.
        )

    def on_right_click_release(self, event=None):
        self.createanims.tile_utils.clear_in_motion() #Do it for aaall tile images.

class TileUtils:

    def __init__(self, createanims):
        self.createanims = createanims

    def refresh_palette(self): #Show according to what's already stored, or, well yeah. Passing the index isn't my style. I think.
        palette = self.createanims.characters[self.createanims.current_character].palette #I'm likely going to refactor this soon. Rather than characters_ for each type of data, I will have characters, and then access each character from there.
        initial_x = 0
        self.createanims.pal_rectangles = {} #Updated to dictionary now. Easier to pick up by pal_rectangle id. #So now I'm wondering how much I need init_state? Well it's more for stuff that needs an initial value because it won't be necessarily initialized at some other points, or it may be used at multiple points the first time. It's not the case here. This is meant to run the first time the UI starts. But there's a bit of randomness to it. Sometimes I just like to add stuff there to have it all in one place.
        for i, pal in enumerate(palette):
            rgb_triplet = SYSTEM_PALETTE[pal]
            r, g, b = rgb_triplet[0], rgb_triplet[1], rgb_triplet[2]
            rgb = f"#{r:02X}{g:02X}{b:02X}"
            pal_rectangle = self.createanims.character_palette_canvas.create_rectangle(initial_x, 0, initial_x + 31, 31, fill=rgb, outline=rgb, width=1)
            pal_rectangle_object = PalRectangle(self.createanims, self.createanims.character_palette_canvas, pal_rectangle, i, pal, self.createanims.pal_label)
            self.createanims.pal_rectangles[pal_rectangle] = pal_rectangle_object
            initial_x += 32

    def refresh_chr(self):
        if self.createanims.current_tile_image_rectangle is not None: #Typical fix. #I put this here but... actually it should be part of refresh. Let's move it.
            self.store_tile_image_rectangle_coords() #The just in case goes more for the deletion in chr_canvas, but the current selection must be updated to None otherwise we get bug where rectangles are not drawn on screen anymore. Probably images overlap them? Or something of the sort. #Just in case. Let us avoid a memory leak, performance issues and stuff like that.
        self.createanims.chr_canvas.delete("all") #Nah changed my mind but still leaving it here. #I could import it at the top but it gives wrong idea. It's not really something that TileUtils uses like images. It's... for a variable. We could in fact just pass the string and whatever. It's not the same as saying "we can just copypaste the code". It's not the same thing.
        self.createanims.tiles_images = [] #Let's follow same as pal_rectangles for refresh_palette. Sometimes I use clear... this will do. Plus it won't work first time and it's already like this before so, yeah.
        chr_palette = self.createanims.characters[self.createanims.current_character].chr_palettes[self.createanims.current_chr_bank]
        character_chr = self.createanims.characters[self.createanims.current_character].chrs[self.createanims.current_chr_bank]
        self.create_chr_images(chr_palette, character_chr)
        if self.createanims.current_tile_image_rectangle is not None:
            self.regenerate_tile_image_rectangles()

    def create_chr_images(self, chr_palette, character_chr):
        tile_i = 0
        initial_y = -16
        for row in range(8):
            initial_x = 0
            initial_y += 16
            for col in range(16):
                self.create_chr_image(initial_x, initial_y, tile_i, chr_palette, character_chr)
                initial_x += 16
                tile_i += 1

    def create_chr_image(self, initial_x, initial_y, tile_i, chr_palette, character_chr):
        pixels = self.get_pixels(tile_i, character_chr)
        img = Image.frombytes("P", (8, 8), bytes(pixels))
        tile_palette_group, tile_palette = self.get_tile_palette(tile_i, chr_palette) #Let's change the name. tile_palette. It's more accurate. #Exactly. As we have CHR and pixels. We also have chr_palette and pixels_palette. Beautiful.
        img.putpalette(tile_palette) #Though, it'll always be the rgb of the group 0 or 1 palette so, in a way, it could be called even pal_rectangle.
        final_img = ImageTk.PhotoImage(img.resize((16, 16)))
        tile_image = self.createanims.chr_canvas.create_image(initial_x, initial_y, anchor="nw", image=final_img)
        self.createanims.tiles_images.append(TileImage(self.createanims, self.createanims.chr_canvas, tile_image, tile_i, tile_palette_group, self.createanims.tile_label, img, final_img)) #Now we'll send final_img as a parameter. Had to move it here when we now have the ID tile_image.

    def get_pixels(self, tile_i, character_chr): #First 8 values are for row 0, then for row 1, and until row 7 (8 rows total).
        pixels = []
        chr_row = 0x10*tile_i #Let's distinguish: chr_row is the row with all the pixels_rows. So 16 bytes from chr_row have bits for the 8 pixel rows. chr_row and pixel_row.
        bytes_tile_chr_row = character_chr[chr_row:chr_row+0x10] #tile_row+0x10 is not included, so this gets us what we want.
        for pixel_row in range(8): #Until 7, but don't include 8.
            pixel_row_byte_low = bytes_tile_chr_row[pixel_row] #I know most documentation refers to it as planes and bla bla bla yada yada but I understand it more as high and low.
            pixel_row_byte_high = bytes_tile_chr_row[pixel_row+8] #So bytes_tile_chr_row has the bytes for the CHR row, in other words, for the tile (yeah, chr_tile_row might be a bit redundant but I understand it better that way). 
            bit_col = 0x80 #To different of pixel_col which will be used for the range. But they fundamentally represent the same just with different numbers.
            for pixel_col in range(8): #And another 8 times for a total of 64 pixels to add. #Okay much better, pixel_row and pixel_col.
                bit_low = pixel_row_byte_low & bit_col
                if bit_low:
                    bit_low = 0x1 #To avoid having to shift aaaaall the way to the right.
                bit_high = pixel_row_byte_high & bit_col
                if bit_high:
                    bit_high = 0x1
                pixel = (bit_high << 1) | (bit_low) #Will give either 0, 1, 2 or 3. That will be the color to use.
                pixels.append(pixel)
                bit_col >>= 1 #Can you do >>= without it breaking?
        return pixels

    def get_tile_palette(self, tile_i, chr_palette):
        tile_palette = []
        tile_palette_row = tile_i // 8 #We don't care, in this context, about the remainder. Not yet, at least. #We can also do >> 3 which is same as the lsr we see in the code but I mean whatever.
        tile_palette_row_tile = tile_i % 8 #Changed to tile, seems more accurate now. #Now we care about the remainder. So chr_palette_row and chr_palette_row_tile will pinpoint us the exact location.
        tile_palette_row_byte = chr_palette[tile_palette_row]
        tile_palette_group = tile_palette_row_byte & (1 << tile_palette_row_tile)
        if tile_palette_group:
            pal_group = self.createanims.characters[self.createanims.current_character].palette[4:8] #This makes it more explicit that I want exactly the last 4.
        else:
            pal_group = self.createanims.characters[self.createanims.current_character].palette[0:4] #And here the first 4.
        for pal in pal_group: #Some call the pal_group the subpalette so aka subpalette.
            rgb_triplet = SYSTEM_PALETTE[pal]
            tile_palette.extend(rgb_triplet) #putpalette doesn't accept triplets it would seem, has to be all values as a sequence.
        return int(bool(tile_palette_group)), tile_palette #Could be int(bool(tile_palette_group)), maybe to be more explicit but... either works. Actually yes, I'll just add it to make it explicit for me.

    def delete_tile_image_rectangles(self): #I will need this for several sources. A restart that for now can come from ColorPickerRectangle or TileImage, but it may come also from Anim and potentially other places.
        self.createanims.chr_canvas.delete(self.createanims.current_tile_image_rectangle)
        self.createanims.chr_canvas.delete(self.createanims.current_tile_image_inner_rectangle)
        self.createanims.chr_canvas.delete(self.createanims.current_tile_image_outer_rectangle)
        self.createanims.current_tile_image_rectangle = None
        self.createanims.current_tile_image_inner_rectangle = None
        self.createanims.current_tile_image_outer_rectangle = None

    def store_tile_image_rectangle_coords(self):
        self.x1, self.y1, self.x2, self.y2 = self.createanims.chr_canvas.coords(self.createanims.current_tile_image_rectangle)
        self.x1_inner, self.y1_inner, self.x2_inner, self.y2_inner = self.createanims.chr_canvas.coords(self.createanims.current_tile_image_inner_rectangle)
        self.x1_outer, self.y1_outer, self.x2_outer, self.y2_outer = self.createanims.chr_canvas.coords(self.createanims.current_tile_image_outer_rectangle)

    def regenerate_tile_image_rectangles(self):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        self.createanims.current_tile_image_rectangle = self.createanims.chr_canvas.create_rectangle(x1, y1, x2, y2, width=1, outline="white")
        x1, y1, x2, y2 = self.x1_inner, self.y1_inner, self.x2_inner, self.y2_inner
        self.createanims.current_tile_image_inner_rectangle = self.createanims.chr_canvas.create_rectangle(x1, y1, x2, y2, width=1, outline="black")
        x1, y1, x2, y2 = self.x1_outer, self.y1_outer, self.x2_outer, self.y2_outer
        self.createanims.current_tile_image_outer_rectangle = self.createanims.chr_canvas.create_rectangle(x1, y1, x2, y2, width=1, outline="black")

    def clear_in_motion(self):
        for tile_image in self.createanims.tiles_images: #tile_images but... whatever. Let's leave tiles_images.
            tile_image.in_motion = False