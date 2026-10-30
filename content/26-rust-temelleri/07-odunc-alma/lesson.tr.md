# Referanslar ve Ödünç Alma

Önceki bölümün sonunda bir sıkıntıyla kaldık: Metnin uzunluğunu ölçmek için onu fonksiyona verip demetle geri almak zorunda kaldık.
Oysa fonksiyon metne sahip olmak istemiyor, yalnızca bakmak istiyor.

## Referans: Sahipliği vermeden kullanmak

**Referans** (reference) bir değeri gösterir ama ona sahip olmaz. `&` ile alınır. Referans almaya **ödünç alma** (borrowing) denir:

```rust
fn length_of(text: &String) -> usize {
    text.len()
}

fn main() {
    let name = String::from("Ada");
    let length = length_of(&name);
    println!("{name} has {length} letters");
}
```

```text
Ada has 3 letters
```

İki yerde `&` var: Çağrıda `&name` "ödünç veriyorum", imzada `&String` "ödünç alıyorum". `length_of` bittiğinde `text` kapsamdan çıkar, ama sahip
olmadığı için metin silinmez. `name` geçerliliğini korur.

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">name</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 3, cap 3</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">text</text><text class="dim" x="110" y="129" font-size="12.5">&amp;String</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">Ada</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve2" d="M20 124 C-4 124 -4 66 14 66"/><polygon class="dot2" points="20,66 10,61 10,71"/></svg><figcaption><code>text</code> metni değil, <code>name</code> değişkenini gösterir. Sahip hâlâ <code>name</code>.</figcaption></figure>

Gerçek hayattaki gibi: Kitabı ödünç alan onu okuyabilir, ama kitap sahibinindir ve ödünç alan yakamaz.

Referansın gösterdiği değere `*` ile ulaşılır (**dereference**). Çoğu zaman yazmana gerek kalmaz, çünkü metot çağrısında ve `println!`'de Rust bunu
kendisi yapar:

```rust
fn main() {
    let x = 5;
    let r = &x;
    println!("{}", *r + 1);
    println!("{r}");
}
```

```text
6
5
```

## Değiştirmek için: &mut

Normal referans yalnızca okur. Ödünç alınan değeri değiştirmeye çalışınca:

```rust
fn add_mark(text: &String) {
    text.push_str("!");
}

fn main() {
    let word = String::from("hi");
    add_mark(&word);
}
```

```text
error[E0596]: cannot borrow `*text` as mutable, as it is behind a `&` reference
 --> main.rs:2:5
  |
2 |     text.push_str("!");
  |     ^^^^ `text` is a `&` reference, so it cannot be borrowed as mutable
  |
help: consider changing this to be a mutable reference
  |
1 | fn add_mark(text: &mut String) {
  |                    +++
```

Değiştirmek için **değişebilir referans** gerekir. Üç yere `mut` yazılır: değişken, çağrı, imza.

```rust
fn add_mark(text: &mut String) {
    text.push_str("!");
}

fn main() {
    let mut word = String::from("hi");
    add_mark(&mut word);
    println!("{word}");
}
```

```text
hi!
```

## İki büyük kural

Bu bölümün kalbi burası. Bir değer için aynı anda ya da:

<figure class="fig"><div class="versus"><div><h4>İstediğin kadar okuyan</h4>Çok sayıda <code>&amp;T</code> aynı anda olabilir. Hiçbiri değiştiremez.</div><div><h4>Tek bir yazan</h4>Yalnızca bir <code>&amp;mut T</code> olabilir ve o varken başka hiçbir referans olamaz.</div></div><figcaption>İkinci kural: Referans, gösterdiği değerden uzun yaşayamaz.</figcaption></figure>

Bu, veri yarışlarını derleme anında önleyen kuraldır. Bir **veri yarışı** şöyle olur: İki kod parçası aynı veriye aynı anda erişir, en az biri yazar ve
aralarında düzen yoktur. Sonuç tahmin edilemez. Rust'ta böyle kod derlenmez.

İki yazan:

```rust
fn main() {
    let mut s = String::from("hi");
    let a = &mut s;
    let b = &mut s;
    a.push_str("1");
    b.push_str("2");
}
```

```text
error[E0499]: cannot borrow `s` as mutable more than once at a time
 --> main.rs:4:13
  |
3 |     let a = &mut s;
  |             ------ first mutable borrow occurs here
4 |     let b = &mut s;
  |             ^^^^^^ second mutable borrow occurs here
5 |     a.push_str("1");
  |     - first borrow later used here
```

Okuyan varken yazan:

```rust
fn main() {
    let mut s = String::from("hi");
    let reader = &s;
    let writer = &mut s;
    writer.push_str("!");
    println!("{reader}");
}
```

```text
error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
 --> main.rs:4:18
  |
3 |     let reader = &s;
  |                  -- immutable borrow occurs here
4 |     let writer = &mut s;
  |                  ^^^^^^ mutable borrow occurs here
5 |     writer.push_str("!");
6 |     println!("{reader}");
  |                ------ immutable borrow later used here
```

