The STATUS column in the output of `docker ps -a` tells you which stage a
container is at and how it ended. It is the first place to look when
debugging.

## States

| State | Meaning |
|---|---|
| **Created** | Created but never run. |
| **Up 5 minutes** | Running (for 5 minutes). |
| **Exited (0) 2 minutes ago** | Finished; the number in brackets is the exit code. |
| **Restarting** | It crashed and Docker is restarting it (if there is a restart rule). |
| **Paused** | Frozen with `docker pause`. |

## What is an exit code?

Every program leaves a number for the operating system when it ends: the
**exit code**. `0` means "all is well"; any other number is a problem. In
Python, if the program ends with an uncaught error, the exit code is `1`;
if you write `sys.exit(3)`, it is `3`.

A container's exit code is the exit code of its main program.

## Common codes

| Code | What happened? | Where to look? |
|---|---|---|
| **0** | The program finished without problems. | — |
| **1** | The program ended with an error (an uncaught error in Python). | `docker logs name` |
| **125** | Docker could not start the container at all (wrong option, name conflict). | The command itself |
| **126** | The command was found but could not be run (no permission). | File permissions |
| **127** | The command was not found (a typo, or not in the image). | The command's name |
| **137** | The program was killed by force (`docker kill`, out of memory or the `stop` time ran out). | Memory, `stop` |
| **143** | The program received the shutdown request and closed properly (`docker stop`). | — |

The numbers 137 and 143 are not random: `128 + signal number`. Signal 9 is
"die now" (SIGKILL), signal 15 "please shut down" (SIGTERM).

## Try it yourself

```text
docker run --rm alpine:3.22 sh -c "exit 3"
echo $LASTEXITCODE
```

In PowerShell the exit code of the last command is in the `$LASTEXITCODE`
variable; the output is `3`. (`sh -c "..."` runs the line in quotes with the
shell.)

```text
docker run --rm alpine:3.22 no-such-command
```

This one ends with 127; Docker also prints the reason (command not found).

## Which when?

- If the container ends **immediately** and the code is not 0 → look at
  what the program printed last with `docker logs`.
- If the code is between 125 and 127 → the problem is not the program but
  the **command**.
- If the code is 137 → the container was killed; the memory limit or the
  `stop` time.
