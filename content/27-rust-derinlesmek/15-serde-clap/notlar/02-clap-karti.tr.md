## Tür davranışı belirler

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

| Alan türü | Davranış |
|---|---|
| `String` | Zorunlu değer |
| `Option<String>` | İsteğe bağlı değer |
| `Vec<String>` | Birden çok değer |
| `bool` | Bayrak: Verilirse `true` |
| `u32`, `f64` | Değer sayıya çevrilir, olmazsa hata |
| `ValueEnum` enum'u | Yalnızca o seçenekler |

## Öznitelikler

| Yazım | Ne yapar |
|---|---|
| `#[arg(short)]` | Tek harfli bayrak: `-t` |
| `#[arg(long)]` | Uzun bayrak: `--times` |
| `#[arg(default_value_t = 1)]` | Varsayılan değer |
| `#[arg(value_enum)]` | `ValueEnum` türü için |
| `#[command(name = "x", version)]` | Program adı, `--version` |
| `#[command(subcommand)]` | Alt komut alanı |
| `///` | Yardım metni |

## Hangi fonksiyon?

| Yazım | Girdi | Hata olunca |
|---|---|---|
| `Cli::parse()` | Süreç argümanları | Yazar, çıkar |
| `Cli::try_parse()` | Süreç argümanları | `Result` döner |
| `Cli::parse_from(dizi)` | Verilen dizi | Yazar, çıkar |
| `Cli::try_parse_from(dizi)` | Verilen dizi | `Result` döner |

Dizinin ilk öğesi program adıdır, ayrıştırılmaz.

## Çıkış kodları

| Durum | Kod |
|---|---|
| `--help`, `--version` | 0 |
| Yanlış kullanım | 2 |
| `main`'den `Err` | 1 |
