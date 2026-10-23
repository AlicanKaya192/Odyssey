Ask the user for a web address and remove the `http://` or `https://` at its start, and the `www.` that may follow, with `re.sub`; print the rest. A `www.` in the middle of the address stays.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
URL: https://www.cs50.harvard.edu/python
cs50.harvard.edu/python
```
