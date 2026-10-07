**What to do:** write two commands in `commands.sh`:

1. Run the `app` image in the background, named `api`: a read-only file
   system, all special powers dropped (`--cap-drop ALL`), a memory limit of
   `512m`.
2. Run the `id` command in the `app` image as user number 1000; remove it
   when done.

Do not use `--privileged`.
