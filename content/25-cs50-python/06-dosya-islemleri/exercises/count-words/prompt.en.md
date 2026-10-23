Take a file name from the command line (`python cozum.py notes.txt`) and print the number of lines and words in it, as `4 lines, 10 words`. A blank line is still a line; words are separated by whitespace (`split()`). With the wrong number of arguments, `sys.exit("Usage: python cozum.py FILE")`; if the file does not exist, `sys.exit("File does not exist")`.

Example run (the prompt can say anything you like; only your output and your file are checked):

```text
$ python cozum.py notes.txt
4 lines, 10 words
```
