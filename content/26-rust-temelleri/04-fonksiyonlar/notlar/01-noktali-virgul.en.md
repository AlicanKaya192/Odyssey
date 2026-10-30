## What one sign means

In Rust a semicolon means "throw this value away". See the two versions side by side:

<figure class="fig"><div class="versus"><div><h4>A value returns</h4><code>fn f() -&gt; i32 { 5 }</code><br>The block gives the value 5.</div><div><h4>An error</h4><code>fn f() -&gt; i32 { 5; }</code><br>The block gives <code>()</code>, but <code>i32</code> was promised.</div></div><figcaption>The only difference is one semicolon.</figcaption></figure>

## Where is it needed?

| Place | Semicolon |
|---|---|
| End of a `let` line | Needed |
| End of a `println!(...)` line | Needed; on a last line it makes no difference since the value is `()` |
| A final expression with a return value | **Not allowed** |
| After a `fn` body's closing `}` | Not needed |
| After the close of an `if` or `for` block | Not needed |
| `return x` | Written as `return x;` by convention |

## If you forget the return type

This is common too:

```rust
fn double(n: i32) {
    n * 2
}

fn main() {
    double(2);
}
```

```text
error[E0308]: mismatched types
 --> main.rs:2:5
  |
1 | fn double(n: i32) {
  |                  - help: try adding a return type: `-> i32`
2 |     n * 2
  |     ^^^^^ expected `()`, found `i32`
```

The body gives an `i32`, but the signature promises nothing. The fix is to add `-> i32` to the signature. The `help:` line says so.

## Naming rules

| Item | Style | Example |
|---|---|---|
| Function | `snake_case` | `total_price` |
| Variable | `snake_case` | `user_name` |
| Constant | `SCREAMING_SNAKE_CASE` | `MAX_SIZE` |
| Type, trait | `PascalCase` | `UserAccount` |

The compiler warns about names that break these rules.
