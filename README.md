# CREATEANIMS: To make creating animations easier and smoother.

CreateAnims is a tool that was originally intended to be used for creating animations in MK3 Arkade Edition, but it has been written in a way that can be easily extendable to other games as well. Here's some of the features it supports (you can check the docs in README.html for further details):

- Playing animations
- Editing physics (add, remove, modify)
- Update palette of characters
- Update frames of animation
- Save individual changes
- Save changes automatically
- Import files (all files .chr, .chr.pal, .frame, .anim, .pal, .physics supported)
- Undo and redo of every action
- Switch branch of undo and redo (this is one of my most emotional ones, I love it and I wish more tools had it, I made it exactly because of that wish).
- Log History (to show every single action you've taken)
- Customization of frame drawing (you can toggle transparency, blue rectangles indicating empty $FF tiles and the red rectangle surrounding the frame)
- Frame modification (you can modify tiles in the frame, adjust width, height and offsets)
- CHR palette toggle (you can drag and automatically toggle palette for lots of tiles)

## HOW DOES IT WORK (in a nutshell)

This is a bit of internals in a nutshell. It divides every possible data type: .chr, .chr.pal, .frame, .anim, .pal, .physics. Then it loads those based on MK3's format (for now only MK3 is supported but with a few changes and a dropdown or some setting to change the expected format it could support more). As you do changes, it keeps track of the affected files and then when you're done with your changes, you can save them and it will overwrite the files (you will get a summary of what will be overwritten and will be asked to confirm this is what you want to do). You can also save changes individually, in which case it will just save the current state of the character to whatever file you choose (can be helpful if you want to keep temporary changes saved somewhere for example, but you still don't want them in the ROM).

It is up to the user to generate the corresponding data files, though I have some disassembly scripts that might help if you want to do that.

For new data (new physics, frames or anims), it will also be up to the user how to include those in the ROM (you will have to search free space, update pointers tables etc. etc.).

## HOW TO BUILD FROM SOURCE

This is more for people interested in doing changes in the source or stuff like that, not really meant for people other than programmers. But, you will need either
PyInstaller and pass create_anims.spec if you want to create another executable, or Python along with Pillow to be able to build without an executable.