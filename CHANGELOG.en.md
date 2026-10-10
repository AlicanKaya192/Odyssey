# Odyssey — Changelog

The Release Notes screen inside the application shows this file. It is written
here before a new version is published, so the release description on GitHub
and the text inside the application come from the same source.

The Turkish version is in `CHANGELOG.md`; both are kept in step.

## How the version numbers move

`MAJOR.MINOR.PATCH` — three parts:

- **Patch** (`1.0.0` → `1.0.1`): bug fixes only.
- **Minor** (`1.0.x` → `1.1.0`): a new path or a major feature.
- **Major** (`1.x` → `2.0.0`): a version in which the application is largely
  rebuilt.

The `0.x` versions were the development period: open beta from `0.7.1` to
`0.9.3`, alpha before that. `1.0.0` is the first full release.

The course content has its own version (`content_version`), so fixing a single
lecture note does not mean downloading the whole application again.

---

## [1.0.0] — 10 October 2026

### Added
- **Algorithms path.** It teaches writing algorithms in your own code and
  telling in advance how a solution behaves as the data grows. **Core Algorithms**
  (17 sections) covers core algorithms and data structures: complexity,
  searching and sorting, hashing, stacks, queues, trees and heaps. **Algorithm Techniques**
  (17 sections) covers problem-solving techniques: divide and conquer,
  backtracking, greedy methods, dynamic programming, graphs and shortest
  paths, string and number algorithms, randomised and probabilistic methods,
  heuristic optimisation. **ML Algorithms** (23 sections) has you write machine
  learning algorithms from scratch with NumPy and compare the results with
  scikit-learn: linear and logistic regression, gradient descent, KNN, Naive
  Bayes, decision trees, random forests, boosting, SVMs, clustering, PCA,
  association rules, PageRank, neural networks and recommender systems. Every
  time, step count and result in the lessons was measured; some exercises
  only finish within the time limit with an efficient solution. New badges,
  the "Puzzle Solver", "Strategist" and "Daedalus" titles, and algorithm terms
  in the glossary.
- **Core Libraries path.** It covers the libraries of Python and data science
  that are a must to know. **Python Libraries: Beginner** (17 sections)
  teaches working with the standard library without installing any package:
  maths and statistics, dates and times, files and folders, CSV, regular
  expressions, collections, itertools, archives. **Python Libraries:
  Advanced** (18 sections) covers the tools of growing programs: types and
  dataclasses, logging, argparse, sqlite3, pickle, decimal, hashlib,
  concurrency and asyncio, tests, measurement and memory leaks. **Data
  Science Libraries** (17 sections) covers NumPy, pandas, Matplotlib, seaborn
  and SciPy in depth: array types and broadcasting, the index and MultiIndex,
  combining, reshaping, time, text and categories, performance, chart types
  and customisation, statistical tests, optimisation. The charts in the
  lessons are matplotlib's real output. **Machine Learning Libraries** (17
  sections) walks a model's whole path with scikit-learn, statsmodels and
  LightGBM: preprocessing and pipelines, hyperparameter search, validation
  tools, metrics and the decision threshold, linear, tree and boosting
  models, clustering, statistical inference, saving and explaining models.
  New badges, the "Artisan", "Architect", "Cartographer" and "Alchemist"
  titles; a new step in the Data Scientist route.

### Changed
- **`raise` is explained in more depth.** The Python path's Handling Errors
  lesson now walks through raising an error yourself, choosing the error
  type and raising a caught error again. The Object-Oriented Programming
  lesson gained writing your own error class and `raise ... from`, with a new
  exercise.
- **Odyssey is no longer an open beta.** 1.0 is the first full release: the
  "Open Beta" label is gone from the start-up screen, and first-time users
  see a short welcome window instead of the beta notice.
- **Levels were widened for the new paths.** The XP needed for the next
  level went up a little; your current level may drop by a few steps. The
  titles you have earned stay yours.

## [0.9.3] — 7 October 2026

### Added
- **The API track.** Two modules: **API 1** (17 sections) is about using
  REST APIs: addresses, HTTP, JSON, `requests`, authentication, paging,
  errors and retries, building a dataset from an API. Exercises send
  requests to a practice server inside the app; no internet needed.
  **API 2** (18 sections) is the other side of the table: writing your own
  API with FastAPI; validation, CRUD, error responses, dependencies,
  authentication, SQLite, tests, async and serving a machine learning
  model. In API 2 you can start the server you wrote with one button, try
  it in the browser, and send requests from the **Request** tab in the side
  panel.
- **The Git track.** Version control in seventeen sections: the first
  commit and the three areas, looking at and undoing changes, `.gitignore`,
  branches, merging and conflicts, remotes and GitHub (pull requests,
  forks), stash, rewriting history, tags, recovering what was lost and good
  habits. Exercises are typed into a Git terminal inside the app; you don't
  need to install Git or open a GitHub account, and the goals are checked
  off one by one next to the terminal.
