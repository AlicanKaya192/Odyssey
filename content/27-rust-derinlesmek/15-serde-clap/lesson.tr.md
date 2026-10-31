# Bitirme: serde ve clap

Gerçek Rust programları her şeyi kendisi yazmaz. Bu modülün sonunda iki yaygın paketi öğreniyor ve bir araç yapıyoruz:
**serde** değerleri JSON gibi biçimlere çevirir, **clap** komut satırı argümanlarını okur. İkisi de bu modülde gördüğün
trait, derive ve hata tasarımı üzerine kurulu.

## Paket eklemek

Başkasının yazdığı crate `Cargo.toml`'daki `[dependencies]` tablosuna yazılır. Kendi projende bunu `cargo add` yapar ve
paket crates.io'dan iner:

```bash
cargo add serde --features derive
cargo add serde_json
cargo add clap --features derive
```

**Feature** paketin isteğe bağlı parçasıdır; `derive`, `#[derive(...)]` desteğini açar. Odyssey'de bu üç paketin kaynağı
programla geliyor, indirme gerekmiyor ve alıştırmaların `Cargo.toml`'u hazır. İlk derleme paketlerin kendisini de
derlediği için uzun sürer (bu bilgisayarda yaklaşık 10 saniye), sonrası bir saniyenin altında.

## serde: Değerden metne, metinden değere

**Serileştirme** (serialization) bellekteki değeri metne ya da baytlara çevirmektir; tersi **ters serileştirme**
(deserialization). `serde` genel çerçevedir, `serde_json` onun JSON biçimi:

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

`#[derive(Serialize, Deserialize)]` iki trait'in kodunu derleyiciye yazdırır. `to_string` ve `from_str` `Result` döndürür,
çünkü ikisi de başarısız olabilir. Hedef tür `let back: Note` ile söyleniyor; `parse` gibi.

`Vec`, `HashMap`, `Option` ve iç içe struct'lar da kendiliğinden çalışır. `to_string_pretty` okunur biçimde yazar:

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

## Yanlış veri bir hatadır

Python'da JSON okuyunca sözlük gelir ve yanlış alan ancak kullanıldığında patlar. Burada hedef tür bellidir, uymayan veri
daha okunurken reddedilir ve hata nerede olduğunu söyler:

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

Bu üç satır üç farklı sorun: eksik alan, yanlış tür, yarım JSON. `from_str` başarılı olduysa elindeki `Note` gerçekten
geçerli bir `Note`'tur.

## Şekli ayarlamak

Dışarıdan gelen JSON Rust'ın adlarına uymayabilir. Öznitelikler bunu kapatır:

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

| Öznitelik | Ne yapar |
|---|---|
| `rename_all = "camelCase"` | `task_name` alanı JSON'da `taskName` olur |
| `default` | Alan yoksa türün varsayılanı (`Vec` için boş liste) |
| `skip_serializing_if = "Option::is_none"` | `None` ise JSON'a hiç yazma |

`Option` alanlar okurken kendiliğinden isteğe bağlıdır: JSON'da yoksa `None`.

Enum'lar da çalışır. Varyant adı metin olur, bilinmeyen değer hata verir:

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

## Şekli bilinmeyen JSON: Value

Her JSON'a struct yazmak gerekmez. `serde_json::Value` her JSON değerini tutan bir enum'dur:

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

Olmayan anahtar panik yapmaz, `null` verir. `as_str`, `as_i64` gibi metotlar `Option` döndürür. Bu yol esnek ama denetimi
sana bırakır; şekli biliyorsan struct yaz.

## clap: Komut satırı

Argümanları Python'daki gibi `std::env::args` ile elle ayrıştırmak zordur: bayraklar, varsayılanlar, yardım metni, hata
mesajları. clap'te bir struct yazarsın, gerisi ondan üretilir:

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

`cargo run --` içindeki `--` "bundan sonrası programın" demektir. `///` yorumları yardım metnine dönüşür:

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

Yardımı yazmadık, alan adlarından ve türlerden çıktı. Yanlış kullanımda clap açıklayıp 2 koduyla çıkar:

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

## Alt komutlar

`git add`, `git log` gibi araçlar için enum yazılır, her varyant bir komuttur. `try_parse_from` hata durumunda çıkmak yerine
`Result` verir ve argümanı dizi olarak alır; denemek ve test için idealdir:

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
    // Denemek için: Gerçek programda Cli::parse()
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

## İkisi bir arada: Not aracı

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

Her parça tanıdık: `Box<dyn Error>` ile `?` farklı hataları toplar, `ok_or` `Option`'ı `Result`'a çevirir, `load` dosya
yokluğunu hata saymaz. Çalıştıralım:

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

Hata `main`'den döndüğü için Rust onu yazıp 1 koduyla çıktı.

## Sınamak

clap ve serde'nin ikisi de saf fonksiyon gibi sınanır: `try_parse_from` süreç argümanı istemez, gidiş dönüş testi dosya
istemez.

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

## Özet

- Paket `[dependencies]`'e yazılır; `derive` gibi parçalar feature ile açılır.
- `#[derive(Serialize, Deserialize)]`, `to_string`, `from_str`; hedef tür bellidir, uymayan veri okunurken reddedilir.
- `rename_all`, `default`, `skip_serializing_if` şekli ayarlar; şekil bilinmiyorsa `Value`.
- clap'te struct alanları argüman, türler davranış, `///` yardım olur; `Subcommand` enum'u alt komuttur.
- `try_parse_from` ile komut satırı da sınanır.
