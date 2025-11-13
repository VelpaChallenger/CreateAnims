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

    def character_left_arrow_button(self, event=None):
        new_character = self.createanims.current_character - 1
        self.createanims.anim.load_new_character(new_character)

    def character_right_arrow_button(self, event=None):
        new_character = self.createanims.current_character + 1
        self.createanims.anim.load_new_character(new_character)

    def play_anim_button(self, event=None):
        import tkinter
        self.createanims.current_frame_aux = self.createanims.current_frame
        self.createanims.anim.generate_png_from_anim_frames(self.createanims.characters[self.createanims.current_character]) #From the frames in the anim.
        self.createanims.in_play_anim = True
        self.createanims.play_anim_button.configure(state="disabled")
        self.createanims.stop_anim_button.configure(state="normal")
        self.createanims.anim_canvas.delete('all')
        self.createanims.anim.disable_all()
        self.createanims.tile_utils.disable_all()
        self.createanims.play_anim_label = tkinter.Label(self.createanims.anim_canvas, bd=0)
        self.play_anim()

    def play_anim(self, event=None): #The one that runs over and over. Then the init code runs only once. Alternative is to create StringVar and then trace and pass this. But you still get two functions. I like more this.
        import tkinter
        if not self.createanims.in_play_anim:
            return #And the chain stops.
        self.createanims.png_img.clear()
        character = self.createanims.characters[self.createanims.current_character]
        frame_id = character.anims[self.createanims.current_anim].frame_ids[self.createanims.current_frame]
        img = tkinter.PhotoImage(file=f"{self.createanims.root_dir}/{character.name}/images/{character.name}_frame_{frame_id:03d}.png") #(self.createanims.tiles_images[0].pre_tkimg.resize((16, 16)))
        self.createanims.png_img.append(img) #Say no to garbage collection of PhotoImage.
        frame = character.frames[frame_id]
        self.createanims.play_anim_label.place(x=375+(frame.metadata.x_offset*2), y=200 - (frame.metadata.y_offset*2) - (16*frame.metadata.y_length))
        self.createanims.play_anim_label.configure(image=img)
        if self.createanims.current_frame == len(character.anims[self.createanims.current_anim].frame_ids) - 1:
            self.createanims.current_frame = 0
        else:
            self.createanims.current_frame += 1
        self.createanims.root.after(47, self.play_anim) #I think 47 is the magical number. Looks really, really good.

    def stop_anim_button(self, event=None):
        self.createanims.anim.enable_all()
        self.createanims.tile_utils.enable_all()
        self.createanims.play_anim_label.destroy()
        self.createanims.anim.load_new_character(self.createanims.current_character, new_frame=self.createanims.current_frame_aux) #For now, but the idea is to save whatever frame was active when the anim was started. Then restore that. So load_new_frame and that frame. Anim will be the same, cannot be changed during playing since it's all disabled.
        self.createanims.play_anim_button.configure(state="normal")
        self.createanims.stop_anim_button.configure(state="disabled")
        self.createanims.in_play_anim = False