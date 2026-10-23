Write a program that takes the name of a CSV file from the command line: `python cozum.py students.csv`. The file's header row has the columns `name` and `house` (in any order). The program prints each house in alphabetical order with the number of students in it: `Gryffindor: 3`.

In problem cases it exits with `sys.exit`: with no argument, `Too few command-line arguments`; with more than one, `Too many command-line arguments`; if the name does not end in `.csv`, `Not a CSV file`; if the file does not exist, `File does not exist`. The folder has `students.csv` and `club.csv`, whose columns are in the opposite order.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py students.csv
Gryffindor: 3
Hufflepuff: 1
Ravenclaw: 2
Slytherin: 1
```
