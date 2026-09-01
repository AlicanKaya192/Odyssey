You will write your first file and then read the same file back.

**What you need to do:**

1. Open a file called `names.txt` and write three lines into it:

```
Ada
Alan
Grace
```

2. Open the same file again and take the lines into a list.
3. Hold that list in a variable called `names`.
4. Print how many lines there are, then the list itself.

**Expected output:**

```
3
['Ada', 'Alan', 'Grace']
```

Note: `write` does not move to the next line on its own; you have to write
`\n`.

> Always open a file with `with open(...) as file:` and do not forget
> `encoding="utf-8"`. For a list of lines you can use
> `file.read().splitlines()`.
