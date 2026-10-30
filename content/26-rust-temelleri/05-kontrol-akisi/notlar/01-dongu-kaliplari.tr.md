Sık karşılaşılan döngü kalıpları. Hepsini derleyip çalıştırdık.

## Toplam

```rust
fn main() {
    let mut total = 0;
    for n in 1..=100 {
        total += n;
    }
    println!("{total}");
}
```

```text
5050
```

Toplam değişkeni `mut` olmalı ve döngüden önce açılmalı. Döngünün içinde açarsan her turda sıfırlanır.

## Sayma

```rust
fn main() {
    let mut evens = 0;
    for n in 1..=10 {
        if n % 2 == 0 {
            evens += 1;
        }
    }
    println!("{evens}");
}
```

```text
5
```

## En büyüğü bulmak

```rust
fn main() {
    let values = [3, 9, 2, 7];
    let mut largest = i32::MIN;
    for v in values {
        if v > largest {
            largest = v;
        }
    }
    println!("{largest}");
}
```

```text
9
```

Başlangıç değeri olarak `i32::MIN` kullandık: Hangi sayı gelirse gelsin ondan büyük ya da ona eşittir.

## Bulunca durmak

```rust
fn main() {
    let values = [4, 8, 15, 16];
    for v in values {
        if v % 5 == 0 {
            println!("first: {v}");
            break;
        }
    }
}
```

```text
first: 15
```

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Son eleman eksik | `1..n` son değeri dışarıda bırakır, `1..=n` gerekir |
| Toplam hep son değer | `total` döngünün içinde açılmış |
| Program bitmiyor | `while` koşulundaki değişken hiç değişmiyor |
| `cannot assign twice` | Sayaç `mut` değil |
