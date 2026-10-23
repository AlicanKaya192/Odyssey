Greet every name on the command line on its own line, as `hello, David`. Do not greet the program's name: skip it with a slice (`sys.argv[1:]`). With no names, `sys.exit("Too few arguments")`.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py David Carter Rongxin
hello, David
hello, Carter
hello, Rongxin
```