- **The Docker track.** Containers in seventeen sections: images and
  layers, the Dockerfile, caching and `.dockerignore`, ports, environment
  variables, volumes, Docker Compose and multi-service apps, smaller
  images, security, debugging and packaging a Python API. Exercises check
  your Dockerfile and compose file; with Docker Desktop running they also
  really build and run the image. The new **Storage** page in Settings
  removes the images and SQL databases the exercises leave behind.
- **The Big Data track.** Working with data that does not fit in memory, in
  seventeen sections: measuring memory, shrinking with data types, reading
  in chunks, Parquet and partitioned data, SQL on files with DuckDB,
  sampling, parallel processing and dask, MapReduce, how Spark works,
  streaming data and an end-to-end data pipeline. The exercises' large data
  files are generated on your computer; the Spark and Kafka sections use
  small look-alikes that come with the program, so nothing needs to be
  installed.
- **A JSON section in the Python track.** A new section after Working with
  Files: writing dictionaries and lists to a file as JSON and reading them
  back, moving through nested data step by step, and dealing with missing
  fields and broken files; 24 questions and 7 exercises.
- **The Data Engineer roadmap.** A new route in Roadmaps for the work of
  pulling data from a source, cleaning, storing and serving it: Python,
  Git, SQL, pandas, Big Data, APIs and Docker, with focus sections at each
  step. The Big Data track is also an optional step on the Data Scientist
  and ML Engineer routes.

### Fixed
- **Step-by-step tracing names classes correctly.** While the body of a
  class was being traced, the panel called it "inside the function" and
  said it "returned" a value at the end; it now says "body of the class".
- **The error summary is fully English in the English interface.** When
  code raised an error, the line information in the summary still said
  "satır".

## [0.9.2] — 6 October 2026

### Added
- **22 new exercises in Python Fundamentals.** The Getting Started,
  Variables, Operators, Conditions, Loops and Dictionaries sections now
  have seven exercises each. The new ones are harder and meant to make you
  think: quotes inside quotes, output aligned space for space, operator
  precedence traps, the leap year rule, the order of conditions, primes and
  twin primes, the longest Collatz journey, binary search, a diamond of
  stars, counting words, processing orders and turning a dictionary around,
  among others. If you had already finished these sections, they stay
  finished; the new exercises wait for you as extra practice.
- **Placement test.** If you already know a module's topics, you no
  longer have to start from the beginning: the optional test from the card
  at the top of the path asks four questions from each section (three right
  means you know it) and unlocks the sections you know plus the first one
  after them. It stops by itself
  after two sections in a row are missed, and the result shows which
  sections you know and which to review. Unlocked sections do not count as
  completed.
- **Tracing code step by step.** In Python exercises the **Step by
  step** button replays your code line by line: the next line is marked
  in the editor, and below you see the variables and the output so far
  at every step. A new variable shows in green, a changed value in
  yellow; inside a function its own variables are shown separately, and
  when it finishes you see what it returned. Use the arrow keys to move
  back and forth. If your code is empty or you do not know where to start,
  switch to **Sample solution** to watch a correct solution unfold line by
  line (your own code stays as it is). The "Stuck?" card opens it too.
- **A glossary of terms.** In lessons, lesson notes and exercise
  instructions, terms are marked with a dotted underline where they first
  appear; hovering shows a short explanation, so there is no need to leave
  the lesson to look up "what was a parameter?". All terms are gathered
  by track in the new **Glossary** tab under About and can be searched
  with `Ctrl+K`.
- **A pointer back to the lesson when you are stuck.** After three failed
  tries in a row on an exercise, a "Stuck?" card appears under the brief:
  it names the heading of the lesson the exercise builds on, and **Go to
  the lesson** opens it right there.
- **Moving your progress to another computer.** From the new **Data** page
  in Settings, your progress, notes, settings and profile photo are
  exported to a single `.odyssey` file; importing it on another computer
  from the same page restarts Odyssey and you continue where you left off.
  The progress that was on that computer is not deleted but kept as a
  backup. The automatic backups folder opens from the same page.
- **The line with the error is marked in the editor.** When your code
  fails, that line is shaded red in the editor, its number is marked and
  the editor scrolls to it if it is out of view; the mark goes away once
  you change the code.
- **More error explanations.** The 💡 explanations in the terminal now
  recognise 28 more errors: working with a variable that holds nothing
  (`None`), a comma as the decimal separator, a missing file, a function
  that keeps calling itself, a column the table does not have, a mismatch
  between the number of variables and values, a single `=` in a condition,
  and missing values and table shape errors in machine learning, among
  others. If Windows Smart App Control blocks a library an exercise needs,
  you are told it has nothing to do with your code.
- **Keyboard in quizzes.** Pick an answer with 1–4 or A–D and press Enter
  to confirm it and move on to the next question.
