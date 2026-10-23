Write a program that takes two options from the command line with argparse:

- `-n` or `--number`: how many times (an integer, default 1)
- `-s` or `--sound`: which sound (default `meow`)

The program prints the sound that many times, one per line. The options may come in any order. With an invalid number like `-n dog`, argparse should print its own message and end the program with code 2; don't write that yourself, `type=int` does it.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py -n 2 -s purr
purr
purr
```
