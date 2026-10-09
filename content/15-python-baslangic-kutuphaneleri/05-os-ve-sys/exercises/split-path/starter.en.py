import os


def split_path(path):
    # os.path.split, then os.path.splitext
    return ()

print(split_path("data/raw/sales.csv"))
print(split_path("archive.tar.gz"))
