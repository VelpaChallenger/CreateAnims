import requests
import zipfile
import os
import subprocess

CHUNK_SIZE = 4096

with requests.get("https://github.com/VelpaChallenger/CreateAnims/releases/latest/download/create_anims.zip", stream=True) as request:
    #self.download_bar['maximum'] = int(request.headers.get('Content-Length'))
    request.raise_for_status()
    with open("new_create_anims.zip", "wb") as new_create_anims_zip:
        for chunk in request.iter_content(chunk_size=CHUNK_SIZE):
            new_create_anims_zip.write(chunk)
            #self.download_bar['value'] += CHUNK_SIZE

with zipfile.ZipFile("new_create_anims.zip", 'r') as zip_file:
    zip_file.extractall(".")

os.remove("new_create_anims.zip")

subprocess.Popen("create_anims.exe") #With this, the updater closes and ends.