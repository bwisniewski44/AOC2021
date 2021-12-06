import sys
import os
import shutil

for i in range(6, 25+1):
    parent = ("%02d" % i) + "/"
    shutil.copytree("05/", f"{parent}", dirs_exist_ok=True)
    open(parent + "input.txt", "a").close()
    original_name = parent + "05.py"
    new_name = parent + "%02d.py" % i
    os.rename(original_name, new_name)