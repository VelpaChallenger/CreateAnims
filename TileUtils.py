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

    def __init__(self, createanims, palette_canvas, pal_rectangle, pal, pal_label):
        self.createanims = createanims
        self.palette_canvas = palette_canvas
        self.pal_rectangle = pal_rectangle #This is actually a literal int. Pretty cool. #Alternative name pal_rectangle_id to make it clear it's a literal int/ID.
        self.pal = pal
        self.pal_label = pal_label
        self.palette_canvas.tag_bind(self.pal_rectangle, "<Enter>", self.on_enter)
        self.palette_canvas.tag_bind(self.pal_rectangle, "<Button-1>", self.on_left_click)

    def on_enter(self, event=None):
        self.pal_label.config(text=f"Palette: {self.pal:02X}")

    def on_left_click(self, event=None):
        if self.createanims.current_pal_rectangle is not None:
            self.palette_canvas.itemconfig(self.createanims.current_pal_rectangle, outline="")
        self.palette_canvas.itemconfig(self.pal_rectangle, outline="red")
        self.createanims.current_pal_rectangle = self.pal_rectangle

class ColorPickerRectangle: #So like PalRectangle, but rectangles used for the color picker.

    def __init__(self, createanims, color_picker_canvas, color_picker_rectangle, pal, pal_label):
        self.createanims = createanims
        self.color_picker_canvas = color_picker_canvas
        self.color_picker_rectangle = color_picker_rectangle
        self.pal = pal
        self.pal_label = pal_label
        self.color_picker_canvas.tag_bind(self.color_picker_rectangle, "<Button-1>", self.on_left_click)

    def on_left_click(self, event=None):
        if self.createanims.current_color_picker_rectangle is not None:
            self.color_picker_canvas.itemconfig(self.createanims.current_color_picker_rectangle, outline="")
        self.color_picker_canvas.itemconfig(self.color_picker_rectangle, outline="blue")
        self.createanims.current_color_picker_rectangle = self.color_picker_rectangle

class TileUtils:

    def __init__(self, createanims):
        self.createanims = createanims

    def refresh_palette(self): #Show according to what's already stored, or, well yeah. Passing the index isn't my style. I think.
        palette = self.createanims.characters_palettes[self.createanims.current_character]
        initial_x = 0
        self.createanims.pal_rectangles = [] #So now I'm wondering how much I need init_state? Well it's more for stuff that needs an initial value because it won't be necessarily initialized at some other points, or it may be used at multiple points the first time. It's not the case here. This is meant to run the first time the UI starts. But there's a bit of randomness to it. Sometimes I just like to add stuff there to have it all in one place.
        for pal in palette:
            rgb_triplet = SYSTEM_PALETTE[pal]
            r, g, b = rgb_triplet[0], rgb_triplet[1], rgb_triplet[2]
            rgb = f"#{r:02X}{g:02X}{b:02X}"
            pal_rectangle = self.createanims.character_palette_canvas.create_rectangle(initial_x, 0, initial_x + 31, 31, fill=rgb, outline=rgb, width=1)
            self.createanims.pal_rectangles.append(PalRectangle(self.createanims, self.createanims.character_palette_canvas, pal_rectangle, pal, self.createanims.pal_label))
            initial_x += 32