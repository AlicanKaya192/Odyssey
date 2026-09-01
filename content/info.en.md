# What is Odyssey?

Odyssey is an offline desktop application that teaches data science and
machine learning through a structured curriculum.

Its purpose is to replace moving between scattered sources with a single,
measurable path: every topic has a clear beginning and end, progress is
recorded, and there is a step where what you learned is tested.

## How it works

Each section has four parts: the lesson, the lecture notes, a quiz and coding
exercises. A section counts as finished only when the quiz is passed and the
exercises are solved.

Sections unlock in order. To reach one, the section before it must be
complete, so the curriculum never runs ahead of the ground it is built on.

You write the code inside the application. When you run it, the program
executes your code in its own environment, inspects the output and the
variables it produced, and shows you condition by condition what was met and
what was not.

## Principles

**Assessment is deterministic.** Exercises are checked against rules defined
in advance: output comparison, variable and function checks, and checks that
look at the structure of the code. The same code gives the same result on
every run. The application contains no language model, no API calls and no
network connection.

**Your data stays on your machine.** Progress, the code you write and your
settings are kept in a local database inside the `%APPDATA%\Odyssey` folder.
No data is sent anywhere. Moving to a new version leaves that folder
untouched, so your progress is preserved.

**It is open source.** The application is distributed under the MIT licence;
the source can be read, modified and redistributed.

## Where things stand

The application is in early development. It works end to end: the learning
path, lessons, lecture notes, quizzes, coding exercises, staged hints,
progress tracking, a Turkish/English interface and light and dark themes are
all in place.

The curriculum continues to grow. The Python Fundamentals module is published
today; the target is 23 modules. Badges, a personal notes area and an in-app
update system are on the roadmap.

You can follow which change arrived in which version from the **Release
Notes** screen.
