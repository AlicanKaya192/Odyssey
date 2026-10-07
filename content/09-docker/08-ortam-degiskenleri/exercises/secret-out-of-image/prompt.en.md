This Dockerfile bakes the API key into the image with `ENV`: anyone who gets
the image can see it with `docker image inspect`.

**What to do:** get the key out of the image. `app.py` already reads the key
from an environment variable; the key will be given when running.

Odyssey will check that `API_KEY` is not in the image and run the container
with `-e API_KEY=test-key-123`.

**Expected output:**

```
key loaded: 12 chars
```
