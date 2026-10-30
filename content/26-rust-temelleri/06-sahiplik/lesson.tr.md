# Sahiplik

Rust'ı başka dillerden ayıran şey bu bölümde. Burayı anladığında dilin geri kalanı yerine oturur. Yavaş oku,
örnekleri çalıştır. İlk okuyuşta her şeyin oturmaması normal.

## Önce neden: Bellek ne zaman geri verilecek?

Bir program çalışırken iki bellek alanı kullanır:

- **Yığın (stack):** Hızlı ve düzenlidir. Fonksiyon çağrılınca değişkenleri buraya konur, fonksiyon bitince hepsi
  birden kalkar. Yığına konan her şeyin **boyutu derlemede bilinmelidir**. `i32`, `bool`, sabit dizi buraya gider.
- **Öbek (heap):** Boyutu çalışırken belli olan ya da değişen veriler içindir: Kullanıcının yazdığı bir metin gibi.
  Program bellekten yer ister, yerin **adresini** alır. Bu adresi tutan değere **işaretçi** (pointer) denir. Öbekteki
  yer kendiliğinden geri verilmez.

Bütün zorluk o öbek belleğinde. Geri vermeyi unutursan bellek biter. Verdikten sonra kullanırsan ya da iki kez verirsen
program bozulur. Rust'ın cevabı üç kuraldır.

## Üç kural

<figure class="fig"><div class="anat"><div class="anat-row"><span><b>1</b></span><span>Her değerin bir <b>sahibi</b> vardır: o değeri tutan değişken.</span></div><div class="anat-row"><span><b>2</b></span><span>Bir anda yalnızca <b>tek</b> sahip olabilir.</span></div><div class="anat-row"><span><b>3</b></span><span>Sahip kapsamdan çıkınca değer <b>silinir</b>, belleği geri verilir.</span></div></div><figcaption>Sahipliğin bütün kuralları bu kadar. Geri kalan her şey bunların sonucu.</figcaption></figure>

## İlk öbek türümüz: String

Şimdiye kadarki `"Ada"` metinleri programın içine gömülüydü ve değişmezdi. `String` ise öbekte durur, büyüyebilir:

```rust
fn main() {
    let mut greeting = String::from("Hello");
    greeting.push_str(", world");
    println!("{greeting}");
}
```

```text
Hello, world
```

`String::from` öbekten yer alır ve metni oraya kopyalar. `push_str` sonuna ekler; bunun için değişken `mut` olmalı.

Bir `String` yığında üç parça tutar: öbekteki yerin adresi, şu anki uzunluk ve ayrılan kapasite.

<figure class="fig"><svg viewBox="0 0 640 110" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">greeting</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 12, cap 12</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">Hello, world</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Yığındaki üç parça öbekteki metni gösterir. (Kapasite ölçüldü: <code>String::capacity</code>.)</figcaption></figure>

## Kural 3: Kapsam bitince silinir

```rust
fn main() {
    {
        let text = String::from("short life");
        println!("{text}");
    }
    println!("the block ended, text is gone");
}
```

```text
short life
the block ended, text is gone
```

`text` bloğun sonunda kapsamdan çıktı. Rust o noktada öbekteki belleği kendiliğinden geri verdi. Bunu çalışan bir yardımcı
değil, **derleyici** ayarlıyor: Bloğun kapanışına temizlik kodunu kendisi ekliyor. Elle `free` yazmak yok, çöp toplayıcı da yok.

Bu silme işini kendimiz de gözleyebiliriz. Sonraki örneği şimdilik yalnızca oku; `Noisy` kendi türümüz, `impl Drop` ise
"silinirken şunu yap" demek. Ayrıntısını ileride göreceğiz:

```rust
struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("dropping {}", self.0);
    }
}

fn main() {
    let _a = Noisy("a");
    let _b = Noisy("b");
    println!("end of main");
}
```

```text
end of main
dropping b
dropping a
```

Çıktıdaki sıraya bak: `b` önce, `a` sonra silindi. Değişkenler tanımlandıkları sıranın **tersiyle** silinir.

## Kural 2: Taşıma (move)

Şimdi en önemli örnek. Sayılarla başlayalım, hiçbir şaşırtıcı yanı yok:

```rust
fn main() {
    let x = 5;
    let y = x;
    println!("{x} {y}");
}
```

```text
5 5
```

Aynısını `String` ile yapalım:

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{s1} {s2}");
}
```

```text
error[E0382]: borrow of moved value: `s1`
 --> main.rs:4:16
  |
2 |     let s1 = String::from("hello");
  |         -- move occurs because `s1` has type `String`, which does not implement the
  `Copy` trait
3 |     let s2 = s1;
  |              -- value moved here
4 |     println!("{s1} {s2}");
  |                ^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let s2 = s1.clone();
  |                ++++++++
