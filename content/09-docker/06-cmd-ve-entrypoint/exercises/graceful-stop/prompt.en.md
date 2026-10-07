`worker.py` runs in a loop and should print `saved, bye` and close when it is
stopped. Right now it does not catch SIGTERM: when the signal arrives the
program dies at once and the last line is never printed.

**What to do:** catch SIGTERM in `worker.py`:

1. Import the `signal` module.
2. Write a function that sets the `running` variable to `False`
   (`global running`).
3. Connect it with `signal.signal(signal.SIGTERM, function)`.

Odyssey will start the program, send it SIGTERM a second later and look at
how the program ended.

**Expected output:**

```
saved, bye
exit=0
```
