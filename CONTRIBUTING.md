<div align="right">
  <a href="./CONTRIBUTING.tr.md">Türkçe</a> · <b>English</b>
</div>

# Contributing Guide

Issues and pull requests are open to anyone who wants to contribute to Odyssey.
Please read the [Code of Conduct](./CODE_OF_CONDUCT.md) before you start.

## 📑 Contents

- [How can I contribute?](#how-can-i-contribute)
- [Setting up a development environment](#setting-up-a-development-environment)
- [Reporting a bug](#reporting-a-bug)
- [Proposing a feature](#proposing-a-feature)
- [Contributing content](#contributing-content)
- [Code standards](#code-standards)
- [Running the validators](#running-the-validators)
- [Pull request process](#pull-request-process)

## How can I contribute?

- **Bug fixes:** If you find a button that does nothing, a broken layout or a
  wrong translation, open an issue or send a pull request directly.
- **New content:** If you want to add a section, an exercise or a set of
  lecture notes, it helps to share the idea in an issue first. The curriculum
  order follows the
  [Data Science Roadmap](https://github.com/AlicanKaya192/Data-Science-RoadMap)
  project.
- **Translation:** The application is available in Turkish and English. If you
  want to add another language, use `app/i18n/en.json` as your reference.
- **Documentation:** Improving the READMEs and the explanations inside the code
  is always welcome.

## Setting up a development environment

```bash
py -3.14 tools/setup_env.py
.venv\Scripts\python app\main.py
```

**Do not use Anaconda's Python.** Anaconda ships its own (older) MSVC runtime
libraries; when Qt's DLLs load those, the application fails to start with
`WinError 127`. A clean CPython installation is required.

## Reporting a bug

Including these in the issue helps a great deal:

- What you were trying to do, what you expected and what happened instead
- Step-by-step instructions to reproduce it
- Your Windows version and the output of `python --version`
- A screenshot and the error text from the terminal, if you have them

You can use the [issue templates](.github/ISSUE_TEMPLATE) for a ready-made
structure.

## Proposing a feature

When you write the proposal, describe **which problem it solves** rather than
what should be added. What can a learner not do today, where do they get stuck?
Add your idea for a solution if you have one, but that part is optional.

## Contributing content

Content lives under `content/` as JSON and Markdown. Three rules apply:

### 1. Exercise code must be ASCII

Everything the user is **required to type** — variable names, function names,
expected output, sample values — contains ASCII characters only. `ş ğ ı İ ç ö ü`
are not allowed.

The reason: those letters do not exist on an English keyboard. Someone using
the application in English **cannot solve** an exercise that asks for
`takim = "Beşiktaş"`.

```jsonc
// Wrong
{ "type": "variable", "name": "takim", "equals": "Beşiktaş" }

// Right
{ "type": "variable", "name": "team", "equals": "Galatasaray" }
```

Variable and function names are written in English (`team`, `year`, `total`,
`calculate_age`). Real Python code is written that way anyway.

**Lesson text is exempt** — it is read, not typed, so non-ASCII characters are
free there.

### 2. A section is not finished until both languages are

Preparing the English version of a lesson while you have just written it costs
an extra 30-40% of the time; doing it months later nearly doubles that, because
you have to read your own writing from scratch first.

`starter` and `solution` files are also split by `{lang}`, so that the comments
are in the user's language.

### 3. Content ids are permanent

Once a section or an exercise has been given an id, that id **never changes**.
The title and the file name may change; the id stays — users' progress records
are tied to those ids.

## Code standards

- Python 3.10+ syntax, with type hints.
- Colours and measurements come from `app/resources/theme/tokens.py`; styles are
  not scattered across widgets.
- Interface text lives in `app/i18n/*.json`; no strings are hard-coded.
- Comments explain **why**, not what. The code already says what.
- There is **no** artificial intelligence and no external service call inside
  the application. Exercise evaluation is entirely deterministic.

## Running the validators

Run all three before you send a pull request:

```bash
.venv\Scripts\python tools\validate_i18n.py      # are both languages in sync
.venv\Scripts\python tools\validate_content.py   # schema + ASCII + translation coverage
.venv\Scripts\python app\main.py                 # does the application start
```

`validate_content.py` catches missing files, invalid quiz answer indices,
differing option counts between languages, a solution identical to the starter
code, ASCII violations and missing translations.

## Pull request process

1. Fork the repository and create a branch: `git checkout -b fix/short-description`
2. Make your change and run the validators.
3. Write a descriptive commit message: what changed and **why**.
4. When you open the pull request, state which issue it closes.

For a pull request to be accepted:

- The validators must pass cleanly
- New content must exist in both languages
- The application must start and the relevant screen must work

You do not need to open an issue for small typo fixes; send a pull request
directly.
