If you cannot reach the server in a container, check in this order. Each step
rules out the previous one.

## 1. Is the container running?

```text
docker ps
```

If it is not in the list, the program crashed as soon as it started. Look at
its state with `docker ps -a` and at what it printed last with
`docker logs name`.

## 2. Is the port published?

The PORTS column of `docker ps`:

| Shown | Meaning |
|---|---|
| `0.0.0.0:8080->8000/tcp` | Published: the computer's 8080 → the container's 8000 |
| `8000/tcp` | Only `EXPOSE`d, **not published** (`-p` forgotten) |
| (empty) | Neither EXPOSE nor `-p` |

## 3. Are you going to the right port?

In the browser you type the number **on the left**: with `-p 8080:8000` it is
`localhost:8080`. The number on the right is for inside the container.

## 4. Is the program listening on the right port?

If you wrote `-p 8080:8000` but the program listens on 5000, the request goes
nowhere. Look at the program's own log; most servers print their port when
they start:

```text
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

## 5. Is the program listening on 0.0.0.0?

If you see `127.0.0.1` or `localhost` in the log, this is the problem:

| Error | Most likely |
|---|---|
| `Could not connect to server` | The port is not published, or the container is not running |
| `Empty reply from server` / `connection reset` | The port is published but the program listens on 127.0.0.1 |
| `port is already allocated` | The host port is held by something else |

## 6. Try from inside

Sending a request from inside the container tells whether the problem is
outside or inside:

```text
docker exec -it web python
>>> import urllib.request
>>> urllib.request.urlopen("http://127.0.0.1:8000").status
200
>>> exit()
```

If `200` comes back from inside, the program works; the problem is in publishing or in the
address listened on.

## In Odyssey

For the HTTP check, Odyssey publishes the container to a random free host
port and sends a request. If you get a "could not be reached" message, look
at steps 4 and 5 first.
