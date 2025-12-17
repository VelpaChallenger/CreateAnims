class FileFormatValidator: #Why a class? At a module level, it feels like it'd complicate imports. Specially when refreshing with a different format. I'm leaving that for far later but I'd still like to write it with that in mind.

    def __init__(self, createanims):
        self.createanims = createanims
        self.OFFSET_WIDTH = 0
        self.OFFSET_HEIGHT = 1
        self.OFFSET_X_OFFSET = 2
        self.OFFSET_CHR_BANK = 3
        self.OFFSET_Y_OFFSET = 4
        self.OFFSET_SPECIAL_PALETTE_ID = 5
        self.OFFSET_START_TILES = 6

    def validate_palette_length(self, pal_bytes):
        return len(pal_bytes) == 8

    def validate_palette_values(self, pal_bytes):
        return all([pal_byte <= 0x3F for pal_byte in pal_bytes])

    def validate_chr(self, chr_bytes):
        return len(chr_bytes) == 2048

    def validate_chr_pal(self, chr_pal_bytes):
        return len(chr_pal_bytes) == 16

    def validate_frame_minimum_bytes(self, frame_bytes): #Structured this way so that later we can just call this and caller can still add custom responses depending on what failed specifically vs 'just failed'.
        return len(frame_bytes) >= 7

    def validate_frame_total_tiles(self, frame_bytes):
        width = frame_bytes[self.OFFSET_WIDTH] #You might think, this shouldn't be frame_bytes[0], this should be FrameBytesObject.width or something. But no, this is exactly what I want. If I add new formats, that will have to be added here. In fact, I might need different FileFormat. And it will still be all encapsulated here. Here will be the expected offsets and all. It's great. In fact, when you think about it this way, perhaps, each Anim, Frame etc. should have its own component FileFormatValidator which does the bytes assignment. Right now how I'd handle it is a separate class also. But yeah it would still be two code, one for validation of offsets and another for setting them.
        height = frame_bytes[self.OFFSET_HEIGHT] #But I guess... yes, I could also assign those, then do the comparison and leave them but, what about the import? We don't create the object in that case. So this is fine. #Besides yeah that's the point. Validate first, and set later. I get the point about offsets being duplicated and then if it was all in the same class the offsets could be part of attributes but... and yeah they could be custom for each format... I would still need again two changes, one validation, one for setting, the only difference is that I wouldn't have the numbers directly.
        tiles = frame_bytes[self.OFFSET_START_TILES:] #Won't be just one return. Some will, some won't. All the logic encapsulated here. This was actually the reason why I finally created FileFormatValidator.
        return len(tiles) == (width*height)

    def validate_frame_width(self, frame_bytes):
        return 1 <= frame_bytes[self.OFFSET_WIDTH] <= 60

    def validate_frame_height(self, frame_bytes):
        return 1 <= frame_bytes[self.OFFSET_HEIGHT] <= 60

    def validate_anim(self, anim_bytes):
        return len(anim_bytes) >= 2

    def validate_physics_terminator(self, physics):
        return physics[len(physics) - 1] == 0x80

    def validate_physics_parity(self, physics):
        return len(physics) % 2 == 1