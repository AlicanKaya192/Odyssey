This Dockerfile writes `CMD` in the shell form: the container's process
number 1 is `sh`, not Python, and the signal from `docker stop` does not reach
the program.

**What to do:** turn the last line into the **exec form** running the same
command. The command has three parts: `python`, `report.py`, `--short`.

**Expected output:**

```
report mode: short
```
