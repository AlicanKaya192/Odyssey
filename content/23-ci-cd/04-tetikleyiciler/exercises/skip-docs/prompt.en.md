The tests run for nothing when only the documentation changes. Add ignored paths to both `push` and `pull_request`:

- `docs/**` (the documentation folder)
- `**.md` (Markdown files in every folder)

Keep the branch filters as they are.
