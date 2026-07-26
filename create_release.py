import subprocess
import zipfile
import shutil
import os

TARGET_FOLDER = "dist"
ZIP_NAME = "CreateAnims.zip"
RELEASE_NOTES = "release-notes.md"

#Validation 1: Working tree must be clean. #(I'm really liking this format of validations via comments.)
git_status_porcelain_subprocess = subprocess.Popen("git status --porcelain", shell=True, stdout=subprocess.PIPE) #Exactly, exactly what we need.
working_tree_contents = git_status_porcelain_subprocess.stdout.readline().strip().decode("ascii")
if working_tree_contents: #i.e. it is not clean.
    print("The working tree is not empty (clean). I cannot continue with your request of building CreateAnims. Please, revise and let me know.") #This is intended for me so yeah print to the console.
    exit(999) #After Tkinter's experience, I'm kinda preferring using sys. Ah but wait. This is pure Python so arghh... whatever, like the old times.

git_hash_subprocess = subprocess.Popen("git log -1 --format=%H", shell=True, stdout=subprocess.PIPE)
git_hash = git_hash_subprocess.stdout.readline().strip().decode("ascii") #subprocess returns the bytes and then you need to know what to expect and decode it accordingly.
git_short_hash = git_hash[0:8]

#Validation 2: commit must be associated to a tag. Included here because, well, we need to calculate the hash first. Won't do all that for trickery and stuff to get output from git rev-parse HEAD and such.
git_tag_subprocess = subprocess.Popen(f"git describe --tags --exact-match {git_hash}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = git_tag_subprocess.communicate()
if git_tag_subprocess.returncode != 0:
    print("The commit is not associated to any tag. Please create a tag and try again.")
    exit(999)
version = stdout.strip().decode('ascii')

from datetime import datetime, timezone
datetime_object = datetime.now(timezone.utc) #I'm liking the _object suffix.
version_date = datetime_object.strftime("%b %d, %Y")

#Preprocessing starts here.
with open("rinfo.py", "w") as temp_rinfo:
    temp_rinfo.write(f"#Release info.\n")
    temp_rinfo.write(f"CREATEANIMS_VERSION_DATE = \"{version_date}\"\n")
    temp_rinfo.write(f"CREATEANIMS_VERSION = \"{version}\"\n")
    temp_rinfo.write(f"COMMIT_ID = \"{git_short_hash}\"\n")

#And finally, create executable.
shutil.rmtree(TARGET_FOLDER, ignore_errors=True)
subprocess.run("PyInstaller create_anims.spec") #Run is better in this case. It waits, so otherwise we get an "empty console" of sorts where I have to manually press Enter (return) to continue using cmd.
os.chdir(TARGET_FOLDER) #ZipFile.write() essentially gives each file the same path than it had when reading it. So dist/CreateAnims.exe will add a dist folder to the zip file. Not what we want.
all_files = os.listdir()
with zipfile.ZipFile(f"{ZIP_NAME}", mode="x") as temp_zip:
    for file_ in all_files:
        temp_zip.write(file_)
subprocess.run(f"gh release create {version} -F ../{RELEASE_NOTES} --latest=true -t {version} {ZIP_NAME}")