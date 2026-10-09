from pathlib import Path


def unique_path(path):
    # while candidate.exists():
    return path

Path("report.txt").write_text("v1", encoding="utf-8")
print(unique_path(Path("report.txt")).name)
Path("report-1.txt").write_text("v2", encoding="utf-8")
print(unique_path(Path("report.txt")).name)
print(unique_path(Path("new.txt")).name)
