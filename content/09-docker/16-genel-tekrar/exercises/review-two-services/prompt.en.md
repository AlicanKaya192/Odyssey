The `api` folder has the notes API from the Packaging section (its
Dockerfile has a `HEALTHCHECK`), and the `client` folder has a program that
sends it one request and prints the result. Write `compose.yaml`.

**What to do:**

1. The `api` service: built from `./api`, with the `notes-data` volume
   mounted on `/data`.
2. The `client` service: built from `./client`, starting **when api is
   healthy** (`condition: service_healthy`).
3. Define the `notes-data` volume at the bottom.

If `client` starts before api is ready, it fails with `Connection refused`.

**Expected output (client):**

```
notes: 0 starts: 1
```
