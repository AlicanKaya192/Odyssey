This workflow runs the tests but has no quality gates.

Replace the comment with three steps that come **before** the tests:

- `pip install ruff`
- `ruff check .` (lint)
- `ruff format --check .` (format, without changing the files)

Fast gates first: the ruff steps must come before the `pip install -r requirements.txt` step.
