<div align="right">
  <a href="./README.tr.md">Türkçe</a> · <b>English</b>
</div>

# Odyssey

An offline desktop application that teaches Data Science and Machine Learning, one section at a time.

Every section has a lesson, lecture notes, a quiz and coding exercises. To complete a section you need to pass the quiz and solve the exercises. You write the code inside the application; it runs your code, then checks the output, the variables it created and the functions it defined. No artificial intelligence is involved — every check is defined in advance and evaluated deterministically, so the same code always produces the same result.

## Status

Early development (`0.7.0`). The application works end to end. The engine — learning paths, lessons, quizzes, the exercise runner, progress tracking — is in place; the curriculum is still at the beginning.

**Content today:** two modules are **complete**. Python Fundamentals has fifteen sections, from your first program to databases; Data Science has ten, from NumPy to exploratory analysis. 560 quiz questions, 115 coding exercises and 54 sets of lecture notes, all of it in both Turkish and English.

**Six learning paths** are defined: Python and Data Science are open, while Machine Learning, SQL, API and Docker are visible but locked until their content is written.

**Working:** learning paths, lessons with a section outline and reading progress, lecture notes, timed quizzes, coding exercises with automatic checking, graded hints, error explanations, sections that unlock in order, persistent progress, a profile with your own photo, Turkish/English interface and content, light and dark themes, and options to remove the section lock and the quiz time limit.

**Not there yet:** the content for the other paths (23 modules are planned), badges, a place for your own notes, the in-app update system.

The roadmap moves along in [CHANGELOG.en.md](CHANGELOG.en.md).

## Installing

If you would rather not install Python, download the ready-made package from [Releases](https://github.com/AlicanKaya192/Odyssey/releases), extract the folder and run `Odyssey.exe`. No installation, no admin rights, no Python needed.

## Requirements (for running from source)

- Windows 10 / 11
- Python 3.10 – 3.14 (a clean CPython installation)

Do not use Anaconda's Python. Anaconda ships its own MSVC runtime libraries, and when Qt's DLLs load those, the application will not start.

## Setting up (development)

```bash
py -3.14 tools/setup_env.py
```

This command creates both the environment the application runs in and the separate environment the exercises run in. Then:

```bash
.venv\Scripts\python app\main.py
```

## Languages

Both the interface and the content are available in Turkish and English. You can switch at any time from Settings, without restarting. If a section has not been translated into English yet, the Turkish version is shown with a notice at the top.

## Where is your data kept?

Your progress, quiz scores, the code you write, your notes, your profile and the photo you choose are stored inside `%APPDATA%\Odyssey\`. Updating the application, or removing and reinstalling it, does not touch that folder — your progress is not lost.

## How are exercises checked?

Your code runs in a separate process, inside an isolated working folder. Its output, the variables it creates and the functions it defines are then compared against expected values. Every check is predefined; no external service takes part in evaluating your code.

**Note:** this is not a security sandbox. You are running your own code on your own machine. What the system provides is an isolated working folder, a timeout, an output limit, and the guarantee that the application does not crash when your code raises an error.

## Internet

Everything about learning works offline: the lessons, the lecture notes, the quizzes, the exercises and your progress. None of it involves a server, and your progress never leaves your computer.

The application makes exactly one network request, and only if you leave it on: at every start (and every three hours if you leave it open) it asks GitHub whether a newer version has been released. The request sends nothing — no identity, no progress, no usage data — and when a new version exists, a link to the release page appears in the strip at the bottom of the window. The application does not update itself; you download and unpack the new version yourself. Turn the check off under **Settings > Updates** and the application never touches the network.

Addresses in the "My Links" and "Extra Content" tabs do not open inside the application; clicking one hands it to your system browser.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first. Security reports have their own route: see [SECURITY.md](SECURITY.md).

## Licence

MIT Licence — Copyright (c) 2026 Alican Kaya. See [LICENSE](LICENSE) for details.

The course content comes from the [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) project and falls under the same licence.
