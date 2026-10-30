## Sayaç üreteci

Her closure kendi durumunu taşır:

```rust
fn counter(start: u32) -> impl FnMut() -> u32 {
    let mut count = start;
    move || {
        count += 1;
        count
    }
}

fn main() {
    let mut a = counter(0);
    let mut b = counter(100);
    println!("{} {} {}", a(), a(), b());
}
```

```text
1 2 101
```

`FnMut` döndürülüyor, `count` closure'ın içinde yaşıyor. İki sayaç birbirinden bağımsız. Çağıran değişkeni `mut` tanımlamak zorunda.

## Geri çağırma (callback)

Bir işin ortasında çağırana söz vermek için:

```rust
fn process(items: &[i32], mut report: impl FnMut(i32)) -> i32 {
    let mut total = 0;
    for item in items {
        total += item;
        report(total);
    }
    total
}

fn main() {
    let mut seen = Vec::new();
    let total = process(&[1, 2, 3], |t| seen.push(t));
    println!("{total} {:?}", seen);
}
```

```text
6 [1, 3, 6]
```

## Bileştirme

İki fonksiyonu birleştiren fonksiyon:

```rust
fn compose<A, B, C>(f: impl Fn(A) -> B, g: impl Fn(B) -> C) -> impl Fn(A) -> C {
    move |x| g(f(x))
}

fn main() {
    let len_doubled = compose(|s: &str| s.len(), |n| n * 2);
    println!("{}", len_doubled("rust"));
}
```

```text
8
```

## Küçük alışkanlıklar

| Kötü | İyi |
|---|---|
| <code>&#124;x&#124; foo(x)</code> | `foo` |
| <code>&#124;x&#124; x.len()</code> | `str::len` (tür belliyse) |
| `.clone()` closure'a geçsin diye | Önce ödünç dene |
| Uzun gövdeli closure | Adlı fonksiyon yaz |

Bir closure beş satırı geçtiyse fonksiyon olmalıdır: Adı, ne yaptığını anlatır.
