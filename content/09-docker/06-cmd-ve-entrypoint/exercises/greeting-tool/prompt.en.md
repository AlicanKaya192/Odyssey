Turn the image into a command-line tool: `docker run --rm greet Ada` should
greet Ada, and with no argument, the world.

**What to do:**

1. With `ENTRYPOINT`, `python greet.py` should always run.
2. With `CMD`, the default argument should be `World`.

Both in the bracketed form. Odyssey will run the container twice: with no
argument and with `Ada Lovelace`.

**Expected outputs:**

```
Hello, World!
Hello, Ada Lovelace!
```
