# Cargo ve İlk Proje

Tek dosyalık program için `rustc main.rs` yeter. Ama gerçek bir proje birden fazla
dosyadan oluşur, başkalarının yazdığı kodu kullanır ve ayarlar ister. Bunları elle
yönetmek zordur. **Cargo**, Rust'ın proje yöneticisidir ve bütün Rust dünyası onu kullanır.

Cargo'nun yaptığı üç temel iş var: projeyi derler, çalıştırır ve projenin ihtiyaç duyduğu
başka kodları indirir.

## Yeni proje

Terminalde bir proje oluşturalım:

```bash
cargo new hello
```

```text
Creating binary (application) `hello` package
```

Cargo bir klasör açtı ve içine şunları koydu:

```text
hello
├── .git
├── .gitignore
├── Cargo.toml
└── src
    └── main.rs
```

Kaynak kod `src` (source, kaynak) klasöründe durur. `src/main.rs` dosyası ilk programımızla
neredeyse aynıdır; Cargo hazır bir "Hello, world!" yazıyor. `.git` ve `.gitignore` sürüm kontrol
aracı Git içindir: Bilgisayarında Git varsa Cargo bir depo da açar. Git'i bilmiyorsan şimdilik önemli değil.

## Cargo.toml: projenin kimliği

`Cargo.toml` projenin ayar dosyasıdır. TOML adlı basit bir biçimde yazılır: `ad = "değer"`
satırları ve köşeli parantezli başlıklar.

```toml
[package]
name = "hello"
version = "0.1.0"
edition = "2024"

[dependencies]
```

| Satır | Anlamı |
|---|---|
| `[package]` | Bu başlığın altı projenin kendisini anlatır |
| `name` | Projenin adı; oluşan programın adı da budur |
| `version` | Projenin sürüm numarası |
| `edition` | Rust'ın hangi **baskısının** kurallarıyla derleneceği |
| `[dependencies]` | Projenin kullandığı başka paketler; şimdilik boş |

**Baskı** (edition) ne demek? Rust birkaç yılda bir, eski kodu bozmadan dile küçük değişiklikler
getiren yeni bir baskı çıkarıyor: 2015, 2018, 2021, 2024. Her proje hangi baskıyı kullandığını
kendi dosyasında söyler, böylece eski projeler derlenmeye devam eder. Yeni projelerde en sonuncuyu
kullanırız.

## Derlemek ve çalıştırmak

Proje klasörüne girip derleyelim. `cd` terminalde klasör değiştirir:

```bash
cd hello
cargo build
```

```text
Compiling hello v0.1.0 (C:\projects\hello)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
```

Satırda bir şey öğreniyoruz: Bu derleme `dev` profiliyle yapıldı, yani **hızlı derleme, yavaş
program** ayarıyla. `unoptimized` kod iyileştirilmedi demek, `debuginfo` hata ayıklama bilgisi
eklendi demek. Süre bilgisayara göre değişir.

Program `target/debug/` altında oluşur. Cargo'nun bütün üretimi `target` klasöründedir; onu
silsen de kaynak kodun yerinde kalır ve bir sonraki derlemede yeniden oluşur.

Derleyip hemen çalıştırmak için:

```bash
cargo run
```

```text
Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.01s
Running `target\debug\hello.exe`
Hello, world!
```

Bu kez `Compiling` satırı yok: Cargo hiçbir şeyin değişmediğini gördü ve yeniden derlemedi. Kodu
değiştirirsen `cargo run` önce derler.

## Hızlı denetim: cargo check

Kod yazarken çoğu zaman yalnızca "derleniyor mu?" sorusunun cevabını isteriz. `cargo check` kuralları
denetler ama program üretmez, bu yüzden büyük projelerde `cargo build`'den çok daha hızlıdır.

```bash
cargo check
```

```text
Checking hello v0.1.0 (C:\projects\hello)
Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
```

## Hızlı program: --release

Yayınlayacağın programı iyileştirmeli derlersin:

```bash
cargo build --release
```

```text
Compiling hello v0.1.0 (C:\projects\hello)
Finished `release` profile [optimized] target(s) in 0.17s
```

Bu kez profil `release`, sonuç `optimized`: derleme daha uzun sürer, program daha hızlı çalışır.
Dosya `target/release/` altına gider.

Farkı ölçmek için aynı programı iki profille çalıştırdık. Program bir döngüde 300 milyon kez toplama
yapıyor. Bu bilgisayarda:

```text
debug:   1.59 s
release: 0.46 s
```

Bir programın hızını ölçerken `--release` kullanmayı unutma. Debug derlemede ölçülen sayılar yanıltır.

<figure class="fig"><div class="versus"><div><h4>cargo build</h4>Geliştirirken. Hızlı derlenir, yavaş çalışır, taşma gibi hataları denetler. Sonuç <code>target/debug/</code>.</div><div><h4>cargo build --release</h4>Yayınlarken ve ölçerken. Yavaş derlenir, hızlı çalışır. Sonuç <code>target/release/</code>.</div></div><figcaption>İki profil aynı koddan iki farklı program üretir.</figcaption></figure>

## Paketler: crate

Rust'ta bir derleme birimine, yani bir kütüphaneye ya da programa **crate** denir (İngilizce "sandık").
Başkalarının yazdığı crate'ler `crates.io` sitesinde durur. Birini kullanmak için `[dependencies]`
altına adını ve sürümünü yazman yeter, Cargo gerisini halleder:

```toml
[dependencies]
serde = "1"
```

Bu ilk derlemede crate'i indirir ve derler. Hangi sürümlerin kullanıldığını `Cargo.lock` dosyasına yazar;
böylece projeyi başka bir bilgisayarda derleyen de aynı sürümleri alır. `Cargo.toml` senin isteğin,
`Cargo.lock` Cargo'nun o istekten çıkardığı kesin kayıttır.

Dış paketleri bu modülde kullanmayacağız. Önce dilin kendisini öğreneceğiz.

## Odyssey'de Cargo

Bu patikanın çoğu alıştırması tek dosyadır ve `rustc main.rs` ile derlenir. Alıştırmada `Cargo.toml`
görürsen Odyssey `cargo` kullanır ve hepsi internet olmadan çalışır. Bu bölümün alıştırmalarında
`Cargo.toml` dosyasını da düzenleyeceksin.

Bir ipucu: Bir değeri derleme sırasında `Cargo.toml`'dan okuyabilirsin. `env!` makrosu verilen adı
derleme anında metne çevirir ve Cargo projenin adını `CARGO_PKG_NAME` adıyla verir:

```rust
fn main() {
    println!("{} {}", env!("CARGO_PKG_NAME"), env!("CARGO_PKG_VERSION"));
}
```

```text
hello 0.1.0
```

## Özet

- `cargo new ad` proje açar; kod `src/main.rs`'te, ayarlar `Cargo.toml`'da.
- `cargo run` derleyip çalıştırır, `cargo build` yalnızca derler, `cargo check` yalnızca denetler.
- `--release` yavaş derler, hızlı çalıştırır. Hız ölçümleri onunla yapılır.
- `target` üretilen dosyalardır, kaynak kod değildir.
- Paketlere crate denir; `Cargo.toml`'daki `[dependencies]` altına yazılır, kesin sürümler `Cargo.lock`'ta durur.
