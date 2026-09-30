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
every run. The application contains no language model and makes no API
calls; nothing to do with learning goes over the network.

**Your data stays on your machine.** Progress, the code you write and your
settings are kept in a local database inside the `%APPDATA%\Odyssey` folder.
No data is sent anywhere. Moving to a new version leaves that folder
untouched, so your progress is preserved.

**It is open source.** The application is distributed under the MIT licence;
the source can be read, modified and redistributed.

## Where things stand

The application is in open beta and works end to end: the learning path,
lessons, lecture notes, quizzes, coding exercises, staged hints, a history
of past attempts in exercises and quizzes, progress tracking, a profile,
badges, XP, levels and titles, a study timer, suggested routes, your own
notes, a global search, a guided tour, a Turkish/English interface, light
and dark themes and in-app updates are all in place.

Six paths are complete: **Python Fundamentals**, **Data Science**,
**Machine Learning**, **SQL**, **Time Series** and **Mathematics**. The
Mathematics path has two modules: foundational mathematics for someone
starting from zero, and the linear algebra, calculus, probability and
statistics that machine learning rests on. Together they hold 140 sections,
4026 quiz questions, 420 coding exercises and 300 mathematics problems. The
API, Docker and other advanced paths are in preparation.

If you are new to the application, **Settings › Learning › Guided tour**
walks you through every screen in turn.

A free coding area outside the exercises and a macOS build are on the
roadmap.

You can follow which change arrived in which version from the **Release
Notes** screen.
