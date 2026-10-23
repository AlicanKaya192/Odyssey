The lesson collects the syntax of the ten weeks; this note collects the error
messages. When a program fails, read the **last line** of the message: first
the type of error, then what happened. The messages were measured on this
computer with Python 3.14.

## Common errors

| Last line | What happened | Week |
|---|---|---|
| `NameError: name 'x' is not defined` | a name that was not defined (or was misspelled) | 0 |
| `TypeError: can only concatenate str (not "int") to str` | joining a string and a number with `+`; `str(n)` or an f-string | 0 |
| `ValueError: invalid literal for int() with base 10: 'cat'` | a string that can't be turned into a number; `try`/`except ValueError` | 3 |
| `IndexError: list index out of range` | a position that is not in the list | 2 |
| `KeyError: 'b'` | a key that is not in the dictionary; `in` or `.get` | 2 |
| `FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'` | a file that does not exist | 6 |
| `AttributeError: 'str' object has no attribute 'append'` | a method or attribute that type does not have | 8 |
| `UnboundLocalError: cannot access local variable ...` | assigning to a global variable in a function; `global` | 9 |
| `StopIteration` | the generator (iterator) has run out of values | 9 |

## Reading a traceback

The traceback of the bank program from week 9:

```text
Traceback (most recent call last):
  File "bank.py", line 19, in <module>
    main()
    ~~~~^^
  File "bank.py", line 5, in main
    deposit(100)
    ~~~~~~~^^^^^
  File "bank.py", line 11, in deposit
    balance += n
    ^^^^^^^
UnboundLocalError: cannot access local variable 'balance' where it is not
associated with a value
```

- The traceback goes from outside in: at the top, where the program started;
  at the bottom, the line where the error came out.
- Look at the bottom line from your own file; the mistake is usually there, or
  in the value that reached it.
- The `^^^^` marks show which part of the line failed.

## Which tool when

| Job | Tool |
|---|---|
| The user may type something invalid | `while True` + `try`/`except` |
| The program was used wrongly | `sys.exit("Usage: ...")` |
| Your own function got invalid input | `raise ValueError("...")` |
| The format of a value | `re.fullmatch(r"...", s)` |
| Data and behavior that belong together | a class |
| That a function works correctly | `pytest`, `assert` |
| Several options on the command line | `argparse` |
| Very large data, or data of unknown length | a generator, `yield` |
