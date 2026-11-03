def patch_plan(installed, advisories):
    lines = []
    for name, fixed in advisories:
        if name in installed and installed[name] < fixed:
            lines.append(f"{name}: {installed[name]} -> {fixed}")
    return sorted(lines)

INSTALLED = {
    "tlslib": "3.0.9",
    "webserver": "1.24.0",
    "zipper": "1.3.1",
    "fetcher": "8.9.0",
}
ADVISORIES = [
    ["tlslib", "3.0.13"],
    ["webserver", "1.22.1"],
    ["zipper", "1.3.1"],
    ["fetcher", "8.10.0"],
    ["vcs", "2.45.1"],
]
for line in patch_plan(INSTALLED, ADVISORIES):
    print(line)
