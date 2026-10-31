# Capstone: serde and clap

Real Rust programs do not write everything themselves. At the end of this module we learn two widely used packages and build
a tool: **serde** converts values to formats such as JSON, and **clap** reads command line arguments. Both are built on the
traits, derives and error design you saw in this module.

## Adding a package

A crate written by someone else goes in the `[dependencies]` table of `Cargo.toml`. In your own project `cargo add` does this
and the package is downloaded from crates.io:

```bash
cargo add serde --features derive
cargo add serde_json
cargo add clap --features derive
```

A **feature** is an optional part of a package; `derive` turns on support for `#[derive(...)]`. In Odyssey the source of these
three packages comes with the program, nothing needs downloading, and the exercises' `Cargo.toml` is ready. The first build is
slow because it builds the packages too (about 10 seconds on this computer); after that it takes under a second.

## serde: from value to text and back

**Serialization** is turning a value in memory into text or bytes; the reverse is **deserialization**. `serde` is the general
framework, and `serde_json` is its JSON format:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Note {
    id: u32,
    title: String,
    done: bool,
}

fn main() {
    let note = Note { id: 1, title: "Buy tea".to_string(), done: false };
    let text = serde_json::to_string(&note).unwrap();
    println!("{text}");

    let back: Note = serde_json::from_str(&text).unwrap();
    println!("{back:?}");
}
```

```text
{"id":1,"title":"Buy tea","done":false}
Note { id: 1, title: "Buy tea", done: false }
```

`#[derive(Serialize, Deserialize)]` has the compiler write the code of two traits. `to_string` and `from_str` return a
`Result` because both can fail. The target type is stated by `let back: Note`, just as with `parse`.

`Vec`, `HashMap`, `Option` and nested structs work by themselves too. `to_string_pretty` writes in a readable form:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Note {
    id: u32,
    title: String,
    done: bool,
}

fn main() {
    let notes = vec![
        Note { id: 1, title: "Buy tea".to_string(), done: false },
        Note { id: 2, title: "Call Ada".to_string(), done: true },
    ];
    println!("{}", serde_json::to_string_pretty(&notes).unwrap());
}
```

```text
[
  {
    "id": 1,
    "title": "Buy tea",
    "done": false
  },
  {
    "id": 2,
    "title": "Call Ada",
    "done": true
  }
]
```

## Wrong data is an error

In Python, reading JSON gives you a dictionary, and a wrong field only blows up when it is used. Here the target type is
known, so data that does not fit is rejected while reading, and the error says where:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Note {
    id: u32,
    title: String,
    done: bool,
}

fn main() {
    let inputs = [
        r#"{"id": 1, "title": "Tea"}"#,
        r#"{"id": "one", "title": "Tea", "done": false}"#,
        r#"{"id": 1, "title": "Tea", "#,
    ];
    for input in inputs {
        match serde_json::from_str::<Note>(input) {
            Ok(note) => println!("ok: {note:?}"),
            Err(e) => println!("{e}"),
        }
    }
}
```

```text
missing field `done` at line 1 column 25
invalid type: string "one", expected u32 at line 1 column 12
EOF while parsing a value at line 1 column 26
```

These three lines are three different problems: a missing field, a wrong type, incomplete JSON. If `from_str` succeeded, the
`Note` in your hand really is a valid `Note`.

## Adjusting the shape

JSON from outside may not match Rust's names. Attributes close the gap:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Task {
    task_name: String,
    #[serde(default)]
    tags: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    due_date: Option<String>,
}

