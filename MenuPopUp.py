
class MenuPopUp:

    def __init__(self, createanims):
        self.createanims = createanims

    def create_pop_up(self, menu, event): #Everything is a creation in here.
        menu.tk_popup(event.x_root, event.y_root, 0)

    def frame_entry_insert(self):
        frame_ids = self.createanims.characters[self.createanims.current_character].anims[self.createanims.current_anim].frame_ids
        if len(frame_ids) == 60:
            self.createanims.anim_info_text.configure(text="Won't insert. Too many frames.", fg="red")
            return
        frame_index = self.createanims.current_frame
        new_frame_index = frame_index + 1 #Even if at maximum, it doesn't matter. Will be new entry.
        self.createanims.undo_redo.undo_redo([self.createanims.anim.remove_frame_value, new_frame_index], [self.createanims.anim.insert_frame_value, new_frame_index])

    def frame_entry_remove(self):
        frame_ids = self.createanims.characters[self.createanims.current_character].anims[self.createanims.current_anim].frame_ids
        if len(frame_ids) == 1:
            self.createanims.anim_info_text.configure(text="If this frame is removed, the anim would have no frames. Impossible.", fg="red")
            return
        frame_index = self.createanims.current_frame
        self.createanims.undo_redo.undo_redo([self.createanims.anim.insert_frame_value, frame_index], [self.createanims.anim.remove_frame_value, frame_index])