- **Reading focus.** The frame button in a section's header, or `F11`,
  opens the lesson full screen without the side menu and bars. Press `Esc`
  or `F11` to leave; a note at the top of the screen reminds you of this
  when you enter.
- **Share card.** The "Save share card" button on your profile saves your
  level, title, progress, latest badges and your study chart for the last
  year as a single image you can share on sites such as LinkedIn. If you
  enter your GitHub username in the profile edit window, it appears in the
  card's corner.
- **Commands from search.** `Ctrl+K` no longer only finds content: type
  "theme", "language", "timer", "tour", "shortcuts" or "menu" and a
  command that does it appears.
- **"Something wrong on this page?" button.** The flag icon in a
  section's header opens a GitHub bug report with this page's details
  already filled in, so you can report a wrong fact or a broken exercise
  without describing where it is. The program sends nothing itself.
- **A daily backup of your progress.** Each day the program starts, it
  keeps a copy of your progress file and holds on to the last three days.
  If the file is damaged by a power cut or a disk error, the program notices
  at startup, puts the newest healthy backup in its place and tells you; the
  damaged file is not deleted.
- **A log file.** When something goes wrong, the reason is written to a file
  in `%APPDATA%\Odyssey\logs`; you can attach it when reporting a bug. Your
  code, notes and answers are not logged, and the file is never sent
  anywhere.

### Changed
- **A "What's new?" window after updates.** The first time the program
  opens after an update, it shows the five most important changes of that
  version instead of the beta notice; "All release notes" opens the Release
  Notes screen.
- **The quiz screen has been reworked.** The start card sums up your past
  attempts (best score, last score, number of attempts) and explains how
  the quiz works, the question card shows "Question 3 / 10", and the result
  card shows how many you got right, wrong or left blank and how long it
  took.
- **The guided tour covers the new features too:** the placement test, the
  glossary, focus mode and reporting a problem, step-by-step tracing and
  the share card. You can restart it from Settings › Learning.
- **A window stays on screen while an update installs.** After the
  download Odyssey closed and nothing was visible until the new version
  opened, which could look like a crash. Now an "Odyssey is updating"
  window, which you can minimise, stays until the new version opens and
  then closes by itself. You will see it on updates after 0.9.2.
- **Answers from an unfinished quiz are no longer lost.** When you leave a
  quiz before finishing it (or close the program), the answers you have
  given so far are saved to Past attempts as "left unfinished", so you can
  look at your mistakes there. Such an attempt is not scored.
- **Refreshed tooltips.** The card that appears when you hover over a
  badge, the streak flame, the level bar or a button now matches the app's
  theme and opens without delay or stutter; it reads as a title, a coloured
  status line (such as when your streak ends) and a description.

### Fixed
- When Windows blocked the update's installer (for example Smart App
  Control), the update window said the download had failed. It now gives
  the real reason and what you can do.

## [0.9.1] — 30 September 2026

### Added
- **The Time Series track.** 23 chapters at three levels: **Basic** covers
  working with dates and the time index, resampling and windows;
  **Intermediate** decomposition, stationarity, autocorrelation, missing
  values and outliers, baselines and validating a forecast; **Advanced**
  exponential smoothing, ARIMA, external variables, forecasting with machine
  learning, prediction intervals, anomalies and change points. The last
  chapter brings it all together in one job: from a messy dump to a 28-day
  forecast with an interval. 153 exercises, 628 quiz questions and three new
  badges.
- **Levels and titles.** Every section you finish and every badge you earn
  gives XP; badges give more than sections, and hard badges more still. As
  XP builds up you level up (50 levels, each asking for more XP than the
  last) and a card appears in the bottom right with its own sound. Your
  profile shows your level and an XP bar under your name. At certain
  levels, on finishing a whole track and for a few hard feats you earn a
  **title**; click the title under your name to pick one of those you have
  earned, and hover over a locked one to see how to earn it. Sections you
  finished and badges you earned earlier count too.
- **Study timer.** From the clock icon on the right of the bottom bar you
  can pick a routine and start: Pomodoro (25 / 5, with a long break every
  four rounds), 52 / 17, deep work (90 / 20), small steps (15 / 3) or your
  own lengths. The time left runs as a small counter in the bottom bar and
  only grows slightly in the last seconds; you can pause, skip the break or
  finish. When a round or a break ends a card appears with a short sound,
  and a Windows notification if Odyssey is in the background. Finished
  focus rounds count as that day's study, for your streak and activity
  calendar.
- **Past attempts.** A new **My attempts** tab in exercises: your last
  correct solution and your wrong attempts, each with why it did not pass;
  in a wrong attempt the lines that are not in your correct solution are
  marked in red. In mathematics problems the answers you tried are listed.
  In quizzes, **See my mistakes** and **Past attempts**: for every attempt,
  what you answered to each question, the correct answer and the
  explanation. Attempts are recorded from this version on.
