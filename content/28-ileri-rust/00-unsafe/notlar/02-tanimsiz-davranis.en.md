## What undefined behavior is not

| Assumed | Reality |
|---|---|
| The program crashes | It may not, and may show nothing |
| A random value is read | The compiler may delete the code entirely |
| It affects only that line | Even earlier lines can change |
| It appears in debug mode | It may appear only in `--release` |

The compiler optimizes **assuming undefined behavior never happens**. It can delete a branch reasoning "this branch would be undefined, so it never runs". So the result cannot be predicted.

## The list of rules

These are always undefined behavior:

| Rule | Example |
|---|---|
| Reading an invalid pointer | Null, freed, out of bounds |
| Reading unaligned | A `u32` from an odd address with `*p` |
| Breaking the aliasing rule | Changing through another path while a `&mut` is alive |
| Producing an invalid value | `bool` 2, an absent `enum` variant, a non-UTF-8 `str` |
| A data race | Two branches without a lock, one writing |
| Changing what is behind a `&T` | Without `UnsafeCell` |

## How is it caught?

| Tool | What it does | Its limit |
|---|---|---|
| Tests | Show some errors | Passing is no proof |
| Miri | Interprets the program, checks most rules | Needs nightly, slow, does not run FFI |
| Sanitizers | Catch memory errors while running | Nightly, only the path taken |
| Review | Reading the `// SAFETY:` comments | Human effort |

Miri and sanitizers are not installed in this path; knowing the names is enough. If you write a real `unsafe` crate, put Miri in CI.

## A short rule

If you showed an `unsafe` block is correct with only **one run**, you showed nothing. Write the reasoning, then compare it with the list of rules.
