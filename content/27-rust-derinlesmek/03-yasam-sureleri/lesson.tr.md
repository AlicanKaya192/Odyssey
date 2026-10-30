# Yaşam Süreleri

Ödünç alma kuralının ikinci yarısını hatırla: **Referans sahibinden uzun yaşayamaz.** Derleyici bunu çoğu zaman kendi başına denetler. Bazen ise kodun tek başına söylemediği bir bilgi gerekir: "Dönen referans hangi girdiye bağlı?" Bu bilgiyi **yaşam süresi** (lifetime) işaretiyle yazarsın.

En önemli cümle baştan: **Yaşam süresi işareti hiçbir değeri daha uzun yaşatmaz.** Yalnızca referanslar arasındaki ilişkiyi derleyiciye anlatır.

## Sorun: Sallanan referans

```rust
fn main() {
    let r;
    {
        let x = 5;
        r = &x;
    }
    println!("{r}");
}
```

```text
error[E0597]: `x` does not live long enough
 --> main.rs:5:13
  |
4 |         let x = 5;
  |             - binding `x` declared here
5 |         r = &x;
  |             ^^ borrowed value does not live long enough
6 |     }
  |     - `x` dropped here while still borrowed
7 |     println!("{r}");
  |                - borrow later used here
```

`x` iç blokta silindi, `r` hâlâ onu gösteriyor. Rust bunu derleme zamanında yakalar. Bu denetimi yapan parçaya **ödünç denetleyicisi** (borrow checker) denir.

## Derleyicinin soramadığı soru

İki metinden uzun olanı döndüren bir fonksiyon:

```rust
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    println!("{}", longest("a", "bb"));
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:1:33
  |
1 | fn longest(x: &str, y: &str) -> &str {
  |               ----     ----     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does
    not say whether it is borrowed from `x` or `y`
help: consider introducing a named lifetime parameter
  |
1 | fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
  |           ++++     ++          ++          ++
```

Derleyici fonksiyonun gövdesine bakarak karar vermez, imzasına bakar. İmzada iki referans girip bir referans çıkıyor. Dönen hangisine bağlı? `x`'e mi, `y`'ye mi? Çağıran kodun güvende olup olmadığını bilmek için bunu öğrenmesi gerekiyor.

## İşareti yazmak

Yaşam süresi parametresi `'a` diye yazılır ve generic gibi köşeli parantezde tanıtılır:

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let a = String::from("long text");
    let b = "short";
    println!("{}", longest(&a, b));
}
```

```text
long text
```

Okunuşu: "Bir `'a` süresi var; `x` ve `y` en az o kadar yaşıyor; dönen referans da en az o kadar geçerli." Pratikte `'a`, `x` ile `y`'nin **kısa olanına** eşit olur.

Bu yüzden şu kod derlenmez:

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let a = String::from("long text");
    let result;
    {
        let b = String::from("short");
        result = longest(&a, &b);
    }
    println!("{result}");
}
```

```text
error[E0597]: `b` does not live long enough
  --> main.rs:10:30
   |
 9 |         let b = String::from("short");
   |             - binding `b` declared here
10 |         result = longest(&a, &b);
   |                              ^^ borrowed value does not live long enough
11 |     }
   |     - `b` dropped here while still borrowed
12 |     println!("{result}");
   |                ------ borrow later used here
```

`b`, `result`'tan önce silindi. Fonksiyonun gövdesi `a`'yı seçecek olsa bile derleyici yalnızca imzaya bakıyor ve imza "dönen, kısa olana bağlı" diyor.

## Yalnızca gerektiği yere

`y` dönüşü hiç etkilemiyorsa ona işaret koyma:

```rust
fn keep_first<'a>(x: &'a str, y: &str) -> &'a str {
    println!("ignoring {y}");
    x
}

fn main() {
    let a = String::from("kept");
    let result;
    {
        let b = String::from("gone");
        result = keep_first(&a, &b);
    }
    println!("{result}");
}
```

