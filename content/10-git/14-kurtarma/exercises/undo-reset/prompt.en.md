Someone typed `git reset --hard HEAD~2` and the `Two` and `Three` commits seem gone.

- Find the state before the reset with `git reflog`.
- Take `main` back there: all three commits must be visible again.
