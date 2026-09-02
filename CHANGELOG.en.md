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

## [0.5.0] — unreleased

### Added
- **Badges.** Twelve of them: running your first program, finishing a quiz
  without a mistake, studying seven days in a row and so on. The ones you
  have not earned stay on your profile too, and hovering over one tells you
  how it is earned — so you can see what is there to aim for.
- **Activity calendar.** Every day of a year is a square, and a square gets
  darker the more you did that day. Hovering over a day tells you what you
  did. The list on the right selects the year; a new year appears on its own
  once it arrives. The calendar is filled in retroactively: the lessons you
  read and the exercises you solved earlier are placed on their own dates.

### Changed
- **The theme is now picked with two buttons.** The moon selects the dark
  theme, the sun the light one, and which one is active is obvious at a
  glance. It used to be an on/off switch, where "off" meaning dark only
  became clear once you read the description.
- **The settings and profile-edit windows sit fixed in the centre of the
  screen.** They cannot be moved or resized.
- **The profile page was rearranged.** Photo, name and overall progress on
  the left; the badge wall on the right; the activity calendar below. When
  the badges do not fit on one page, arrows page through them. Half the
  page used to be empty and longer labels were cut off.
- **The numbers on the learning path are fractions now.** "13/65" instead
  of "13", "3/15" instead of "3" — you can see how much of the whole is
  done. The same four numbers appeared a second time on the profile; they
  were removed from there.
- **Editing your profile now opens in its own window.** Choosing "Edit"
  dims the background and puts first name, last name and photo in one
  window. The fields were squeezed into a narrow column before and the text
  was unreadable.

### Fixed
- **The quiz timer setting now takes effect immediately.** Turning the
  timer off while a quiz is open stops the countdown at once, and turning
  it back on restarts it. You used to have to leave the quiz and re-enter.
- **Switching themes no longer flickers.** Going from light to dark could
  briefly show an unstyled frame.
- **Tooltips appear sooner.** The wait before an explanation shows up when
  you hover over something is shorter.

---

## [0.4.0] — 1 September 2026

### Added
- **The quizzes grew: 150 → 250 questions.** From the Modules section onwards
  every section has **20 questions**. The Overall Review quiz went up to
  **50 questions** and covers all fourteen sections — from the details of
  `print` to database work. The time limits were rescaled to match.
- **Comprehensions, `lambda` and `sorted(key=...)` were added.** These appear
  everywhere in real Python code yet were nowhere in the curriculum: the
  `[x * 2 for x in items]` form, filtering, dictionary comprehensions; saying
  what to sort a list by; and functions that take an unknown number of
  arguments (`*args` / `**kwargs`). They went into the Lists and Functions
  sections as a lecture note and two exercises each.
- **Installing libraries** is now covered: `pip install`, why a virtual
  environment is needed, `requirements.txt`, and where `ModuleNotFoundError`
  comes from. This is the first thing needed when moving on to the Data
  Science path, and it only appeared in two passing sentences.
- **A hard exercise was added to the Getting Started and Variables
  sections.** In both, the hardest exercise stopped at medium.
- **An exercise on working with tuples** was added. Despite the section being
  called "Lists and Tuples", no exercise asked for a tuple.
- **Python Fundamentals is complete.** Four more sections were written and the
  module is finished: **Working with Files** (`with`, modes, `encoding`, line
  endings, reading a data file), **Object-Oriented Programming** (`class`,
  `__init__`, `self`, `__str__`, inheritance), **Working with Databases**
  (`sqlite3`, creating tables, the `?` placeholder,
  `SELECT`/`WHERE`/`GROUP BY`, `commit`) and **Overall Review** (how the
  pieces connect, a quick-reference page, where to go from here). All fifteen
  sections are now open.
- **From the Modules section onwards there are five exercises.** Each of those
  sections has one easy, two medium and two hard exercises. The hard ones use
  more than one section at a time rather than a single topic.
- **Two lecture notes were added to the Conditionals section** — a comparison
  reference and a list of condition traps. That section had none at all.
- **A second lecture note was added to the Getting Started section:** the
  Python data science ecosystem, what each library is for and where it is
  taught.
