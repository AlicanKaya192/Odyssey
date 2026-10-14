This workflow works, but its steps have no names; finding which one failed in the logs is hard.

Add a `name:` to each step, above its `uses`/`run` line and in the same column. The names should be exactly:

- `Get the code`
- `Set up Python`
- `Install dependencies`
- `Run tests`

The step starts with `- name: ...`, and `uses:` or `run:` continues on the next line, in the same column as `name`.
