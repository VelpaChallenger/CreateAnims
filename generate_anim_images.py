#This script can help to make PNG images out of frames.
#It's very similar to Character.py. It tries to do pretty much the same, but outside the context of CreateAnims, in a simplfied environment.

from PIL import Image
import os
from Character import Character #I changed my mind. Let's just import it. I was literally copypasting the exact same code, but without all the self and... no, let's just do this. It's separated, let's take advantage of that. Character per se has literally nothing to do with UI. So yeah.
from TileUtils import SYSTEM_PALETTE

ROOT_DIR = "../characters" #Still not really feeling like using os.sep.
tiles_images = [] #A new one. Doesn't contain TileImage in this context. But the pre_tkimg directly.

def refresh_chr(character, current_chr_bank): #There's actually a lot that we need from CreateAnims. #But yes, importing Character already simplifies so much. I love it.
    tiles_images.clear() #Yeah whatever, here.
    character_palette = character.palette
    chr_palette = character.chr_palettes[current_chr_bank]
    character_chr = character.chrs[current_chr_bank]
    create_chr_images(character_palette, chr_palette, character_chr)

def create_chr_images(character_palette, chr_palette, character_chr):
    tile_i = 0
    initial_y = -16
    for row in range(8):
        initial_x = 0
        initial_y += 16
        for col in range(16):
            create_chr_image(initial_x, initial_y, tile_i, character_palette, chr_palette, character_chr)
            initial_x += 16
            tile_i += 1

def create_chr_image(initial_x, initial_y, tile_i, character_palette, chr_palette, character_chr):
    pixels = get_pixels(tile_i, character_chr)
    img = Image.frombytes("P", (8, 8), bytes(pixels))
    tile_palette_group, tile_palette = get_tile_palette(character_palette, tile_i, chr_palette) #Let's change the name. tile_palette. It's more accurate. #Exactly. As we have CHR and pixels. We also have chr_palette and pixels_palette. Beautiful.
    img.putpalette(tile_palette) #Though, it'll always be the rgb of the group 0 or 1 palette so, in a way, it could be called even pal_rectangle.
    tiles_images.append(img)

def get_pixels(tile_i, character_chr): #First 8 values are for row 0, then for row 1, and until row 7 (8 rows total).
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

def get_tile_palette(character_palette, tile_i, chr_palette):
    tile_palette = []
    tile_palette_row = tile_i // 8 #We don't care, in this context, about the remainder. Not yet, at least. #We can also do >> 3 which is same as the lsr we see in the code but I mean whatever.
    tile_palette_row_tile = tile_i % 8 #Changed to tile, seems more accurate now. #Now we care about the remainder. So chr_palette_row and chr_palette_row_tile will pinpoint us the exact location.
    tile_palette_row_byte = chr_palette[tile_palette_row]
    tile_palette_group = tile_palette_row_byte & (1 << tile_palette_row_tile)
    if tile_palette_group:
        pal_group = character_palette[5:8] #Custom code. So for this specific case, we want first to be always white. #This makes it more explicit that I want exactly the last 4.
    else:
        pal_group = character_palette[1:4]
    rgb_triplet = [0xE0, 0xE0, 0xE0] #Always white or whatever we want, configurable from here. # (Moved comment) #Update black to white.
    tile_palette.extend(rgb_triplet)
    for pal in pal_group: #Some call the pal_group the subpalette so aka subpalette.
        rgb_triplet = SYSTEM_PALETTE[pal]
        tile_palette.extend(rgb_triplet) #putpalette doesn't accept triplets it would seem, has to be all values as a sequence.
    return int(bool(tile_palette_group)), tile_palette #Could be int(bool(tile_palette_group)), maybe to be more explicit but... either works. Actually yes, I'll just add it to make it explicit for me.

def generate_png(frame):
    png = Image.new("RGB", (16*frame.metadata.x_length, 16*frame.metadata.y_length), "white")
    initial_y = -16
    cell_id = 0
    for row in range(frame.metadata.y_length):
        initial_x = 0
        initial_y += 16
        for col in range(frame.metadata.x_length):
            tile_id = frame.tiles[cell_id]
            if tile_id != 0xFF:
                pre_tkimg = tiles_images[tile_id & 0x7F]
                png.paste(pre_tkimg.resize((16, 16)), (initial_x, initial_y))
            else:
                pixels = [0x00] * 64 #Maybe I can create an image like this and just reference it? Not sure how'd that work but might be worth a try. #Fully transparent. This works as a fill.
                img = Image.frombytes("P", (8, 8), bytes(pixels))
                tile_palette = [0xE0] * 12 #Like, just whatever. We won't use them.
                img.putpalette(tile_palette)
                pre_tkimg = img
                png.paste(pre_tkimg.resize((16, 16)), (initial_x, initial_y))
            initial_x += 16
            cell_id += 1
    return png #Yeah, the caller will decide how to use it, save it and stuff.

characters_name_list = os.listdir(ROOT_DIR)
for character_name in characters_name_list:
    character = Character(ROOT_DIR, character_name) #There you go. Now it's completely decoupled from the UI component.
    for i, frame in enumerate(character.frames): #Now the magic starts.
        refresh_chr(character, frame.metadata.chr_bank) #Let's do it here. Makes more sense to me.
        png = generate_png(frame) #Oww, I really wanted this code to be exactly in the middle. Well, let's move generate_png as closest to the top. Yay.
        png_path = f"{ROOT_DIR}/{character_name}/images"
        os.path.isdir(png_path) or os.makedirs(png_path) #I love that.
        png.save(f"{png_path}/{character_name}_frame_{i:03d}.png", "PNG")