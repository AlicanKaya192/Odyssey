# Terminal, Shell and Prompt

Most of the time you use a computer with the mouse: you double-click a folder,
you drag and drop a file. This way of working is called a **graphical
interface**. There is also a way to do the same jobs by **typing**: you write
a command and the computer does it. This is called the **command line**.

In this path we learn the command line from scratch. First you will see why it
is useful, then the parts of the terminal, and finally your first commands.

## Why the command line?

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Graphical interface</h4><p>You click with the mouse</p><p>Only the buttons you see</p><p>You repeat the same job 100 times by hand</p></div>
    <div class="ok"><h4>Command line</h4><p>You type the command</p><p>Every program, every option</p><p>Write it once, repeat it as often as you like</p></div>
  </div>
  <figcaption>Both do the same job; the command line wins for repeated and remote work.</figcaption>
</figure>

A graphical interface is comfortable for doing a job **once**. But think about
these situations:

- You need to rename 300 photos one by one.
- You are working on a server (another computer on the internet) and it has no
  screen, no mouse and no windows.
- Every morning you repeat the same five steps.

On the command line these jobs become one line, or a **script** of a few lines
(a small file with commands written in order). Git, Docker, Python
environments, servers, data science tools: all of them are used from the
command line first. Graphical tools often run these same commands behind the
scenes.

## Terminal and shell: two different things

These two words should not be mixed up.

- The **terminal** is the **window** that shows the text you type and the
  answer that comes back.
- The **shell** is the **program** that reads the line you typed, understands
  it and runs it.

<figure class="fig">
  <div class="flow">
    <span class="node">You<br><small>type on the keyboard</small></span><span class="arrow">→</span>
    <span class="node">Terminal<br><small>the window</small></span><span class="arrow">→</span>
    <span class="node acc">Shell (bash)<br><small>reads and runs the command</small></span><span class="arrow">→</span>
    <span class="node">Operating system<br><small>files, programs</small></span>
  </div>
  <figcaption>The terminal is only the window that shows what you type. The program that understands and runs the command is the shell.</figcaption>
</figure>

The most common shell on Linux is called **bash**. On macOS the default shell
is *zsh*, but almost all commands are the same. On Windows you can use bash in
two ways: **Git Bash**, which comes with Git, or **WSL**, which runs a real
Linux inside Windows. Everything you learn in this path works in all three.

> The terminal in Odyssey behaves like real bash but does not touch the files
> on your computer: the files and folders all live inside Odyssey, on a small
> Linux computer of your own. If you break something, the **Start over**
> button is enough.

## The prompt

When the terminal opens, you see something like this at the start of a line:

```text
~ $
```

This is called the **prompt**. The prompt tells you two things: which folder
you are in right now, and that the shell is waiting for a command. You type
what comes after the `$` sign.

<figure class="fig">
  <pre><code class="language-text">~/notes $ ls -a docs</code></pre>
  <div class="anat">
    <div class="anat-row"><span>~/notes</span><span>The folder you are in right now. <code>~</code> means your home folder.</span></div>
    <div class="anat-row"><span>$</span><span>The end of the prompt: the shell is waiting for a command.</span></div>
    <div class="anat-row"><span>ls</span><span>Command: the name of the program to run.</span></div>
    <div class="anat-row"><span>-a</span><span>Option: changes how the command works. Starts with a dash.</span></div>
    <div class="anat-row"><span>docs</span><span>Argument: what the command works on (here a folder).</span></div>
  </div>
  <figcaption>Every command line has the same order: the command, then options, then arguments, separated by spaces.</figcaption>
</figure>

The `~` (tilde) sign means your **home folder**: the folder where your own
files live. In this terminal the full name of your home folder is
`/home/ada`. On a real Linux the prompt is usually a bit longer and shows the
user name and the computer name as well: `ada@laptop:~$`. The meaning is the
same.

> In the lesson examples, a line that starts with `$` is a command **you
> type**; the lines under it are the command's answer. You do not type the `$`.

