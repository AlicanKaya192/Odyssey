# Rust Nedir, Nasıl Kurulur

Bu patika hiç kod yazmamış birinin de yürüyebileceği şekilde yazıldı. Her
yeni kelime ilk geçtiği yerde açıklanıyor. Daha önce başka bir dil bildiysen
ilk birkaç bölümden hızlı geçersin; asıl yeni olan şeyler Sahiplik bölümünde
başlıyor.

## Program ne, derleyici ne?

Bilgisayarın işlemcisi yalnızca kendi dilini anlar: **makine kodu**, yani
sayılardan oluşan çok küçük komutlar. İnsanın okuyacağı metin olarak yazdığımız
koda **kaynak kod** denir. Arada biri çeviri yapmalı.

Rust'ta bu işi **derleyici** (compiler) yapar. Derleyici kaynak kodunu baştan
sona okur, kuralları denetler ve tek parça bir program dosyası üretir. Windows'ta
bu dosyanın uzantısı `.exe`'dir. Program bir kez derlendikten sonra çalışması
için ne kaynak koda ne de derleyiciye ihtiyaç duyar.

<figure class="fig"><div class="flow"><span class="node">main.rs<br>kaynak kod</span><span class="arrow">→</span><span class="node acc">rustc<br>derleyici</span><span class="arrow">→</span><span class="node ok">main.exe<br>program</span></div><figcaption>Rust'ın derleyicisinin adı <code>rustc</code>. Kod hatalıysa üçüncü kutu hiç oluşmaz.</figcaption></figure>

Python gibi yorumlanan dillerde ise program çalışırken satır satır çevrilir.
Farkı şöyle düşün:

<figure class="fig"><div class="versus"><div><h4>Python</h4>Hata, o satıra gelince ortaya çıkar. Nadiren çalışan bir satırdaki yanlış haftalarca fark edilmeyebilir.</div><div><h4>Rust</h4>Hata, program çalışmadan önce ortaya çıkar. Derleyici razı olmadan program oluşmaz.</div></div><figcaption>İki yolun da yeri var; Rust bedeli başta ödetiyor.</figcaption></figure>

## Rust neden var?

Programlar çalışırken verilerini **bellekte** (RAM) tutar. Bellek işi bitince
geri verilmelidir. Dillerin çoğu bu işi iki yoldan biriyle çözer:

- **Elle yönetim** (C, C++): Programcı "şu belleği geri ver" der. Çok hızlıdır,
  ama unutmak ya da iki kez vermek güvenlik açıklarına yol açar.
