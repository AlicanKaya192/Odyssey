# Odyssey — Changelog

The Release Notes screen inside the application shows this file. It is written
here before a new version is published, so the release description on GitHub
and the text inside the application come from the same source.

The Turkish version is in `CHANGELOG.md`; both are kept in step.

## How the version numbers move

`MAJOR.MINOR.PATCH` — three parts:

- **Patch** (`0.1.0` → `0.1.1`): fixes and small additions. During development
  this is the one that usually moves.
- **Minor** (`0.1.x` → `0.2.0`): when a milestone is finished, such as the
  content import.
- **Major** (`0.x` → `1.0.0`): the first version somebody other than me can use.

The course content has its own version (`content_version`), so fixing a single
lecture note does not mean downloading the whole application again.

---

## [0.1.2] — 27 August 2026

### Added
- Links and Extra Content sections: GitHub, LinkedIn, portfolio, Medium and open source projects.
- Licence screen: the MIT text and the licence covering the course content.
- Graded hints in exercises; you open as much help as you need.
- Error messages now explain what they mean underneath.
- A ready-made Windows package: `Odyssey.exe` runs without installing Python.
- The application now has its own name and icon.

### Changed
- Exercise code is now pure ASCII. English keyboards have no Turkish characters, so the earlier exercises could not be solved by anyone using English.
- The progress indicator reflects the real state; opening a section no longer counts as having read it.
- Icons in the left rail are easier to read in the dark theme.

### Fixed
- On the last lecture note, "Next note" was shown but could not be clicked; it is now hidden.
- In the release notes, every heading was drawn as a separate card.

## [0.1.1] — 26 August 2026

### Added
- Learning path screen: module cards and section nodes.
- Profile screen: first name, surname and progress statistics.
- Lecture notes open as text instead of PDF, so they can be searched and copied.

### Changed
- Lesson text is rendered with Chromium: coloured code blocks, rounded corners, and a table of contents that stays in place while you scroll.
- Sections are not locked; you can return to completed ones whenever you like.

### Fixed
- The settings window would not open.
- Switching to lecture notes opened a second window.

## [0.1.0] — 26 August 2026

### Added
- First working version: the Python Fundamentals module with lessons, a quiz and code exercises.
- Code runner: five check types, a timeout, and understandable error messages.
- Turkish and English interface, switchable without restarting.
- Progress is stored permanently.
