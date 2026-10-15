The release will use the version's section in `CHANGELOG.md` as its notes. Write the function `release_notes(changelog, version)`:

- The section starts after the line that starts with `## [0.4.0]` (the line can go on with a date).
- It ends at the next line that starts with `## [` or at the end of the text.
- Join the section's lines with `"\n"`, remove the spaces at the start and end (`strip`), return it.
- If the version has no section, `None`.

**Expected output:**

```
- Add kelvin conversion.
- Round results to two places.
---
- First release.
---
None
```
