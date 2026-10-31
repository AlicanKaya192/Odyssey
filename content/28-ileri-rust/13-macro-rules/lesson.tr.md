# Bildirimsel Makrolar

İlk günden beri `println!` ve `vec!` yazıyoruz. Sondaki `!` onların fonksiyon değil **makro** olduğunu söyler. Bu bölümde kendimizinkini yazıyoruz.

Fonksiyon çalışma zamanında çağrılır; argümanlarının sayısı ve türü sabittir. Makro ise **derleme zamanında kod üretir**: Derleyici makroyu yerinde açar, sonra çıkan kodu normal şekilde derler. `println!("{} {}", a, b)` ile `vec![1, 2, 3]` değişken sayıda argümanı bu sayede alır.

Rust'ta iki tür makro var. Bu bölümdeki **bildirimsel** (declarative) olanı `macro_rules!` ile yazılır; bir sonraki bölümdeki procedural olanı ayrı bir derleyici eklentisidir.

## İlk makro

```rust
macro_rules! say_hello {
    () => {
        println!("hello");
    };
}

fn main() {
    say_hello!();
    say_hello!();
}
```

```text
hello
hello
```

Yapısı `match`'e benzer: `(kalıp) => { şablon };`. Kalıp boş, şablon bir `println!`.

## Argüman yakalamak

Kalıpta `$ad:tür` bir parça yakalar. Buradaki tür Rust türü değil, **söz dizimi parçasının türüdür**. `expr` "bir ifade" demektir:

```rust
macro_rules! square {
    ($x:expr) => {
        $x * $x
    };
}

fn main() {
    println!("{}", square!(3));
    println!("{}", square!(1 + 2));
}
```

```text
9
9
```

İkinci satıra dikkat: C'nin metin makrolarında `1 + 2 * 1 + 2` olur ve 5 çıkardı. Rust'ta `$x` bir bütün olarak yerleşir, sonuç 9.

Ama başka bir tuzak var. Şablonda `$x` iki kez geçiyor, yani ifade **iki kez çalışıyor**:

```rust
macro_rules! square {
    ($x:expr) => {
        $x * $x
    };
}

fn next(counter: &mut u32) -> u32 {
    *counter += 1;
    *counter
}

fn main() {
    let mut counter = 0;
    println!("result {}", square!(next(&mut counter)));
    println!("calls {counter}");
}
```

```text
result 2
calls 2
```

Sonuç `1 * 2` oldu. Çare, değeri bir kez alıp saklamak. Dikkat: Şablon artık iki katlı süslü parantez içinde. Dıştaki makronun sınırı, içteki Rust'ın blok ifadesi:

```rust
macro_rules! square {
    ($x:expr) => {{
        let value = $x;
        value * value
    }};
}

fn next(counter: &mut u32) -> u32 {
    *counter += 1;
    *counter
}

fn main() {
    let mut counter = 0;
    println!("result {}", square!(next(&mut counter)));
    println!("calls {counter}");
}
```

```text
result 1
calls 1
```

## Hijyen

Makronun içindeki `temp`, dışarıdaki `temp` ile karışır mı?

```rust
macro_rules! add_ten {
    ($x:expr) => {{
        let temp = 10;
        $x + temp
    }};
}

fn main() {
    let temp = 1;
    println!("{}", add_ten!(temp));
    println!("{temp}");
}
```

```text
11
1
```

Karışmadı. Makronun kendi yazdığı adlar ayrı bir bağlamda yaşar; buna **hijyen** denir. `$x` olarak gelen `temp` ise çağıranın `temp`'idir. Sonuç `1 + 10`.

Aynı kural öbür yöne de işler. Makronun tanımladığı değişkeni dışarıdan göremezsin:

```rust
macro_rules! define {
    () => {
        let value = 1;
    };
}

fn main() {
    define!();
    println!("{value}");
}
```

```text
error[E0425]: cannot find value `value` in this scope
 --> main.rs:9:16
  |
9 |     println!("{value}");
  |                ^^^^^ not found in this scope
  |
help: an identifier with the same name is defined here, but is not accessible due to
macro hygiene
 --> main.rs:3:13
  |
3 |         let value = 1;
  |             ^^^^^
...
8 |     define!();
  |     --------- in this macro invocation
  = note: this error originates in the macro `define` (in Nightly builds, run with -Z
    macro-backtrace for more info)
```

Dışarıda görünsün istiyorsan adı çağıran vermelidir. `ident` bir ad yakalar:

```rust
macro_rules! define {
    ($name:ident, $value:expr) => {
        let $name = $value;
    };
}

fn main() {
    define!(answer, 42);
    println!("{answer}");
}
```

```text
42
```

## Tekrar

`vec!` gibi değişken sayıda argüman almanın yolu tekrar kalıbıdır:

```rust
macro_rules! my_vec {
    ( $( $x:expr ),* $(,)? ) => {{
        let mut out = Vec::new();
        $( out.push($x); )*
        out
    }};
}

fn main() {
    println!("{:?}", my_vec![1, 2, 3]);
    println!("{:?}", my_vec!["a", "b",]);
    let empty: Vec<u32> = my_vec![];
    println!("{:?}", empty);
}
```

```text
[1, 2, 3]
["a", "b"]
[]
```

`$( $x:expr ),*` şunu der: "İçindekinden sıfır ya da daha çok, aralarında virgül." Şablondaki `$( out.push($x); )*` da yakalanan her öğe için bir satır üretir. Bu bir döngü değildir: `my_vec![1, 2, 3]` derlemede üç ayrı `push` satırına dönüşür.

