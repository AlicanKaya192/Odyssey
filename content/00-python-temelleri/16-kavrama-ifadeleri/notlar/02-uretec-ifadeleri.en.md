When you write round brackets instead of square ones, what comes out is
not a list but a **generator**. The difference fits in one sentence: a
list builds every element in memory, a generator hands them over one at a
time as they are asked for.

```python
numbers = [1, 2, 3, 4, 5]

as_list = [n * n for n in numbers]
as_generator = (n * n for n in numbers)

print(as_list)
print(as_generator)
```

```
[1, 4, 9, 16, 25]
<generator object <genexpr> at 0x000001>
```

The generator has not computed anything yet; it only says "I can produce
this if you ask".

## Where it helps

```python
total = sum(n * n for n in numbers)
```

To add the squares up there is no need to keep them all: each square is
produced, added and forgotten. On a file with a million rows that is the
difference between filling memory and not.

The same thing is even clearer with `any` and `all`:

```python
has_negative = any(n < 0 for n in numbers)
```

`any` **stops** at the first `True`; the rest of the list is never
computed.

## Single use

A generator is walked over once:

```python
squares = (n * n for n in numbers)

print(sum(squares))
print(sum(squares))
```

```
55
0
```

The second sum is zero because the generator is used up. If you need the
same data twice, build a list.

## Which one to pick

<figure class="fig versus">
  <div class="ok">
    <h4>List</h4>
    <p>When you use the result more than once, ask for its length
    (<code>len</code>) or reach an element by index.</p>
  </div>
  <div class="dim">
    <h4>Generator</h4>
    <p>When you walk the result once and the data is large; when you hand
    it straight into <code>sum</code>, <code>any</code>, <code>all</code>
    or <code>max</code>.</p>
  </div>
</figure>

## One pair of brackets is enough

When the generator is the only argument of a function, there is no need
for a second pair of brackets:

```python
total = sum(n * n for n in numbers)        # right
total = sum((n * n for n in numbers))      # brackets not needed
```

With two arguments the brackets are required:

```python
print(max((n for n in numbers), default=0))
```
