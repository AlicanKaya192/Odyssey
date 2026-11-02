The most common mistakes when you start working with pipes.

## Writing a file on the right of a pipe

`sort names.txt | top.txt` does not work: the shell looks for a program named
`top.txt`. A **command** always stands on the right of a pipe. To write into a
file, use `>`: `sort names.txt > top.txt`.

## Giving a file name through a pipe

`echo names.txt | cat` does not show what is inside the file; it prints the
text `names.txt`. A pipe carries text. If you want the file to be opened, give
the name as an argument: `cat names.txt`.

## Piping into a command that does not read input

`ls`, `cd`, `mkdir` and `rm` ignore text coming from a pipe. `echo docs | ls`
lists the folder you are in, not `docs`.

## Errors that are not counted

`ls a nope | wc -l` does not count the error line, because the error leaves
through stderr and does not enter the pipe. To count it, use
`ls a nope 2>&1 | wc -l`.

## Mixing up the order

`tail -n 2 poem.txt | cat -n` numbers the last two lines as **1 and 2**; `cat -n`
only sees the two lines it receives. For the real numbers, number first and
cut afterwards: `cat -n poem.txt | tail -n 2`.

## Writing it all at once

If you write and run a long chain in one go, finding the wrong step gets
harder. Run it after each `|`, look at the output, then add the next step.
