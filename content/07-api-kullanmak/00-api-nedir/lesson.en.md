# What Is an API?

The weather app on your phone does not measure the weather itself. It has no
thermometer and no satellite. All it does is **ask another program**: "How
warm is it in Istanbul?" That program sends the answer back.

The door that lets programs ask each other questions and get answers is
called an **API**. On this path you will first learn to ask someone else's
API for data (API 1), then to write your own API (API 2).

In this section we do not connect to the internet yet. First we settle the
ideas: who asks, who answers, and what the rules in between are.

## An analogy: the restaurant

Imagine you are at a restaurant.

- **You** want food, but you do not walk into the kitchen.
- **The kitchen** cooks the food, but does not talk to you directly.
- **The menu** tells you what you can ask for.
- **The waiter** takes your order to the kitchen and brings the plate back.

An API is like the waiter and the menu together. What you can ask for is
fixed (the menu), how you ask is fixed (you tell the waiter), and the inside
of the kitchen is hidden from you. Even if the cook or the stove changes, you
keep ordering from the same menu in the same way.

<figure class="fig">
  <div class="flow">
    <span class="node">Customer<br><small>client</small></span><span class="arrow">→</span>
    <span class="node acc">Waiter + menu<br><small>API</small></span><span class="arrow">→</span>
    <span class="node">Kitchen<br><small>server</small></span>
  </div>
  <figcaption>The customer never enters the kitchen; they only tell the waiter what is on the menu. An API likewise shows the client only the server's door, not its inside.</figcaption>
</figure>

That last sentence is the most important idea behind APIs: **the inside can
change, the door stays the same.** Even if the weather company rewrites its
whole measuring system, your app keeps asking the same question in the same
way.

## What the letters stand for

API stands for **A**pplication **P**rogramming **I**nterface.

- **Application:** a program.
- **Programming:** the one using it is also a program, not a person.
- **Interface:** the surface where two things meet. A wall socket is an
  interface: the shape of the plug is fixed, and you do not need to know
  the wiring behind it.

So an API is **a door that one program opens to other programs.** The
program's author decides what the door looks like.

## Client and server

There are two sides in an API conversation:

- The **client**: the program that asks. The weather app, your browser, the
  Python code you are about to write.
- The **server**: the program that answers. Usually on another computer,
  always switched on and waiting.

The question the client sends is called a **request**, and the answer the
server sends back is called a **response**. Every conversation is one
request and one response; the server never speaks on its own, it always
waits to be asked.

<figure class="fig">
  <div class="flow">
    <span class="node">Client</span><span class="arrow">→ request →</span>
    <span class="node acc">Server</span><span class="arrow">→ response →</span>
    <span class="node">Client</span>
  </div>
  <figcaption>Every conversation is one request and one response. The client always starts the conversation.</figcaption>
</figure>

Do not let the word "server" scare you. A server does not have to be a
special machine; **any program** that waits for requests and answers them is
a server. In API 2 you will run a server on your own computer.

## What a request and a response look like

We will learn the parts one by one later; for now, just take a look. A
request to a weather API looks roughly like this:

```text
GET /weather?city=Istanbul
```

It means "**get** (GET) the information at `/weather` where `city` is
`Istanbul`". The server's response:

```text
200 OK

{"city": "Istanbul", "temp": 18, "sky": "cloudy"}
```

`200 OK` means "all is well". The line below it is the data itself; this way
of writing data is called **JSON**, and it looks a lot like a Python
dictionary. We will see both in their own sections.

## Endpoint: one door of the API

An API usually has more than one door. A weather API might offer:

- `/weather`: the weather right now
- `/forecast`: the coming days
- `/cities`: the list of known cities

Each of these is called an **endpoint**. An endpoint is a single door of the
API that does one particular job, like one dish on the menu.

What happens if you ask for something that is not on the menu? The waiter
says "we don't have that". An API does the same: if you send a request to an
endpoint that does not exist, the server answers **404 Not Found**. You have
probably seen that number on websites too.

## Documentation: the API's menu

Before using an API you read its **documentation**. It tells you:

- which endpoints exist,
- what each one needs to be sent (for example `city`),
- what the response looks like,
- which errors can come back.

A good API's documentation is as clear as a menu. For every API you read on
this path, the first job will be to look at the documentation.

## The difference between a website and an API

The same data can be offered in two forms:

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Website (for people)</h4><pre><code class="language-text">&lt;h1&gt;Istanbul&lt;/h1&gt;
&lt;p class="big"&gt;18°&lt;/p&gt;
&lt;p&gt;Cloudy&lt;/p&gt;</code></pre><p>Colours, fonts, layout. The information sits among the decorations.</p></div>
    <div class="ok"><h4>API (for programs)</h4><pre><code class="language-json">{"city": "Istanbul",
 "temp": 18,
 "sky": "cloudy"}</code></pre><p>No decoration. Every piece of information has a name; a program reads it directly.</p></div>
  </div>
  <figcaption>The same information in two forms. When a program needs to pull information, an API is used.</figcaption>
</figure>

A website is **for people**: colours, layout, buttons. Pulling the
information out with a program is hard, because it is scattered among the
decorations. An API is **for programs**: no decoration, just orderly data.
That is why APIs are used whenever one program needs information from
another.

## Why do APIs exist?

- **Fresh data:** Exchange rates, weather and stock prices change every
  minute. Instead of everyone measuring, everyone asks the source.
- **Using someone else's work:** Instead of writing hard things like maps,
  payments or translation from scratch, you ask the service that does them.
- **Control:** The server decides what to give, to whom and how much.
  Instead of opening its database to everyone, it offers only what is on
  the menu.
- **Language independence:** The server may be written in Java and the
  client in Python. As long as the rules of the door are shared, they
  understand each other.

## Why should a data scientist know this?

Data does not always arrive as a ready CSV file. Very often it is pulled from
an API:

- open data portals (population, traffic, air quality),
- the company's own services (sales, user events),
- public services such as GitHub, exchange rates or weather.

There is also the other direction: the most common way to let other people
use a model you trained is to put it behind an API. An app that asks "what
would this house sell for?" gets the answer from your model's API. You will
do that in API 2.

## REST: the most common API style

APIs can be designed in different styles. Today the most common one is
**REST**. For now you only need two of its ideas:

- Everything is a **resource**: books, users, orders. Every resource has an
  address: `/books`, `/books/42`.
- The **HTTP method** says what to do with the resource: get it (GET), add
  one (POST), change it (PUT), delete it (DELETE).

"REST API" means an API that follows these rules. Towards the end of the
path we will read REST in detail.

## This section's exercises

We are not connecting to a real server yet. In the exercises you will
**imitate the server with Python dictionaries and functions**: one function
will be the server, taking a request and returning a response; another piece
will be the client calling it. Real APIs are built on exactly this idea;
the only difference is that the internet sits in between.

## Summary

- An API is a door that a program opens to other programs: what can be
  asked and how is fixed, the inside is hidden.
- The one asking is the **client**, the one answering is the **server**.
  Every conversation is one **request** and one **response**.
- An **endpoint** is a single door of the API (`/weather`). A missing door
  → **404**.
- The **documentation** is the API's menu; read it before using the API.
- A website is for people, an API is for programs.
- **REST** is the most common style: resources and the HTTP methods applied
  to them.
