import os

os.makedirs("/out", exist_ok=True)
rows = "".join(f"<li>{n} x {n} = {n * n}</li>" for n in range(1, 6))
with open("/out/index.html", "w", encoding="utf-8") as handle:
    handle.write(f"<h1>Squares</h1><ul>{rows}</ul>\n")
print("report written")
