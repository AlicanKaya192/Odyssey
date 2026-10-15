The pipeline runs only on pushes to `main`; PRs are merged without being tested. Add two events to the triggers:

- PRs opened against `main`: `pull_request`, `branches: [main]`.
- The merge queue: `merge_group`.