- **Guided tour.** On first start (and once after this update) you are
  asked whether you would like a short tour of the app. Odyssey's centaur
  guides you through every part in turn: tracks, a section's tabs, the
  lesson, notes, the quiz, the exercise screen, profile, badges, routes,
  notes, search, the study timer and settings. You can leave the tour at
  any moment and restart it from Settings › Learning.

### Changed
- **No more leaving a quiz by accident.** While a quiz is in progress,
  moving to another tab, section or screen asks first; if you choose
  "Leave the quiz", that attempt is cancelled and does not count.
- **Updates now download only the files that changed.** If you have the
  previous version installed, you get a small update package with just the
  files changed since then instead of the 233 MB full installer (from the
  next update on). The package checks the installed version; if it does not
  match, it touches nothing and Odyssey downloads the full installer on the
  next try. Moving to 0.9.1 is the last update that uses the full installer.

### Fixed
- After an update, the desktop shortcut kept showing the old icon. The
  installer now makes Windows refresh its icons.

## [0.9.0] — 29 September 2026

### Added
- **A new first chapter in the Python track: Packages and Environments.**
  pip and `python -m pip`, virtual environments (`venv`), `requirements.txt`,
  Anaconda and conda and how they differ; connecting VS Code and Jupyter to
  an environment, and common setup errors. The commands to know by heart are
  gathered on a command sheet, and the chapter ends with a 24-question quiz.
  Anyone who had already started Python keeps their chapters open and their
  earned badges.

### Changed
- **A refreshed interface.** Smooth transitions between screens, new icons
  and track logos, badges as medals. Motion can be reduced in Settings ›
  Appearance › Animations.
- **A new start-up.** Instead of the loading card, a short animation with
  sound plays while the program opens: Odyssey's mascot, a centaur with a
  bow, gallops in, looses an arrow and hits the target dead centre. Click or
  press `Esc` to skip it; the sound can be turned off in Settings ›
  Notifications › Sounds. The centaur also stands on the welcome card of the
  Learning Path, aiming at the target that shows your overall progress. It
  is also the new application icon.
- **A refreshed update window.** The downloaded and total size, speed and
  time left are shown as the download runs; the window can be minimised and
  left in the background, and Odyssey stays usable meanwhile. When the
  download finishes, installation runs without a window and Odyssey opens
  with the new version.
- **Clearer roadmaps.** Each step says what the track covers, what you will be
  able to do by the end and roughly how long it takes. Every chapter to focus
  on says why it matters, and clicking an open chapter takes you straight to
  it.
- **Discord shows the screen you are on.** The selected route in Roadmaps,
  and My Notes, My Profile, About and Release Notes are shown too; before,
  every screen outside a chapter read "Browsing the path". The titles and
  contents of your notes are not sent.
- **Clearer streaks.** When you close the program, the exit window tells you
  whether your streak is safe today. Hovering over the flame shows a
  countdown to when the streak ends and what makes a day count. Spending
  2 minutes in a section now counts as well; before, only finishing a
  lesson, running an exercise or taking a quiz did.

### Fixed
- **No reminders on days you use the program.** Someone who opened the
  program in the morning and looked through the topics could get a "your
  streak is in danger" or "you've been away for 3 days" notification in the
  evening. "Away" is now counted from the last day the program was opened.
- **Updating no longer locks the desktop.** The window that opened after
  clicking "Update" kept you from switching to other windows (Alt+Tab and
  the taskbar did not respond). The fix applies to updates after 0.9.0: the
  update from 0.8.3 to 0.9.0 is still done by the old version's window.

## [0.8.3] — 26 September 2026

### Added
- **The Mathematics path has been added.** Two modules: **MATH 1 —
  Foundational Mathematics**, from numbers to functions, geometry and
  trigonometry, probability and statistics for someone starting from zero;
  **MATH 2 — The Mathematics of AI**, the linear algebra, calculus,
  probability and statistics machine learning rests on. Problems are worked
  on a drawing sheet; only the result is checked, and the solution paths
  open on the left.
- **Streak reminders.** If you haven't studied that day, a playful Windows
  notification arrives at the time you choose; if your streak is at risk
  there's one last warning at 21:30, and if you stay away for long the
  reminders get less frequent and stop after two months. It works while the
  program is closed: a small task that runs for a few seconds a day is added
  to Windows Task Scheduler, and nothing is sent over the internet. You're
  asked on first launch whether you want it; the time and the on/off switch
  are in Settings › Notifications.
- **The left menu can be hidden.** With the small button on the edge of
  the strip or `Ctrl+M`; the content gets more room and your choice is
  remembered.
- **Odyssey now comes with an installer.** The application installs for
  your own user account, with a shortcut in the Start menu and on your
  desktop, and no `_internal` folder to keep track of. When you update from
  inside the application from an unpacked folder, the new version is
  installed and the program files in the old folder are removed; your
  progress, notes and settings are kept. It can be removed from Settings ›
  Apps.