## First commands

Let's start with three commands:

- `pwd` (*print working directory*): prints the full path of the folder you
  are in.
- `ls` (*list*): lists what is in the folder you are in.
- `echo`: writes back the text you give it, exactly as it is.

```text
~ $ pwd
/home/ada
~ $ ls
notes/  projects/  todo.txt
~ $ echo Hello
Hello
~ $ echo "Hello, terminal"
Hello, terminal
```

In the `ls` output, names that end with `/` are **folders**, the others are
**files**. (This terminal and Git Bash show folders this way; some systems
use colours instead.)

## The shape of a command: command, option, argument

A command line always has the same order:

```text
command  options  arguments
```

- **Command**: the name of the program to run (`ls`).
- **Option** (flag): changes how the command works. It starts with a dash:
  `-a`.
- **Argument**: what the command works on: a file, a folder, some text.

There **must be a space** between them. `ls -a` is two parts; if you type
`ls-a`, the shell looks for a command called `ls-a` and does not find it.

`ls -a` also shows hidden files. On Linux, a file or folder whose name starts
with a dot is **hidden**; plain `ls` does not show it.

```text
~ $ ls notes
plan.txt
~ $ ls -a notes
./  ../  .draft  plan.txt
~ $ ls -a
./  ../  .bashrc  notes/  projects/  todo.txt
```

`ls -a` added two strange names: `./` is the folder you are in, `../` is the
folder above it. We will look at both in detail in the next section. In the
home folder a `.bashrc` showed up as well: bash's settings file. Its name
starts with a dot, so plain `ls` did not show it.

Options can be combined: instead of `ls -a -l` you can write `ls -al`. We will
use this a lot in later sections.

## Reading error messages

The terminal does not get angry when you make a mistake; it tells you what
happened. Reading the error message is half of the job.

```text
~ $ Ls
bash: Ls: command not found
~ $ sl
bash: sl: command not found
~ $ ls nope
ls: cannot access 'nope': No such file or directory
```

- `command not found`: there is no such command. Usually it is a typo.
- On Linux **upper and lower case are different**: `Ls` and `ls` are not the
  same thing. The same goes for file names: `Notes.txt` and `notes.txt` are
  two different files.
- `No such file or directory`: the command is right, but the file or folder
  you gave it is not there.

## Spaces and quotes

The shell splits a line into parts at **spaces**. So several spaces in a row
are a single separator for the shell:

```text
~ $ echo Hello     world
Hello world
~ $ echo "Hello     world"
Hello     world
```

In the first command `echo` received two separate arguments (`Hello` and
`world`) and joined them with one space. In the second, the quotes made the
text **a single argument**; the spaces inside stayed as they were. We will use
quotes a lot more: you also write the name of a file with spaces in quotes.

## History and shortcuts

The shell remembers the commands you type. The **up arrow** brings back the
previous command; press it again for the one before. The `history` command
lists everything you typed in this session, with numbers:

```text
~ $ pwd
/home/ada
~ $ echo hi
hi
~ $ history
    1  pwd
    2  echo hi
    3  history
```

In a real terminal a few more keys make your life easier:

| Key | What it does |
|---|---|
| Up / down arrow | Previous / next command |
| `Ctrl+L` or `clear` | Clears the screen |
| `Ctrl+C` | Stops a running command (it does not copy!) |
| `Tab` | Completes the rest of a command or file name |

In Odyssey's terminal the arrow keys, `Ctrl+L` and `clear` work; there is no
`Tab` completion, you type the names yourself.

## Summary

- The **terminal** is the window, the **shell** (bash) is the program that
  reads and runs commands.
- The **prompt** shows where you are; `~` is your home folder, `$` means
  "waiting for a command".
- A command line: **command, option, argument**, with spaces between them.
- `pwd` where you are, `ls` what is there, `ls -a` including hidden files,
  `echo` prints text.
- Case matters; text with spaces goes in quotes.
- An error message tells you what happened: read it first.
