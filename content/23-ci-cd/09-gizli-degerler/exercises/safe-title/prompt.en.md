This job prints the PR's title and branch name, but both are written straight into the `run:` line with `${{ }}`: whoever opens the PR can put a command in the title or the branch name. Give both through environment variables:

- The title in the `TITLE` variable, the command `echo "Checking PR $TITLE"`.
- The branch name in the `BRANCH` variable, the command `echo "From branch $BRANCH"`.