| İşaret | Anlamı |
|---|---|
| `*` | Sıfır ya da daha çok |
| `+` | Bir ya da daha çok |
| `?` | Sıfır ya da bir |

`$(,)?` böylece "sonda isteğe bağlı bir virgül" demektir.

## Birden çok kol

Kollar `match` gibi yukarıdan aşağı denenir, ilk uyan kazanır:

```rust
macro_rules! greet {
    () => {
        String::from("hello")
    };
    ($name:expr) => {
        format!("hello {}", $name)
    };
    ($name:expr, $times:literal) => {
        format!("hello {} x{}", $name, $times)
    };
}

fn main() {
    println!("{}", greet!());
    println!("{}", greet!("ada"));
    println!("{}", greet!("ada", 3));
}
```

```text
hello
hello ada
hello ada x3
```

Hiçbiri uymazsa derleme durur:

```rust
macro_rules! square {
    ($x:expr) => {
        $x * $x
    };
}

fn main() {
    println!("{}", square!(1, 2));
}
```

```text
error: no rules expected `,`
 --> main.rs:8:29
  |
1 | macro_rules! square {
  | ------------------- when calling this macro
...
8 |     println!("{}", square!(1, 2));
  |                             ^ no rules expected this token in macro call
  |
note: while trying to match meta-variable `$x:expr`
 --> main.rs:2:6
  |
2 |     ($x:expr) => {
  |      ^^^^^^^
```

## Özyineleme

Makro kendini çağırabilir. "İlkini al, kalanına kendini uygula" kalıbı sık kullanılır:

```rust
macro_rules! total {
    ($x:expr) => {
        $x
    };
    ($x:expr, $($rest:expr),+) => {
        $x + total!($($rest),+)
    };
}

fn main() {
    println!("{}", total!(5));
    println!("{}", total!(1, 2, 3, 4));
}
```

```text
5
10
```

`tt` (token tree) en esnek parçadır: Tek bir token ya da parantezli bir grubun tamamı. Token saymak onunla yapılır:

```rust
macro_rules! count {
    () => { 0usize };
    ($head:tt $($tail:tt)*) => { 1usize + count!($($tail)*) };
}

fn main() {
    println!("{}", count!());
    println!("{}", count!(a b c));
    println!("{}", count!(1 + (2 * 3)));
}
```

```text
0
3
3
```

`(2 * 3)` tek `tt` sayıldı, sonuç 3: `1`, `+` ve parantezli grup.

## Asıl kullanım: Tekrar eden kod

Makronun en değerli olduğu yer, birçok tür için neredeyse aynı `impl`'i yazmaktır. Standart kütüphane de sayı türlerinin çoğunu böyle üretir:

```rust
trait TypeName {
    fn type_name() -> &'static str;
}

macro_rules! impl_type_name {
    ($($t:ty),* $(,)?) => {
        $(
            impl TypeName for $t {
                fn type_name() -> &'static str {
                    stringify!($t)
                }
            }
        )*
    };
}

impl_type_name!(i32, f64, Vec<u8>);

fn main() {
    println!("{}", i32::type_name());
    println!("{}", <Vec<u8>>::type_name());
}
```

```text
i32
Vec<u8>
```

`ty` bir tür yakalar. `stringify!` ise token'ları çalıştırmadan metne çevirir. Kendi `assert`'imizi yazarken de işe yarar:

```rust
macro_rules! show {
    ($x:expr) => {
        println!("{} = {:?}", stringify!($x), $x)
    };
}

fn main() {
    let items = [1, 2, 3];
    show!(1 + 2);
    show!(items.len() * 2);
    println!("{}:{}", file!().ends_with(".rs"), line!() > 0);
}
```

```text
1 + 2 = 3
items.len() * 2 = 6
true:true
```

## Sıra ve görünürlük

Fonksiyonların aksine makrolar **metin sırasına** bağlıdır: Önce tanım, sonra kullanım.

```rust
fn main() {
    say_hello!();
}

macro_rules! say_hello {
    () => {
        println!("hello");
    };
}
```

```text
error: cannot find macro `say_hello` in this scope
 --> main.rs:2:5
  |
2 |     say_hello!();
  |     ^^^^^^^^^ consider moving the definition of `say_hello` before this call
  |
note: a macro with the same name exists, but it appears later
 --> main.rs:5:14
  |
5 | macro_rules! say_hello {
  |              ^^^^^^^^^

warning: unused macro definition: `say_hello`
 --> main.rs:5:14
  |
5 | macro_rules! say_hello {
  |              ^^^^^^^^^
  |
  = note: `#[warn(unused_macros)]` (part of `#[warn(unused)]`) on by default
```

Modülden dışarı açmak için `pub(crate) use` yazılır:

```rust
mod helpers {
    macro_rules! double {
        ($x:expr) => {
            $x * 2
        };
    }

    pub(crate) use double;
}

fn main() {
    println!("{}", helpers::double!(4));
}
```

```text
8
```

Başka crate'lere açmak için `#[macro_export]` gerekir. O zaman makro içindeki yollar `$crate::` ile başlamalıdır, yoksa makronun kullanıldığı crate'te aranır.

## Özet

- Makro derlemede kod üretir; `macro_rules!` kalıp ve şablondan oluşur.
- `$x:expr` bir ifade yakalar ve bir bütün olarak yerleşir, ama her geçtiği yerde yeniden çalışır.
- Hijyen: Makronun kendi adları çağıranınkilerle karışmaz.
- `$( ... ),*` tekrar; şablonda her öğe için kod üretir.
- Kollar sırayla denenir; makro kendini çağırabilir.
- En iyi kullanımı birçok tür için aynı `impl`'dir. Fonksiyon yetiyorsa fonksiyon yaz.
