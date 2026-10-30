## Commands and forms

| Job | Written |
|---|---|
| Inline module | `mod a { ... }` |
| Module from a file | `mod a;` |
| Opening outwards | `pub fn`, `pub struct`, `pub mod` |
| Short name | `use a::b;` |
| Several names | `use a::{b, c};` |
| With a new name | `use a::b as c;` |
| All | `use a::*;` (avoid outside tests) |
| Opening again | `pub use a::b;` |

## Where is the file looked for?

| Where you are | What you wrote | Looked for |
|---|---|---|
| `src/main.rs` | `mod net;` | `src/net.rs` |
| `src/net.rs` | `mod tcp;` | `src/net/tcp.rs` |

If not found you get `E0583`, and the error names both possible paths.

## Error codes

| Code | Meaning |
|---|---|
| `E0603` | This name is private (`pub` is missing) |
| `E0616` | A struct field is private |
| `E0433` | The path was not found (`use` or `mod` is missing) |
| `E0432` | The thing being `use`d does not exist |
| `E0583` | The module file is missing |