fn main() {
    let task: Task = serde_json::from_str(r#"{"taskName": "Write"}"#).unwrap();
    println!("{task:?}");
    println!("{}", serde_json::to_string(&task).unwrap());
}
```

```text
Task { task_name: "Write", tags: [], due_date: None }
{"taskName":"Write","tags":[]}
```

| Attribute | What it does |
|---|---|
| `rename_all = "camelCase"` | The field `task_name` becomes `taskName` in JSON |
| `default` | If the field is missing, the type's default (an empty list for `Vec`) |
| `skip_serializing_if = "Option::is_none"` | If it is `None`, do not write it into the JSON at all |

`Option` fields are optional by themselves when reading: if missing from the JSON, they are `None`.

Enums work too. The variant name becomes text, and an unknown value gives an error:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
enum Status {
    Open,
    Done,
}

#[derive(Debug, Serialize, Deserialize)]
struct Job {
    id: u32,
    status: Status,
}

fn main() {
    let job = Job { id: 7, status: Status::Done };
    println!("{}", serde_json::to_string(&job).unwrap());
    let open: Job = serde_json::from_str(r#"{"id": 8, "status": "open"}"#).unwrap();
    println!("{open:?}");
    let bad = serde_json::from_str::<Job>(r#"{"id": 9, "status": "lost"}"#);
    println!("{}", bad.unwrap_err());
}
```

```text
{"id":7,"status":"done"}
Job { id: 8, status: Open }
unknown variant `lost`, expected `open` or `done` at line 1 column 26
```

## JSON of unknown shape: Value

You do not have to write a struct for every JSON. `serde_json::Value` is an enum that holds any JSON value:

```rust
use serde_json::{Value, json};

fn main() {
    let text = r#"{"user": {"name": "Ada"}, "scores": [3, 5]}"#;
    let data: Value = serde_json::from_str(text).unwrap();
    println!("{}", data["user"]["name"]);
    println!("{:?}", data["user"]["name"].as_str());
    println!("{}", data["scores"][1]);
    println!("{}", data["missing"]);

    let made = json!({"ok": true, "count": 2});
    println!("{made}");
}
```

```text
"Ada"
Some("Ada")
5
null
{"count":2,"ok":true}
```

A missing key does not panic; it gives `null`. Methods such as `as_str` and `as_i64` return an `Option`. This way is flexible
but leaves the checking to you; if you know the shape, write a struct.

## clap: the command line

Parsing arguments by hand with `std::env::args` is hard: flags, defaults, help text, error messages. In clap you write a
struct, and the rest is generated from it:

```rust
use clap::Parser;

/// Greets someone.
#[derive(Parser)]
#[command(bin_name = "hello", version)]
struct Cli {
    /// Who to greet
    name: String,

    /// How many times
    #[arg(short, long, default_value_t = 1)]
    times: u32,
}

fn main() {
    let cli = Cli::parse();
    for _ in 0..cli.times {
        println!("Hello, {}!", cli.name);
    }
}

```

```text
$ cargo run -- Ada --times 2
Hello, Ada!
Hello, Ada!
```

The `--` in `cargo run --` means "what follows belongs to the program". The `///` comments become the help text:

```text
$ cargo run -- --help
Greets someone

Usage: hello [OPTIONS] <NAME>

Arguments:
  <NAME>  Who to greet

Options:
  -t, --times <TIMES>  How many times [default: 1]
  -h, --help           Print help
  -V, --version        Print version
```

We did not write the help; it came from the field names and types. On wrong use clap explains and exits with code 2:

```text
$ cargo run --
error: the following required arguments were not provided:
  <NAME>

Usage: hello <NAME>

For more information, try '--help'.

$ cargo run -- Ada --times x
error: invalid value 'x' for '--times <TIMES>': invalid digit found in string

For more information, try '--help'.
```

## Subcommands

For tools like `git add` and `git log` you write an enum, and each variant is a command. `try_parse_from` gives a `Result`
instead of exiting on error and takes the arguments as an array, which is ideal for trying things out and for tests:

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "notes")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Add a note
    Add { title: String },
    /// List all notes
    List,
}

