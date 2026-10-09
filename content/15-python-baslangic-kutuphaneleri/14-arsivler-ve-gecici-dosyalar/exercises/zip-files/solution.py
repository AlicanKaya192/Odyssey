import zipfile


def zip_files(zip_path, paths):
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in paths:
            zf.write(path)
    with zipfile.ZipFile(zip_path) as zf:
        return sorted(zf.namelist())

print(zip_files("out.zip", ["a.txt", "data/c.csv"]))
