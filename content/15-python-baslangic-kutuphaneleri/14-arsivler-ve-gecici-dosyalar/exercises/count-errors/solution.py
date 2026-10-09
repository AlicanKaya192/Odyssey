import gzip


def count_errors(path):
    count = 0
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if line.startswith("ERROR"):
                count += 1
    return count

with gzip.open("app.log.gz", "wt", encoding="utf-8") as f:
    f.write("INFO start\nERROR disk\nINFO ok\nERROR net\nERROR disk\n")
print(count_errors("app.log.gz"))
