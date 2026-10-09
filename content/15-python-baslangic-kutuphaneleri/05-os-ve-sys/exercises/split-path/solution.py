import os


def split_path(path):
    folder, filename = os.path.split(path)
    stem, ext = os.path.splitext(filename)
    return folder, stem, ext

print(split_path("data/raw/sales.csv"))
print(split_path("archive.tar.gz"))
