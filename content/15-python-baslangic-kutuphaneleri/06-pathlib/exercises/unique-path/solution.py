from pathlib import Path


def unique_path(path):
    candidate = path
    counter = 1
    while candidate.exists():
        candidate = path.with_stem(f"{path.stem}-{counter}")
        counter += 1
    return candidate

Path("report.txt").write_text("v1", encoding="utf-8")
print(unique_path(Path("report.txt")).name)
Path("report-1.txt").write_text("v2", encoding="utf-8")
print(unique_path(Path("report.txt")).name)
print(unique_path(Path("new.txt")).name)
