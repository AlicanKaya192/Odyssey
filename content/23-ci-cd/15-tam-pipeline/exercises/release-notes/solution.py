def release_notes(changelog, version):
    lines = changelog.splitlines()
    head = f"## [{version}]"
    body = None
    for line in lines:
        if line.startswith(head):
            body = []
        elif line.startswith("## [") and body is not None:
            break
        elif body is not None:
            body.append(line)
    if body is None:
        return None
    return "\n".join(body).strip()


changelog = """# Changelog

## [0.4.0] - 2026-10-15

- Add kelvin conversion.
- Round results to two places.

## [0.3.0] - 2026-09-01

- First release.
"""
print(release_notes(changelog, "0.4.0"))
print("---")
print(release_notes(changelog, "0.3.0"))
print("---")
print(release_notes(changelog, "9.9.9"))
