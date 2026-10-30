## Bu bölümün yenileri

| İş | Yazım |
|---|---|
| Argümanlar | `let args: Vec<String> = env::args().collect();` |
| Dosya oku | `fs::read_to_string(path)` |
| Satırlar | `text.lines()` |
| Küçük harf | `line.to_lowercase()` |
| İçeriyor mu | `line.contains("a")` |
| Stderr'e yaz | `eprintln!("...")` |
| Çık | `process::exit(1)` |

## Dosyaya yazmak

Araç yazmıyor ama kardeşi burada:

```rust
use std::fs;

fn main() -> Result<(), std::io::Error> {
    fs::write("out.txt", "first\nsecond\n")?;
    let text = fs::read_to_string("out.txt")?;
    println!("{}", text.lines().count());
    Ok(())
}
```

```text
2
```

| İş | Yazım |
|---|---|
| Bütününü yaz | `fs::write(path, text)` |
| Var mı | `Path::new(path).exists()` |
| Klasör aç | `fs::create_dir_all(path)` |

## Standart girdi

Dosya yerine stdin okumak için: `io::read_to_string(io::stdin())`. Aynı `search` fonksiyonuna verilebilir: Yan etkisiz ayırmanın faydası.

## Cargo komutları

| Komut | İş |
|---|---|
| `cargo run -- rust notes.txt` | `--`'den sonrası programın argümanı |
| `cargo test` | Testler |
| `cargo test parse` | Adında `parse` geçen testler |
| `cargo build --release` | En iyileştirilmiş derleme |
