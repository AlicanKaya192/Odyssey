You do not need Python installed on your machine to use this application — the exercises run inside the app. But sooner or later you will want to write your own projects, and then you need an installation.

## Installing on Windows

Download the installer from [python.org/downloads](https://www.python.org/downloads/).

There is **one very important checkbox** on the installer screen:

> ☑ **Add python.exe to PATH**

If you continue without ticking it, typing `python` at the command line gives you a "command not found" error. It can be fixed later, but it is fiddly; tick it the first time.

## Checking the installation

Open a command line (`cmd` or PowerShell on Windows) and type:

```
python --version
```

If you see a version number, the installation is done.

## Which version?

Install the most recent one. Older examples you find online may be written for Python 2; the clearest difference is how `print` is used:

```python
print "hello"      # Python 2 — no longer works
print("hello")     # Python 3 — the correct form
```

If an example does not run, check this first.

## A word about Anaconda

Data science resources often recommend installing **Anaconda**. It is convenient because it brings Python together with libraries such as NumPy and pandas.

There is something you should know, though: Anaconda carries its own system libraries, and those can clash with other programs. This very application will not start when it is installed with Anaconda's Python — the interface library loads Anaconda's older files and fails.

If you are starting out, I would suggest beginning with a **clean Python installation**. You add libraries with `pip install` as you need them.

## Pick an editor

You could write code in Notepad, but you would be making life hard for yourself. The common choices:

- **VS Code** — free, light, the most widely used
- **PyCharm** — Python-specific, free community edition
- **Jupyter Notebook** — heavily used in data analysis; you run code in pieces and see the result immediately

If data science is what you are after, it is worth meeting Jupyter early.