- **Roadmaps.** A new screen in the left rail, above My Notes, that explains
  which track to study in which order. There are three routes — for someone
  who has never written code, for someone who knows Python and wants to move
  into data science, and for someone who wants to become an ML engineer.
  Each step says why it sits where it does, which chapters to focus on and
  how much of it you have finished; tracks that are not written yet stay in
  place, marked "Coming soon".
- **Typing help in the editor.** Brackets and quotes close on their own;
  typing the closing character steps over it, `Backspace` removes an empty
  pair together, and selected text is wrapped in brackets or quotes. `Tab`
  and `Shift+Tab` indent and unindent every selected line; `Backspace` in
  the indentation removes one level. `Enter` between `(|)` puts the content
  on its own line and unindents after `return` or `pass`. `Ctrl+/` comments
  or uncomments the selected lines. Faint vertical indent guides show where
  blocks begin and end. The same help works inside code blocks in My Notes.
- **The streak flame grows.** A flame sits next to the streak count on the
  welcome card; as your streak gets longer it changes colour and size, from
  a small yellow spark to a golden flame after a hundred days. Hovering
  over it shows how many days are left until the next stage.
- **GitHub star in the bottom strip.** The bottom left corner shows how many
  stars Odyssey has on GitHub; clicking it opens the repository, where you
  can add yours if you like it. The count is refreshed together with the
  update check, and if the check is turned off in Settings › Updates the
  application never touches the network.

### Changed
- **Exercise results in a terminal.** Instead of the results panel that
  opened when you ran your code, a terminal now sits under the editor at all
  times: your program's output, errors and what they mean, passed or not,
  and for a mismatched output the expected and yours one under the other,
  aligned. If your code produced a chart or a multi-line table didn't match,
  the **Output** tab opens on the left: the chart at full width, expected
  and your output line by line, with mismatched lines marked. The divider
  between the terminal and the editor can be dragged to resize them.
- **The Data Science path has been renewed.** Thirteen exercises were
  rewritten: you now write the imports yourself, read the data from a CSV
  file that sits next to the exercise, and the chart you draw appears on
  screen. All five exercises of the Visualisation section are new,
  including one where you see a misleading and an honest axis side by side.
  The DataFrame Basics, Selecting and Filtering, Grouping and Aggregation,
  Cleaning Data, Exploratory Data Analysis and Overall Review sections gain
  exercises that start from a file too. The DataFrame lesson has a new part
  on reading a CSV file, and the quizzes have 55 new questions; every
  section except the Overall Review now has 35. If you had already finished
  these sections, they show as in progress until you solve the new
  exercises.
- **The settings window has been redesigned.** Settings now sit in
  categories on the left: Appearance, Learning, Notifications, SQL and
  Updates. Each page has a short description of what it is for, and the
  window keeps the same size on every page. "Show on Discord" moved to the
  Appearance page.
- **Search sits in the middle of the left strip.** The overall progress
  ring in the middle of the strip is gone; the same percentage is already
  shown on the learning path screen. The search button took its place.
- **Badge and section celebrations in the bottom right.** The notification
  bell in the bottom strip is gone. When you finish a section or earn a
  badge, a card with its icon appears in the bottom right and closes by
  itself after a few seconds; it waits while the pointer is over it, the
  cross closes it at once, and clicking a badge card opens your profile.
  A short celebration sound plays with the card; it can be turned off in
  Settings › Notifications. The shortcuts button moved to the bell's place
  in the bottom right.

### Fixed
- **Difficulty labels in Machine Learning exercises are no longer
  empty.** Twenty exercises showed nothing after "Difficulty:"; they now
  show the difficulty dots.
- **Opening and closing Settings no longer crashes the program.** When
  Settings closed, the background job counting the SQL databases was cut
  off mid-run and the program closed unexpectedly.
- **Closing the program no longer crashes it.** Closing the program while
  the update check at startup was running, or while an exercise was
  running, could make it crash.
- **Undo works on the first press.** After opening an exercise or a note,
  the first few presses of `Ctrl+Z` seemed to do nothing. It now undoes
  your last change straight away.
- **Opening a hint no longer makes the screen jump.** Opening a hint reloaded
  the whole instructions page; it flashed back to the top and then returned
  to where you were. Now only the hint box changes and your place stays put.
  An opened hint can be closed again with "Hide".
- **SQL code is coloured everywhere.** SQL code blocks in the SQL path's
  lessons, lecture notes and My Notes were plain; SQL in quiz questions and
  in the exercise editor was coloured with Python's rules (`SELECT` stayed
  plain and a `--` comment did not look like one). SQL now uses its own
  rules everywhere.
- **Replaced exercises no longer count towards a finished section.** When an
  exercise was replaced by a new one, having solved the old one marked the
  section as complete even though the new one was unsolved. Only the
  section's current exercises are counted now.
- **Correct solutions written differently are accepted.** In exercises
  that ask for a loop or a condition, a list comprehension
  (`[x for x in items if ...]`) or a one-line conditional
  (`a if condition else b`) failed even when the result was right. These
  now count as a loop and a condition. When an exercise really does ask for
  another method, the result says "Your result is correct, but this
  exercise practises a particular method" instead of just "wrong".

