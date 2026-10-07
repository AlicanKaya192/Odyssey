docker run --rm -v ${PWD}:/app -w /app python:3.13-slim python app.py
docker run --rm -v ${PWD}/config:/config:ro app
docker run --rm -v notes:/data -v ${PWD}:/backup alpine:3.22 `
  tar czf /backup/notes.tgz -C /data .
