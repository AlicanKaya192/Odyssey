**What to do:** write four commands in `commands.sh`, in order:

1. Run the `site` image in the background, named `web`; the computer's 8080
   should go to the container's 8000.
2. Show where `web`'s ports are published.
3. Run `site` named `local`; the port should be reachable only from this
   computer: 9000 of `127.0.0.1` → the container's 8000.
4. Run `site` named `random`; the `EXPOSE`d ports should be published to
   random free ports.