## Neden önemli: Listeyi değiştirirken okumak

"Tek iş parçacığında ne zararı var?" diye düşünebilirsin. İşte zararı. `Vec` büyüyen bir listedir (on ikinci bölümde görüyoruz). Listeye eleman
eklemek belleği taşıyabilir, o zaman ilk elemana alınan referans silinmiş belleği gösterir:

```rust
fn main() {
    let mut list = vec![1, 2, 3];
    let first = &list[0];
    list.push(4);
    println!("{first}");
}
```

```text
error[E0502]: cannot borrow `list` as mutable because it is also borrowed as immutable
 --> main.rs:4:5
  |
3 |     let first = &list[0];
  |                  ---- immutable borrow occurs here
4 |     list.push(4);
  |     ^^^^^^^^^^^^ mutable borrow occurs here
5 |     println!("{first}");
  |                ----- immutable borrow later used here
```

C++'ta aynı kod derlenir ve bazen çalışır, bazen çöker. Rust'ta derlenmez.

## Referans nerede biter?

Referans son kullanıldığı yerde biter, bloğun sonunda değil. Bu kurala **NLL** (non-lexical lifetimes) denir ve kodu çok rahatlatır:

```rust
fn main() {
    let mut s = String::from("hello");
    let r1 = &s;
    let r2 = &s;
    println!("{r1} {r2}");
    let r3 = &mut s;
    r3.push_str(" world");
    println!("{r3}");
}
```

```text
hello hello
hello world
```

`r1` ve `r2` son kez `println!`'de kullanıldı, orada bittiler. Bu yüzden sonraki `&mut` kabul ediliyor. Bu sıralamayı değiştirip `E0502` almayı deneyebilirsin.

Pratikte `E0502` ve `E0499` hatalarının çoğu böyle çözülür: Okuma işini önce bitir, sonra yaz.

## Sarkan referans olamaz

C'de bir fonksiyon, içindeki yerel değişkenin adresini döndürebilir ve bu büyük bir hata kaynağıdır. Rust buna izin vermez:

```rust
fn make_text() -> &String {
    let text = String::from("gone soon");
    &text
}

fn main() {
    println!("{}", make_text());
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:1:19
  |
1 | fn make_text() -> &String {
  |                   ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but there is no value
    for it to be borrowed from
help: consider using the `'static` lifetime, but this is uncommon unless you're
returning a borrowed value from a `const` or a `static`
  |
1 | fn make_text() -> &'static String {
  |                    +++++++
help: instead, you are more likely to want to return an owned value
  |
1 - fn make_text() -> &String {
1 + fn make_text() -> String {
  |
```

Mesaj `missing lifetime specifier` diyor; yaşam sürelerini ikinci modülde göreceğiz. Şimdilik sonuç şu: `text` fonksiyon bitince silinecek, onu gösteren
referans boşluğu gösterirdi. Çözüm referans değil, değerin kendisini döndürmek:

```rust
fn make_text() -> String {
    let text = String::from("made here");
    text
}

fn main() {
    println!("{}", make_text());
}
```

```text
made here
```

## for döngüsü ve referans

Artık önceki bölümdeki `.iter()`'i anlayabiliriz. Bir diziyi `for` ile gezmek, öğeleri `Copy` değilse onları taşır. Ödünç gezmek için `&` yazılır:

```rust
fn main() {
    let names = [String::from("Ada"), String::from("Linus")];
    for name in &names {
        println!("{}", name.len());
    }
    println!("{}", names[0]);
}
```

```text
3
5
Ada
```

`&names` diziyi ödünç verir, `name` her turda bir `&String` olur. Değiştirmek için `&mut`:

```rust
fn main() {
    let mut values = [1, 2, 3];
    for n in &mut values {
        *n *= 10;
    }
    println!("{:?}", values);
}
```

```text
[10, 20, 30]
```

`*n` referansın gösterdiği değere ulaşır: `n` bir adres, `*n` oradaki sayı.

## Hangisini almalı? Fonksiyon imzası rehberi

| Fonksiyonun yapacağı | Parametre | Çağrı |
|---|---|---|
| Yalnızca okuyacak | `x: &T` | `f(&value)` |
| Değiştirecek | `x: &mut T` | `f(&mut value)` |
| Saklayacak ya da tüketecek | `x: T` | `f(value)` |

Kural: **En az gücü iste.** Okumak yetiyorsa `&T`.

## Özet

- `&` ödünç alır, sahipliği almaz. Referans bitince değer silinmez.
- `&mut` değiştirme izni verir; değişken de `mut` olmalıdır.
- Bir anda ya çok sayıda `&T` ya da tek bir `&mut T`. Hatalar `E0499`, `E0502`.
- Referans son kullanıldığı yerde biter. Sıralamayı değiştirmek çoğu hatayı çözer.
- Sarkan referans derlenmez; yerel değerin kendisini döndür.
- Fonksiyon imzasında en az gücü iste.