---

## [0.8.2.1] — 16 September 2026

### Changed
- **The update system is ready for an installer.** The next version will
  come as an installer: when you press Update, Odyssey installs itself,
  leaves a shortcut on your desktop and removes the program files from the
  old folder. Your progress, notes and settings are kept. This version only
  makes that move possible; nothing else changes.

---

## [0.8.2] — 16 September 2026

### Added
- **Two new sections in Python Fundamentals.** **Formatting Text:** f-string
  format specifiers — decimal places, thousands separators, percentages,
  alignment and column width, and printing numbers as an aligned table.
  **Comprehensions:** list, dictionary and set comprehensions, the
  difference between a filter and a conditional value, nested comprehensions
  and generator expressions. Each section has a lesson, two lecture notes, a
  fifteen-question quiz and five exercises.
- **My Notes.** The notebook icon on the left strip opens your own notes.
  Notes are filed by path; you give each note a name and can tie it to a
  lesson, and then go back to that lesson from the note. You can also make
  your own folders and move notes between folders; deleting a folder does
  not delete the notes in it. Notes are written
  in markdown: the Code button in the toolbar adds a Python or SQL code
  block, and code is coloured the way it is in the lessons. Inside a lesson,
  the "Take a note" button in the header (`Ctrl+N`) opens the note next to
  the lesson: you can right-click something you selected in the lesson to
  add it to the note, and put the code you wrote in an exercise into the
  note with one button. What you write is saved automatically. You can
  download your notes one by one (`.md`) or a folder at a time (`.zip`),
  and upload notes you got from someone else; an uploaded note never
  overwrites one of yours.
- **Search everywhere.** `Ctrl+K` or the magnifier on the left strip opens a
  search box in the middle of the screen, with suggestions appearing
  below as you type. It searches sections, lesson headings and text,
  lecture notes, exercises, your own notes and screens. Choosing a result
  takes you straight there: a lesson scrolls to that heading, a lecture
  note or exercise opens on the right one. Searches typed without Turkish
  letters still match ("dongu" → "Döngüler").
- **A list of keyboard shortcuts.** The keyboard icon in the bottom strip,
  or `F1`, opens the list of shortcuts: search, taking a note, running code
  and the rest. They were not written down anywhere.
- **A memory limit for exercises.** A list that keeps growing or a very
  large array no longer eats up your computer's memory: the code is stopped
  once it goes over 3 GB and the result area says why. Such code used to be
  able to use up all the memory before the time limit ran out and slow the
  computer down.

---

## [0.8.1] — 15 September 2026

### Added
- **Part 2 of the SQL path.** Its sections — **Intermediate:** Table Design,
  Dates and Text. **Advanced:** Window Functions, WITH and Recursion,
  Indexes, Views and Stored Procedures, Overall Review. Every section comes
  with its own notes, quiz, exercises and badge, and there is a separate
  badge for finishing the whole path.
- **Notifications.** The bell on the right of the bottom strip lists the
  badges you earn, with the number of unread ones on top of it. You can mark
  each one as read or clear them all.

---

## [0.8.0] — 10 September 2026

### Added
- **Part 1 of the SQL path.** You write queries inside Odyssey and the SQL
  Server on your own machine runs them. The sections — **Beginner:** Setup,
  SELECT and WHERE, Ordering and Limiting, Filtering Patterns, Calculated
  Columns, Grouping. **Intermediate:** Joining Tables, Subqueries, Changing
  Data. Every section comes with its own notes, quiz, exercises and badge.
  In the exercises you can see the tables in a separate window, and delete
  the databases they create from Settings.

### Fixed
- **There was no way forward after a quiz or an exercise.** The lesson and
  note pages had a "next" button at the bottom, but the quiz result and the
  exercises did not; you had to look for the tabs or the exercise numbers
  in the top right. Finishing a quiz now shows "Exercise →", each exercise
  ends with "Next exercise →", and the last one shows "Next →" once the
  section is complete.
- **External links in the lecture notes did not open.** Clicking the
  download address in the Python setup note did nothing; it now opens in
  your browser.
- **Term tables in the lessons ran together.** In sections like "Glossary"
  the term and its explanation flowed into one line with no space between
  them: "sample (örnek)a row in the table". They now sit in two columns
  with a separator between them.
- **The text on Discord appeared late.** It did not show when the
  application opened, only once you entered a section or a minute later.

---

## [0.7.5] — 7 September 2026

### Added
- **What is coming next now shows on the path screen.** The paths in
  preparation were added to the main screen: Time Series, Natural Language
  Processing, Generative AI, Algorithms, AI Mathematics, Essential
  Libraries and System Design.

### Fixed
- **Enter took two presses in the exercise editor.** Before opening a new
  line, the line you were on and the next one squeezed together, and the
  second press put them back.