- **A Type Annotations section.** How to write down what a function expects
  and what it gives back: `text: str`, `-> int`, `list[str]`,
  `dict[str, int]`, `int | None` when a value may be absent, `-> None` for
  functions that return nothing, and the `Optional[str]` spelling you meet in
  older code. It also covers the point people get wrong most often — that
  annotations are **not checked** at run time, so they are a note rather than
  a rule. Two lecture notes (a type reference, a guide to decoding long
  annotations), a ten-question quiz and three exercises.
- **Diagrams in the lessons.** Where a drawing makes the point land faster,
  the lessons now carry one: which part of a function signature means what,
  which of the two types in `dict[str, int]` is the key and which is the
  value, and what actually happens to an annotation at run time. The diagrams
  are drawn by the page itself, so they follow the theme and scale with the
  text.
- **A Handling Errors section.** The two kinds of error, reading a traceback,
  `try` / `except`, choosing which error to catch, why a bare `except` is
  bad, `as error`, `else` and `finally`, and raising errors yourself with
  `raise`. Two lecture notes (a glossary of error types, a guide to reading
  tracebacks), a ten-question quiz and three exercises.
- **The quizzes were rewritten.** Every section now has **10 questions** (it
  was 4, and 3 in one section). The module now holds 150 questions. They get
  harder as the sections progress, more of them rest on reading code, and
  each section ends with one that makes you think.
- **A Modules section.** `import`, `from ... import ...`, nicknames with
  `as`, using your own file as a module and `if __name__ == "__main__"`.
  Two lecture notes (a tour of the standard library, import forms and
  common mistakes), a ten-question quiz and three exercises. In the last
  one you import a real module file placed next to your code.
- **API and Docker learning tracks** added. Neither has content yet, so
  both appear locked.
- **A setting for removing the section lock.** With it on, sections no longer
  open in order; you can enter any of them whenever you like.
- **A setting for removing the quiz time limit.** With it on, quizzes have no
  time limit.
- **A quiz start screen.** Questions no longer appear the moment you touch
  the tab; first you see how many there are, how long you have and **your
  previous score**. You start when you are ready.
- **Quizzes are timed.** The time allowed per question grows as the topics
  get harder. When the time runs out the quiz is submitted for you. The
  clock sits in the top right corner, out of the way of the text.
- **Questions and options are shuffled on every attempt**, and the correct
  answer never lands in the same position more than twice in a row.
- **About screen.** Overview, FAQ, My Links, Extra Content and Licence are now
  on one screen, with tabs at the top to move between them.
- **FAQ page.** The questions asked most often about the application;
  click one to open its answer.
- **Overview page** explaining what the application is, how it works and the
  principles it is built on.
- **A profile photo.** You can pick your own picture on the profile screen;
  it also appears on the profile button in the rail. The image is copied
  into the data folder on your computer and never sent anywhere.
- **Sections now unlock in order.** A section stays locked until the one
  before it is finished, and the locked circle says which section you
  need to complete. You can still revisit anything you have finished.
- `CS_Complete_Terminology_Guide` added to Extra Content.
- If you did not use the variable name an exercise asked for but held the
  right value under another name, the application now says so: "You have a
  variable named `second` with the right value, but this exercise asks for it
  under the name `seconds`." It used to say only that the variable was missing.

### Changed
- **The language is now chosen with TR / EN buttons in the settings.** A
  toggle was the wrong control for a choice between two options; which side
  meant which language was only clear once you read the description.
- **The settings screen was reorganised.** Language and theme were dropdowns,
  and that layout fell apart as the number of settings grew. Each setting is
  now readable at a glance: its name and what it does on the left, and a
  switch showing on or off by its position on the right. The settings are
  split into Appearance and Learning.
- **The application now opens with the dark theme.**
- **The left rail went from seven icons to five.** My Links, Extra Content and
  Licence became tabs on the About screen.
- **The top of the rail shows an overall progress ring** with the percentage in
  the middle, so how far along you are stays on screen while you read a lesson
  or work through an exercise. Clicking it returns to the learning path.
- **Screen titles are centred** with a thin accent line beneath them, and the
  back button moved to the far left.
- **The module path is centred on the page.** It used to hug the left edge.
- **The rail icons are now two-tone.** Drawn as outlines only they looked
  lifeless; their bodies are now lightly filled in their own colour.
