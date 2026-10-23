Draw the staircase Mario climbs: right-aligned, one more brick on each row. For a height of 3:

```text
  #
 ##
###
```

Let a function called `get_height` get the height: it keeps asking until a number between 1 and 8 (both included) arrives and **returns** it. The spaces at the start of the rows are checked too; no spaces at the end.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Height: 3
  #
 ##
###
```
