A module is ready in the exercise's folder, `shapes.py`:

```python
def square(n):
    return n * n


def cube(n):
    return n * n * n
```

Import `square` and `cube` from it (`from shapes import ...`). Take exactly one integer from the command line and print its square and cube on one line. With the wrong number of arguments, `sys.exit("Usage: python cozum.py NUMBER")`.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py 3
9 27
```
