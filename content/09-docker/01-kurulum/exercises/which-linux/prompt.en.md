See that the container has its own files. On every Linux the file
`/etc/os-release` holds the system's name and version; `cat` is the command
that prints a file's contents.

**What to do:** write a Dockerfile that starts from the `alpine:3.22` image
and runs the command `cat /etc/os-release` when it runs.

The line `NAME="Alpine Linux"` will appear in the output: even though you
are on Windows, the container sees Alpine Linux's files.
