class UndoRedo:

    def __init__(self, createanims): #The classics. Every component always has access to CreateAnims.
        self.createanims = createanims
        self.stack = [[None]] #Let's go with a list to start. #It starts with None because first is always undo, but there's nothing to undo, yet we need the space for the redo to work.
        self.stack_ptr = 0 #Our index. Where are we in the stack?

    def undo(self, event=None): #func is the function, *args the arguments of said function. They can be of variable length, that will depend on the specific function.
        undo = self.stack[self.stack_ptr][0] #node = stack[stack_ptr] #This was the thing. This doesn't return the undo per se, it returns the node.
        undo[0](*undo[1:]) #So now, node[0] is undo data. Therefore node[0][0] is func, node[0][1] is args. #And the args.
        self.stack_ptr -= 1 #We went backwards one step.
        self.decide_undo_redo_status()

    def redo(self, event=None): #This doesn't take arguments actually.
        redo = self.stack[self.stack_ptr][1] #Funny. For redo I had indeed done it this way. Though it's 1 (there was 0 zero).
        redo[0](*redo[1:])
        self.stack_ptr += 1 #We advanced one step.
        self.decide_undo_redo_status()

    def undo_redo(self, undo, redo): #When you perform an action... ah right, the same function is going to be called. So there are a few details to keep in mind. I got this. #Yeah maybe, the function that we pass is not recursive, that is, we create an additional layer. Looks like huge work, but it could work pretty good. It seems reasonable yet at this stage. And if not, perhaps it could be automated somehow. You know, like moving directories and stuff like that. I don't see it very often but that doesn't mean it can't be done. I think it works very well in a lot of situations. Let's do this.
        self.stack[self.stack_ptr].append(redo) #Here we do want an append. #Where we are, add the redo.
        redo[0](*redo[1:]) #And, very important, do perform the action.
        self.stack_ptr += 1
        self.stack.append([]) #stack[stack_ptr] = [] #By definition of undo_redo (called for new actions), this will be empty. Won't have anything.
        self.stack[self.stack_ptr].append(undo) #It really has to be an append. #It's an extend, otherwise it creates a list inside the list. #And where we are after the changes, add the undo.
        self.decide_undo_redo_status()

    def decide_undo_redo_status(self): #True! I won't be able to reuse this exact same class. But I don't care.
        if self.stack_ptr == len(self.stack) - 1:
            self.createanims.edit_menu.entryconfigure("Redo", state="disabled")
        else:
            self.createanims.edit_menu.entryconfigure("Redo", state="normal")
        if self.stack_ptr == 0:
            self.createanims.edit_menu.entryconfigure("Undo", state="disabled")
        else:
            self.createanims.edit_menu.entryconfigure("Undo", state="normal")