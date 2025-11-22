class EntryReturn:

    def __init__(self, createanims):
        self.createanims = createanims

    def chr_entry(self, event=None): #chr is reserved keyword and should not matter in this context but I still feel more comfortable, if not technically then aesthetically when I see chr_entry.
        chr_entry_value = self.createanims.chr_entry.get()
        if not chr_entry_value:
            self.createanims.chr_entry.configure(highlightcolor="red", highlightbackground="red")
            self.createanims.chr_info_text.configure(text="You haven't entered a CHR Bank number yet.", fg="red")
            return False
        if int(chr_entry_value) % 2 == 1: #Validation 4: number must be even. Though for this, it will have to be on enter, there's no other way to know the input is finished.
            self.createanims.chr_entry.configure(highlightcolor="red", highlightbackground="red")
            self.createanims.chr_info_text.configure(text="CHR Bank must be an even number.", fg="red")
            return False
        new_chr_bank = int(chr_entry_value)
        self.createanims.tile_utils.load_new_chr_bank(new_chr_bank) #New because it's not exactly the same thing we do on init. We don't display the text for example. Nor we care if the character has the CHR or not.

    def anim_entry(self, event=None):
        anim_entry_value = self.createanims.anim_entry.get()
        if not anim_entry_value:
            self.createanims.anim_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_anim = int(anim_entry_value)
        self.createanims.anim.load_new_anim(new_anim)

    def frame_entry(self, event=None):
        frame_entry_value = self.createanims.frame_entry.get()
        if not frame_entry_value:
            self.createanims.frame_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_frame = int(frame_entry_value)
        self.createanims.anim.load_new_frame(new_frame)

    def frame_id_entry(self, event=None):
        frame_id_entry_value = self.createanims.frame_id_entry.get()
        if not frame_id_entry_value:
            self.createanims.frame_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_frame_id = int(frame_id_entry_value)
        self.createanims.anim.load_new_frame_id(new_frame_id)

    def physics_id_entry(self, event=None):
        physics_id_value = self.createanims.physics_id_entry.get()
        if not physics_id_value:
            self.createanims.physics_id_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_physics_id = int(physics_id_value)
        self.createanims.anim.load_new_physics_id(new_physics_id)

    def physics_dialog_x_entry(self, event=None):
        physics_dialog_x_value = self.createanims.physics_dialog_x_entry.get()
        physics_dialog_y_value = self.createanims.physics_dialog_y_entry.get()
        if not physics_dialog_x_value or not physics_dialog_y_value or physics_dialog_x_value == "-" or physics_dialog_y_value == "-": #If any of them empty. #Or the negative sign was entered but without a number.
            self.createanims.physics_dialog.destroy() #Just interpret it as an X cross click.
            return False
        new_x_physics = (0x100 - abs(int(physics_dialog_x_value))) if physics_dialog_x_value.startswith("-") else int(physics_dialog_x_value) #Well it could also be + int, but, yeah. Also it looks like no need to abs of an int, can apply abs directly yey. Yay or yey was typo but yey. Ah actually no you can't, it's just I wasn't entering a negative so it never ran :p There now. #Oh wait. Not that simple you're right. I need to apply the inverse.
        new_y_physics = (0x100 - abs(int(physics_dialog_y_value))) if physics_dialog_y_value.startswith("-") else int(physics_dialog_y_value) #Aaaaaand, in case you're wondering! If you enter -0, it still works! Why? 0x100 - 0 will give 0x100. But then, in the physics grid, 0x100 - 0x100 = 0. Then -0. And it becomes just 0! But actually, it doesn't work! Because internally 0x100 is saved, so when you try to save the physics, it breaks.
        physics = self.createanims.physics_list[self.createanims.current_physics_id]
        old_x_physics = physics[2*self.createanims.physics_dialog_current_frame]
        old_y_physics = physics[(2*self.createanims.physics_dialog_current_frame) + 1]
        if (new_x_physics, new_y_physics) == (old_x_physics, old_y_physics): #Has to be exact match. If one of them is different, that's alright, it does count as UndoRedo.
            self.createanims.physics_dialog.destroy()
            return
        self.createanims.undo_redo.undo_redo([self.createanims.anim.load_new_physics_value, self.createanims.physics_dialog_current_frame, old_x_physics, old_y_physics], [self.createanims.anim.load_new_physics_value, self.createanims.physics_dialog_current_frame, new_x_physics, new_y_physics])

    def x_offset_entry(self, event=None):
        x_offset_value = self.createanims.x_offset_entry.get()
        if not x_offset_value or x_offset_value == "-": #Same.
            self.createanims.x_offset_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_x_offset = int(x_offset_value)
        self.createanims.anim.load_new_x_offset(new_x_offset)

    def y_offset_entry(self, event=None):
        y_offset_value = self.createanims.y_offset_entry.get()
        if not y_offset_value or y_offset_value == "-": #Same.
            self.createanims.y_offset_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_y_offset = int(y_offset_value)
        self.createanims.anim.load_new_y_offset(new_y_offset)

    def width_entry(self, event=None):
        width_value = self.createanims.width_entry.get()
        if not width_value:
            self.createanims.width_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_width = int(width_value)
        self.createanims.anim.load_new_width(new_width)

    def height_entry(self, event=None):
        height_value = self.createanims.height_entry.get()
        if not height_value:
            self.createanims.height_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_height = int(height_value)
        self.createanims.anim.load_new_height(new_height)

    def character_entry(self, event=None):
        character_entry_value = self.createanims.character_entry.get()
        if not character_entry_value:
            self.createanims.character_entry.configure(highlightcolor="red", highlightbackground="red")
            return False
        new_character = int(character_entry_value)
        self.createanims.anim.load_new_character(new_character)