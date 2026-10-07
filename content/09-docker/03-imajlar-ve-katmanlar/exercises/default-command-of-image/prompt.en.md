`docker image inspect python:3.13-slim --format "{{.Config.Cmd}}"` shows
`[python3]`: this image's default command is interactive Python. Your own
`CMD` line takes its place.

**What to do:** write a `CMD` that runs this code with `python -c`:

```python
import sys; print(sys.version_info[:2])
```

`sys.version_info[:2]` gives Python's major and minor version as a tuple.

**Expected output:**

```
(3, 13)
```
