The Dockerfile and `.env` are ready. Write `compose.yaml`.

**What to do:** a service called `web` that:

1. Builds the image from this folder (`build: .`).
2. Sends the computer's 8095 to the container's 8000 (in quotes).
3. Takes its environment variables from the `.env` file.
4. Mounts the volume called `notes-data` on `/data`; also define the volume
   at the bottom.
5. `restart: unless-stopped`.

Odyssey will start the service, wait for it to become `healthy` and look at
`/stats`:

```
{"notes": 0, "starts": 1}
```
