If you know another language, the difference is here:

| Question | Python | C | Rust |
|---|---|---|---|
| `a` after `b = a` | Usable, same object | Usable, same address | **Not usable** (moved) |
| Who gives memory back | Garbage collector | The programmer (`free`) | Code added by the compiler |
| Forgetting to give it back | Cannot happen | Easy | Cannot happen in most cases |
| Reading dropped memory | Cannot happen | Easy, dangerous | **Does not compile** |
| Run-time overhead | Yes | None | None |

## Through Python's eyes

In Python `b = a` gives one list two names. Changing one changes the other, and this is a common source of bugs. In Rust this situation does not exist to
begin with: there is one owner at a time.

## Through C's eyes

In C you write the `free` call. In Rust the end of a scope does the same job and you cannot write it wrongly. In C++ this idea is called RAII: a resource is tied
to an object's lifetime.

## This is not only about memory

Cleanup at the end of a scope works for every resource: a file closes when its variable goes out of scope, a lock is released when its variable goes. No chance of forgetting.

## Can Rust still leak memory?

It can. Leaking memory lies outside Rust's safety guarantee. `Box::leak` or `Rc` cycles pointing at each other do not give memory back, but those are written on purpose.
We will measure this when we see `Rc` in the second module.
