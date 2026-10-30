# Değişkenler ve Değiştirilebilirlik

Program çalışırken bir değeri hatırlaması gerekir: bir fiyat, bir ad, bir toplam. Değere bir
ad verip sonra o adla kullanmaya **değişken** denir.

## let ile değişken

```rust
fn main() {
    let age = 36;
    let city = "Istanbul";
    println!("{} lives in {}", age, city);
    println!("{age} lives in {city}");
}
```

```text
36 lives in Istanbul
36 lives in Istanbul
```

`let` "bir ad tanımlıyorum" demektir. `=` işaretinin sağındaki değer soldaki ada bağlanır.
Metnin içinde değişkeni iki şekilde kullanabilirsin:

- `{}` ve sonra virgülle değer: `println!("{}", age)`
- Süslü parantezin içine doğrudan adı: `println!("{age}")`

İkinci yazım daha kısa ve okunaklıdır, ama yalnızca düz değişken adı alır. `{age + 1}` gibi bir işlem
yazılamaz; işlem için ilk yol kullanılır.

Değişken adları küçük harf ve alt çizgiyle yazılır: `total_price`. Rust buna `snake_case` der ve
farklı yazarsan uyarır.

## Değişkenler varsayılan olarak değişmez

İşte ilk Rust sürprizi. Çoğu dilde değişkenin değeri istendiği zaman değiştirilebilir. Rust'ta
değiştirilemez:

```rust
fn main() {
    let x = 5;
    println!("{x}");
    x = 6;
    println!("{x}");
}
```

```text
error[E0384]: cannot assign twice to immutable variable `x`
 --> main.rs:4:5
  |
2 |     let x = 5;
  |         - first assignment to `x`
3 |     println!("{x}");
4 |     x = 6;
  |     ^^^^^ cannot assign twice to immutable variable
  |
help: consider making this binding mutable
  |
2 |     let mut x = 5;
  |         +++
```

Derleyici hem sorunu söylüyor hem de `help:` satırında çözümü veriyor. Bu bir kısıtlama gibi görünür
ama büyük bir kazanç: Bir değişkenin `mut` işareti yoksa, **hiçbir yerde değişmediğinden emin olursun**.
Uzun bir fonksiyonu okurken bu seni çok düşünmekten kurtarır.

## mut ile değişebilir değişken

Değerin gerçekten değişmesi gerekiyorsa bunu açıkça söylersin:

```rust
fn main() {
    let mut score = 10;
    println!("start: {score}");
    score += 5;
    println!("after: {score}");
}
```

```text
start: 10
after: 15
```

`mut` "mutable", yani değiştirilebilir kelimesinden gelir. `+=` soldaki değere ekleme yapar:
`score += 5` ile `score = score + 5` aynı işi yapar.

Değişmeyen bir değişkene gereksiz yere `mut` yazarsan derleyici uyarır. Kural basit: **önce `mut`
olmadan yaz, derleyici isterse ekle.**

## Değişkeni gölgelemek

Aynı adla yeniden `let` yazabilirsin. Buna **gölgeleme** (shadowing) denir: yeni değişken eskisinin
üstünü örter.

```rust
fn main() {
    let price = 100;
    let price = price + 20;
    let price = price * 2;
    println!("{price}");
}
```

```text
240
```

İlk bakışta `mut` ile aynı görünür, ama iki önemli fark var:

<figure class="fig"><div class="versus"><div><h4>mut</h4>Aynı değişkenin değeri değişir. Tür aynı kalmalıdır.</div><div><h4>Gölgeleme</h4>Yepyeni bir değişken açılır. Eski değer durur ama artık o adla ulaşılamaz. Tür de değişebilir.</div></div><figcaption>Bir değeri dönüştürüp aynı adla devam edeceksen gölgeleme; aynı şeyi güncelleyeceksen <code>mut</code>.</figcaption></figure>

Türün değişebilmesi pratikte çok işe yarar. Bir metni uzunluğuna çevirmek için iki ayrı ad uydurman gerekmez:

```rust
fn main() {
    let text = "hello";
    let text = text.len();
    println!("{text}");
}
```

```text
5
```

`.len()` metnin uzunluğunu verir. Aynı şeyi `mut` ile yapmayı denersen hata alırsın, çünkü türü
değiştirmeye çalışıyorsun:

```rust
fn main() {
    let mut text = "hello";
    text = text.len();
    println!("{text}");
}
```

```text
error[E0308]: mismatched types
 --> main.rs:3:12
  |
2 |     let mut text = "hello";
  |                    ------- expected due to this value
3 |     text = text.len();
  |            ^^^^^^^^^^ expected `&str`, found `usize`
```

`E0308` "türler uyuşmuyor" demektir ve Rust'ta en sık göreceğin hatalardan biridir: `expected` beklenen
türü, `found` senin verdiğini gösterir.

## Kapsam: değişken nerede yaşar?

Süslü parantezler bir **blok** açar. Bloğun içinde tanımlanan değişken blok bitince yok olur:

```rust
fn main() {
    let x = 1;
    {
        let x = 2;
        println!("inner: {x}");
    }
    println!("outer: {x}");
}
```

```text
inner: 2
outer: 1
```

Bloğun içindeki `x`, dıştakini yalnızca blok boyunca gölgeler. Blok bitince dıştaki yeniden görünür.
Bu kapsam fikri ileride sahiplik konusunun temeli olacak.

## Sabitler: const

Hiç değişmeyecek, program boyunca geçerli bir değer için `const` kullanılır:

```rust
const MAX_POINTS: u32 = 100_000;

fn main() {
    println!("{MAX_POINTS}");
}
```

```text
100000
```

`let`'ten farkları:

| | `let` | `const` |
|---|---|---|
| Tür yazmak | İsteğe bağlı | **Zorunlu** |
| Değer ne zaman bilinir | Çalışırken olabilir | Derlerken bilinmeli |
| `mut` olabilir mi | Evet | Hayır |
| Nerede yazılır | Fonksiyon içinde | Her yerde, dosyanın başında da |
| Ad yazımı | `snake_case` | `BUYUK_HARF` |

Buradaki `u32` bir **tür**: işaretsiz (eksi olamayan) 32 bitlik tam sayı. Türleri sonraki bölümde
göreceğiz. Sayıdaki `_` yalnızca okumayı kolaylaştırır: `100_000` ile `100000` aynıdır.

## Kullanılmayan değişken

Tanımlayıp hiç kullanmadığın değişken için derleyici uyarır. Adı bilerek kullanılmıyorsa başına `_`
koyarsın, uyarı kaybolur: `let _unused = 5;`

## Özet

- `let` ad tanımlar. Değişken varsayılan olarak **değişmez**; değişecekse `let mut`.
- `{age}` ile metne doğrudan değişken adı yazılabilir.
- Aynı adla yeniden `let` yazmak gölgelemedir; yeni değişkendir, türü de değişebilir.
- Blok bitince içindeki değişkenler yok olur.
- `const` derleme anında bilinen, türü yazılı, değişmez değerdir.
