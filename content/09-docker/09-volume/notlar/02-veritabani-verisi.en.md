One of Docker's most common uses is running a database in a container without
installing it on the computer. Knowing where the data lives is vital here.

## Where do official database images keep their data?

| Image | Data folder |
|---|---|
| `postgres` | `/var/lib/postgresql/data` |
| `mysql` | `/var/lib/mysql` |
| `mongo` | `/data/db` |
| `redis` | `/data` |

The image's Docker Hub page says this ("Where to Store Data"). If no volume
is mounted on that folder, the data stays in the container's writable layer
and goes when the container is removed.

## Example: PostgreSQL

This command is not run in this path (the `postgres` image downloads
separately), but the layout is like this:

```text
docker volume create pgdata
docker run -d --name db -e POSTGRES_PASSWORD=secret `
  -v pgdata:/var/lib/postgresql/data -p 5432:5432 postgres:17
```

- The data is in the `pgdata` volume.
- `docker rm -f db` and running the same command again: the tables are in
  place.
- Moving to a new PostgreSQL version: change the image's tag, the volume is
  the same.

## SQLite: the file in a volume

In small applications the database is a single file (SQLite). The rule is the
same: put the file in a folder mounted on a volume.

```python
import sqlite3

con = sqlite3.connect("/data/app.db")
```

```text
docker run -d -v appdata:/data app
```

If the file were `/app/app.db`, it would be reset on every update.

## Before removing a volume

- `docker volume rm` and `docker volume prune` delete the data
  irrecoverably.
- Take a backup first (the `tar` command in the Volumes lesson).
- `docker compose down` does not touch volumes; `docker compose down -v`
  removes them (the Compose section).
