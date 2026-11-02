Make `ll` run `ls -l`, and make that hold in every new terminal too.

- Add this line to the **end** of `~/.bashrc` (the other lines in the file must not be erased):

```text
alias ll='ls -l'
```

- Make the current terminal read the file, and try it with `ll names.txt`.
