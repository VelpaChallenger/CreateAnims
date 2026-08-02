#This script can help to make PNG images out of frames.
#It's very similar to Character.py. It tries to do pretty much the same, but outside the context of CreateAnims, in a simplified environment.
#Currently unused. It supports 8x8 mode, to make it support 8x16 too, it pretty much needs the exact same code and acceses as CreateAnims, losing its stand-alone purpose. So leaving it here mostly for historical purposes.
#You believed that!!!!
#(it's still in use... reusing create_chr_images is way too expensive due to TileImage doing the bind, and adding an if and stuff kinda like... to begin with, there are enough differences in the logic so... I went with the current solution, a bit of all worlds.)

from PIL import Image
import os
from Character import Character #I changed my mind. Let's just import it. I was literally copypasting the exact same code, but without all the self and... no, let's just do this. It's separated, let's take advantage of that. Character per se has literally nothing to do with UI. So yeah.
from TileUtils import SYSTEM_PALETTE

ROOT_DIR = "../characters" #Still not really feeling like using os.sep.
tiles_images = [] #A new one. Doesn't contain TileImage in this context. But the pre_tkimg directly.

def refresh_chr(character, current_chr_bank, ypixels, sprites_8x16_mode, create_chr_image): #There's actually a lot that we need from CreateAnims. #But yes, importing Character already simplifies so much. I love it.
    tiles_images.clear() #Yeah whatever, here.
    chr_palette = character.chr_palettes[current_chr_bank]
    character_chr = character.chrs[current_chr_bank]
    create_chr_images(chr_palette, character_chr, ypixels, sprites_8x16_mode, create_chr_image)

def create_chr_images(chr_palette, character_chr, ypixels, sprites_8x16_mode, create_chr_image):
    tile_i = sprites_8x16_mode
    yincrement = ypixels // 16
    for row in range(8 // yincrement):
        for col in range(16):
            _, img, __ = create_chr_image(tile_i, chr_palette, character_chr, custom_background=0xE0)
            tiles_images.append(img)
            tile_i += yincrement

def generate_png(frame, ypixels, get_tile_image_i):
    png = Image.new("RGB", (16*frame.metadata.x_length, ypixels*frame.metadata.y_length), "white")
    initial_y = -ypixels
    cell_id = 0
    for row in range(frame.metadata.y_length):
        initial_x = 0
        initial_y += ypixels
        for col in range(frame.metadata.x_length):
            tile_id = frame.tiles[cell_id]
            if tile_id != 0xFF:
                pre_tkimg = tiles_images[get_tile_image_i(tile_id & 0x7F)]
                png.paste(pre_tkimg.resize((16, ypixels)), (initial_x, initial_y))
            else:
                pixels = [0x00] * 64 #Maybe I can create an image like this and just reference it? Not sure how'd that work but might be worth a try. #Fully transparent. This works as a fill.
                img = Image.frombytes("P", (8, 8), bytes(pixels)) #Same, doesn't break.
                tile_palette = [0xE0] * 12 #Like, just whatever. We won't use them.
                img.putpalette(tile_palette)
                pre_tkimg = img
                png.paste(pre_tkimg.resize((16, ypixels)), (initial_x, initial_y))
            initial_x += 16
            cell_id += 1
    return png #Yeah, the caller will decide how to use it, save it and stuff.

if __name__ == "__main__": #This is obviously gonna fail now.
    characters_name_list = os.listdir(ROOT_DIR)
    for character_name in characters_name_list:
        character = Character(ROOT_DIR, character_name) #There you go. Now it's completely decoupled from the UI component.
        for i, frame in enumerate(character.frames): #Now the magic starts.
            refresh_chr(character, frame.metadata.chr_bank) #Let's do it here. Makes more sense to me.
            png = generate_png(frame) #Oww, I really wanted this code to be exactly in the middle. Well, let's move generate_png as closest to the top. Yay.
            png_path = f"{ROOT_DIR}/{character_name}/images"
            os.path.isdir(png_path) or os.makedirs(png_path) #I love that.
            png.save(f"{png_path}/{character_name}_frame_{i:03d}.png", "PNG")