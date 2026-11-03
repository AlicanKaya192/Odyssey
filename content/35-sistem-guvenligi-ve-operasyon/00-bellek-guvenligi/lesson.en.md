# Memory Safety and Buffer Overflows

A running program keeps its data in memory: a name, a number, the contents
of a file. These pieces of data sit **next to each other** in memory.
Writing outside the space reserved for one variable silently damages the
variable right next to it. This is called a **memory safety bug**, and for
years it has been among the most serious kinds of security vulnerability.

This section shows how these bugs happen using a **toy memory** we build in
Python: we do not touch real memory, we only follow the same logic on a
`bytearray`. The goal is to recognise the bug and learn to prevent it.

## What is a buffer?

A **buffer** is a region of memory reserved for a fixed number of bytes. In
languages such as C, writing `char name[8];` reserves exactly 8 bytes in
memory. What happens when you try to write more than 8 bytes into it
depends on the language.

Python checks the bounds on every write. Writing outside the region stops
with an error:

```python
buffer = bytearray(8)
print(len(buffer))
try:
    buffer[8] = 65
except IndexError as error:
    print("IndexError:", error)
```

```text
8
IndexError: bytearray index out of range
```

The last valid index of an 8-byte buffer is `7`; writing to `8` was
blocked. This check is called **bounds checking**. C and C++ do not do it
on their own: the write runs past the region and damages the data beside
it. This is called a **buffer overflow**.

## Seeing an overflow in a toy memory

To imitate C's behaviour, let us build a 12-byte memory. The first 8 bytes
hold the user's name and the last 4 bytes hold the user's role:

| Bytes | 0–7 | 8–11 |
|---|---|---|
| Field | `name` (8 bytes) | `role` (4 bytes) |

A copy function that does not check bounds writes all of the data,
whatever its length:

```python
memory = bytearray(12)
memory[8:12] = b"USER"


def unsafe_copy(memory, start, data):
    for i, byte in enumerate(data):
        memory[start + i] = byte


unsafe_copy(memory, 0, b"alice")
print("name:", bytes(memory[0:8]))
print("role:", bytes(memory[8:12]))
unsafe_copy(memory, 0, b"Bartholomew!")
print("name:", bytes(memory[0:8]))
print("role:", bytes(memory[8:12]))
```

```text
name: b'alice\x00\x00\x00'
role: b'USER'
name: b'Bartholo'
role: b'mew!'
```

`alice` is 5 bytes; it fitted, and the remaining 3 bytes stayed zero.
`Bartholomew!` is 12 bytes: the first 8 went into the name
field and the other 4 bytes were written over the role. The role
is no longer `USER` but the tail of the name. The program raised no error;
it simply carried on with the wrong role.

That is the heart of the problem: an overflow is **silent**. In real
programs the overflowing data can damage a role, a counter, a pointer, or
the information that tells the program where to go next. If data from
outside (a network packet, a file, a form field) can trigger the overflow,
an attacker can change how the program behaves. That is why an overflow is
a **security** bug and not just a software bug.

## The fix: measure before you write

The fix is simple: before copying, check whether the data fits in the
region.

```python
def safe_copy(memory, start, size, data):
    if len(data) > size:
        return False
    memory[start:start + len(data)] = data
    return True


memory = bytearray(12)
memory[8:12] = b"USER"
print(safe_copy(memory, 0, 8, b"alice"))
print(safe_copy(memory, 0, 8, b"Bartholomew!"))
print("role:", bytes(memory[8:12]))
```

```text
True
False
role: b'USER'
```

The long name was rejected and the role stayed in place. Rejecting long
data and keeping only as much as fits (truncating) are both valid choices;
which one is right depends on the job. The one wrong thing is writing
without measuring.

This is why some standard C functions are considered dangerous: `gets`,
`strcpy`, `strcat` and `sprintf` write without knowing the size of the
target. Their size-aware counterparts `fgets`, `strncpy` / `strlcpy`,
`strncat` and `snprintf` are used instead. In a code review (the Code Review
and Static Analysis section) these names are among the first things
searched for.

## One too many: off-by-one

The sneakiest form of overflow is writing **one too many**. Writing a loop
bound with `<=` (or `range(size + 1)`) damages the single byte right after
the region:

```python
size = 8
written = []
for i in range(size + 1):
    written.append(i)
print(len(written), "bytes written into", size)
print("last index:", written[-1])
```

```text
9 bytes written into 8
last index: 8
```

9 bytes were written into an 8-byte region; the last index is
`8`, outside the region. One byte looks small, but that byte may be the
zero that marks the end of a string or part of a length field. Strings in C
end with a zero byte; an 8-letter name needs **9** bytes. Forgetting that
one byte causes the same bug.

## Integer overflow: when the size calculation goes wrong

Sometimes the problem starts not in the copy but **while calculating the
size of the region**. Numbers in C have a fixed width; an 8-bit number holds
at most 255 and anything above wraps around to the start (`n & 0xFF`
imitates this):

```python
def size_8bit(n):
    return n & 0xFF


header = 200
body = 100
print("real size:", header + body)
print("8-bit size:", size_8bit(header + body))
```

```text
real size: 300
8-bit size: 44
```

For data that needs 300 bytes, a region of only 44 bytes
is reserved; the copy that follows writes all 300 bytes and the
region overflows. That is why the size calculation is part of bounds
checking too: you check whether the result will fit **before** adding or
multiplying.

## The family of memory bugs

| Bug | What happens? |
|---|---|
| **Buffer overflow** | Writing past the end of the region damages nearby data |
| **Out-of-bounds read** | Reading outside the region leaks other data |
| **Off-by-one** | A bound is calculated one too small or one too large |
| **Integer overflow** | The size calculation wraps, the region is too small |
| **Use-after-free** | Memory that was given back is still used |
| **Double free** | The same memory is given back twice |

What they all share: the program touches a region of memory that does not
belong to it or is no longer valid.

## Memory-safe languages

<figure class="fig"><div class="versus">
  <div><h4>Not memory-safe (C, C++)</h4>They give speed and closeness to the hardware. Bounds checks and deciding when memory is given back are left to the <b>programmer</b>. One slip means a silent overflow.</div>
  <div><h4>Memory-safe (Python, Rust, Go, Java)</h4>The language checks every access or manages the lifetime of memory itself. An overflow <b>stops as an error</b> and does not damage nearby data.</div>
</div><figcaption>A memory-safe language removes most of this family of bugs from the start.</figcaption></figure>

Code you write in Python is protected from most of these bugs, but not all
of them: Python itself and many of the libraries you use (such as NumPy)
are written in C. An overflow in that C code affects the Python program
too. Rust checks memory safety at compile time and does so as fast as C;
the Rust track covers this in detail.

The next section covers the layers that operating systems and compilers add
to protect programs that are not memory-safe: ASLR, DEP and canaries.

## Summary

- A buffer is a fixed-size region of memory; writing outside it is a
  **buffer overflow** and **silently** damages nearby data.
- Python does **bounds checking** on every write; C and C++ do not.
- The fix: **measure** before writing; reject or truncate long data.
- `gets`, `strcpy`, `strcat`, `sprintf` write without knowing the size;
  their size-aware counterparts are used instead.
- **Off-by-one** and **integer overflow** lead to the same result: the
  region is smaller than assumed.
- **Memory-safe languages** prevent most of this family of bugs from the
  start.
