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

    def get_tile_index_for_chr_pal(self, tile_i):
        if self.sprites_8x16_mode:
            return tile_i*2 + 1
        else:
            return tile_i

    def get_tile_index_for_pixels(self, tile_i):
        if self.sprites_8x16_mode:
            return tile_i*2
        else:
            return tile_i