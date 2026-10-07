`docker ps -a` shows the container as `Exited (127)` and `docker run` prints:

```text
exec: "pyhton": executable file not found in $PATH
```

**What to do:** exit code 127 means "command not found". Fix the command.

**Expected output:**

```
debugged and running
```
