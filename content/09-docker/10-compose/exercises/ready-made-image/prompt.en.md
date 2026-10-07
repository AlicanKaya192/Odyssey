Not every service needs a Dockerfile; a ready-made image can be used too.

**What to do:** a service called `worker`:

1. It uses the ready-made `alpine:3.22` image (`image`).
2. Its command is `sh -c "echo hello from compose && sleep 300"` (`command`,
   three parts in the bracketed form).

Odyssey will bring the service up and check that it is running and that its
log says `hello from compose`.
