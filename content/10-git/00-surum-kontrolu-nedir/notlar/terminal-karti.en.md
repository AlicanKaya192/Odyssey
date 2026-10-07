The shell commands you will use most while working with Git. They are the
same in Git Bash, on Mac and on Linux.

## Seeing where you are

| Command | What it does |
|---|---|
| `pwd` | The full path of the folder you are in. |
| `ls` | What is in the folder; folders end with `/`. |
| `ls -a` | Including hidden ones (`.git/` shows up here). |

## Moving around

| Command | What it does |
|---|---|
| `cd notes` | Go into the `notes` folder. |
| `cd notes/site` | Go down two levels at once. |
| `cd ..` | Go up one folder. |
| `cd ../..` | Go up two folders. |
| `cd ~` or just `cd` | Go back to your home folder. |

In paths, `~` is your home folder, `.` is the folder you are in and `..` is
the one above it.

## Creating and deleting

| Command | What it does |
|---|---|
| `mkdir notes` | Create a folder. |
| `mkdir -p a/b/c` | Create nested folders in one go. |
| `touch a.txt` | Create an empty file (leaves an existing one alone). |
| `echo "text" > a.txt` | Write the file **from scratch**. |
| `echo "text" >> a.txt` | Add to the **end** of the file. |
| `cat a.txt` | Print the file. |
| `mv a.txt b.txt` | Rename or move. |
| `rm a.txt` | Delete the file. |
| `rm -r old` | Delete a folder with everything inside. |

## A few conveniences

- **↑ / ↓**: walk through previous commands.
- **Tab**: completes file and folder names (in a real terminal; not in
  Odyssey's practice terminal).
- **`clear`** or **Ctrl+L**: clears the screen, deletes nothing.
- **`command1 && command2`**: runs the second only if the first succeeded.
  `mkdir notes && cd notes` is a common pattern.

## Watch out

- `rm` does not send to the recycle bin; a deleted file is gone.
- `>` wipes the file's old content without asking.
- Put names with spaces in quotes: `cd "my notes"`. Better: don't use spaces
  in file and folder names.
