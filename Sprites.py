from tkinter import messagebox

class Sprites:

    def __init__(self, createanims):
        self.createanims = createanims
        self.sprites_8x16_mode = 0

    @property
    def ypixels(self):
        if self.sprites_8x16_mode:
            return 32
        else:
            return 16

    def create_chr_image(self, tile_i, chr_palette, character_chr, custom_background=None):
        if self.sprites_8x16_mode:
            return self.createanims.tile_utils.create_chr_image_for_8x16(tile_i, chr_palette, character_chr, custom_background=custom_background)
        else:
            return self.createanims.tile_utils.create_chr_image_for_8x8(tile_i, chr_palette, character_chr, custom_background=custom_background)

    def get_tile_image_i(self, tile_i):
        if self.sprites_8x16_mode:
            return (tile_i-1) // 2
        else:
            return tile_i

    def get_tile_i(self, tile_image_i):
        if self.sprites_8x16_mode:
            return (tile_image_i*2) + 1
        else:
            return tile_image_i

    def validate_tile_id(self, cell_id, tile_id):
        if self.sprites_8x16_mode:
            if tile_id % 2 == 0:
                if not any(tile_image.in_motion for tile_image in self.createanims.tiles_images): #I hope you don't hate nesting. #Want context instead? Messageboxes showing up one on top of the other during motion.
                    messagebox.showwarning(title="Tile ID Mismatch!", message=f"You are in 8x16 mode, but the frame has an even-numbered tile ID. Tile ID {tile_id:02X} at cell {cell_id:02X} will be rounded up to {tile_id+1:02X}. IMPORTANT: Tile ID's high bit is not considered in any mode.")
                return tile_id+1
            return tile_id
        else:
            return tile_id