Rules to follow when choosing file and folder names. Names that follow them
need no quotes, no escaping and bring no surprises in the terminal.

## Safe names

- Use lower-case letters, digits, `-`, `_` and `.`: `monthly-report.txt`,
  `data_2026.csv`.
- **Do not use spaces.** If you do, you need quotes every time:
  `cat "my notes.txt"`.
- Letters with accents (`é`, `ş`, `ü`) technically work, but not every
  keyboard can type them and some tools have trouble with them. Plain English
  letters are easier in file names.

## Upper and lower case

For Linux, `Report.txt`, `report.txt` and `REPORT.TXT` are three different
files. Windows and macOS usually treat them as the same; this is where
problems start when you move a project between the two. The easiest is to
always use lower case.

## Extensions

| Extension | Usually |
|---|---|
| `.txt` | Plain text |
| `.md` | Markdown text |
| `.csv` | Comma-separated table |
| `.sh` | Bash script |
| `.py` | Python code |
| `.log` | Log file |

An extension is not required; on Linux a text file named `notes` with no
extension is fine. The extension is a hint for the person and the program
that will open the file.

## Hidden names

A name starting with a dot is hidden: `.bashrc`, `.gitignore`, `.env`. Hidden
files usually hold settings; `ls -a` shows them.

## Characters to avoid

`* ? [ ] $ & ; | < > ( ) ' " \` and `!` have a meaning for the shell. If a
name contains one of them, commands may do something you did not expect. Do
not use them in names.
