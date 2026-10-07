A container has a single main program. To run several commands one after
another, you hand them to a shell: `sh -c "command1 && command2"`. `&&` means
"run the next one if the previous one succeeded".

**What to do:** write the `CMD` line: with `sh -c`, first `echo start`, then
`echo done` should run. In the bracketed form there are three parts: `"sh"`,
`"-c"` and the whole line in quotes.

This exercise really builds and runs the image (Docker must be open).

**Expected output:**

```
start
done
```
