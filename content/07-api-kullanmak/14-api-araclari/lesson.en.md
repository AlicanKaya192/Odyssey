# API Tools: Browser, curl, Postman, Swagger

So far you have sent every request with Python code. But when getting to know
an API you usually **try things** before writing code: "what does this
address return?", "what happens if I leave out this header?". There are tools
made for that, and they are used almost every day at work.

In this section we get to know the tools. They all do the same job: build an
HTTP request, send it and show the response. What differs is how easy they
are and where they are used.

> Note: The practice server (`api.odyssey.test`) exists only inside Odyssey's
> exercise runner; outside tools cannot reach it. You try the tools on real,
> public APIs; this section's exercises teach you to read and run, with
> Python, the texts the tools produce (a curl command, an OpenAPI document, a
> Postman collection).

## The browser: the quickest GET

Typing a `GET` address into the browser's address bar is the quickest way to
try an API. A public API's JSON response appears on screen; most browsers
show JSON in a readable form.

Its limits are clear: from the address bar a browser only sends `GET` and
cannot add headers. Requests that need an identity or send data need another
tool.

### Developer Tools: the Network tab

The **Network** tab of the Developer Tools, opened with **F12** in a browser,
lists every request a web page sends in the background. Click a request to
see its address, method, headers, status code and response.

This is a very valuable habit for a data scientist: here you can find **which
API the data you see on a site comes from**. Most modern pages already pull
their data from a JSON API. (Check the site's terms of use before using that
API in your own program.)

## curl: requests from the command line

**curl** is a small program that sends HTTP requests from the command line.
It comes with Windows 10 and 11, and with Linux and macOS too. Almost every
piece of documentation gives its examples in curl, so being able to read it
is essential.

```text
curl https://api.example.com/books
curl -i https://api.example.com/books/1
curl --json @book.json -H "Authorization: Bearer abc" https://api.example.com/books
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>curl</code></span><span>The program</span></div>
    <div class="anat-row"><span><code>-X POST</code></span><span>The method (<code>GET</code> if not given)</span></div>
    <div class="anat-row"><span><code>https://api.../books</code></span><span>The address</span></div>
    <div class="anat-row"><span><code>-H "Name: value"</code></span><span>A header; can be written several times</span></div>
    <div class="anat-row"><span><code>-d '...'</code> / <code>--json '...'</code></span><span>The body</span></div>
    <div class="anat-row"><span><code>-i</code></span><span>Show the response headers too</span></div>
  </div>
  <figcaption>A curl command is the command-line form of the request you saw piece by piece in Section 02.</figcaption>
</figure>

On Windows, PowerShell may give the name `curl` to a different command; write
`curl.exe` to be sure.

### From curl to requests

Translating a curl command you saw in documentation into Python is a very
common job. The pieces match one to one:

| curl | requests |
|---|---|
| `curl URL` | `requests.get(URL)` |
| `-X POST` | `requests.post(...)` or `requests.request("POST", ...)` |
| `-H "Name: value"` | `headers={"Name": "value"}` |
| `-d '{"a": 1}'` + the JSON header | `json={"a": 1}` |
| `-u user:password` | `auth=("user", "password")` |
| `-i` | `r.status_code`, `r.headers` |

Python's built-in `shlex` module splits a command into pieces, understanding
the quotes correctly:

```python
import shlex

cmd = 'curl -X POST "http://api.odyssey.test/books" -H "Authorization: Bearer letmein"'
print(shlex.split(cmd))
# ['curl', '-X', 'POST', 'http://api.odyssey.test/books',
#  '-H', 'Authorization: Bearer letmein']
```

In the exercise you will build a request from these pieces.

## Swagger UI and OpenAPI

Many APIs also publish their documentation as a **machine-readable** file:
the **OpenAPI** specification (formerly called Swagger). This JSON (or YAML)
file describes every endpoint, its parameters, its identity requirements and
its responses:

```json
{"openapi": "3.1.0",
 "paths": {"/books": {"get": {"summary": "List books"},
                      "post": {"summary": "Add a book", "security": [{"bearer": []}]}}}}
```

**Swagger UI** reads this file and draws an interactive page in the browser:
next to each endpoint a "Try it out" button, parameter boxes, a send button
and the response. You try things on the same page while reading the
documentation. **ReDoc** produces a more readable (but non-interactive)
documentation page from the same file.

The FastAPI applications you will write in the Writing APIs module produce this page **on their
own**: run the application, go to `/docs` and Swagger UI opens. So knowing
Swagger UI well will help when you try out your own API too.

The practice server has a small OpenAPI document as well: `GET /openapi.json`.

## Postman: the standard in companies

**Postman** is the most widely used desktop application for working with
APIs; teams in most companies use it. Its basic ideas:

- **Request:** pick the method, write the address, add parameters, headers,
  a body and authentication from the tabs, press **Send**. The response code,
  time, headers and body appear in the panel below.
- **Collection:** groups related requests in a folder (list, add, delete
  under "Library API"...). It can be shared with the team.
- **Environments and variables:** placeholders such as `{{base_url}}` and
  `{{token}}`. You run the same collection against a test server and the
  live server just by switching the environment, and you do not write the key
  inside the requests.
- **Tests:** small scripts that run after the response arrives ("is the code
  200?").
- **Code generation:** a "Code" button that translates a request into curl,
  Python requests and other languages. The quickest way to turn a request
  that works in Postman into code.

Postman's cloud sync needs an account. Collections can be exported as JSON;
in the exercise you will read and run such a collection with Python.

## Bruno: no account, offline

**Bruno** is an application like Postman, but **open source**, needing no
account and working entirely offline. Its key difference: it keeps
collections as plain text files in the project folder, so they can go into git
along with the code. A good choice if you want to start without an account or
keep your requests with the project.

## The others: a short introduction

- **Insomnia:** a desktop application similar to Postman.
- **Thunder Client:** an extension that runs inside VS Code; you send requests
  without leaving the editor.
- **HTTPie:** a more readable command-line tool than curl:
  `http GET api.example.com/books author==Austen`.

## Which one when?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>A quick look at a GET</span><span>The browser</span></div>
    <div class="anat-row"><span>Where does a site's data come from?</span><span>Developer Tools → Network</span></div>
    <div class="anat-row"><span>Trying a documentation example, using it in a script</span><span>curl</span></div>
    <div class="anat-row"><span>Trying an API inside its documentation</span><span>Swagger UI (<code>/docs</code>)</span></div>
    <div class="anat-row"><span>Organised team work, environments, tests</span><span>Postman</span></div>
    <div class="anat-row"><span>No account, offline, requests in git</span><span>Bruno</span></div>
    <div class="anat-row"><span>Repeated work, pulling data</span><span>Python + requests</span></div>
  </div>
  <figcaption>Tools are for trying and exploring; code is for repeated work. The two complement each other.</figcaption>
</figure>

## Summary

- The browser is the quickest `GET` test; **F12 → Network** shows the APIs a
  page uses.
- **curl** is the command line's request tool and the language of
  documentation examples. `-X` method, `-H` header, `-d` body, `-i` response
  with headers.
- **OpenAPI** is an API's machine-readable documentation; **Swagger UI** draws
  a page you can try things on from it. FastAPI produces `/docs` on its own.
- **Postman** is the company standard: collections, environment variables,
  tests, code generation. **Bruno** needs no account, works offline and is git
  friendly.
- Turning a request that works in a tool into code: the curl ↔ requests
  match.
