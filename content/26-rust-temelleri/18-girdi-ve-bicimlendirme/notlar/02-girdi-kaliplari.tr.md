## Aynı satırda iki sayı

Girdi `6 7` gibi tek satırdaysa `split_whitespace` metni boşluklardan böler, her `next` sıradakini verir. `next`'in de
`expect` istemesinin sebebi: Parça kalmamış olabilir.

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");

    let mut parts = line.split_whitespace();
    let a: i32 = parts.next().expect("first").parse().expect("not a number");
    let b: i32 = parts.next().expect("second").parse().expect("not a number");
    println!("{}", a * b);
}
```

Girdi `6 7` iken:

```text
42
```

## Bütün girdiyi bir kerede

`io::read_to_string` girdi bitene kadar okur. Kaç satır geleceği belli değilse işe yarar:

```rust
use std::io;

fn main() {
    let text = io::read_to_string(io::stdin()).expect("could not read");
    println!("{}", text.lines().count());
    println!("{}", text.split_whitespace().count());
}
```

Girdi iki satırken (`one two` ve `three`):

```text
2
3
```

## Girdi bittiyse

`read_line` okuduğu bayt sayısını da döndürür. Girdi bitmişse 0 bayt okur ve metin boş kalır:

```rust
use std::io;

fn main() {
    let mut line = String::new();
    io::stdin().read_line(&mut line).expect("could not read");
    println!("{}", line.len());
}
```

Hiç girdi verilmediğinde:

```text
0
```

Bu sayıyı döngüde bitişi anlamak için kullanacağız (Koşullar ve Döngüler).

## Sık hatalar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `InvalidDigit` | `trim` unutuldu ya da girdi sayı değil | `line.trim().parse()` |
| `Empty` | Girdi boş | Girdiyi denetle |
| `E0284` | Hedef tür yazılmadı | `let n: i32 = ...` |
| `E0596` | `let line`, `mut` değil | `let mut line` |
| İkinci sayı yanlış | `clear` unutuldu | `line.clear();` |
| Soru görünmüyor | `print!` bekliyor | `io::stdout().flush()` |
