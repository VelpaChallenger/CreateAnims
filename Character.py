CHARACTER_PALETTE_FILEPATH = "sub_zero.pal"

class Character:

    def __init__(self, character_name):
        self.palette = self.get_palette("subzero")

    def get_palette(self, name):
        with open(CHARACTER_PALETTE_FILEPATH, "rb") as character_pal:
            palette = list(character_pal.read())
        return palette