fn main() {
    // To try it out: a real program uses Cli::parse()
    let add = vec!["notes", "add", "tea"];
    let list = vec!["notes", "list"];
    let wrong = vec!["notes", "remove"];
    for args in [add, list, wrong] {
        match Cli::try_parse_from(args) {
            Ok(cli) => match cli.command {
                Command::Add { title } => println!("adding {title}"),
                Command::List => println!("listing"),
            },
            Err(e) => println!("rejected: {}", e.kind()),
        }
    }
}
```

```text
adding tea
listing
rejected: unrecognized subcommand
```

## Both together: a notes tool

```toml
[package]
name = "notes"
version = "0.1.0"
edition = "2024"

[dependencies]
clap = { version = "4", features = ["derive"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

```

```rust
use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use std::error::Error;
use std::fs;

const FILE: &str = "notes.json";

#[derive(Parser)]
#[command(name = "notes")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Add a note
    Add { title: String },
    /// Mark a note as done
    Done { id: u32 },
    /// List all notes
    List,
}

#[derive(Serialize, Deserialize)]
struct Note {
    id: u32,
    title: String,
    done: bool,
}

fn load() -> Result<Vec<Note>, Box<dyn Error>> {
    match fs::read_to_string(FILE) {
        Ok(text) => Ok(serde_json::from_str(&text)?),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(Vec::new()),
        Err(e) => Err(e.into()),
    }
}

fn save(notes: &[Note]) -> Result<(), Box<dyn Error>> {
    fs::write(FILE, serde_json::to_string_pretty(notes)?)?;
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let cli = Cli::parse();
    let mut notes = load()?;
    match cli.command {
        Command::Add { title } => {
            let id = notes.iter().map(|n| n.id).max().unwrap_or(0) + 1;
            notes.push(Note { id, title, done: false });
            save(&notes)?;
            println!("added {id}");
        }
        Command::Done { id } => {
            let note = notes.iter_mut().find(|n| n.id == id).ok_or("no such note")?;
            note.done = true;
            save(&notes)?;
            println!("done {id}");
        }
        Command::List => {
            for n in &notes {
                let mark = if n.done { "x" } else { " " };
                println!("[{mark}] {} {}", n.id, n.title);
            }
        }
    }
    Ok(())
}

```

Every piece is familiar: `?` with `Box<dyn Error>` collects different errors, `ok_or` turns an `Option` into a `Result`, and
`load` does not count a missing file as an error. Let us run it:

```text
$ cargo run -- add tea
added 1

$ cargo run -- add milk
added 2

$ cargo run -- done 1
done 1

$ cargo run -- list
[x] 1 tea
[ ] 2 milk

$ cargo run -- done 9
Error: "no such note"
```

Because the error was returned from `main`, Rust wrote it and exited with code 1.

## Testing

clap and serde can both be tested like pure functions: `try_parse_from` needs no process arguments and a round trip test needs
no file.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_add() {
        let cli = Cli::try_parse_from(["notes", "add", "tea"]).unwrap();
        assert!(matches!(cli.command, Command::Add { title } if title == "tea"));
    }

    #[test]
    fn rejects_bad_id() {
        assert!(Cli::try_parse_from(["notes", "done", "x"]).is_err());
    }

    #[test]
    fn note_round_trip() {
        let note = Note { id: 1, title: "a".into(), done: true };
        let text = serde_json::to_string(&note).unwrap();
        let back: Note = serde_json::from_str(&text).unwrap();
        assert_eq!((back.id, back.done), (1, true));
    }
}
```

```text
running 3 tests
test tests::note_round_trip ... ok
test tests::parses_add ... ok
test tests::rejects_bad_id ... ok
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in
```

## Summary

- A package goes in `[dependencies]`; parts such as `derive` are turned on with a feature.
- `#[derive(Serialize, Deserialize)]`, `to_string`, `from_str`; the target type is known, so data that does not fit is rejected on reading.
- `rename_all`, `default` and `skip_serializing_if` adjust the shape; if the shape is unknown, `Value`.
- In clap struct fields become arguments, types behaviour and `///` the help; a `Subcommand` enum makes subcommands.
- The command line can be tested with `try_parse_from`.