```text
ignoring gone
kept
```

Artık dönen yalnızca `x`'e bağlı, `y` istediği kadar kısa yaşayabilir.

## Yerel değişkene referans döndürülemez

İşaret büyü yapmaz. Fonksiyonun kendi yarattığı değer fonksiyon bitince silinir:

```rust
fn make<'a>() -> &'a str {
    let text = String::from("hi");
    &text
}

fn main() {
    println!("{}", make());
}
```

```text
error[E0515]: cannot return reference to local variable `text`
 --> main.rs:3:5
  |
3 |     &text
  |     ^^^^^ returns a reference to data owned by the current function
```

Çözüm işaret değil, sahipli değer döndürmektir: `String`.

## Neden çoğu fonksiyonda yazmıyoruz?

`fn first_word(s: &str) -> &str` hiç işaret içermiyor ama derleniyor. Derleyici yaygın durumlarda işareti kendisi ekler. Bunun adı **yaşam süresi çıkarımı** (elision). Üç kural var:

| Kural | Anlamı |
|---|---|
| 1 | Her referans parametresi kendi süresini alır |
| 2 | Tek girdi süresi varsa çıktılara o verilir |
| 3 | `&self` varsa çıktılara onun süresi verilir |

Üç kural sonunda çıktının süresi belirlenemezse derleyici sana sorar: `E0106`. `longest` tam olarak buraya düşüyordu.

## Referans tutan struct

Struct referans tutuyorsa onun da işarete ihtiyacı vardır: "Bu struct, tuttuğu metinden uzun yaşayamaz."

```rust
struct Excerpt<'a> {
    text: &'a str,
}

impl<'a> Excerpt<'a> {
    fn text(&self) -> &str {
        self.text
    }

    fn first_word(&self) -> &'a str {
        self.text.split_whitespace().next().unwrap_or("")
    }
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago");
    let first = novel.split('.').next().unwrap();
    let part = Excerpt { text: first };
    println!("{}", part.text());
    println!("{}", part.first_word());
}
```

```text
Call me Ishmael
Call
```

`impl<'a> Excerpt<'a>` generic'teki gibi tanıtır. `text(&self) -> &str` için üçüncü kural yeter. Yazılmazsa:

```rust
struct Excerpt {
    text: &str,
}

fn main() {
    let e = Excerpt { text: "hi" };
    println!("{}", e.text);
}
```

```text
error[E0106]: missing lifetime specifier
 --> main.rs:2:11
  |
2 |     text: &str,
  |           ^ expected named lifetime parameter
  |
help: consider introducing a named lifetime parameter
  |
1 ~ struct Excerpt<'a> {
2 ~     text: &'a str,
  |
```

Metni taşıyan yapıda çoğu zaman `String` tutmak daha basittir. Referans tutan struct, kopyadan kaçınmak gerçekten gerektiğinde tercih edilir.

## 'static

Özel bir süre: Programın sonuna kadar yaşar. Metin sabitleri böyledir, çünkü programın içine gömülüdür:

```rust
fn name() -> &'static str {
    "Odyssey"
}

fn main() {
    let n: &'static str = name();
    println!("{n}");
}
```

```text
Odyssey
```

Derleyici bazen `'static` önerir. Çoğu zaman doğru çözüm bu değildir: Yanlış süreyi gizler. Önce sahipliği düşün.

## Özet

- Referans sahibinden uzun yaşayamaz; denetimi ödünç denetleyicisi yapar.
- İşaret değeri uzatmaz, referanslar arasındaki ilişkiyi yazar.
- `fn f<'a>(x: &'a str, y: &'a str) -> &'a str`: Dönen, kısa olana kadar geçerli.
- Derleyici yalnızca imzaya bakar. Yerel değer referansla döndürülemez, sahipli döndür.
- Üç çıkarım kuralı çoğu işareti gereksiz kılar.
- Referans tutan struct `struct S<'a>` ister. `'static` programın sonuna kadardır.
