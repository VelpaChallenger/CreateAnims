function_name_translation_dict = { #Given a function name, what will we show in the UI?
    "load_new_anim_value": ("Navigated anim", "Navigation"), #I like the idea. Have a setting that shows both navigation and changes, and another that shows only changes, stuff like that.
    "load_new_frame_value": ("Navigated frame in anim", "Navigation"),
    "load_new_frame_id_value": ("Changed frame ID in frame in anim", "Change"), #This could be a nice scenario for format strings but not the f ones, the ones that allow for replacing/formatting later on.
}

class UndoRedo:

    def __init__(self, createanims): #The classics. Every component always has access to CreateAnims.
        self.createanims = createanims
        self.stack = [[None]] #Let's go with a list to start. #It starts with None because first is always undo, but there's nothing to undo, yet we need the space for the redo to work.
        self.stack_ptr = 0 #Our index. Where are we in the stack?
        self.stack_copy = None #We'll use this to know whether we can actually switch branches.
        self.stack_copy_ptr = 0
        self.last_saved_ptr = 0
        self.trace = []
        self.amount_changes = 0 #Also, to understand why/how it works, think of it as a ptr of sorts. It makes it a lot easier to understand. #Not anymore! I never liked it in the first place. I like this a lot more. #self.unsaved_changes = False #We'll use this instead because we need to differentiate changes from navigation. I still think that, maybe, it would be better to have two completely different implementations, and that UndoRedo only refers to changes. But I'm not fully convinced of the implications at UI level, experience and whatnot. So I'm giving a try to this approach.
        self.saved = False #True, I agree. Those are different things. self.strack_ptr I mean self.stack_ptr == 0 doesn't imply not saved, and != 0 doesn't imply saved. Saved is something that literally means that: a save happened. It is not related to the stack_ptr. In other words, yes, after you save, you can have either Unsaved changes or Saved, meaning there was at least one save.

    def switch_branch_undo_redo(self, event=None):
        if self.createanims.edit_menu.entrycget(2, 'state') == "disabled": #Won't use it after all. It still works. #If in physics_window, we won't care about that status. #Same, we'll check the status. #self.stack_copy is None: #We won't call undo. Undo will always pass parameters doing things its own way. We'll do things our way, so we'll have it in a different function here.
            return
        aux_refresh_UI = self.createanims.refresh_UI #Everything in Python is an object, so this works like butter. Or like... I mean butter is fine.
        aux_anim_fill_physics_grid = self.createanims.anim.fill_physics_grid
        self.createanims.anim.fill_physics_grid = lambda : None
        self.createanims.refresh_UI = lambda : None #Just don't do anything. For now.
        init_physics_window_flag = False
        destroy_physics_window_flag = False
        while self.stack_ptr != self.stack_copy_ptr:
            undo = self.stack[self.stack_ptr][0]
            if undo[0].__name__ == "init_physics_window": #How about this huh? Do you like it? You want some init, I'll give you some init! #self.createanims.init_physics_window = lambda : None #I guess maybe there is some sort of copy being used? Well no matter. I have more tricks under my sleeve.
                init_physics_window_flag = True
                destroy_physics_window_flag = False
            elif undo[0].__name__ == "destroy_physics_window":
                init_physics_window_flag = False
                destroy_physics_window_flag = True #You might think this is redundant, but it's not. What if the init_physics_window_flag was in False because of the default? How can you distinguish and disambiguate between the two scenarios? flag in False because of a destroy, or because of a default? This one unties (or breaks the tie).
            else:
                undo[0](*undo[1:])
            self.stack_ptr -= 1 #Come to think of it, with the new approach of partially switching refresh_UI, I could use undo. Meh. Still, I wouldn't want to call decide_undo_redo_status.
            function_undo = undo[0]
            undo_type = self.get_function_type(function_undo) #Done, I love it. #I might encapsulate this in a method yeah. get_function_type. It can Unknown, Navigation or Change. Beautiful.
            if undo_type == "Change":
                self.amount_changes -= 1
        if self.createanims.in_physics_window:
            init_physics_window_flag = False #Even if the algorithm says 'True'. (I mean the chain of Undo in the stack). If anything, we may have to destroy, but never init if we're already in physics window.
        self.createanims.refresh_UI = aux_refresh_UI #Sweet, smooth like cheese! Am I hungry maybe?
        self.createanims.anim.fill_physics_grid = aux_anim_fill_physics_grid
        aux_stack = self.stack[:]
        self.stack = self.stack_copy[:] #Now you can redo again as you please, yayyyyy.
        self.stack_copy = aux_stack #Otherwise stack_copy would be overwritten before its time. Also ptrs are fine at this point so I'm not touching them.
        self.createanims.refresh_UI() #Do call it now to draw with all the latest updates.
        self.decide_undo_redo_status() #I do need to call it at this point otherwise I won't be able to redo in the new branch which is the whole point.
        if self.createanims.in_physics_window and not init_physics_window_flag:
            self.createanims.anim.fill_physics_grid() #So, don't draw it (don't init) but do update it because we're currently there. And well actually, to avoid doing it twice, only do it if flag was False.
        if destroy_physics_window_flag:
            self.createanims.destroy_physics_window()
        if init_physics_window_flag:
            self.createanims.init_physics_window() #Always, always at the end.

    def copy_undo_redo(self): #We'll need a dedicated function. Let's do this. #Future me/someone I don't know asks details? copy.deepcopy doesn't work because Tkinter objects cannot be pickled. And we pretty much need that. Otherwise, the stack gets corrupted at self.stack[self.stack_ptr] due to the last pop and reinsertion before we jump back to the previous branch. So 5-10-15-20 then 5-8-11, you go back, now you get 5-8-15-20. Not what we want.
        anim_undo_redo_list = [] #Brand.
        for undo_redo in self.stack:
            anim_undo_redo_list.append(undo_redo[:])
        return anim_undo_redo_list

    def undo(self, event=None): #func is the function, *args the arguments of said function. They can be of variable length, that will depend on the specific function.
        if self.createanims.edit_menu.entrycget(0, 'state') == "disabled": #I prefer it this way really. If you can't do it from the UI, you shouldn't be able to do it with a keyboard shortcut either. This will be our common source in our case. #self.stack_ptr == 0: #Nothing to undo.
            return
        undo = self.stack[self.stack_ptr][0] #node = stack[stack_ptr] #This was the thing. This doesn't return the undo per se, it returns the node.
        function_undo = undo[0]
        undo_type = self.get_function_type(function_undo) #Done, I love it. #I might encapsulate this in a method yeah. get_function_type. It can Unknown, Navigation or Change. Beautiful.
        if undo_type == "Change":
            self.amount_changes -= 1
        self.stack_ptr -= 1 #We went backwards one step.
        self.decide_undo_redo_status()
        undo[0](*undo[1:]) #So now, node[0] is undo data. Therefore node[0][0] is func, node[0][1] is args. #And the args.

    def redo(self, event=None): #This doesn't take arguments actually.
        if self.createanims.edit_menu.entrycget(1, 'state') == "disabled":
            return
        redo = self.stack[self.stack_ptr][1] #Funny. For redo I had indeed done it this way. Though it's 1 (there was 0 zero).
        function_redo = redo[0]
        redo_type = self.get_function_type(function_redo)
        if redo_type == "Change":
            self.amount_changes += 1
        self.stack_ptr += 1 #We advanced one step.
        self.decide_undo_redo_status()
        redo[0](*redo[1:])

    def undo_redo(self, undo, redo): #When you perform an action... ah right, the same function is going to be called. So there are a few details to keep in mind. I got this. #Yeah maybe, the function that we pass is not recursive, that is, we create an additional layer. Looks like huge work, but it could work pretty good. It seems reasonable yet at this stage. And if not, perhaps it could be automated somehow. You know, like moving directories and stuff like that. I don't see it very often but that doesn't mean it can't be done. I think it works very well in a lot of situations. Let's do this.
        if len(self.stack[self.stack_ptr]) == 2: #This needs to happen first, otherwise self.stack already lost its previous state. #Oh well whatever. Pop only returns default None for dictionaries, not for lists.
            self.stack_copy = self.copy_undo_redo() #self.stack[:] #And this also needs to happen first, before we pop. #We'll need this for the switch_branch_undo_redo functionality feature. #But only do it if a different branch was created. Seems clearer to me that way (I don't think there are performance differences).
            self.stack_copy_ptr = self.stack_ptr
            self.stack[self.stack_ptr].pop(1) #If there is currently a redo, remove it. There are no more references to old data.
        function_redo = redo[0]
        function_type = self.get_function_type(function_redo)
        if function_type == "Change": #I love this.
            self.amount_changes += 1
        self.stack = self.stack[:self.stack_ptr+1] #Clear all the redo.
        self.stack[self.stack_ptr].append(redo) #Here we do want an append. #Where we are, add the redo.
        self.stack_ptr += 1
        self.stack.append([]) #stack[stack_ptr] = [] #By definition of undo_redo (called for new actions), this will be empty. Won't have anything.
        self.stack[self.stack_ptr].append(undo) #It really has to be an append. #It's an extend, otherwise it creates a list inside the list. #And where we are after the changes, add the undo.
        self.decide_undo_redo_status()
        redo[0](*redo[1:]) #And, very important, do perform the action.

    def decide_undo_redo_status(self): #True! I won't be able to reuse this exact same class. But I don't care.
        if self.stack_ptr == len(self.stack) - 1:
            self.createanims.edit_menu.entryconfigure("Redo", state="disabled")
        else:
            self.createanims.edit_menu.entryconfigure("Redo", state="normal")
        if self.stack_ptr == 0:
            self.createanims.edit_menu.entryconfigure("Undo", state="disabled")
        else:
            self.createanims.edit_menu.entryconfigure("Undo", state="normal")
        if self.stack_copy is None or self.stack_ptr < self.stack_copy_ptr: #If we're behind, we don't have any common base. Yeah like merge base. Technically the merge base would be the very start but that's not point of the feature. The point is, I was redoing stuff, and accidentally clicked something, pressed something. Oh no! I lost my work! Nope, don't panic! Switch branches. There you go! You've recovered your work!
            self.createanims.edit_menu.entryconfigure("Switch UndoRedo branch", state="disabled")
        else:
            self.createanims.edit_menu.entryconfigure("Switch UndoRedo branch", state="normal")
        if self.amount_changes: # != 0. The beauty that negative numbers are also considered True.
            self.createanims.root.title("Create Anims - Unsaved changes") #print(self.createanims.root.title()) I was going to use .title() to get the current title and then append to that, I could also use a constant but, let's go with this. I will tell if the title at some point changes to maybe CreateAnims and after redoing something or undoing it won't match so I'll just come update it here.
        elif not self.saved:
            self.createanims.root.title("Create Anims")
        else:
            self.createanims.root.title("Create Anims - Saved")

    def get_function_type(self, function):
        name_UI = function_name_translation_dict.get(function.__name__, function.__name__)
        if name_UI == function.__name__:
            function_type = "Unknown"
        elif name_UI[1] == "Navigation":
            function_type = "Navigation"
        elif name_UI[1] == "Change": #I know, those could be constants.
            function_type = "Change"
        return function_type #I know, there's no else. In this case, the only way this would break is if instead of Navigation we typed Navigationn for example, or if we forgot to add a new type. But it will break immediately due to function_type not defined. I will tell right away. That is exactly what I want.