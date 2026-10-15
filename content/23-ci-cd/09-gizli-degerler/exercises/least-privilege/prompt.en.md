This pipeline tests and creates a GitHub release when a tag arrives, but no permissions are written; `GITHUB_TOKEN` is as broad as the repository's default. Narrow the permissions:

- At the top of the workflow, `contents: read` for all jobs.
- Only the `release` job should get `contents: write` (to create the release).
