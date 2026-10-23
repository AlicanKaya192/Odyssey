Users sometimes type their name as `Last, First`. Get the name; if it has the form `Last,First` (with zero or more spaces after the comma), turn it into `First Last`. Then print `hello, First Last`. Use capturing groups and the walrus operator (`:=`).

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
What's your name? Malan, David
hello, David Malan
```