- **Çöp toplayıcı** (Python, Java, C#): Program çalışırken arkada bir yardımcı
  kullanılmayan belleği bulup temizler. Rahattır, ama ek iş ve bekleme demektir.

Rust üçüncü yolu seçti: **sahiplik** kuralları. Hangi verinin ne zaman geri
verileceği derleme sırasında kanıtlanır. Çalışırken arkada bir yardımcı yoktur ve
bu kuralları çiğneyen kod derlenmez. Sonuç, C'ye yakın hız ve bellek güvenliğidir.
Bu kuralları Sahiplik bölümünde adım adım göreceğiz.

Bedeli de açıkça söyleyelim: **Derleyici sıkıdır.** Başlarda kodun sık sık
reddedilecek. Bu bir başarısızlık değil, Rust'ın çalışma şekli. Derleyicinin
mesajları çoğu zaman sorunu ve çözümü de yazar; onları okumayı öğreneceğiz.

## Kurulum

Rust'ı kurmanın resmî yolu **rustup** adlı programdır. Rustup derleyiciyi kurar,
yeni sürümleri getirir ve yanına iki araç daha koyar:

| Araç | Ne işe yarar |
|---|---|
| `rustc` | Derleyici: kaynak kodu programa çevirir |
| `cargo` | Proje yöneticisi: derler, çalıştırır, paket indirir (ileride kendi bölümü var) |
| `rustup` | Kurulum yöneticisi: Rust'ın kendisini günceller |

Windows'ta adımlar şöyle:

1. Tarayıcıda `https://www.rust-lang.org/tools/install` sayfasını aç ve
   `rustup-init.exe` dosyasını indir.
2. Dosyayı çalıştır. Kurulum sırasında Visual Studio kurmanı isteyebilir: Rust'ın
   programı birleştirirken kullandığı **bağlayıcı** (linker) oradan geliyor. Yönergeyi
   izle, varsayılan seçenekleri kabul et.
3. Kurulum bitince açık terminalleri ve **Odyssey'i kapatıp yeniden aç**. Rust'ın
   klasörü ancak yeni açılan programlarda görünür.

**Terminal**, komut yazdığın yazı penceresidir. Windows'ta Başlat menüsünden
"PowerShell" yazarak açabilirsin. Kurulumu şu iki komutla sına:

```bash
rustc --version
cargo --version
```

Numaralar farklı olabilir; önemli olan bir sürüm yazmasıdır:

```text
rustc 1.99.1 (58cf8f9c3 2026-10-13)
cargo 1.99.1 (5f94df478 2026-08-27)
```

Sorun çıkarsa bu bölümün "Kurulum Sorunları" notuna bak. Bu patikadaki
alıştırmalar senin bilgisayarındaki derleyiciyi kullanır; yani bu adım şart.

## İlk program

Geleneksel ilk program ekrana bir selam yazar. Kodun tamamı üç satır:

```rust
fn main() {
    println!("Hello, world!");
}
```

Çıktısı:

```text
Hello, world!
```

Üç satırda dört yeni şey var. Tek tek bakalım.

<figure class="fig"><div class="anat"><div class="anat-row"><span><code>fn</code></span><span>"function" (fonksiyon) kelimesinin kısaltması: birazdan bir fonksiyon tanımlıyorum demek. Fonksiyon, adı olan bir iş parçasıdır.</span></div><div class="anat-row"><span><code>main</code></span><span>Fonksiyonun adı. Bu ad özeldir: program her zaman <code>main</code> fonksiyonundan başlar.</span></div><div class="anat-row"><span><code>{ }</code></span><span>Süslü parantezler fonksiyonun gövdesini sarar. İşler bunların arasında yazılır.</span></div><div class="anat-row"><span><code>println!</code></span><span>Ekrana bir satır yazar. Sondaki <code>!</code> bunun bir <b>makro</b> olduğunu gösterir: şimdilik "ünlemle çağrılan özel komut" diye düşün.</span></div><div class="anat-row"><span><code>;</code></span><span>Noktalı virgül komutun bittiğini söyler.</span></div></div><figcaption>İlk programın parçaları.</figcaption></figure>

Tırnak içindeki yazıya **metin** (string) denir ve olduğu gibi yazılır. Birden
fazla `println!` yazarsan yukarıdan aşağıya sırayla çalışırlar:

```rust
fn main() {
    println!("First line");
    println!("Second line");
}
```

```text
First line
Second line
```

## Metnin içine değer koymak

Metnin içindeki `{}` bir **yer tutucudur**: "buraya sonraki değeri koy" demektir.
Sayılarla işlem de yapabilirsin; `*` çarpma işaretidir:

```rust
fn main() {
    println!("{} times {} is {}", 6, 7, 6 * 7);
}
```

```text
6 times 7 is 42
```

Her `{}` sırayla bir değer alır. Yer tutucu sayısı ile değer sayısı tutmazsa
derleyici kabul etmez. Bu, Rust'ın başına gelecek hatalardan birini daha program
çalışmadan yakalamasının ilk örneği.

## Bir derleme hatası okumak

Bir harfi yanlış yazalım. `println` yerine `prinln` yazınca:

```rust
fn main() {
    prinln!("Hello");
}
```

```text
error: cannot find macro `prinln` in this scope
 --> main.rs:2:5
  |
2 |     prinln!("Hello");
  |     ^^^^^^
  |
  |
  = note: similarly named macro `println` defined here
help: a macro with a similar name exists
  |
2 |     println!("Hello");
  |         +
```

Mesajı parça parça oku:

- `error:` satırı sorunun ne olduğunu söyler: böyle bir makro yok.
- `-->` satırı yerini gösterir: `main.rs` dosyası, 2. satır, 5. sütun.
- `^^^^^^` işareti tam olarak hangi kelimeyi kastettiğini gösterir.
- `help:` varsa çoğu zaman çözümdür. Burada doğru adı öneriyor.

Bir hata gördüğünde panik yapma, **ilk hatadan başla** ve bu dört parçayı oku.
Sonraki hatalar çoğu zaman ilkinin devamıdır, o düzelince kendiliğinden kaybolur.

## Odyssey'de çalıştırmak

Alıştırma ekranında **Çalıştır** düğmesine basınca Odyssey kodunu `main.rs` adıyla
kaydeder, bilgisayarındaki `rustc` ile derler ve oluşan programı çalıştırır. Terminal
panelinde derleyicinin kendi mesajlarını görürsün; hata varsa altında kısa bir Türkçe
açıklama çıkar.

Derleyici bulunamazsa alıştırma bunu açıkça söyler. Bu senin kodunla ilgili değildir;
kurulum adımlarına dönmen yeterlidir.

## Özet

- Derleyici (`rustc`) kaynak kodu tek parça bir programa çevirir, kuralları önceden denetler.
- Rust belleği çöp toplayıcı olmadan, derleme anında kanıtlanan kurallarla yönetir.
- Program `fn main()` içinden başlar; `println!` ekrana yazar; `{}` değer yer tutucusudur.
- Hata mesajında önce `error`, sonra `-->`, sonra `help` satırını oku. İlk hatadan başla.
