import requests #Updating CreateAnims. Please wait...
import zipfile
import os
import subprocess
import tkinter
import threading
from tkinter import ttk, messagebox

CHUNK_SIZE = 4096

def thread_download():
    try:
        with requests.get("https://github.com/VelpaChallenger/CreateAnims/releases/latest/download/CreateAnims.zip", stream=True) as request:
            download_bar['maximum'] = int(request.headers.get('Content-Length'))
            request.raise_for_status()
            with open("new_create_anims.zip", "wb") as new_create_anims_zip:
                for chunk in request.iter_content(chunk_size=CHUNK_SIZE):
                    new_create_anims_zip.write(chunk)
                    download_bar['value'] += CHUNK_SIZE
    except requests.exceptions.ConnectionError:
        messagebox.showerror(title="Unable to download update", message="Unable to download update. Please confirm you have an stable internet connection.")
        root.after(10, cancel_download)
        return
    except requests.exceptions.HTTPError:
        messagebox.showerror(title="Unable to download update", message="Unable to download update. GitHub might be down, or the updater is old enough that the download URL is no longer valid. Please consider downloading directly from CreateAnims repo.") #I remember all the times I read stuff like this, what do you mean I don't have an STABLE internet connection, it's more stable than you are you...!! lol. Oh this is a comment right? Which means other people are gonna read it? I mean. Whatever.
        root.after(10, cancel_download)
        return
    except Exception as e:
        messagebox.showerror(title="Unable to download update", message=f"Unable to download update. Unknown exception: {e}")
        root.after(10, cancel_download)
        return
    root.after(10, post_download) #Looks hacky and maybe it is? But works. Destroy cannot happen in this thread as I originally thought but still gave it the try yeah now I know for sure.

def post_download():
    try:
        with zipfile.ZipFile("new_create_anims.zip", 'r') as zip_file:
            zip_file.extractall(".", members=(member for member in zip_file.namelist() if member != "CreateAnimsUpdater.exe")) #CreateAnimsUpdater is running. Don't extract it, you won't be able to.
    except PermissionError as e:
        messagebox.showerror(title="Unable to extract files", message=f"Unable to extract files. Exception details: {e}. Please avoid opening files while the update is in progress.") #I remember all the times I read stuff like this, what do you mean I don't have an STABLE internet connection, it's more stable than you are you...!! lol. Oh this is a comment right? Which means other people are gonna read it? I mean. Whatever.
        root.destroy() #We're no longer in the thread.
        return
    except Exception as e:
        messagebox.showerror(title="Unable to extract files", message=f"Unable to extract files. Unknown exception: {e}.")
        root.destroy() #We're no longer in the thread.
        return
    try: #Let's make it as robust as possible from the beginning, so that we don't have to make changes to it except for IDs changing and stuff like that, and we'll be able to inform them.
        os.remove("new_create_anims.zip")
    except Exception as e:
        messagebox.showerror(title="Unable to remove downloaded zip", message=f"Unable to remove downloaded zip. Unknown exception: {e}.")
        root.destroy() #We're no longer in the thread.
        return
    try:
        subprocess.Popen("CreateAnims.exe") #With this, the updater closes and ends. #Also it has to be in this order, if you run destroy first, this never runs. Like priorities and such. #Nah it can happen in any order the important part is that the destroy doesn't happen in a thread.
    except Exception as e:
        messagebox.showerror(title="Unable to reopen CreateAnims", message=f"Unable to reopen CreateAnims. Unknown exception: {e}.")
        root.destroy() #We're no longer in the thread.
        return
    root.destroy()

def cancel_download():
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