It might be interesting to know how many lines of code a program has, not counting comments and blank lines.

Implement a program that expects **exactly one** command-line argument, the name (or path) of a Python file, and outputs the number of lines of code in it, excluding comments and blank lines. A line that starts with `#`, optionally preceded by whitespace, is a comment; a docstring is **not** a comment, so it counts; a line with only whitespace is blank.

If there is not exactly one argument (`Too few command-line arguments` or `Too many command-line arguments`), the name does not end in `.py` (`Not a Python file`), or the file does not exist (`File does not exist`), exit via `sys.exit`. (In CS50 the file is `lines.py`.)

Hint: `str.lstrip` and `str.startswith`; `open` can raise a `FileNotFoundError`.

## How to test

The cases CS50 gives; Odyssey runs each one in a separate folder and compares your output and the file you write.

- No input → output (nothing) (exit code 1)
- Command `python cozum.py hello.py goodbye.py` → output (nothing) (exit code 1)
- Command `python cozum.py invalid_extension.txt` → output (nothing) (exit code 1)
- Command `python cozum.py non_existent_file.py` → output (nothing) (exit code 1)
- Command `python cozum.py hello.py` → output `2`
- Command `python cozum.py grade.py` → output `11`
