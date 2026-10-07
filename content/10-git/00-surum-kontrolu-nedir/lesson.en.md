# What Is Version Control?

Imagine you have been working on a project for a few days. You look at the
folder and see this:

```text
report.docx
report_final.docx
report_final_v2.docx
report_REALLY_final.docx
report_final_v2_teacher_edits.docx
```

Which one is the newest? What changed between the second and the third? If
you want back the paragraph you deleted yesterday, which file do you open?
If a friend works on the same report, how do the two sets of changes come
together?

In code this problem is much bigger. A program is made of hundreds of files;
changing one line can break something elsewhere, and "it worked yesterday,
why not today?" is asked every day. **Version control** is the name of the
method that answers all of these questions.

## What does version control do?

A version control system watches the project's folder and, whenever you ask,
takes a **snapshot** of how it looks right now. In Git this snapshot is
called a **commit**.

Every commit keeps four things:

- **What changed:** which line was added or removed in which file.
- **Who did it:** your name and e-mail address.
- **When:** the date and time.
- **Why:** a short explanation you write, the **commit message**.

<figure class="fig">
  <div class="flow">
    <span class="node">commit 1<br><small>"Add readme"</small></span><span class="arrow">→</span>
    <span class="node">commit 2<br><small>"Add contact page"</small></span><span class="arrow">→</span>
    <span class="node">commit 3<br><small>"Fix typo in title"</small></span><span class="arrow">→</span>
    <span class="node acc">now<br><small>the files in the folder</small></span>
  </div>
  <figcaption>Each commit is a snapshot of the project at that moment, with a message. You can go back to any of them.</figcaption>
</figure>

So the folder holds a single copy of each file, and the whole history lives
inside Git. You no longer fill the folder with copies like `report_final_v2`.

What this gives you:

1. **You can go back.** If something breaks, one command takes you back to
   the last working state.
2. **You see what changed.** The difference between two commits is shown
   line by line.
3. **You experiment freely.** You try a new idea on a separate **branch**;
   if you don't like it, you throw it away without touching your main work.
4. **You work together.** Several people work on the same project and Git
   brings their changes together.

## What is Git, what is GitHub?

These two names are often mixed up, because both start with "Git".

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Git</h4><p>A program on your computer</p><p>Works offline</p><p>commits, branches, history</p><p><b>The tool</b></p></div>
    <div class="dim"><h4>GitHub</h4><p>A website on the internet</p><p>Stores and shares repositories</p><p>pull requests, issues</p><p><b>Where repositories live</b></p></div>
  </div>
  <figcaption>GitHub means nothing without Git; Git works fine on its own without GitHub.</figcaption>
</figure>

**Git** is a program that runs on your computer. Linus Torvalds wrote it in
2005 to develop the Linux kernel, and today almost the whole software world
uses it. It works without the internet too: making commits, looking at the
history and opening branches all happen on your computer.

**GitHub** is a website that stores Git repositories on the internet. You
send your project there, others see it, download it and contribute. GitLab
and Bitbucket are other sites doing the same job. In short: **Git is the
tool, GitHub is a place where the repositories that tool makes are kept.**

## Repository

The folder Git watches is called a **repository** (*repo* for short). When
you turn a folder into a repository, Git creates a hidden folder named
`.git` inside it. The whole history, every commit, the branches and the
settings live there.

> Do not edit or delete the `.git` folder by hand. If you delete it, the
> files in the folder stay where they are but the whole history is gone: the
> folder becomes an ordinary folder again.

## Why the terminal?

Git's real face is the **command line** (the terminal). Visual tools such as
the Git panel in VS Code or GitHub Desktop run the same commands in the
background. Someone who knows the commands:

- can use any tool on any computer,
- understands the error messages (they are written in the language of the
  commands),
- can apply the solutions they find online (almost all of them are written
  as commands).

That is why this track teaches Git from the terminal. On Windows you use the
**Git Bash** terminal that comes with Git; on Mac and Linux you use the
system's own terminal. The commands are the same on all three.

## Reading the terminal

The terminal greets you on every line with a **prompt**. The prompt means
"ready for you to type" and tells you where you are:

