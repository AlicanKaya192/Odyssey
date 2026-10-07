# Working with JSON

In the previous section you wrote **text** to a file and read it back. But
your programs usually hold **structured data**, not text: a dictionary, a
list of dictionaries, a dictionary with a list inside. How do you write
those to a file and later get them back **with the same structure**?

This section's answer is **JSON**. Settings files, the data a program saves
and the replies of almost every service on the internet use this format.
Working with it in Python comes down to four functions.

## The problem first: storing a dictionary as plain text

Turning a dictionary into text with `str()` and writing it to a file is the
first idea that comes to mind:

```python
profile = {"name": "Ada", "languages": ["Python", "SQL"]}

with open("profile.txt", "w", encoding="utf-8") as file:
    file.write(str(profile))

with open("profile.txt", encoding="utf-8") as file:
    loaded = file.read()

print(loaded)
print(type(loaded))
```

```text
{'name': 'Ada', 'languages': ['Python', 'SQL']}
<class 'str'>
```

It looks like a dictionary on the screen, but it is not: `loaded` is
**text** (`str`). Try to take the name out of it:

```python
print(loaded["name"])
```

```text
TypeError: string indices must be integers, not 'str'
```

The text holds a **picture** of the dictionary, not the dictionary itself.
To turn it back into a dictionary you would have to take the text apart
character by character. JSON does exactly this job: a shared rule for
turning a structure into text and building **the same structure** back
from the text.

## What is JSON?

**JSON** (*JavaScript Object Notation*) is a format for writing data as
text. Although its name mentions JavaScript, every language can read and
write it; that is why it is the most common way to move data between
programs.

A JSON text looks a lot like a Python dictionary:

```json
{
  "name": "Ada",
  "age": 36,
  "languages": ["Python", "SQL"],
  "admin": true,
  "manager": null
}
```

The likeness is strong but they are not the same. The differences are small
and important:

<figure class="fig">
  <div class="versus">
    <div><h4>Python dictionary</h4>
<pre><code>{'name': 'Ada',
 'admin': True,
 'manager': None}</code></pre>
    </div>
    <div class="ok"><h4>JSON text</h4>
<pre><code class="language-text">{"name": "Ada",
 "admin": true,
 "manager": null}</code></pre>
    </div>
  </div>
  <figcaption>In JSON, strings are written with double quotes only; <code>true</code> instead of <code>True</code>, <code>null</code> instead of <code>None</code>.</figcaption>
</figure>

Every piece of JSON has a counterpart in Python:

| JSON | Python | Example |
|---|---|---|
| object `{ }` | `dict` | `{"a": 1}` |
| array `[ ]` | `list` | `[1, 2, 3]` |
| string `"..."` | `str` | `"Ada"` |
| number | `int` or `float` | `36`, `3.5` |
| `true` / `false` | `True` / `False` | |
| `null` | `None` | |

## From text to Python: `json.loads`

`json` is a module that comes with Python; you do not need to install it,
only to `import` it. `json.loads` takes a JSON **text** and turns it into a
Python structure:

```python
import json

text = '{"name": "Ada", "age": 36, "admin": true, "manager": null}'
data = json.loads(text)

print(data)
print(type(data))
print(data["age"] + 1)
```

```text
{'name': 'Ada', 'age': 36, 'admin': True, 'manager': None}
<class 'dict'>
37
```

This time a real dictionary came back: `data["age"]` is a number and you can
add 1 to it. `true` became `True` and `null` became `None` by themselves.

Notice that we wrapped the JSON text in single quotes: there are double
quotes **inside** the text, so wrapping the outside in single quotes is the
easiest way.

## From Python to text: `json.dumps`

The other direction is `json.dumps`: it turns a Python structure into JSON
text.

```python
profile = {
    "name": "Ada",
    "city": "London",
    "languages": ["Python", "SQL"],
    "active": True,
}

text = json.dumps(profile)
print(text)
print(type(text))
```

```text
{"name": "Ada", "city": "London", "languages": ["Python", "SQL"], "active": true}
<class 'str'>
```

The quotes became double and `True` became `true`. The result is text; it
can be written to a file or sent over the internet.

