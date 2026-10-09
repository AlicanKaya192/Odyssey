import zipfile


def zip_sizes(zip_path):
    sizes = []
    # zf.infolist(): info.filename, info.file_size
    return sizes

with zipfile.ZipFile("pack.zip", "w") as zf:
    zf.writestr("big.txt", "x" * 500)
    zf.writestr("small.txt", "hi")
    zf.writestr("docs/mid.txt", "y" * 50)
for name, size in zip_sizes("pack.zip"):
    print(name, size)
