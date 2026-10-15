def release_notes(changelog, version):
    # Satirlari gez; basligi bulunca toplamaya basla, sonraki baslikta dur.
    pass


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
