In PowerShell the current folder is `${PWD}`.

**What to do:** write three commands in `commands.sh`, in order:

1. Mount the current folder on `/app`, make the container's working folder
   `/app` (`-w`) and run `python app.py` in the `python:3.13-slim` image;
   remove it when done.
2. Run the `app` image with the `config` sub-folder of the current folder
   mounted **read-only** on `/config`; remove it when done.
3. Mount the `notes` volume on `/data` and the current folder on `/backup`,
   and run `tar czf /backup/notes.tgz -C /data .` in `alpine:3.22`; remove it
   when done. (You can split the long line with `` ` ``.)
