import zipfile


def zip_files(zip_path, paths):
    # ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED)
    return []

print(zip_files("out.zip", ["a.txt", "data/c.csv"]))
