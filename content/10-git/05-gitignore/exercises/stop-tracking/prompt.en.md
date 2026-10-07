`config.local.json` is everyone's own setting but was committed by mistake. It shows up in `git status` after every change.

- Write the file into `.gitignore`.
- Make Git stop tracking it, but **don't delete** the file.
- Commit with the message `Stop tracking local config`.
