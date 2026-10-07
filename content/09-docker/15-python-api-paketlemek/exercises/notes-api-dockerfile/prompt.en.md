The notes API from the lesson (`app.py`) is ready. Write a Dockerfile for it.

**What to do:**

1. Base `python:3.13-slim`, working folder `/app`.
2. **First** copy `requirements.txt` and install the packages with
   `pip install --no-cache-dir -r requirements.txt`.
3. **Then** copy `app.py` and `healthcheck.py`.
4. `EXPOSE 8000`.
5. `CMD` in exec form: `python app.py`.

Odyssey will build and run the image and send a request to `/health`:

```
{"status": "ok"}
```
