import os


def find_files(folder, ext):
    found = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            if os.path.splitext(name)[1] == ext:
                full = os.path.join(root, name)
                found.append(os.path.relpath(full, folder).replace(os.sep, "/"))
    return sorted(found)

for path in find_files("project", ".csv"):
    print(path)
