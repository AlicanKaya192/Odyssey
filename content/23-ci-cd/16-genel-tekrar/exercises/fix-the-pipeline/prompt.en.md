This workflow has four mistakes we saw in the module. Fix them all:

- Permissions: only read (`contents: read`) instead of `write-all`.
- A time limit: `timeout-minutes: 15` on the `test` job.
- An action without a version: `actions/checkout` → `actions/checkout@v4`.
- Code injection: the PR title must not be written straight into the `run:` line; the command is `echo "Testing $TITLE"`, the `TITLE` environment variable is `${{ github.event.pull_request.title }}`.
