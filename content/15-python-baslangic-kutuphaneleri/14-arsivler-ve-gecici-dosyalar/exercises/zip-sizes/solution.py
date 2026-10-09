import zipfile


def zip_sizes(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        sizes = [(info.filename, info.file_size) for info in zf.infolist()]
    return sorted(sizes, key=lambda item: item[1], reverse=True)

with zipfile.ZipFile("pack.zip", "w") as zf:
    zf.writestr("big.txt", "x" * 500)
    zf.writestr("small.txt", "hi")
    zf.writestr("docs/mid.txt", "y" * 50)
for name, size in zip_sizes("pack.zip"):
    print(name, size)
