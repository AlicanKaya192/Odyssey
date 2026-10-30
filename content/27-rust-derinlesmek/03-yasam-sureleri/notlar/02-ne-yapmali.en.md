## When a lifetime error comes, ask in order

1. **Who should own what is returned?** If the function makes a new value, return an owned type rather than a reference.
2. **Which input does the returned reference come from?** Mark only that one.
3. **Must the struct really hold a reference?** A `String` is usually simpler.
4. **`clone` as a last resort:** On small data it is acceptable and no mistake.

## Owned or reference?

| Situation | Choice |
|---|---|
| You return a part of the input | `&str` |
| You make new text | `String` |
| The struct will live long | A `String` field |
| A short-lived view of very large text | A `&'a str` field |

## Practice: words

A structure holding parts of the input without copying:

```rust
#[derive(Debug)]
struct Token<'a> {
    text: &'a str,
    position: usize,
}

fn tokens(line: &str) -> Vec<Token<'_>> {
    let mut found = Vec::new();
    for (position, text) in line.split_whitespace().enumerate() {
        found.push(Token { text, position });
    }
    found
}

fn main() {
    let line = String::from("go rust");
    for t in tokens(&line) {
        println!("{} {}", t.position, t.text);
    }
}
```

```text
0 go
1 rust
```

Each `Token` points to the original text, and not one byte was copied. The price: `tokens` cannot live unless `text` does.

## Wrong fixes

| Seen | Why it is wrong |
|---|---|
| `'static` everywhere | A local value is not `'static`; the error shifts elsewhere |
| Adding `'a` and returning a local reference | A mark does not keep a value alive |
| A needless `<'a>` | Elision already does it; `cargo clippy` says so |
