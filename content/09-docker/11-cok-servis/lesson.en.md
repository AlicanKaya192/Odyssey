# Multi-Service Apps: Networks and Dependencies

Real applications are not made of a single container: a web front end, an API
behind it, a database behind that, maybe a cache. Each in its own container,
with its own image. In this section we will learn how services find each
other, which one starts first and what being "ready" means.

## The project

A small shop with two services:

```text
shop/
├── compose.yaml
├── api/          # an API that returns the number of products as JSON
│   ├── Dockerfile
│   └── server.py
└── web/          # a client that sends a request to the API and prints the result
    ├── Dockerfile
    └── client.py
```

```yaml
services:
  api:
    build: ./api
  web:
    build: ./web
```

`build: ./api` → the image comes from the Dockerfile in the `api` folder.

## Services find each other by name

Compose sets up a network for each project (`shop_default`) and connects the
services to it. Inside the network **every service's name is an address**:
the `web` container reaches the API at this address:

```text
http://api:8000/
```

Inside Docker's network there is a small **name resolver** (DNS): it turns
the name `api` into the address of that service's container. You do not need
to know any IP address; even if the container is re-created and its address
changes, the name stays the same.

<figure class="fig">
  <div class="flow">
    <span class="node">web<br><small>http://api:8000</small></span><span class="arrow">→ name resolver →</span>
    <span class="node acc">api<br><small>on the shop_default network</small></span>
  </div>
  <div class="flow">
    <span class="node no">web<br><small>http://localhost:8000</small></span><span class="arrow">→</span>
    <span class="node no">web itself<br><small>Connection refused</small></span>
  </div>
  <figcaption>Services on the same network find each other by name. <code>localhost</code> in every container is that container itself.</figcaption>
</figure>

The output of a real try (`web` sent requests to three addresses; we removed the `web-1  |` prefixes):

```text
http://api:8000/ {'items': 3}
http://localhost:8000/ ERROR <urlopen error [Errno 111] Connection refused>
http://apii:8000/ ERROR <urlopen error [Errno -5] No address associated with hostname>
```

- `api` → worked.
- `localhost` → **refused.** In the `web` container, `localhost` is `web`
  itself; nobody listens on 8000 there. The most common mistake.
- `apii` → **no such name.** A typo; the name resolver could not find it.

## No need to open it to the outside

`api` has no `ports:` line, yet `web` reaches it. Services on the same
network see **all the ports** of each other. `ports:` is only needed for the
service to be reached **from your computer** (from outside); usually only the
web service at the front.

Not opening the database to the outside is a security gain: only the
application on the same network can reach it.

## Start order: `depends_on`

If `web` sends a request to the API as soon as it starts, the API must have
started before it:

```yaml
  web:
    build: ./web
    depends_on:
      - api
```

Compose starts `api` first, then `web`. But careful: this is only the
**start** order. The API container having started does not mean the program
inside it is **ready** to accept requests. Our API prepares for three seconds
when it starts; a request arriving during that time is refused.

## Being ready: `healthcheck`

The command that answers "is it ready?" for a service is the
**healthcheck**. Docker runs this command at intervals; if the command
succeeds (ends with code 0), the service counts as **healthy**.

```yaml
  api:
    build: ./api
    healthcheck:
      test:
        - CMD
        - python
        - -c
        - import urllib.request; urllib.request.urlopen('http://localhost:8000')
      interval: 2s
      timeout: 3s
      retries: 10
      start_period: 2s
```

- `test`: the check command; in list form, each part on its own line (the same as the bracketed form). `python:3.13-slim` has no `curl`; Python's own
  `urllib` was used. Here `localhost` is right: the command runs **in the
  API's own container**.
- `interval`: how many seconds between tries.
- `timeout`: how long one try may last at most.
- `retries`: after how many failures in a row it is called "unhealthy".
- `start_period`: the time at start-up during which failures do not count.

Now let `web` wait for the API to be **healthy**:

```yaml
  web:
    build: ./web
    depends_on:
      api:
        condition: service_healthy
```

```text
 Container shop-api-1 Waiting
 Container shop-api-1 Healthy
 Container shop-web-1 Started
```

`docker compose ps` shows the health status too: `Up 9 seconds (healthy)`.

<figure class="fig">
  <div class="flow">
    <span class="node">api started<br><small>starting</small></span><span class="arrow">→ test succeeds →</span>
    <span class="node ok">api healthy<br><small>healthy</small></span><span class="arrow">→</span>
    <span class="node acc">web starts<br><small>condition: service_healthy</small></span>
  </div>
  <figcaption><code>depends_on</code> alone only gives the order; with the health condition, <code>web</code> waits until the API is really ready.</figcaption>
</figure>

## A network without Compose

You can do what Compose does by hand too:

```text
docker network create shopnet
docker run -d --name api --network shopnet shop-api
docker run --rm --network shopnet shop-web
```

Containers connected to the same network find each other by the name given
with `--name`. On the default network (called `bridge`) there is **no** name
resolution; that is why you need to create your own network. Compose does it
for you.

```text
docker network ls
docker network inspect shopnet
```

## Summary

- Compose sets up a network for each project; services find each other **by
  name**: `http://api:8000`.
- In a container `localhost` is that container itself: writing `localhost`
  for another service gives `Connection refused`.
- Services on the same network reach each other's ports; `ports:` only for
  the service to be reached from outside.
- `depends_on` sets the start order; to wait for **readiness**, use
  `healthcheck` + `condition: service_healthy`.
- Outside Compose: `docker network create` + `--network`.
