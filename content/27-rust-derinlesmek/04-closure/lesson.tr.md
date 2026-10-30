# Closure'lar

`|x| x + 1` yazımını birkaç yerde gördün. Bu bir **closure**: Adsız, satır içinde yazılan fonksiyon. Sıradan fonksiyondan iki farkı var: Kısa yazılır ve **çevresindeki değişkenleri kullanabilir.**

## Yazım

```rust
fn main() {
    let double = |x| x * 2;
    let add = |a: i32, b: i32| -> i32 { a + b };
    let hello = || println!("hello");
    println!("{}", double(4));
    println!("{}", add(2, 3));
    hello();
}
```

```text
8
5
hello
```

| Parça | Anlamı |
|---|---|
| <code>&#124;a, b&#124;</code> | Parametreler, dikey çizgi arasında |
| Sonrası | Gövde; tek ifadeyse süslü parantez gerekmez |
| Türler | Çoğu zaman çıkarılır, istersen yazılır |

Bir kez çıkarılan tür sabitlenir. Aynı closure iki farklı türle çağrılamaz:

```rust
fn main() {
    let same = |x| x;
    println!("{}", same(1));
    println!("{}", same("text"));
}
```

```text
error[E0308]: mismatched types
 --> main.rs:4:25
  |
4 |     println!("{}", same("text"));
  |                    ---- ^^^^^^ expected integer, found `&str`
  |                    |
  |                    arguments to this function are incorrect
  |
note: expected because the closure was earlier called with an argument of type
`{integer}`
 --> main.rs:3:25
  |
3 |     println!("{}", same(1));
  |                    ---- ^ expected because this argument is of type `{integer}`
  |                    |
  |                    in this closure call
note: closure parameter defined here
 --> main.rs:2:17
  |
2 |     let same = |x| x;
  |                 ^
```

## Çevreyi yakalamak

Sıradan fonksiyon dışarıdaki yerel değişkeni göremez. Closure görür:

```rust
fn main() {
    let offset = 10;
    let add = |x| x + offset;
    println!("{}", add(1));
    println!("{offset}");
}
```

```text
11
10
```

Buna **yakalama** (capture) denir. `add` değişkeni `offset`'i yakaladı.

## Üç yakalama biçimi

Derleyici gövdeye bakıp gereken en az yetkiyi seçer:

```rust
fn main() {
    let name = String::from("Ada");
    let read = || println!("{name}");
    read();
    println!("{name}");

    let mut count = 0;
    let mut bump = || count += 1;
    bump();
    bump();
    println!("{count}");

    let text = String::from("gone");
    let consume = || drop(text);
    consume();
}
```

```text
Ada
Ada
2
```

| Gövdenin yaptığı | Yakalama | Sonra |
|---|---|---|
| Yalnızca okuyor | `&` ödünç | Dışarıda da okunur |
| Değiştiriyor | `&mut` ödünç | Closure `mut` olmalı |
| Sahipleniyor | Taşıma | Dışarıda kullanılamaz |

Ödünç alma kuralları burada da geçerli. Closure değişkeni `&mut` ile tutarken dışarıdan okuyamazsın:

```rust
fn main() {
    let mut count = 0;
    let mut bump = || count += 1;
    println!("{count}");
    bump();
}
```

```text
error[E0502]: cannot borrow `count` as immutable because it is also borrowed as mutable
 --> main.rs:4:16
  |
3 |     let mut bump = || count += 1;
  |                    -- ----- first borrow occurs due to use of `count` in closure
  |                    |
  |                    mutable borrow occurs here
4 |     println!("{count}");
  |                ^^^^^ immutable borrow occurs here
5 |     bump();
  |     ---- mutable borrow later used here
```

## move

`move`, gövde gerektirmese bile sahipliği closure'a taşır. Closure yerel değişkenlerden uzun yaşayacaksa gerekir:

```rust
fn make_greeter() -> impl Fn() -> String {
    let name = String::from("Ada");
    || format!("Hello, {name}")
}

fn main() {
    println!("{}", make_greeter()());
}
```

```text
error[E0373]: closure may outlive the current function, but it borrows `name`, which is
owned by the current function
 --> main.rs:3:5
  |
3 |     || format!("Hello, {name}")
  |     ^^                  ---- `name` is borrowed here
  |     |
  |     may outlive borrowed value `name`
  |
note: closure is returned here
 --> main.rs:3:5
  |
3 |     || format!("Hello, {name}")
  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
help: to force the closure to take ownership of `name` (and any other referenced
variables), use the `move` keyword
  |
3 |     move || format!("Hello, {name}")
  |     ++++
```

```rust
fn make_greeter() -> impl Fn() -> String {
    let name = String::from("Ada");
    move || format!("Hello, {name}")
}

fn main() {
    let greet = make_greeter();
    println!("{}", greet());
}
```

```text
Hello, Ada
```

