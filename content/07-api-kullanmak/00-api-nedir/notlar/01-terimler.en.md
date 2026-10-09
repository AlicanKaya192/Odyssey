The terms from this section, with short definitions and everyday equivalents.

| Term | Meaning | At the restaurant |
|---|---|---|
| **API** | A door that a program opens to other programs | Waiter + menu |
| **Client** | The program that asks | The customer |
| **Server** | The program that waits for questions and answers them | The kitchen |
| **Request** | The question the client sends | The order |
| **Response** | The answer the server sends back | The plate that arrives |
| **Endpoint** | A single door of the API that does one job | One dish on the menu |
| **Documentation** | The text that lists the endpoints and how to use them | The menu |
| **JSON** | The orderly text format APIs write data in | How the plate is laid out |
| **REST** | The most common API style: resources + HTTP methods | The restaurant's rules |
| **404 Not Found** | The "no such door" response | "We don't serve that" |

## Commonly confused

**An API is not the same as a server.** The server is the running program;
the API is the rules of the doors it opens to the outside. One server can
have several APIs, and one API can run on several servers.

**An API is not the same as a website.** Both can offer the same data. A
site is a decorated page for people to read (HTML); an API is orderly data
for programs to read (usually JSON).

**A client is not necessarily an app.** Your browser, a Python script,
another server, even a single command on the command line can be a client.
Whoever asks is the client.

**A server is not necessarily a distant machine.** A program running on your
own computer and waiting for requests is a server too. You will do that in
the Writing APIs module.

## Worth remembering

> The inside can change, the door stays the same.

All the value of an API is in that sentence: the client works without
knowing the inside of the server, simply by following the rules of the door.
