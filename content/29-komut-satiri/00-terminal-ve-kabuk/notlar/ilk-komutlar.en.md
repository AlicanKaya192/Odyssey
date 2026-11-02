The commands of this section, at a glance.

## Commands

| Command | What it does |
|---|---|
| `pwd` | Prints the full path of the folder you are in. |
| `ls` | Lists what is in the folder you are in; folders end with `/`. |
| `ls -a` | Lists including hidden files (`./`, `../`, `.bashrc`). |
| `ls notes` | Lists the inside of `notes` without going there. |
| `echo Hello` | Prints the text. |
| `echo "a    b"` | Keeps the spaces inside the quotes. |
| `history` | The commands you typed in this session, numbered. |
| `clear` | Clears the screen (shortcut `Ctrl+L`). |

## The shape of a command line

```text
ls  -a  notes
│   │   └── argument: what it works on
│   └────── option: how it works (starts with a dash)
└────────── command: which program
```

## Keys

| Key | What it does |
|---|---|
| Up arrow | Brings back the previous command |
| `Ctrl+C` | Stops a running command |
| `Tab` | Completes a name (not in Odyssey's terminal) |

## Common mistakes

| What you see | Why | What to do |
|---|---|---|
| `bash: Ls: command not found` | Capital letter or a typo | Type `ls` in lower case |
| `bash: ls-a: command not found` | No space between command and option | `ls -a` |
| `ls: cannot access 'x': No such file or directory` | No such file or folder | Check the name with `ls` |
| The spaces disappeared | The text has no quotes | `echo "text"` |
