class CreateAnimsButton:

    def __init__(self, createanims):
        self.createanims = createanims

    def chr_left_arrow_button(self, event=None):
        new_chr_bank = self.createanims.current_chr_bank - 2
        self.createanims.tile_utils.load_new_chr_bank(new_chr_bank)

    def chr_right_arrow_button(self, event=None):
        new_chr_bank = self.createanims.current_chr_bank + 2
        self.createanims.tile_utils.load_new_chr_bank(new_chr_bank)

    def frame_id_left_arrow_button(self, event=None):
        new_frame_id = self.createanims.current_frame_id - 1
        self.createanims.anim.load_new_frame_id(new_frame_id)

    def frame_id_right_arrow_button(self, event=None):
        new_frame_id = self.createanims.current_frame_id + 1
        self.createanims.anim.load_new_frame_id(new_frame_id)

    def frame_left_arrow_button(self, event=None):
        new_frame = self.createanims.current_frame - 1
        self.createanims.anim.load_new_frame(new_frame)

    def frame_right_arrow_button(self, event=None):
        new_frame = self.createanims.current_frame + 1
        self.createanims.anim.load_new_frame(new_frame)

    def anim_left_arrow_button(self, event=None): #Only probably. #Probably for next commit: invert order so that it's always anim, frame and then frame ID.
        new_anim = self.createanims.current_anim - 1
        self.createanims.anim.load_new_anim(new_anim)

    def anim_right_arrow_button(self, event=None):
        new_anim = self.createanims.current_anim + 1
        self.createanims.anim.load_new_anim(new_anim)

    def physics_id_left_arrow_button(self, event=None):
        new_physics_id = self.createanims.current_physics_id - 1
        self.createanims.anim.load_new_physics_id(new_physics_id)

    def physics_id_right_arrow_button(self, event=None):
        new_physics_id = self.createanims.current_physics_id + 1
        self.createanims.anim.load_new_physics_id(new_physics_id)

    def x_offset_left_arrow_button(self, event=None):
        current_x_offset = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.x_offset #This will be different.
        new_x_offset = current_x_offset - 1
        self.createanims.anim.load_new_x_offset(new_x_offset)

    def x_offset_right_arrow_button(self, event=None):
        current_x_offset = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.x_offset
        new_x_offset = current_x_offset + 1
        self.createanims.anim.load_new_x_offset(new_x_offset)

    def y_offset_left_arrow_button(self, event=None):
        current_y_offset = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.y_offset #This will be different.
        new_y_offset = current_y_offset - 1
        self.createanims.anim.load_new_y_offset(new_y_offset)

    def y_offset_right_arrow_button(self, event=None):
        current_y_offset = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.y_offset
        new_y_offset = current_y_offset + 1
        self.createanims.anim.load_new_y_offset(new_y_offset)

    def width_left_arrow_button(self, event=None):
        current_width = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.x_length #This will be different.
        new_width = current_width - 1
        self.createanims.anim.load_new_width(new_width)

    def width_right_arrow_button(self, event=None):
        current_width = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.x_length
        new_width = current_width + 1
        self.createanims.anim.load_new_width(new_width)

    def height_left_arrow_button(self, event=None):
        current_height = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.y_length #This will be different.
        new_height = current_height - 1
        self.createanims.anim.load_new_height(new_height)

    def height_right_arrow_button(self, event=None):
        current_height = self.createanims.characters[self.createanims.current_character].frames[self.createanims.current_frame_id].metadata.y_length
        new_height = current_height + 1
        self.createanims.anim.load_new_height(new_height)

    def character_left_arrow_button(self, event=None):
        new_character = self.createanims.current_character - 1
        self.createanims.anim.load_new_character(new_character)

    def character_right_arrow_button(self, event=None):
        new_character = self.createanims.current_character + 1
        self.createanims.anim.load_new_character(new_character)

    def play_anim_button(self, event=None):
        import tkinter
        self.createanims.current_frame_aux = self.createanims.current_frame
        self.createanims.anim.restart_physics() #Encapsulated here.
        self.createanims.anim.generate_png_from_anim_frames(self.createanims.characters[self.createanims.current_character]) #From the frames in the anim.
        self.createanims.in_play_anim = True
        self.createanims.play_anim_button.configure(state="disabled")
        self.createanims.stop_anim_button.configure(state="normal")
        self.createanims.anim_canvas.delete('all')
        self.createanims.anim.disable_all()
        self.createanims.tile_utils.disable_all()
        self.createanims.play_anim_label = tkinter.Label(self.createanims.anim_canvas, bd=0)
        self.createanims.anim.play_anim()

    def stop_anim_button(self, event=None):
        self.createanims.anim.enable_all()
        self.createanims.tile_utils.enable_all()
        self.createanims.play_anim_label.destroy()
        self.createanims.anim.load_new_character(self.createanims.current_character, new_frame=self.createanims.current_frame_aux) #For now, but the idea is to save whatever frame was active when the anim was started. Then restore that. So load_new_frame and that frame. Anim will be the same, cannot be changed during playing since it's all disabled.
        self.createanims.play_anim_button.configure(state="normal")
        self.createanims.stop_anim_button.configure(state="disabled")
        self.createanims.in_play_anim = False

    def edit_physics_button(self, event=None):
        self.createanims.init_physics_window() #All UI related is always CreateAnims.