You will see the difference between `"w"` and `"a"` with your own eyes.

**What you need to do:**

1. Open `log.txt` **from scratch** and write the line `start` into it.
2. Open the same file in **append** mode and add the line `step one`.
3. Add the line `step two`, again in append mode.
4. Read the file and take the lines into a list called `entries`.
5. Print the number of lines first, then the list.

**Expected output:**

```
3
['start', 'step one', 'step two']
```

If you use `"w"` in steps two and three, the earlier lines are deleted and you
end up with a single line. That is exactly where the difference lies.

> The append mode is `"a"`.
