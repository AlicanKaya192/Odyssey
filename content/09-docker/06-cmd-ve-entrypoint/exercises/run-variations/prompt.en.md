**What to do:** write four commands in `commands.sh`, in order:

1. Run the `greet` image with the argument `Ada`; remove it when done.
2. Go inside the `greet` image with `sh`: change `ENTRYPOINT` once, give a
   keyboard and terminal, remove it when done.
3. Run the `worker` image with the starter that passes signals on (`--init`),
   in the background, named `worker`.
4. Stop the `worker` container; give it **30 seconds** to shut down.
