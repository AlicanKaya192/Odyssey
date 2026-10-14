The repository has a `test_app.py` and a `requirements.txt` (in the other tabs, read-only).

The file `.github/workflows/ci.yml` downloads the code and installs Python, but it never runs the tests. Replace the comment with two steps:

- a step that runs `pip install -r requirements.txt`
- a step that runs `python -m pytest`

A step that runs a command is written `- run: command`. Watch the indentation: the new steps start in the same column as the other `- uses:` lines.
