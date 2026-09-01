# Type Annotations

You opened a function someone else wrote and saw this:

```python
def repeat(text, count):
    return text * count
```

What are you supposed to pass as `count`? A number, a string? What does the
function give back? You cannot tell without reading the body.

This section teaches you how to write down "what goes in here and what comes
out". It is called a **type annotation**.

## What is the problem?

The `repeat` function above works with all sorts of things:

```python
print(repeat("ab", 3))
print(repeat(3, "ab"))
print(repeat([1, 2], 2))
```

```
ababab
ababab
[1, 2, 1, 2]
```

All three ran. So which one did the author mean? There is no way to know.

This is not a problem in a small file. But if the function was written three
months ago, or by someone else, or the file is two thousand lines long, you
have to open the body and read it every single time.

## Your first annotation

An annotation is written next to the parameter, after a colon:

```python
def repeat(text: str, count: int) -> str:
    return text * count
```

That line now explains itself.

<figure class="fig anat">
  <div class="sig">def repeat(<u class="m1">text: str</u>, <u class="m2">count: int</u>) <u class="m3">-&gt; str</u>:</div>
  <ul class="legend">
    <li class="m1"><b>Parameter annotation</b> — <code>text</code> expects a string.</li>
    <li class="m2"><b>Parameter annotation</b> — <code>count</code> expects a whole number.</li>
    <li class="m3"><b>Return annotation</b> — the function gives back a string. It is written after the parentheses with <code>-&gt;</code>.</li>
  </ul>
</figure>

You read it like this: "repeat takes a string and an integer, and returns a
string."

The types you use are types you already know:

| Annotation | Meaning |
|---|---|
| `str` | Text |
| `int` | Whole number |
| `float` | Decimal number |
| `bool` | `True` / `False` |
| `list` | List |
| `dict` | Dictionary |
| `None` | No value |

## Python does not check this

Pay attention here, because this is the part people get wrong most often.

```python
def double(number: int) -> int:
    return number * 2

print(double("ab"))
```

```
abab
```

No error. The program ran. We wrote `int`, we passed a string, and Python did
not care.

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>You write</b><br><code>number: int</code></span>
    <span class="arrow">→</span>
    <span class="node">Python runs<br>the code</span>
    <span class="arrow">→</span>
    <span class="node no">It <b>never looks</b><br>at the annotation</span>
  </div>
  <figcaption>An annotation does nothing at run time. The code behaves exactly as if the annotation had never been written.</figcaption>
</figure>

So an annotation is not a **rule**, it is a **note**. A note to whom?

- **To you.** Three months from now, when you open your own code.
- **To whoever reads the code.** They see what it expects without stepping
  inside the function.
- **To your editor.** VS Code and PyCharm read annotations: they underline a
  value of the wrong type before you even run the program, and once you type
  `text.` they offer you the methods that belong to strings.

The third one is where the real benefit is. Writing annotations moves errors
from run time to **writing time**.

> The program runs even when the annotation is wrong. An annotation adds no
> behaviour to your code; it only states your intent.

## Annotating variables

Variables can be annotated too:

```python
count: int = 0
name: str = "Ada"
```

But most of the time this is **unnecessary.** Python already knows from
`count = 0` that it is an integer; repeating it is noise.

There is one place where it genuinely helps: **containers that start empty.**

```python
scores = []
```

What is going to be inside this list? Numbers, strings? `[]` is empty, so
there is nothing to tell you. This is exactly where an annotation carries
information:

```python
scores: list[int] = []
```

## What is inside the container?

`list` says "this is a list". But a list of what? You say so with square
brackets:

```python
names: list[str] = ["Ada", "Alan"]
ages: dict[str, int] = {"Ada": 36, "Alan": 41}
point: tuple[int, int] = (3, 7)
tags: set[str] = {"python", "basics"}
```

A dictionary takes two types, because a dictionary has two sides:

<figure class="fig anat">
  <div class="sig">ages: <u class="m1">dict</u>[<u class="m2">str</u>, <u class="m3">int</u>]</div>
  <ul class="legend">
    <li class="m1"><b>The container itself</b> — this is a dictionary.</li>
    <li class="m2"><b>The type of the keys</b> — strings such as <code>"Ada"</code>.</li>
    <li class="m3"><b>The type of the values</b> — whole numbers such as <code>36</code>.</li>
  </ul>