<figure class="fig">
  <pre><code class="language-text">~/notes (main) $ git status</code></pre>
  <div class="anat">
    <div class="anat-row"><span>~</span><span>Your home folder (usually /c/Users/yourname in Git Bash). The start of every path.</span></div>
    <div class="anat-row"><span>/notes</span><span>The folder you are in right now.</span></div>
    <div class="anat-row"><span>(main)</span><span>The branch you are on, if you are inside a Git repository. Not shown outside one.</span></div>
    <div class="anat-row"><span>$</span><span>Waiting for a command. You type what comes after it.</span></div>
    <div class="anat-row"><span>git status</span><span>The command you typed.</span></div>
  </div>
  <figcaption>The prompt tells you where you are on every line. In the lesson examples, the lines with $ are the commands you type.</figcaption>
</figure>

You type your command after the `$` sign and press **Enter**. The command's
output is written on the lines below, then a new prompt appears.

## First commands

Before Git, you need to move around in the terminal: see where you are,
create folders, create files. You will use all of these constantly while
working with Git.

| Command | What it does |
|---|---|
| `pwd` | Prints which folder you are in (*print working directory*). |
| `ls` | Lists the files and folders where you are. |
| `ls -a` | Lists them together with the hidden ones (starting with `.`). |
| `mkdir notes` | Creates a new folder named `notes` (*make directory*). |
| `cd notes` | Goes into the `notes` folder (*change directory*). |
| `cd ..` | Goes up one folder. |
| `cd ~` | Goes back to your home folder. |
| `echo "Hi" > a.txt` | Writes the file `a.txt` (any old content is wiped first). |
| `echo "Hi" >> a.txt` | Adds a line to the end of `a.txt`. |
| `cat a.txt` | Prints the content of the file. |
| `rm a.txt` | Deletes the file (it does not go to the recycle bin). |

An example session:

```text
~ $ pwd
/home/ada
~ $ mkdir notes
~ $ ls
notes/
~ $ cd notes
~/notes $ pwd
/home/ada/notes
~/notes $ echo "Buy milk" > todo.txt
~/notes $ echo "Call Ada" >> todo.txt
~/notes $ cat todo.txt
Buy milk
Call Ada
~/notes $ ls
todo.txt
```

A few things to notice:

- `mkdir` and `cd` print **nothing** when they succeed. In the terminal,
  silence usually means "done".
- `ls` puts a `/` after folders; that is how you tell files from folders.
- After `cd notes` the prompt became `~/notes $`: you are there now.
- `>` rewrites the file from scratch, `>>` adds to the end. Mix them up and
  everything in the file is gone; think once before typing `>`.

## The terminal in Odyssey

In this track's exercises you will not write code; **you will type commands
into a terminal**. A terminal opens on the right of the exercise:

- The **goals** are at the top. They are checked after every command; a goal
  that is met gets a ✓. When all of them are met, the exercise is solved.
- The commands behave like real Git and the output is the same as real
  Git's, but **they do not touch the files on your computer**. The exercises
  work even if Git is not installed on your computer.
- The terminal opens on the computer of an imaginary user, Ada Lovelace:
  the home folder is `/home/ada`. On your own computer this path is
  different (`/c/Users/yourname` in Git Bash); the commands are the same.
- The ↑ key brings back the previous command, so you don't have to type the
  same command again.
- If you break something, the **Start over** button puts the exercise back
  as it was.

## A first taste: `git init`

Turning a folder into a repository is one command: `git init`
(*initialize*). First let's see that Git is installed with `git --version`:

```text
~/notes $ git --version
git version 2.55.0
~/notes $ ls -a
.  ..
~/notes $ git init
Initialized empty Git repository in /home/ada/notes/.git/
~/notes (main) $ ls -a
.  ..  .git/
```

Three things changed:

1. Git said it created an empty repository in the folder.
2. `ls -a` now shows the hidden `.git/` folder; the history will live there.
3. **`(main)`** appeared at the end of the prompt. It says you are on the
   **branch** named `main`. We will look at branches in detail later; for
   now, read it as "I am inside a repository".

The repository is still empty: there is no commit yet. We will make the
first commit two sections from now; first we will install Git on your real
computer and set it up.

## Summary

- **Version control** keeps the history of a project: what, who, when, why.
- In Git each step of the history is a **commit**; every commit has a
  message.
- **Git** is the program on your computer, **GitHub** is a site where
  repositories live on the internet.
- The folder Git watches is a **repository**; the history is in the hidden
  `.git` folder.
- In the terminal you move around with `pwd`, `ls`, `cd`, `mkdir`, `echo`,
  `cat` and `rm`.
- `git init` turns a folder into a repository.
