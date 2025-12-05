import requests #Updating CreateAnims. Please wait...
import zipfile
import os
import subprocess
import tkinter
import threading
from tkinter import ttk

CHUNK_SIZE = 4096

def thread_download():
    with requests.get("https://github.com/VelpaChallenger/CreateAnims/releases/latest/download/CreateAnims.zip", stream=True) as request:
        download_bar['maximum'] = int(request.headers.get('Content-Length'))
        request.raise_for_status()
        with open("new_create_anims.zip", "wb") as new_create_anims_zip:
            for chunk in request.iter_content(chunk_size=CHUNK_SIZE):
                new_create_anims_zip.write(chunk)
                download_bar['value'] += CHUNK_SIZE
    root.after(10, post_download) #Looks hacky and maybe it is? But works. Destroy cannot happen in this thread as I originally thought but still gave it the try yeah now I know for sure.

def post_download():
    with zipfile.ZipFile("new_create_anims.zip", 'r') as zip_file:
        zip_file.extractall(".", members=(member for member in zip_file.namelist() if member != "CreateAnimsUpdater.exe")) #CreateAnimsUpdater is running. Don't extract it, you won't be able to.
    os.remove("new_create_anims.zip")
    subprocess.Popen("CreateAnims.exe") #With this, the updater closes and ends. #Also it has to be in this order, if you run destroy first, this never runs. Like priorities and such. #Nah it can happen in any order the important part is that the destroy doesn't happen in a thread.
    root.destroy()

root = tkinter.Tk()
root.geometry(f"+800+450")
root.wm_overrideredirect(True)

download_bar_label = tkinter.Label(root, text="Updating CreateAnims. Please wait...")
download_bar_label.pack(pady=10, padx=(0, 10), anchor="nw")
download_bar = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate', value=0, maximum=0)
download_bar.pack(pady=(0, 10), anchor="nw")
thread_download_object = threading.Thread(target=thread_download)
thread_download_object.start()

root.mainloop()