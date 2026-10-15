Add a `title` job that checks PR titles:

- It should run only in PRs: `if: github.event_name == 'pull_request'`. The machine is `ubuntu-latest`.
- It should get the code, then run `python scripts/check_title.py "$TITLE"`; the `TITLE` environment variable is `${{ github.event.pull_request.title }}`.
- It should also run when the title is fixed: `types: [opened, edited, synchronize, reopened]` under `pull_request`.

The title must not be written straight into the `run:` line.