A single line is hard for a person to read. `indent=2` writes it with each
level moved two spaces in:

```python
print(json.dumps(profile, indent=2))
```

```text
{
  "name": "Ada",
  "city": "London",
  "languages": [
    "Python",
    "SQL"
  ],
  "active": true
}
```

One more detail: by default JSON writes non-English letters as escape
sequences. `ensure_ascii=False` leaves them as they are:

```python
city = {"city": "İzmir"}
print(json.dumps(city))
print(json.dumps(city, ensure_ascii=False))
```

```text
{"city": "\u0130zmir"}
{"city": "İzmir"}
```

Both are valid JSON and both become `"İzmir"` when read back; the
difference is only for a person opening the file to look.

<figure class="fig">
  <div class="flow">
    <span class="node">Python<br>dict, list</span><span class="arrow">→</span>
    <span class="node acc"><code>json.dumps</code><br>to text</span><span class="arrow">→</span>
    <span class="node">JSON text<br>file, internet</span><span class="arrow">→</span>
    <span class="node acc"><code>json.loads</code><br>back again</span><span class="arrow">→</span>
    <span class="node ok">same structure</span>
  </div>
  <figcaption>There with <code>dumps</code>, back with <code>loads</code>. The text in between is the shared format every language can read.</figcaption>
</figure>

## Writing to and reading from a file: `json.dump` and `json.load`

When working with a file there are two sibling functions that take the text
out of the middle. They have no `s` at the end:

```python
with open("profile.json", "w", encoding="utf-8") as file:
    json.dump(profile, file, indent=2)
```

What is inside the file:

```text
{
  "name": "Ada",
  "city": "London",
  "languages": [
    "Python",
    "SQL"
  ],
  "active": true
}
```

Reading it back:

```python
with open("profile.json", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded["languages"][1])
print(loaded == profile)
```

```text
SQL
True
```

The dictionary you wrote comes back from the file as **the same**
dictionary. Even if your program closes and opens again, the data is not
lost.

One rule is enough to keep the four functions apart: **the `s` stands for
"string", that is, text.**

| Function | Takes | Gives |
|---|---|---|
| `json.loads(text)` | JSON text | a Python structure |
| `json.dumps(structure)` | a Python structure | JSON text |
| `json.load(file)` | an open file | a Python structure |
| `json.dump(structure, file)` | a Python structure + an open file | writes to the file |

## Nested data

Real JSON is usually nested: a list inside a dictionary, dictionaries inside
the list.

```python
text = """
{
  "course": "Python",
  "students": [
    {"name": "Ada", "scores": [90, 85]},
    {"name": "Alan", "scores": [70, 95]}
  ]
}
"""
data = json.loads(text)

print(data["students"][0]["name"])
print(data["students"][1]["scores"][1])
```

```text
Ada
95
```

A long chain of lookups can look scary; read it from left to right, checking
what you are holding at each step:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>data</code></span><span>the whole structure: a <b>dictionary</b></span></div>
    <div class="anat-row"><span><code>["students"]</code></span><span>the "students" key in the dictionary: a <b>list</b></span></div>
    <div class="anat-row"><span><code>[0]</code></span><span>the list's first item: a <b>dictionary</b> (Ada)</span></div>
    <div class="anat-row"><span><code>["name"]</code></span><span>the "name" key in that dictionary: <code>"Ada"</code></span></div>
  </div>
  <figcaption><code>data["students"][0]["name"]</code> is four steps from left to right. In a dictionary you go in by key, in a list by position.</figcaption>
</figure>

Each pair of square brackets goes one step in. In a dictionary **by key**
(`["students"]`), in a list **by position** (`[0]`). When you get stuck,
print the in-between step: `print(data["students"])` shows you whether what
you are holding is a list or a dictionary.

Going through the dictionaries inside the list with a loop works the same
way:

```python
for student in data["students"]:
    print(student["name"], sum(student["scores"]))
```

```text
Ada 175
Alan 165
```

## Keys that may be missing: `get`

In JSON that comes from outside, not every field is always there. Asking for
a missing key with square brackets raises an error:

