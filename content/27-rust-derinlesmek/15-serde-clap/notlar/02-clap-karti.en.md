## The type decides the behaviour

```rust
use clap::{Parser, ValueEnum};

#[derive(Clone, Debug, ValueEnum)]
enum Level {
    Low,
    High,
}

#[derive(Parser, Debug)]
struct Cli {
    /// Files to read
    files: Vec<String>,
    /// Print more
    #[arg(short, long)]
    verbose: bool,
    /// Output path
    #[arg(short, long)]
    output: Option<String>,
    #[arg(long, value_enum, default_value_t = Level::Low)]
    level: Level,
}

fn main() {
    let cli = Cli::parse_from(["app", "a.txt", "b.txt", "-v", "--level", "high"]);
    println!("{cli:?}");
}
```

```text
Cli { files: ["a.txt", "b.txt"], verbose: true, output: None, level: High }
```

| Field type | Behaviour |
|---|---|
| `String` | A required value |
| `Option<String>` | An optional value |
| `Vec<String>` | Several values |
| `bool` | A flag: `true` if given |
| `u32`, `f64` | The value is converted to a number, or it is an error |
| A `ValueEnum` enum | Only those choices |

## Attributes

| Written as | What it does |
|---|---|
| `#[arg(short)]` | A one-letter flag: `-t` |
| `#[arg(long)]` | A long flag: `--times` |
| `#[arg(default_value_t = 1)]` | A default value |
| `#[arg(value_enum)]` | For a `ValueEnum` type |
| `#[command(name = "x", version)]` | The program name, `--version` |
| `#[command(subcommand)]` | The subcommand field |
| `///` | The help text |

## Which function?

| Written as | Input | On error |
|---|---|---|
| `Cli::parse()` | Process arguments | Writes, exits |
| `Cli::try_parse()` | Process arguments | Returns a `Result` |
| `Cli::parse_from(array)` | The given array | Writes, exits |
| `Cli::try_parse_from(array)` | The given array | Returns a `Result` |

The first item of the array is the program name and is not parsed.

## Exit codes

| Situation | Code |
|---|---|
| `--help`, `--version` | 0 |
| Wrong use | 2 |
| `Err` from `main` | 1 |
