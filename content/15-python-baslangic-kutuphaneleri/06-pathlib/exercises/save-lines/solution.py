from pathlib import Path


def save_lines(path, lines):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(target.read_text(encoding="utf-8").splitlines())

print(save_lines("out/reports/summary.txt", ["total 345", "days 3"]))
print(Path("out/reports/summary.txt").read_text(encoding="utf-8"))