- **The light theme was softened.** The page was too bright for long
  reading and cards were pure white. Muted text (durations, "Not
  started", the on-this-page list) was also noticeably harder to read
  than in the dark theme. Both were brought to the dark theme's level.

### Fixed
- **Passing an exercise produced several "Passed" lines in a row.** With up
  to six checks in one exercise, the panel filled with them and pushed the
  output down. It now writes a single line on success, and shows only the
  lines that did not hold when something fails. The space that freed up went
  to the output box, which is now nearly twice as tall.
- **The panel said misleading things when the code failed to run.** For a
  class missing its colon it said "you have not defined a class named Book" —
  the class was there; the problem was the syntax. When the code does not run
  at all, only the error itself and its line number are now shown.
- **The screen went black for a moment the first time you opened a page.**
  Lessons, lecture notes, About and Release Notes are drawn with a browser
  engine, and each one showed black until its first frame arrived. That
  first frame is now drawn at startup, before the window is visible.
- **Lessons jumped around while you scrolled.** Reaching the end of the
  text marks it as read, which updates the progress box on the right; that
  update reloaded the whole page and lost your place. The box is now
  changed where it stands, without reloading.
- **The on-this-page list in lessons.** Scrolling to the bottom threw the
  marker back up, and it never reached the last heading ("Summary").
- **Code in quiz questions was shown as plain text.** There were no colours
  and, worse, **the indentation was lost** — in Python the indentation is
  the code. It now looks the way it does in the lessons.
- `>=` was drawn as a single `≥` sign because of the font ligatures. It
  now appears as written.
- `**bold**` markup showed up raw in quiz text.
- Opening a new lesson could start you partway down the page, at the
  position you had reached in the previous lesson, instead of at the top.
- **A white flash when opening pages and settings for the first time.**
- The application appeared behind the splash screen while it was still on
  screen, so both were visible at once. It now arrives as the splash goes.
- Long entries in the release notes were cut off halfway; they now show in full.
- Release-note headings read "EKLENDI" in Turkish; they now read "EKLENDİ".

## [0.3.0] — 28 August 2026

### Added
- The home screen now opens with learning tracks: Python, Data Science, Machine Learning and SQL, laid out as four cards in a 2x2 grid. The three without content yet are faded and carry a lock; the Data Science and Machine Learning cards suggest finishing the Python track first. The progress bar now sits on the track card.
- When a track holds a single module the module list is skipped and you go straight to the topics; clicking through a one-card screen served no purpose. Going back follows the same route.
- A splash screen: the application icon and name appear while the main window is being built. Until now nothing appeared on screen until Chromium had loaded.
- Sections that have not been written yet now appear on the learning path as faded, unclickable circles marked "Coming soon". The rest of Python Fundamentals (modules, error handling, file handling, OOP, SQLite, review) is listed this way.

### Changed
- The lecture notes screen was redesigned. The 270-pixel list panel on the left was removed; a section holds three notes at most, so that panel was both heavy and pushed the text to the right. The notes are now a slim row of tabs above the text, and with a single note the row is not drawn at all.
- The screen headers were redesigned. The bar is now aligned with the same column as the page content: the title sat at the far left of the window while the content was centred, so the two did not look connected. The bar's separate background was removed; it looked like a detached block sitting on top of the page and now shares the page's background, separated only by a thin line. The title is larger (17px to 26px), with a small context line above it and a coloured bar beside it, in the same colour as its icon in the left rail. The text sits vertically centred in the bar.
- The Windows title bar now takes the application's colour. In dark mode the window was dark while the bar stayed light, which split the screen in two. The settings and startup notice windows follow the same colour.

### Fixed
- Scrolling down through a lesson suddenly jumped back to the top. Reaching the end marks it as read, which updates the progress box and reloaded the document. The same happened in an exercise brief when a hint was revealed. The reading position is now kept when a document is redrawn.
- Solving an exercise did not put the tick on its number straight away; it only appeared after switching to another exercise or reopening the section.
- The filled box behind the tabs on the topic screen was removed; it looked like a patch once the bar shared the page's background. The selected tab is now marked by an underline, and the tabs no longer sit on top of each other.
- The duration in a section heading was written in Turkish even in English; it now comes from the translations.
- The counter labels on the welcome card are now capitalised: "Sections Completed", "Exercises Solved".
- Headings written in capitals mangled the Turkish letter `i`: the app showed "ÖĞRENME PATIKALARI" where it should read "ÖĞRENME PATİKALARI". Python's `upper()` turns `i` into `I`; the conversion now follows the selected language.

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
