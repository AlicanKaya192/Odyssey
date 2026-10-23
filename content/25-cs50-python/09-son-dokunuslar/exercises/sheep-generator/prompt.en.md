The `sheep(n)` in the starter code builds the whole flock in a list and returns it all at once; with a very large `n` the memory would run out. Turn it into a **generator**: with no list and no `append`, have it hand out each line one at a time with `yield`. `main` does not change; the output stays the same (`1 sheep`, `2 sheep`, ...).

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
What's n? 3
1 sheep
2 sheep
3 sheep
```