Bölüm 10'da iş parçacıklarında bunu sürekli yazacağız. `Copy` olan değer `move` ile kopyalanır, asıl değişken kullanılmaya devam eder.

## Closure'u parametre almak

Her closure'ın kendi adsız türü vardır, bu yüzden generic ile alınır. Kısıt üç trait'ten biridir:

| Trait | Kaç kez çağrılabilir | Ne yapabilir |
|---|---|---|
| `FnOnce` | En az bir kez | Yakaladığını tüketebilir |
| `FnMut` | Çok kez | Yakaladığını değiştirebilir |
| `Fn` | Çok kez, aynı anda da | Yalnızca okur |

```rust
fn apply<F: Fn(i32) -> i32>(f: F, value: i32) -> i32 {
    f(f(value))
}

fn repeat<F: FnMut()>(mut f: F, times: u32) {
    for _ in 0..times {
        f();
    }
}

fn finish<F: FnOnce() -> String>(f: F) -> String {
    f()
}

fn main() {
    println!("{}", apply(|x| x + 3, 1));
    let mut total = 0;
    repeat(|| total += 2, 3);
    println!("{total}");
    let text = String::from("done");
    println!("{}", finish(|| text));
}
```

```text
7
6
done
```

Bir `Fn` aynı zamanda `FnMut` ve `FnOnce`'tır. Parametrede **yapabildiğin en gevşek olanı iste**: Bir kez çağıracaksan `FnOnce`, çok kez çağırıp değiştirecekse `FnMut`. Böylece daha çok closure kabul edilir.

Tüketen closure ikinci kez çağrılamaz:

```rust
fn main() {
    let text = String::from("gone");
    let consume = || drop(text);
    consume();
    consume();
}
```

```text
error[E0382]: use of moved value: `consume`
 --> main.rs:5:5
  |
4 |     consume();
  |     --------- `consume` moved due to this call
5 |     consume();
  |     ^^^^^^^ value used here after move
  |
note: closure cannot be invoked more than once because it moves the variable `text` out
of its environment
 --> main.rs:3:27
  |
3 |     let consume = || drop(text);
  |                           ^^^^
note: this value implements `FnOnce`, which causes it to be moved when called
 --> main.rs:4:5
  |
4 |     consume();
  |     ^^^^^^^
```

## Fonksiyon adı da geçer

Closure beklenen yere fonksiyon adı verilebilir:

```rust
fn double(n: i32) -> i32 {
    n * 2
}

fn apply(f: fn(i32) -> i32, value: i32) -> i32 {
    f(value)
}

fn main() {
    println!("{}", apply(double, 4));
    let values: Vec<i32> = vec![1, 2].into_iter().map(double).collect();
    println!("{:?}", values);
    let wrapped: Vec<Option<i32>> = vec![1, 2].into_iter().map(Some).collect();
    println!("{:?}", wrapped);
}
```

```text
8
[2, 4]
[Some(1), Some(2)]
```

`Some` ve tuple struct'ın kurucusu da fonksiyondur. `fn(i32) -> i32` yazımı ise **fonksiyon işaretçisi** türüdür: Yakalama yapmaz.

## Closure döndürmek

Gerçek tür adsız olduğu için `impl Fn` döndürülür. Yerel değişken yakalıyorsa `move` zorunludur:

```rust
fn adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

fn main() {
    let add5 = adder(5);
    let add9 = adder(9);
    println!("{} {}", add5(1), add9(1));
}
```

```text
6 10
```

## Bir yerde saklamak

Struct alanında generic ile tutulur:

```rust
struct Lazy<F: Fn() -> u32> {
    compute: F,
    value: Option<u32>,
}

impl<F: Fn() -> u32> Lazy<F> {
    fn new(compute: F) -> Self {
        Lazy { compute, value: None }
    }

    fn get(&mut self) -> u32 {
        if let Some(v) = self.value {
            return v;
        }
        println!("computing");
        let v = (self.compute)();
        self.value = Some(v);
        v
    }
}

fn main() {
    let mut lazy = Lazy::new(|| 6 * 7);
    println!("{}", lazy.get());
    println!("{}", lazy.get());
}
```

```text
computing
42
42
```

Bu **tembel hesap** (lazy) örneği: Fonksiyon yalnızca bir kez, gerekince çalışıyor.

## Özet

- `|x| x + 1` adsız fonksiyondur; türler çoğu zaman çıkarılır, bir kez sabitlenir.
- Çevreyi yakalar: Okuma `&`, değiştirme `&mut`, tüketme taşıma. Ödünç kuralları geçerli.
- `move` sahipliği zorla taşır; closure yerelden uzun yaşayacaksa gerekir.
- `FnOnce`, `FnMut`, `Fn`: Parametrede en gevşeğini iste.
- Fonksiyon adı da geçer. Döndürürken `-> impl Fn(...)` ve `move`.