- **A quiz started from the middle of the page rather than the first
  question.**

---

## [0.7.4] — 4 September 2026

### Added
- **The Machine Learning path is complete.** Its sections: What Is Machine
  Learning?, Your First Model, Regression Metrics, Classification, Preparing
  Data for a Model, Validation and Overfitting, KNN, Decision Trees,
  Ensemble Methods, Imbalanced Data, Unsupervised Learning, Pipelines and
  Saving a Model, Overall Review. Thirteen sections with twenty-six notes,
  513 quiz questions, sixty-five exercises and five end-to-end projects; in
  the exercises you train and measure your own models with scikit-learn.
- **It shows on Discord.** While Discord is open, your profile shows that
  you are using Odyssey, which module and section you are on and how long
  you have been at it; the two buttons beneath it go to the project page
  and the latest release. The
  text is in the language you chose. It can be turned off in Settings.
  If Discord is not installed or not running, nothing changes: the app does
  not even notice, and it connects on its own if you open Discord later.
- **The exercises got longer.** In Machine Learning the starter code no
  longer hands you ready-made `import` lines; you write where each tool
  comes from.
- **Fourteen new badges:** *Into Machine Learning*, *First Model*, *Error
  Reader*, *The Classifier*, *Leak Hunter*, *Honest Measurement*, *The
  Neighbourhood*, *Rule Reader*, *Forest Keeper*, *Rare Signal*, *Group
  Finder*, *One Piece*, *The Reviewer* and *Machine Learning Complete*.
- **The chart you drew now appears on screen.** When an exercise saves a
  chart, the chart itself shows up in the results panel after you run your
  code. It used to be produced, checked and deleted — you never saw what
  you had drawn.
- **scikit-learn is bundled too, for Machine Learning.** Like NumPy, pandas
  and matplotlib it ships inside the application, so there is nothing to
  install. This is why the download is larger.

### Fixed
- **Hints now open one at a time.** Clicking the last hint in an exercise
  also opened every hint before it, so one click undid the whole point of
  graduated help. Now only the one you click opens.
- **The last hint gives the solution in every exercise.** In some exercises
  that step said "the full solution" but showed only part of it.

---

## [0.7.3.1] — 3 September 2026

### Changed
- **The update box can be reached from anywhere.** Clicking the "New
  version" line at the bottom of the window now opens the update box
  instead of a browser, so you can install it from there or go to the
  release page.
- **The "Check now" button in settings turns into "Update"** when a new
  version is found. It used to say one existed without offering any way to
  install it.

- **A module's path screen starts at the top.** The module's name and
  description were repeated above the sections; the screen's own title
  already carries the name, and the description sits on the card you came
  from.

### Fixed
- **An update notice, once dismissed, never came back.** The notice was
  recorded as "shown for this version"; because that record lives with your
  data rather than the application, anyone who went back to an older
  version or reinstalled never saw the same update again. The record now
  includes the installed version as well.

- **A dark patch behind the year selector in the profile.** The year button
  next to the activity calendar looked like a hole in the card: the area
  behind it painted the page background instead of the card. The
  unnecessary frame around the button when there is only one year is gone
  as well.

---

## [0.7.2] — 3 September 2026

### Fixed
- **Enter did nothing on an empty line in the exercise editor.** You could
  not leave extra blank lines between blocks of code; the line-spacing
  setting was applied in the middle of the text change and swallowed the
  key.
- **The lesson stayed in the old language when you switched languages.**
  Changing the language in settings translated the labels but left the
  lesson text as it was, so you had to leave the section and come back. The
  lesson is now translated straight away.

---

## [0.7.1] — 2 September 2026

### Added
- **Updating now happens inside the application.** The new-version notice
  has an "Update" button: the file is downloaded (with progress), checked,
  the application closes, the files are replaced and the new version opens
  by itself. No more downloading and swapping folders by hand.
- **The download can be cancelled**, and a half-finished file is removed.
- **If something goes wrong, the old version comes back.** The old
  installation is kept aside during the swap; if the copy cannot finish it
  is restored, so at worst you stay on the version you had.
- When updating is not possible (the folder cannot be written to, not
  enough disk space), the reason is shown in place of the button, with a
  link to the release page.

### Fixed
- **The check for new versions never returned anything.** Because releases
  are published as pre-releases, the address the check used reported "no
  release"; it now reads the list of releases and finds the newest one.

---

## [0.7.0] — 2 September 2026

### Added
- **A check for new versions.** The application looks for a newer release
  every time it starts, and every three hours if you leave it open. When
  there is one, a link to the release page sits in the strip at the bottom
  of the window.
- **A notice appears when a new version is out.** Once per version, and
  only at startup: no box interrupts you while you are reading a lesson or
  taking a quiz. It shows the new version number, a button that opens the
  release page, and how updating works.
- **The application does not update itself** — you do the downloading:
  unpack the file in place of the old one. Your progress, profile and
  badges are kept, because they are stored separately.
