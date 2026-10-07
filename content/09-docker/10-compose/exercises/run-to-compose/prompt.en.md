Turn this long command into compose.yaml:

```text
docker run -d -p 8091:8000 -e APP_ENV=production -e DB_PATH=/data/app.db `
  -v appdata:/data --restart unless-stopped app
```

**What to do:** a service called `web`; the image from the Dockerfile in this
folder. The port, the two environment variables, the volume and the restart
rule should be the same as in the command. Define the named volume at the
bottom of the file too.

Odyssey will bring the service up and send it a request; the reply must be
`{"env": "production", "db": "/data/app.db"}`.