</figure>

They can nest as well. A dictionary holding each student's list of grades:

```python
grades: dict[str, list[int]] = {
    "Ada": [90, 85],
    "Alan": [70, 95],
}
```

Read it from the inside out: `list[int]` is a list of numbers, so
`dict[str, list[int]]` is "a dictionary with string keys and lists of numbers
as values".

## What if there is no value?

Here is a situation you will meet often: sometimes the function finds
something, sometimes it does not.

```python
def find_score(name):
    scores = {"Ada": 90}
    if name in scores:
        return scores[name]
    return None
```

This function returns an `int` sometimes and `None` other times. You can write
both:

```python
def find_score(name: str) -> int | None:
    scores = {"Ada": 90}
    if name in scores:
        return scores[name]
    return None
```

The vertical bar means "or". `int | None` is "either a whole number or
nothing".

That annotation tells the reader something important: **do not use the
returned value directly, check it first.**

```python
score = find_score("Alan")
if score is None:
    print("not found")
else:
    print(score + 10)
```

Without the annotation you would only discover that you needed this check when
the program raised a `TypeError`.

## A function that returns nothing

Some functions do not return a value; they do a job:

```python
def greet(name: str) -> None:
    print("hello", name)
```

`-> None` means "I give nothing back". Writing that is different from writing
nothing at all:

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>NOT ANNOTATED</h5>
<pre><code>def greet(name: str):
    print("hello", name)</code></pre>
    </div>
    <div class="ok">
      <h5>ANNOTATED</h5>
<pre><code>def greet(name: str) -&gt; None:
    print("hello", name)</code></pre>
    </div>
  </div>
  <figcaption>The function on the left might return a value, or might not — the reader cannot tell. The one on the right says plainly that it does not.</figcaption>
</figure>

Beginners often mix up `print` and `return`; `-> None` makes that difference
visible.

## The older form you will see

When you look at a library you will run into lines like this:

```python
from typing import List, Dict, Optional

def load(path: str) -> Optional[List[Dict[str, int]]]:
    ...
```

These are the old spelling of the same thing. Before Python 3.9 you could not
write `list[str]`; you had to take `List[str]` from the `typing` module.

| Old | New |
|---|---|
| `List[str]` | `list[str]` |
| `Dict[str, int]` | `dict[str, int]` |
| `Tuple[int, int]` | `tuple[int, int]` |
| `Optional[str]` | `str \| None` |
| `Union[int, str]` | `int \| str` |

Use the right-hand column in new code. Recognising the left-hand one is
enough — you will come across it.

## Where to write them and where not to

An annotation is not something you put on every line. The places where it pays
off most:

- **Function signatures.** Write them here. The signature is the only thing
  someone calling your function gets to see.
- **Containers that start empty.** `results: list[str] = []`
- **Values whose meaning is unclear.** `timeout: float = 0.5`

Places where it is unnecessary:

- **Assignments with an obvious value.** Adding `: str` to `name = "Ada"`
  contributes nothing.
- **Loop variables.** No annotation is needed in `for item in items:`.
- **Short, single-use intermediate values.**

The test is simple: **write the annotation if it answers a question, leave it
out if it repeats itself.**

## Summary

- A type annotation is how you write down what type a value is expected to be:
  `text: str`, `-> int`.
- Parameters take a colon; the return type comes after the parentheses with
  `->`.
- **Python does not check any of this at run time.** Passing the wrong type
  raises no error; an annotation is a note, not a rule.
- The benefit goes to the human reader and to the editor: mistakes become
  visible without running the code.
- The type inside a container is written in square brackets: `list[str]`,
  `dict[str, int]`, `dict[str, list[int]]`.
- If a value may be absent, write `int | None`; the reader then knows they have
  to check.
- A function that returns no value gets `-> None`.
- In older code you will see `List[str]` and `Optional[str]`; the modern
  spelling is `list[str]` and `str | None`.
- Write them where they answer a question, not everywhere — starting with
  function signatures.