- **The check can be turned off in settings.** An "Updates" group was added
  to the settings window: a switch turns it off, and a "Check now" button
  looks straight away. With it off, the application never touches the
  network.
- The request sends nothing: no identity, no progress, no usage data. When
  a check fails, nothing appears on screen — having no internet connection
  is an ordinary situation in this application.

---

## [0.6.0] — 2 September 2026

### Added
- **The Data Science path is open.** Its first section is "What Is Data
  Science?": how a piece of data work runs from end to end, why data is
  almost always a table, and which problem NumPy and pandas each answer.
  There are twenty quiz questions and five exercises.
- **No libraries in this section's exercises.** You take an average, filter
  rows, pull out a column, group by city and produce a summary report from
  raw text — all in plain Python. The point is that when you write `groupby`
  in the next section, you know what it replaces.
- **Two lecture notes:** *Data Glossary* (record, variable, mean versus
  median, missing values, file formats) and *Table Recipes* (the same six
  operations in plain Python, each shown next to its pandas form).
- **The NumPy section.** Arithmetic on arrays without writing a loop:
  vectorised operations, `shape` and `dtype`, reshaping, slices and fancy
  indexing, selecting by condition, `axis` and the row/column distinction,
  broadcasting and missing values (`np.nan`). Twenty quiz questions and five
  exercises.
- **NumPy traps in their own lecture note.** A slice changing the original
  array, a decimal silently truncated in an integer array, `&` instead of
  `and`, a single `nan` ruining the whole average, `axis` being read
  backwards, and seven more. Most of these **do not raise an error** — the
  program runs and gives you the wrong number.
- **The Pandas Series section.** The structure that carries **labels**
  alongside the values: building a Series, selecting by label, filtering by
  condition, seeing and filling missing values, counting with
  `value_counts` and summarising at a glance with `describe`. Twenty quiz
  questions and five exercises.
- **Alignment is explained.** When two Series are added, pandas matches on
  labels rather than order, so data from two sources lines up correctly even
  in a different order. This is exactly where NumPy gives a silently wrong
  answer.
- **The DataFrame Basics section.** The real table structure: building a
  table from a dictionary, the first look with `shape` / `columns` /
  `dtypes` / `head`, selecting and adding columns, sorting, making a column
  the index, and summarising with `describe`. Thirty quiz questions and five
  exercises.
- **The Selecting and Filtering section.** Taking the part of the table you
  care about: `loc` by label, `iloc` by position, masks built from
  conditions, several conditions with `&` and `|`, `isin` and
  `str.contains`, sorting and `nlargest`. Thirty quiz questions and five
  exercises.
- **The Grouping section.** Split, compute, combine: `groupby`, several
  summaries with `agg`, each row's own group average with `transform`,
  breaking down by two columns, and `pivot_table` and `crosstab`. Thirty
  quiz questions and five exercises.
- **The Cleaning Data section.** What real data looks like: spaces in the
  column names, inconsistently written text, numeric columns that arrive as
  text, duplicated records and missing values. Cleaning has an order, and
  the section teaches it. Thirty quiz questions and five exercises.
- **The Visualisation section.** Bar, line, histogram and scatter charts;
  which chart answers which question, why a title and axis labels are
  required, saving a chart to a file and putting two charts on one canvas.
  Thirty quiz questions and five exercises.
- **The Exploratory Data Analysis section.** What to do when a new dataset
  lands in front of you: the order to look in, reading a `describe` output,
  judging a group average alongside its size, correlation, finding outliers
  with the IQR rule, and turning a finding into an honest sentence. Thirty
  quiz questions and five exercises.
- **The Overall Review section.** A single example that cleans and analyses
  a raw table from end to end, the key idea of each section, and the most
  common traps in one list. Fifty quiz questions and five exercises, plus a
  quick reference note covering the whole module.
- **Every section has two lecture notes:** one a reference table for the
  topic, the other the traps people fall into. Most of the trap notes are
  about mistakes that **raise no error**: the program runs, a number appears
  and the result is wrong.
- **Data Science quizzes have thirty questions.** Every section but the
  introduction has thirty, and the Overall Review has fifty; these topics
  need more repetition than the Python fundamentals did.
- **Seven new badges:** completing a section on the Data Science path,
  completing a section in two different modules, finishing the NumPy,
  DataFrame, Cleaning Data and Visualisation sections, and completing the
  whole path.

### Changed
- **NumPy, pandas and matplotlib now ship inside the application.** The Data
  Science exercises use them; you do not have to install anything and you do
  not need an internet connection. This is why the download is larger.

### Fixed
- **The comments in an exercise's starter code were not translated when you
  changed language.** The instructions changed but the code in the editor
  stayed in the old language, and once you had run it, it never changed
  again. Now, as long as you have not touched the code, the comments follow
  the language you chose. Code you have written is left alone.

---

## [0.5.0] — 2 September 2026

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