```python
student = data["students"][0]
print(student["email"])
```

```text
KeyError: 'email'
```

`get` from the Dictionaries section is very useful here: if the key is not
there, it returns the default you give instead of raising an error.

```python
print(student.get("email", "no email"))
```

```text
no email
```

The rule: take a field you are **sure will always be there** with square
brackets, and a field that **may be missing** with `get`.

## Types that change on the way there and back

JSON has fewer types than Python. That is why some things **change** when
they go to a file and come back:

```python
point = {"x": 1, "y": 2, "tags": ("a", "b")}
back = json.loads(json.dumps(point))
print(back["tags"])
```

```text
['a', 'b']
```

**A tuple becomes a list.** JSON has no tuples, only arrays.

```python
counts = {1: "one", 2: "two"}
back = json.loads(json.dumps(counts))
print(back)
print(back.get(1))
print(back.get("1"))
```

```text
{'1': 'one', '2': 'two'}
None
one
```

**Keys always become text.** In JSON an object's key can only be text; the
key `1` comes back as `"1"` and `back.get(1)` no longer finds anything. If
you keep the number as a **value** (`{"id": 1}`) it stays a number; the
problem is only with keys.

Then there are things that cannot be converted at all. A **set** does not
exist in JSON:

```python
json.dumps({"tags": {"a", "b"}})
```

```text
TypeError: Object of type set is not JSON serializable
```

The fix is to turn it into a list before writing: `sorted(tags)` gives a
list and also makes the order the same every time.

## Broken JSON

JSON's rules are strict. Try to read text written like a Python dictionary:

```python
try:
    json.loads("{'name': 'Ada'}")
except json.JSONDecodeError as error:
    print(error)
```

```text
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

The error is called `json.JSONDecodeError` (it lives in the `json` module).
The message says **where** it got stuck: line 1, column 2, that is, where
the single quote is ("a name in double quotes was expected"). Three common
kinds of breakage:

| Text | Problem |
|---|---|
| `{'name': 'Ada'}` | single quotes; JSON only has double quotes |
| `{"a": 1,}` | a trailing comma; JSON does not accept it |
| `{"a": True}` | a capital letter; in JSON it is `true` |

If a file may arrive broken, protect the reading with `try`:

```python
DEFAULTS = {"theme": "dark", "language": "en"}

def load_settings(path):
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return DEFAULTS
    except json.JSONDecodeError:
        print("settings file is broken, using defaults")
        return DEFAULTS
```

Whether the file is missing or broken, the program carries on with the
default settings instead of crashing. It is exactly the rule from the Files
section: "catch it if you have a sensible fallback".

## All together: a to-do list that is saved

A small to-do list that is not lost when the program closes:

```python
import json

def load_tasks():
    try:
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)

tasks = load_tasks()
tasks.append({"title": "learn JSON", "done": False})
save_tasks(tasks)
print(len(tasks), "tasks saved")
```

On the first run there is no file and the list starts empty:

```text
1 tasks saved
```

On the second run the earlier task comes from the file:

```text
2 tasks saved
```

The flow is the same every time: **read → change → write.** Writing the
file from scratch with `"w"` matters; if you added to the end with `"a"`,
two JSON texts would sit side by side and the file would no longer be valid
JSON (the note has the details).

## Summary

- JSON is the shared format for writing structured data (dictionaries,
  lists, numbers, text) as text. Every language can read it.
- Text written with `str(dictionary)` does not turn back into a dictionary;
  JSON does.
- JSON has only double quotes; `true`, `false`, `null`; no trailing comma.
- `json.loads` reads from text, `json.load` from a file; `json.dumps`
  writes to text, `json.dump` to a file. **`s` = string.**
- `indent=2` writes it readably, `ensure_ascii=False` keeps non-English
  letters.
- In nested data each pair of square brackets is one step in: a key in a
  dictionary, a position in a list. Take a field that may be missing with
  `get`.
- On the way there and back: a tuple becomes a list, a number key becomes
  text; a set cannot be written.
- Broken JSON raises `json.JSONDecodeError`; catch it with `try` if you have
  a sensible default.
