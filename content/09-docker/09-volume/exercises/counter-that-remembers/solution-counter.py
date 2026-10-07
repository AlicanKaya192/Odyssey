import os

path = "/data/count.txt"
count = 0
if os.path.exists(path):
    with open(path) as handle:
        count = int(handle.read())
count += 1
with open(path, "w") as handle:
    handle.write(str(count))
print("count:", count)
