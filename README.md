<div align="right">
  <a href="./README.tr.md">Türkçe</a> · <b>English</b>
</div>

# Odyssey

A fully offline desktop application that teaches Data Science and Machine Learning, one section at a time.

Every section has a lesson, lecture notes and exercises. To complete a section you need to pass the quiz and solve the coding exercises. You write the code inside the application and it runs your code, then checks the output and the result. No artificial intelligence is involved; the checks are predefined and deterministic.

## Status

Early development (`0.2.0`). The application works end to end, but the content is still at the beginning.

**Working:** learning path, lessons, lecture notes, quizzes, coding exercises with automatic checking, graded hints, error explanations, persistent progress, Turkish/English interface and content, light and dark themes.

**Not there yet:** the full curriculum (eight sections of the Python Fundamentals module exist today; the target is 23 modules), badges, a place for your own notes, the in-app update system.

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

Your progress, quiz scores, the code you write, your notes and your profile are stored in a database inside `%APPDATA%\Odyssey\`. Updating the application, or removing and reinstalling it, does not touch that folder — your progress is not lost.

## How are exercises checked?

Your code runs in a separate process, inside an isolated working folder. Its output, the variables it creates and the functions it defines are then compared against expected values. Every check is predefined; no external service takes part in evaluating your code.

**Note:** this is not a security sandbox. You are running your own code on your own machine. What the system provides is an isolated working folder, a timeout, an output limit, and the guarantee that the application does not crash when your code raises an error.

## Internet

The application works entirely offline. It makes no network calls at all right now.

An update check on startup is planned for later, so the app can tell you when a new version exists; it will be switchable from Settings when it arrives. It does not exist yet.

Addresses in the "Links and Extra Content" sections do not open inside the application; clicking one hands it to your system browser. The application never reaches the network on its own — an address opens only because you asked for it.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first.

## Licence

MIT Licence — Copyright (c) 2026 Alican Kaya. See [LICENSE](LICENSE) for details.

The course content comes from the [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) project and falls under the same licence.
