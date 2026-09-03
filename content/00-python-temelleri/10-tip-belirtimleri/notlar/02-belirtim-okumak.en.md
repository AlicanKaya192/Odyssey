Real code contains lines like this:

```python
def group(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    ...
```

At first glance it is unreadable. But there is a method, and once you learn it
every annotation works the same way.

## The method: find the outermost container

An annotation always has this shape:

<figure class="fig anat">
  <div class="sig"><u class="m1">dict</u>[<u class="m2">str</u>, <u class="m3">list[int]</u>]</div>
  <ul class="legend">
    <li class="m1"><b>The container</b> — the word before the first bracket. This is a dictionary.</li>
    <li class="m2"><b>First part</b> — the type of the keys in that dictionary.</li>
    <li class="m3"><b>Second part</b> — the type of the values. It can be a container itself.</li>
  </ul>
</figure>

So, three steps:

1. Look at the word **before** the first square bracket. That is the container.
2. Split what is inside the brackets. `dict` splits in two, `list` in one.
3. If one of the parts is still a container, apply the same three steps to it.

## Example 1

```python
list[str]
```

- Container: `list`
- Inside: `str`

**A list of strings.** Example value: `["a", "b"]`

## Example 2

```python
dict[str, list[int]]
```

- Container: `dict`, so it has two parts.
- Keys: `str`
- Values: `list[int]` → a container again, so we look once more: a list of
  numbers.

**A dictionary with string keys whose values are lists of numbers.** Example
value:

```python
{"Ada": [90, 85], "Alan": [70]}
```

## Example 3

```python
list[dict[str, str]]
```

- Container: `list`
- Inside: `dict[str, str]` → a dictionary with string keys and string values.

**A list of dictionaries.** This is how the rows of a table are held:

```python
[
    {"name": "Ada", "city": "London"},
    {"name": "Alan", "city": "Wilmslow"},
]
```

## Example 4 — the line from the top

Now we can go back to the difficult line:

```python
def group(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
```

**Parameter:** `list[dict[str, str]]` → a list of dictionaries. In other words,
the rows of a table.

**Return:** `dict[str, list[dict[str, str]]]`

- Container: `dict`
- Keys: `str`
- Values: `list[dict[str, str]]` → a list of rows again.

**Conclusion:** the function takes rows, groups them by some string, and gives
back the rows of each group as a separate list. Its name is `group` already;
the annotation confirms it.

You worked out what it does without looking inside the function once. That is
exactly what an annotation is for.

## The trailing `| None`

If you see `| None` at the end of an annotation, it belongs to the outermost
type:

```python
def find(name: str) -> dict[str, int] | None:
    ...
```

This means "returns a dictionary, or nothing" — it says nothing about the
*values* in the dictionary. People mix these up:

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h5>THE DICTIONARY MAY BE ABSENT</h5>
<pre><code>dict[str, int] | None</code></pre>
    </div>
    <div class="ok">
      <h5>THE VALUES MAY BE ABSENT</h5>
<pre><code>dict[str, int | None]</code></pre>
    </div>
  </div>
  <figcaption>The function on the left may return no dictionary at all. The one on the right always returns a dictionary, but some values inside it may be empty. Inside the brackets or outside — that is the only difference.</figcaption>
</figure>

## When you get stuck

When you see a long annotation, write it on paper and match up the brackets.
Once you have found the outermost container, the rest is the same operation
repeated.

One more thing that helps: write an **example value** that fits the
annotation. The moment you write `{"a": [1, 2]}` for `dict[str, list[int]]`,
the annotation becomes concrete.
