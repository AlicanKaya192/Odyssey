import os
import sys

path = "/data/notes.txt"
os.makedirs("/data", exist_ok=True)
with open(path, "a", encoding="utf-8") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\n")
with open(path, encoding="utf-8") as handle:
    print("notes:", len(handle.readlines()))
