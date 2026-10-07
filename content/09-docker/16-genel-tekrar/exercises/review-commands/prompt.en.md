**What to do:** write five commands in `commands.sh`, in order:

1. Build an image tagged `notes` from this folder.
2. Run `notes` in the background, named `api`: the computer's 8095 to the
   container's 8000, the `notes-data` volume on `/data`.
3. Follow `api`'s log live.
4. Start the Compose services in the background, building their images.
5. Remove the Compose services together with their volumes.
