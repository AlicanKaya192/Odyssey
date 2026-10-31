## syn and quote

In this section we parsed tokens by hand so that we could see behind the door. In a real project almost everyone uses two crates:

| Crate | Its job |
|---|---|
| `syn` | Turns tokens into a full syntax tree (`DeriveInput`, fields, generics, attributes) |
| `quote` | Lets you write code as code with `quote! { ... }`, with placeholders |
| `proc-macro2` | The testable token types these two use |

They are not installed in this path; knowing their names is enough. The fact that our hand-written `field_list` falls short on `enum`s, tuple structs and generics is exactly why these crates exist.

## Ready-made examples

| Macro | Kind | What it produces |
|---|---|---|
| `#[derive(Serialize)]` | Derive | Serialization code |
| `#[tokio::main]` | Attribute | Wraps `main` with an executor |
| `#[test]` | Built-in attribute | Test registration |
| `sqlx::query!` | Function-like | Checks SQL at compile time |

## Security: code runs during compilation

A procedural macro runs inside the compiler, with your permissions. It can read files and reach the network. So adding a crate is not only "adding code to my program" but also "running code on my computer during compilation". The same applies to `build.rs`. When choosing a dependency, look at who wrote it, and fix the version with `Cargo.lock`.

## Compile time

| Factor | Its effect |
|---|---|
| A separate crate | It compiles first |
| Parser crates | `syn` itself is big |
| The code you produce | Each call gives the compiler work |

Widely used derives can take a visible share of compile time. `cargo build --timings` shows how long each crate took.

## Which tool to choose?

| Need | Tool |
|---|---|
| Shared behaviour | Traits and generics |
| The same code for many types | `macro_rules!` |
| Varying numbers of arguments | `macro_rules!` |
| Reading a struct's fields | Derive |
| Wrapping a function | Attribute |
| Checking text at compile time | Function-like |

The order is this: first functions and traits, failing that `macro_rules!`, failing that a procedural macro.

## Testing

You cannot run a macro outside the compiler, because `proc_macro` exists only inside it. Three ways:

| Way | How |
|---|---|
| A usage test | Use the macro in another crate and check the result |
| An error test | The `trybuild` crate, an expected compile error |
| Separating the logic | Put the work in a function using `proc-macro2` |
