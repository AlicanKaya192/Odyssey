import shutil
from pathlib import Path


def clean_release(src, dst):
    shutil.copytree(src, dst)
    return []

for name in clean_release("app", "release"):
    print(name)
