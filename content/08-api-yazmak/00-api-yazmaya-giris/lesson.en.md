# Introduction to Writing APIs

In API 1 you sat on one side of the table: the **client**. You sent a
request to an address, read the JSON that came back and looked at the
status code. In this module you move to the other side of the table: you
will write the program that **receives** the request and **produces** the
answer, the **server**.

The good news: every concept you learned in API 1 holds here too. Method
(`GET`, `POST`), address, status code, JSON, header... Only this time you do
not read them, you give them.

## The server's job

When a request arrives, the server does four things:

<figure class="fig">
  <div class="flow">
    <span class="node">Request<br><small>GET /books</small></span><span class="arrow">→</span>
    <span class="node">Listen<br><small>uvicorn, port 8000</small></span><span class="arrow">→</span>
    <span class="node acc">Route<br><small>FastAPI: which function?</small></span><span class="arrow">→</span>
    <span class="node">Run<br><small>your function</small></span><span class="arrow">→</span>
    <span class="node ok">Answer<br><small>200 + JSON</small></span>
  </div>
  <figcaption>The path of a request on the server. You only write the "Run" step; uvicorn and FastAPI do the rest.</figcaption>
</figure>

1. **Listen:** wait for connections on a port of the computer (e.g. 8000).
2. **Route:** look at the request's method and address and decide which
   code runs (`GET /books` → the code that lists books).
3. **Run:** run that code; read and check the incoming data if needed.
4. **Answer:** turn the result into JSON and send it back with a status
   code.

It is possible to write all of this by hand, but it is long and
error-prone: parsing the incoming bytes, splitting the address into parts,
decoding the JSON, giving a proper answer to bad data... The exercise
server in API 1 did exactly this, and every endpoint needed lines such as
`if request.path == "/books" and request.method == "GET":`.

A ready-made library that takes over these repeated jobs is called a
**framework**. You only say "when this request comes to this address,
return this"; the framework does the rest.

## FastAPI and uvicorn: two parts

In this module we use two tools:

| Tool | What does it do? |
|---|---|
| **FastAPI** | The framework you define the application with: which address goes to which function, how incoming data is checked. |
| **uvicorn** | The server program that runs the application: it listens on the port, hands requests to FastAPI and sends the answers back. |

An analogy: FastAPI is a restaurant's **menu and kitchen** (how each order
is prepared), uvicorn is the **waiter** at the door (takes the order, passes
it to the kitchen, brings the plate to the customer). Both are needed, but
their jobs are separate.

Why FastAPI: it uses Python's **type hints** (`year: int`). When you write a
parameter's type, FastAPI both checks the incoming data against that type
and writes the API's documentation by itself. The type hints you learned on
the Python track start doing real work here.

## Your first application

A whole API, in five lines of code:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, API"}
```

Line by line:

- `from fastapi import FastAPI`: import the framework.
- `app = FastAPI()`: create the **application object**. Every endpoint will
  be built on it. Its name is usually `app`; uvicorn will look for it by
  that name too.
- `@app.get("/")`: connect the function right below it to **`GET /`**. The
  `@` at the start is called a **decorator**: think of it as a label put on
  top of a function's definition. It does not change the function; it
  registers it with FastAPI as "call this function when this address
  comes".
- `def home():`: an ordinary Python function that runs when that request
  comes. Its name does not matter (`home`, `root`, `index`); but choose a
  name that says what it does, because it also appears in the docs.
- `return {"message": "Hello, API"}`: return a dictionary. FastAPI turns it
  into **JSON by itself** and sends it with `200 OK`.

To add another address you repeat the same pattern:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

## Running it

To try it on your own computer you first install two packages (both are
ready in Odyssey):

```text
python -m pip install fastapi uvicorn
```

Then you start uvicorn in the folder where the file (`main.py`) is:

```text
uvicorn main:app --reload
```

`main:app` means "the `app` object in the `main.py` file". `--reload`
restarts the server every time you save the file; very handy while
developing. This appears on the screen (measured, shortened):

```text
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [23324]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Now you can open `http://127.0.0.1:8000` in a browser, or send a request
with `curl` as in API 1:

```text
curl -i http://127.0.0.1:8000/
HTTP/1.1 200 OK
server: uvicorn
content-length: 24
content-type: application/json

{"message":"Hello, API"}
```

You **did not write** the status code, the `content-type` header or the JSON
body: FastAPI produced all of them from the dictionary you returned. When an
address that does not exist is asked for, it gives `404` by itself:

```text
curl http://127.0.0.1:8000/nothing
{"detail":"Not Found"}
```

uvicorn also writes every request on its own screen; you can watch what the
API receives there:

```text
INFO:     127.0.0.1:57893 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:57895 - "GET /nothing HTTP/1.1" 404 Not Found
```

To stop it, `Ctrl+C` in the terminal.

## `/docs`: ready-made documentation

In API 1 you read an API's documentation to get to know it. FastAPI writes
the documentation for you. While the server is running, go to
`http://127.0.0.1:8000/docs`: the **Swagger UI** page lists your endpoints;
you can try each one from the browser with the "Try it out" button.

Behind the page is `/openapi.json`: the API's description for machines to
read. For our application with one endpoint (shortened):

```json
{"openapi": "3.1.0",
 "info": {"title": "FastAPI", "version": "0.1.0"},
 "paths": {"/": {"get": {"summary": "Home", ...}}}}
```

Because the function is called `home`, the summary became "Home". Tools
such as Postman can import this file and set up all the endpoints at once.

## How we will work in Odyssey

In the exercises you write your code in `main.py`. There are three ways:

1. **Run** (Ctrl+Enter): Odyssey calls your application **without starting a
   server**, sends the requests the exercise asks for in order and checks the
   answers. You see each request in the terminal: `→ GET /  200`.
2. The **Request** tab (in the left panel): write and send your own request
   (method, address, body), see the answer and the status code. It is not
   saved and does not count as an attempt.
3. **Start server**: your application really opens on this computer and the
   `/docs` page appears in your browser. After changing the code you stop it
   and start it again.

If you write `uvicorn.run(app)` at the end of the file, Odyssey does not run
it (the check goes on without waiting); on your own computer that line
starts the server:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

## Summary

- The client sends a request, the **server** listens, routes, runs and
  answers.
- **FastAPI** defines the application (`app = FastAPI()`), **uvicorn** runs
  it (`uvicorn main:app --reload`).
- `@app.get("/path")` connects the function below it to that address; the
  returned dictionary becomes JSON, the status code is `200`.
- An unknown address gets `404`; the docs at `/docs` and `/openapi.json` are
  ready by themselves.
