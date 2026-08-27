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

## [0.2.0] — 27 August 2026

### Added
- Every section now has **at least three exercises**; the total went from 6 to 18. The new ones are ordered from easy to hard and use only the concepts taught up to that section.
- The application now opens in the language of your computer's interface: Turkish on a Turkish Windows, English otherwise. Once you pick a language in Settings, that choice wins and detection no longer applies.
- A closed beta notice on startup: it says the application may be unstable, that you may hit errors and crashes, and how to send feedback. It appears once per version.
- The licence screen now follows the selected language: Turkish shows a Turkish translation of the MIT Licence, English shows the original. Both languages show a single licence text.
- A **Getting Started** section: what Python is, your first program, how the application works, and an installation note.
- A **Conditionals** section: if / elif / else, the order of conditions, truthiness.
- A **Loops** section: for, while, range, with notes on break and continue.
- A **Dictionaries and Sets** section: the key-value idea, checking for a key with `in`, adding and updating, looping with `items()`, why sets hold no duplicates, and the `{}` trap. The lecture notes cover dictionary methods and a guide to choosing between the four data structures.
- A **Lists and Tuples** section: creating lists, indexes, negative indexes, slicing, `append`/`remove`/`pop`, `len` and `in`, and why tuples cannot be changed. The lecture notes cover list methods and slicing in detail, including the copy trap.
- A **Functions** section: `def`, parameters, `return`, default values. The lecture notes cover positional and keyword arguments and variable scope (local, global). The difference between `return` and `print` is covered in both the lesson and the quiz.
- Two lecture notes for Operators: arithmetic operators, assignment and comparison.

### Changed
- Code inside quiz questions, options and explanations is now drawn as code: monospaced with a background. As plain text it was hard to tell `[20, 30]` apart from a sentence.
- The exercise bar is now easier to notice: the count is in bold and numbered buttons sit beside it. How many exercises a section has and which ones you have solved is visible at a glance, and you can jump straight to any of them. The Previous/Next buttons were removed.
- The page numbers in the release notes are centred, and the "Page 1 / 2" label was dropped since the numbers already said the same thing.
- The left rail is now split in two: the screens you open every day at the top (Learning Path, My Profile, Extra Content) and the occasional ones at the bottom, right above the settings icon (Release Notes, My Links, Licence).
- A red **ALPHA** badge appears next to the version numbers. Every release before 1.0 counts as alpha; the badge disappears on its own once 1.0 arrives.
- The release notes are paginated; at most three releases appear per page, with page buttons underneath. Previously every release was stacked on one page and the screen went on and on.
- The Python Fundamentals module was reorganised. The order is now: Getting Started, Variables, Operators, Conditionals, Loops.
- Loops were split out of Operators into their own section; the two did not belong together.
- The Operators lecture notes now open as text instead of a PDF.
- Quiz explanations now look like the callout box used in lessons.
- The last question in the Getting Started quiz asked about the application's own interface; it was replaced with something the lesson teaches: what it means that Python is an interpreted language.

### Fixed
- The second exercise in Variables asked you to write a function, but functions had not been taught at that point. It was replaced with something the lesson actually covers: converting text to a number.
- Bold and code markers in the release notes were shown raw on screen; they are now rendered as formatting.
- The packaged application showed a generic program icon in the Windows taskbar and title bar instead of its own. The icon file was inside the package, but the application was looking for it in the wrong folder.
- Reading a lesson to the end did not mark it as read. The page was trying to notify the application, but the browser engine does not allow a page to reach the application without a user click, so the notification was silently dropped. The application now asks the page instead.
- The button at the end of a lesson jumped straight to the quiz even when the section had lecture notes. It now follows the order: lesson, lecture notes, quiz, exercise.
- The last lecture note had no forward button, so you had to go back to the tabs to reach the quiz. There is now a button under the last note that takes you there.
- During the reorganisation two exercises kept their old identifier even though their content had changed completely, so opening one showed the code you had written for the previous exercise. The identifiers were separated and the exercises now start empty.

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
