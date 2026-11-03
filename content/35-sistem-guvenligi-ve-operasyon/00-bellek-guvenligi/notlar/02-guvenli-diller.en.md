Memory bugs are fought in two ways: finding and fixing the faulty code, or
choosing a language in which the bug **cannot be written**. The second is
more lasting, because it does not depend on a programmer never forgetting.

## How does a language protect memory?

- **Bounds checking:** every array access checks that the index is valid
  (Python, Java, Go, Rust). An overflow turns into an error instead of
  silent damage.
- **Automatic memory management:** memory is given back by the language
  once nobody uses it any more (a garbage collector: Python, Java, Go). The
  programmer cannot forget to give it back or do it twice.
- **Ownership rules:** Rust checks **at compile time** that every piece of
  data has a single owner and that borrowed data does not outlive its
  owner. Code with a use-after-free or a double free does not compile.

## What does it cost?

| Approach | Gain | Cost |
|---|---|---|
| C, C++ | Top speed, close to the hardware | Safety is left to the programmer |
| Garbage-collected language | Almost no memory bugs | Some speed and memory |
| Rust | Both speed and safety | Harder to learn, strict rules |

## Care in a safe language too

- Python itself and many packages are written in C; an overflow in them
  affects you too. That is why keeping packages up to date matters (the
  Dependencies and the Supply Chain section).
- In Rust an `unsafe` block switches the compiler's check off for that
  piece. In a review, `unsafe` blocks are read separately.
- Memory safety does not prevent **logic bugs**: a wrong permission check,
  an injection or a leaked password happen in a safe language too.

## What about old code?

Millions of lines of C and C++ cannot be rewritten in a day. The practical
way is layered:

1. Write new code in a memory-safe language.
2. Build and run old code with protection layers (the next section: ASLR,
   DEP, canaries).
3. Search for and replace the dangerous functions; scan with static
   analysis tools.
4. Rewrite first the parts that take the most data from outside (parsers,
   network code).
