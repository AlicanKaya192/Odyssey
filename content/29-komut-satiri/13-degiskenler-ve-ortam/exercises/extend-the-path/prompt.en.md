`tools/greet` is an executable program, but when you type `greet` the shell cannot find it.

- Add the `tools` folder (full path `$HOME/tools`) to the **front** of PATH.
- The old folders in PATH must stay; otherwise not even `ls` can be found.
- Then run it by typing just `greet`.
