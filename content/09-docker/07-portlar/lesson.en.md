# Ports: Reaching a Container from Outside

The containers so far printed something and ended. In real life most
containers are **servers**: a website, an API, a database. They never end;
they wait for requests coming from outside. In this section we will learn how
to reach a server inside a container from your computer.

## What is a port?

Many programs on a computer can listen to the network at the same time. The
**port number** tells which program an incoming request goes to: the same
building address, a different flat number.

- `localhost:8000` → door number 8000 of this computer.
- Websites usually use 80 (http) and 443 (https); during development numbers
  such as 8000, 8080 and 5000 are used.

In the API path you sent requests to `api.odyssey.test`; that also went to a
port on a computer.

## A container has its own network

Let us run Python's ready-made web server in a container:

```dockerfile
FROM python:3.13-slim
WORKDIR /srv
COPY index.html .
CMD ["python", "-m", "http.server", "8000"]
```

`python -m http.server 8000` serves the files in its folder on port 8000.
Build and run it, then open `localhost:8000` in the browser:

```text
docker run -d --name web site
curl localhost:8000
```

```text
curl: (7) Failed to connect to localhost:8000 after 2225 ms: Could not connect to server
```

The server is running but cannot be reached. The reason: the container has
**its own network**. Port 8000 inside it is not port 8000 of your computer.
The container is like a room closed to the outside.

## Publishing a port: `-p`

To open a door to the room from outside, use `-p` (publish):

```text
docker run -d --name web -p 8080:8000 site
curl localhost:8080
```

```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.16
...
```

`-p 8080:8000` says: **pass requests arriving at the computer's 8080 to the
container's 8000.** The order is always `host:container`.

<figure class="fig">
  <div class="flow">
    <span class="node">Browser<br><small>localhost:8080</small></span><span class="arrow">→</span>
    <span class="node acc">The computer's 8080<br><small>-p 8080:8000</small></span><span class="arrow">→</span>
    <span class="node ok">The container's 8000<br><small>python -m http.server</small></span>
  </div>
  <figcaption>The number on the left is the computer's door, the one on the right is inside the container. Without <code>-p</code>, the first arrow does not exist.</figcaption>
</figure>

When you open `http://localhost:8080` in the browser, the page comes. The
container's log also shows that the request arrived:

```text
docker logs web
172.17.0.1 - - [06/Oct/2026 19:43:26] "GET / HTTP/1.1" 200 -
```

`172.17.0.1` is the address of the "outside world" on Docker's network; the
request came in from your computer through that door.

## Options

| Written as | Meaning |
|---|---|
| `-p 8080:8000` | The computer's 8080 → the container's 8000 |
| `-p 8000:8000` | The same number on both sides (the most common) |
| `-p 127.0.0.1:8080:8000` | Reachable only from this computer, not by others on the network |
| `-p 8080:8000 -p 9090:9000` | Several ports |
| `-P` | Publish every `EXPOSE`d port to a random free port |

`docker port` shows which port goes where:

```text
docker run -d --name web2 -P site
docker port web2
8000/tcp -> 0.0.0.0:32768
```

The PORTS column of `docker ps` says the same: `0.0.0.0:32768->8000/tcp`.

## `EXPOSE` does not publish

```dockerfile
EXPOSE 8000
```

`EXPOSE` only **documents**: "the program in this image listens on 8000". It
does not open the door; `-p` does. It should still be written:

- whoever uses the image sees which port to publish,
- `-P` learns from it which ports to publish.

## The most common mistake: listening on 127.0.0.1

**Which address the program listens on** matters too. Let us start the same
server listening only on `127.0.0.1`:

```text
docker run -d -p 8081:8000 site python -m http.server 8000 --bind 127.0.0.1
curl localhost:8081
```

```text
curl: (52) Empty reply from server
```

`-p` is right but the reply is empty. `127.0.0.1` means "only from inside
this computer", and inside the container "this computer" is **the container
itself**. The request Docker passes in from outside arrives at the container
from another address, and the program does not accept it.

The fix: the program inside the container must listen on **`0.0.0.0`** (all
addresses). `http.server` does this by default; with tools such as Flask and
uvicorn you usually have to write it explicitly:

```text
uvicorn main:app --host 0.0.0.0 --port 8000
```

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Listening on 127.0.0.1</h4><p>Only requests from inside the container</p><p>From outside: <code>Empty reply from server</code></p></div>
    <div class="ok"><h4>Listening on 0.0.0.0</h4><p>Requests from all addresses</p><p>From outside: <code>200 OK</code></p></div>
  </div>
  <figcaption>Inside the container, "this computer" is the container itself. The request Docker passes in comes from another address.</figcaption>
</figure>

## The same port cannot be used twice

Only one program can hold a port of the computer. If a second container asks
for the same port:

```text
docker: Error response from daemon: ... Bind for 0.0.0.0:8080 failed:
port is already allocated
```

Choose another host port (`-p 8081:8000`) or stop the earlier one. The port
may also be held by a program outside Docker.

## Summary

- A container has its own network; a port inside it does not open to the
  outside by itself.
- `-p host:container` opens the door: `-p 8080:8000`. The `127.0.0.1:`
  prefix opens it only to this computer; `-P` to a random port.
- `docker port` and `docker ps` show which port goes where.
- `EXPOSE` only documents; `-p` opens.
- The program in the container must listen on `0.0.0.0`; if it listens on
  `127.0.0.1`, you get `Empty reply from server`.
- The same host port cannot be used twice: `port is already allocated`.
