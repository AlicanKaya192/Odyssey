<div align="right">
  <a href="./README.tr.md">Türkçe</a> · <b>English</b>
</div>

# Odyssey

An offline desktop application that teaches Data Science and Machine Learning, one section at a time.

Every section has a lesson, lecture notes, a quiz and coding exercises. To complete a section you need to pass the quiz and solve the exercises. You write the code inside the application; it runs your code, then checks the output, the variables it created and the functions it defined. No artificial intelligence is involved — every check is defined in advance and evaluated deterministically, so the same code always produces the same result.

## Getting started

**1. Download the package.** Take the `Odyssey-<version>-windows-x64.zip` file from the [Releases](https://github.com/AlicanKaya192/Odyssey/releases) page. Windows 10 or 11, 64-bit. There is no installer and no admin rights are needed.

**2. Unpack the whole folder — do not run the application from inside the zip.** Windows lets you open a zip as though it were an ordinary folder, and `Odyssey.exe` looks runnable in there. It is not: the application needs the `_internal` folder sitting next to it, and Windows only unpacks the one file you double-click. Right-click the zip, choose **Extract All**, and keep the `Odyssey` folder together.

Put it somewhere you can write to — your desktop, your documents, a folder of your own. Avoid `C:\Program Files`: the application updates itself by replacing its own files, and that folder needs administrator rights.

**3. Run `Odyssey.exe`.** The first start takes a few seconds longer than the rest.

**4. Windows will warn you the first time.** A blue box appears saying "Windows protected your PC". This is SmartScreen, and it appears because the application is not code-signed — Windows cannot tell who published it, so it warns about everything it has not seen before. Click **More info**, then **Run anyway**. Windows remembers the choice; it will not ask again.

### Your progress is kept outside the application

Everything you do — your progress, quiz scores, the code you write, your profile and the photo you choose — is stored in `%APPDATA%\Odyssey\`, not in the folder you unpacked.

That separation is the point: you can replace the application folder, delete it, or move it to another drive, and none of it touches your progress. When you update, you carry on where you left off.

### Updating

Odyssey checks for a new version when it starts, and every three hours if you leave it open. When there is one, it tells you and offers to install it.

Press **Update** and the application downloads the new version, checks that the file arrived intact, closes itself, replaces its own files and opens again — about a minute in total, with the progress visible throughout. Your progress is untouched.

If the update cannot be applied — the folder is not writable, or the disk is full — the application says so and gives you the release page so you can do it by hand. Doing it by hand is always the same thing: unpack the new folder in place of the old one.

You can turn the check off under **Settings › Updates**. With it off, the application never touches the network at all.

## Status

Early development (`0.7.3.1`), released as an open beta. The application works end to end. The engine — learning paths, lessons, quizzes, the exercise runner, progress tracking, updates — is in place; the curriculum is still growing.

**Content today:** two modules are **complete**. Python Fundamentals has fifteen sections, from your first program to databases; Data Science has ten, from NumPy to exploratory analysis. 560 quiz questions, 115 coding exercises and 54 sets of lecture notes, all of it in both Turkish and English.

**Six learning paths** are defined: Python and Data Science are open, while Machine Learning, SQL, API and Docker are visible but locked until their content is written.

**Working:** learning paths, lessons with a section outline and reading progress, lecture notes, timed quizzes, coding exercises with automatic checking, graded hints, error explanations, sections that unlock in order, persistent progress, 19 badges and an activity calendar, a profile with your own photo, Turkish/English interface and content, light and dark themes, in-app updates, and options to remove the section lock and the quiz time limit.

**Not there yet:** the content for the other four paths, a place for your own notes, and a larger exercise engine for projects that run a dataset end to end.

The roadmap moves along in [CHANGELOG.en.md](CHANGELOG.en.md).

## Running from source

- Windows 10 / 11
- Python 3.10 – 3.14 (a clean CPython installation)

Do not use Anaconda's Python. Anaconda ships its own MSVC runtime libraries, and when Qt's DLLs load those, the application will not start.

```bash
py -3.14 tools/setup_env.py
```

This command creates both the environment the application runs in and the separate environment the exercises run in. Then:

```bash
.venv\Scripts\python app\main.py
```

## Languages

Both the interface and the content are available in Turkish and English. You can switch at any time from Settings, without restarting. On a Turkish computer the application starts in Turkish and on any other in English, until you choose for yourself. If a section has not been translated into English yet, the Turkish version is shown with a notice at the top.

## How are exercises checked?

Your code runs in a separate process, inside an isolated working folder. Its output, the variables it creates and the functions it defines are then compared against expected values. Every check is predefined; no external service takes part in evaluating your code.

**Note:** this is not a security sandbox. You are running your own code on your own machine. What the system provides is an isolated working folder, a timeout, an output limit, and the guarantee that the application does not crash when your code raises an error.

## Internet

Everything about learning works offline: the lessons, the lecture notes, the quizzes, the exercises and your progress. None of it involves a server, and your progress never leaves your computer.

The application makes exactly one network request, and only if you leave it on: the version check described above. It sends nothing — no identity, no progress, no usage data — and downloads a file only when you press Update.

Addresses in the "My Links" and "Extra Content" tabs do not open inside the application; clicking one hands it to your system browser.

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first. Security reports have their own route: see [SECURITY.md](SECURITY.md).

## Licence

MIT Licence — Copyright (c) 2026 Alican Kaya. See [LICENSE](LICENSE) for details.

The course content comes from the [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap) project and falls under the same licence.
