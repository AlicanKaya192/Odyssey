An example Dockerfile for a Python application that brings together
everything you learnt in this path. Use it as a starting point in your own
projects.

```dockerfile
# 1) A pinned, small, official base
FROM python:3.13-slim

# 2) Good defaults for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3) A non-root user
RUN useradd --create-home --uid 1000 app

WORKDIR /app

# 4) Dependencies first (cache), pip without a cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Then the code, owned by the user
COPY --chown=app:app . .

# 6) The data folder to be written belongs to the user
RUN mkdir -p /data && chown app:app /data
VOLUME /data

# 7) Switch to the user
USER app

# 8) A documented port, a healthcheck, the exec form
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health')"
CMD ["python", "app.py"]
```

What should sit next to it:

- `.dockerignore`: `.git`, `.venv`, `**/__pycache__`, `.env`, `data/`.
- `.env.example`: the names of the settings, with fake values.

When running:

```text
docker run -d --name app -p 8000:8000 --env-file .env -v appdata:/data `
  --memory 512m --cap-drop ALL app
```
