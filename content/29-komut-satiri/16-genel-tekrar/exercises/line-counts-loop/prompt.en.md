Build a `for` loop that writes one line for each `.log` file in `inbox`. The lines should look like this:

```text
inbox/a.log: 2
inbox/b.log: 3
```

- The number is the file's line count; to avoid printing the name again, `wc -l < file`.
- Write the whole output of the loop into `sizes.txt`.
