**What to do:** write five commands in `commands.sh`, in order:

1. List all containers, finished ones included.
2. Show the last 20 lines of the `web` container's log.
3. Go inside the `app` image with `sh`: change `ENTRYPOINT`, give a keyboard
   and terminal, remove it when done.
4. Copy the file `/app/error.log` from the `web` container to this folder
   (`.`).
5. Build the `app` image without the cache, showing all output as plain
   text.