```

Hata kodu `E0382`, Rust öğrenirken en çok göreceğin hata. Mesajı iyi oku:

- `move occurs because s1 has type String` : Değer taşındı, çünkü `String` kopyalanmıyor.
- `value moved here` : Taşındığı satır.
- `value borrowed here after move` : Sonra kullanmaya çalıştığın satır.
- `help: consider cloning` : Önerilen çözüm.

Neden oldu? `let s2 = s1;` öbekteki metni kopyalamaz, yalnızca yığındaki üç parçayı kopyalar. O anda iki değişken aynı öbek
yerini gösterirdi. İkisi de kapsamdan çıkınca aynı bellek **iki kez** geri verilirdi. Kural 2 tam da bunu engeller: `s2` yeni
sahip olur, `s1` geçersiz sayılır.

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g opacity="0.45"><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">s1</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 5, cap 5</text></g><line class="curve2" x1="26" y1="66" x2="244" y2="66"/><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">s2</text><text class="dim" x="110" y="129" font-size="12.5">ptr, len 5, cap 5</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">hello</text></g><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption><code>let s2 = s1;</code> sonrası: Öbekte hâlâ tek metin var, sahibi <code>s2</code>. <code>s1</code> artık kullanılamaz.</figcaption></figure>

Buna **taşıma** (move) denir. Yalnızca yığındaki küçük parça kopyalandığı için çok ucuzdur: Metin bir gigabayt da olsa aynı.

## Gerçekten kopya gerekirse: clone

Öbekteki veriyi de kopyalamak istersen bunu açıkça söylersin:

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("{s1} {s2}");
}
```

```text
hello hello
```

<figure class="fig"><svg viewBox="0 0 640 168" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">s1</text><text class="dim" x="110" y="71" font-size="12.5">ptr, len 5, cap 5</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">s2</text><text class="dim" x="110" y="129" font-size="12.5">ptr, len 5, cap 5</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">hello</text></g><g><rect class="box" x="390" y="102" width="220" height="44" rx="8"/><text class="ink" x="404" y="129" font-size="14">hello</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 124 382 124"/><polygon class="dot" points="390,124 380,119 380,129"/></svg><figcaption><code>.clone()</code> sonrası: Öbekte iki ayrı metin, iki ayrı sahip.</figcaption></figure>

`.clone()` görüyorsan pahalı olabilecek bir iş yapılıyor demektir. Rust bunu saklamaz; kopya hiçbir zaman gizlice oluşmaz.

## Copy türleri: Neden sayılar taşınmıyor?

`i32` öbek kullanmaz, bütün değeri yığındadır. Kopyalamak taşımak kadar ucuzdur ve iki kez silinecek bir şey yoktur. Bu yüzden
böyle türler `Copy` özelliğini taşır: Atama kopya üretir, eskisi geçerli kalır.

| `Copy` olanlar | `Copy` olmayanlar |
|---|---|
| `i32`, `u8`, `f64`, bütün sayılar | `String` |
| `bool`, `char` | `Vec` (ileride) |
| Öğeleri `Copy` olan demet ve diziler | İçinde `String` olan demet |
| `&str` gibi paylaşılan referanslar | Öbek kullanan her tür |

## Fonksiyonlar da sahipliği taşır

Fonksiyona değer vermek, atamayla aynı kuralı izler:

```rust
fn consume(text: String) {
    println!("{text}");
}

fn main() {
    let name = String::from("Ada");
    consume(name);
    println!("{name}");
}
```

```text
error[E0382]: borrow of moved value: `name`
 --> main.rs:8:16
  |
6 |     let name = String::from("Ada");
  |         ---- move occurs because `name` has type `String`, which does not implement
  the `Copy` trait
7 |     consume(name);
  |             ---- value moved here
8 |     println!("{name}");
  |                ^^^^ value borrowed here after move
  |
note: consider changing this parameter type in function `consume` to borrow instead if
owning the value isn't necessary
 --> main.rs:1:18
  |
1 | fn consume(text: String) {
  |    -------       ^^^^^^ this parameter takes ownership of the value
  |    |
  |    in this function
help: consider cloning the value if the performance cost is acceptable
  |
7 |     consume(name.clone());
  |                 ++++++++
```

`consume` çağrısı metnin sahipliğini aldı. Fonksiyon bitince `text` parametresi kapsamdan çıktı ve metin silindi. `name` artık
geçersiz. Bu yüzden derleyici reddediyor; aksi hâlde silinmiş belleği okurduk.

Sahiplik dönüş değeriyle geri de verilebilir:

```rust
fn shout(text: String) -> String {
    let mut loud = text;
    loud.push_str("!");
    loud
}

fn main() {
    let name = String::from("Ada");
    let name = shout(name);
    println!("{name}");
}
```

```text
Ada!
```

Bu çalışır ama her fonksiyona verip geri almak yorucu. Üstelik fonksiyonun başka bir şey de döndürmesi gerekirse demet yazman gerekir:

```rust
fn measure(text: String) -> (String, usize) {
    let length = text.len();
    (text, length)
}

fn main() {
    let name = String::from("Ada");
    let (name, length) = measure(name);
    println!("{name} {length}");
}
```

```text
Ada 3
```

Çözüm **ödünç almak**: Değeri vermeden kullanma izni. Sonraki bölümün konusu tam olarak bu.

## Bütün bunlar ne kazandırıyor?

Bu kurallar derlemede denetlendiği için güvenli Rust'ta şunlar **olamaz**:

- Silinmiş belleği okumak (use after free)
- Aynı belleği iki kez geri vermek (double free)
- Geri vermeyi unutarak sürekli bellek kaçırmak (çoğu durumda)

C ve C++ programlarındaki güvenlik açıklarının büyük bölümü bu sınıftan geliyor. Rust'ta bu hataların çoğu program çalışmadan yakalanır.

## Özet

- Her değerin tek sahibi var; sahip kapsamdan çıkınca değer silinir.
- `let b = a;` öbek kullanan türlerde **taşır**: `a` geçersiz olur, hata `E0382`.
- Gerçek kopya için `.clone()`, açıkça ve bedeli görülerek.
- `Copy` türleri (sayılar, `bool`, `char`) atamada kopyalanır, taşınmaz.
- Fonksiyona vermek de taşır; dönüş değeriyle geri alınabilir, ama asıl çözüm ödünç almaktır.
