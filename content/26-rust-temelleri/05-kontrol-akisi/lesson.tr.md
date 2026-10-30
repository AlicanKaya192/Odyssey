# Koşullar ve Döngüler

Program şimdiye kadar yukarıdan aşağıya tek yolda ilerledi. Gerçek programlar karar verir ve iş tekrar eder.

## if ile karar

```rust
fn main() {
    let score = 72;
    if score >= 90 {
        println!("excellent");
    } else if score >= 50 {
        println!("passed");
    } else {
        println!("failed");
    }
}
```

```text
passed
```

Koşulun etrafında parantez yoktur, süslü parantezler ise zorunludur. `else if` yeni bir koşul sınar, `else`
hiçbiri tutmazsa çalışır. Yukarıdan aşağıya ilk tutan dal çalışır, geri kalanlara bakılmaz.

**Koşul mutlaka `bool` olmalıdır.** Bazı dillerde sayı da koşul olabilir; Rust kabul etmez:

```rust
fn main() {
    let number = 3;
    if number {
        println!("yes");
    }
}
```

```text
error[E0308]: mismatched types
 --> main.rs:3:8
  |
3 |     if number {
  |        ^^^^^^ expected `bool`, found integer
```

Niyetin neyse onu yazarsın: `if number != 0`.

## if bir ifadedir

Önceki bölümde bloğun ifade olduğunu gördük. `if` de ifadedir, yani değer verir. Başka dillerdeki üçlü işlecin
(`? :`) yerini bu tutar:

```rust
fn main() {
    let age = 20;
    let label = if age >= 18 { "adult" } else { "child" };
    println!("{label}");
}
```

```text
adult
```

Noktalı virgüllere dikkat: Dalların içinde yok, çünkü değer veriyorlar. `let` satırının sonunda var, çünkü orası deyim.

İki dalın türü aynı olmalıdır. Derleyici değişkenin türünü derleme anında bilmek zorundadır:

```rust
fn main() {
    let flag = true;
    let value = if flag { 5 } else { "six" };
    println!("{value}");
}
```

```text
error[E0308]: `if` and `else` have incompatible types
 --> main.rs:3:38
  |
3 |     let value = if flag { 5 } else { "six" };
  |                           -          ^^^^^ expected integer, found `&str`
  |                           |
  |                           expected because of this
```

## loop: sonsuz döngü

`loop` sen durdurana dek tekrar eder. `break` döngüden çıkar, `continue` bir sonraki tura geçer:

```rust
fn main() {
    let mut n = 0;
    loop {
        n += 1;
        if n == 2 {
            continue;
        }
        if n > 4 {
            break;
        }
        println!("{n}");
    }
}
```

```text
1
3
4
```

`loop` da ifadedir: `break` yanında bir değer verebilir. Bir şeyi tekrar deneyip sonucu almak için çok işe yarar:

```rust
fn main() {
    let mut value = 1;
    let first_big = loop {
        value *= 2;
        if value > 100 {
            break value;
        }
    };
    println!("{first_big}");
}
```

```text
128
```

## while: koşullu döngü

Koşul doğru oldukça döner:

```rust
fn main() {
    let mut n = 3;
    while n > 0 {
        println!("{n}");
        n -= 1;
    }
    println!("go");
}
```

```text
3
2
1
go
```

## for: bir şeyin üzerinde dönmek

Rust'ta en sık kullanılan döngü budur. **Aralık** (range) ya da liste üzerinde gezer:

```rust
fn main() {
    for n in 1..4 {
        print!("{n} ");
    }
    println!();
    for n in 1..=4 {
        print!("{n} ");
    }
    println!();
    for n in (1..4).rev() {
        print!("{n} ");
    }
    println!();
}
```

```text
1 2 3
1 2 3 4
3 2 1
```

| Yazım | Değerler |
|---|---|
| `1..4` | 1, 2, 3 (son dahil değil) |
| `1..=4` | 1, 2, 3, 4 (son dahil) |
| `(1..4).rev()` | 3, 2, 1 (ters) |
| `(0..10).step_by(2)` | 0, 2, 4, 6, 8 |

Bir diziyi gezmek de aynı. Sıra numarası gerekiyorsa `.iter().enumerate()` hem sırayı hem değeri verir:

```rust
fn main() {
    let days = ["mon", "tue", "wed"];
    for day in days {
        println!("{day}");
    }
    for (position, day) in days.iter().enumerate() {
        println!("{position}: {day}");
    }
}
```

```text
mon
tue
wed
0: mon
1: tue
2: wed
```

Burada `.iter()` diziyi tek tek gezen bir yapı veriyor. Bu yazımın neden gerektiğini sahiplik konusunda, iterator'ların
tamamını ileride göreceğiz.

Elle sayaç tutup `array[i]` yazmak yerine `for` tercih edilir: Sınırı aşma ihtimali ortadan kalkar.

<figure class="fig"><div class="versus"><div><h4>Elle sayaç</h4><code>while i &lt; days.len() { ... days[i] ... i += 1; }</code><br>Sınırı yanlış yazmak kolay, her turda denetim gerekir.</div><div><h4>for</h4><code>for day in days { ... }</code><br>Sınır hatası yazılamaz.</div></div><figcaption>Rust'ta alışkanlık: Elinde bir liste varsa <code>for</code>.</figcaption></figure>

## İç içe döngülerden çıkmak: etiket

`break` yalnızca içinde bulunduğu döngüden çıkar. Dıştaki döngüden çıkmak için döngüye **etiket** verilir. Etiket tek
tırnakla başlar:

```rust
fn main() {
    'outer: for row in 1..=3 {
        for col in 1..=3 {
            if row * col == 4 {
                println!("found at {row} {col}");
                break 'outer;
            }
        }
    }
    println!("done");
}
```

```text
found at 2 2
done
```

## Hangisini seçmeli?

| Durum | Döngü |
|---|---|
| Bir liste ya da aralık üzerinde dönüyorsun | `for` |
| Bir koşul doğru oldukça | `while` |
| Bitiş içeriden belli oluyor, sonuç döneceksin | `loop` + `break` |

## Özet

- `if` koşulu `bool` olmalıdır, parantez gerekmez, süslü parantez zorunludur.
- `if` ifadedir: `let x = if ... { a } else { b };` iki dalın türü aynı olmalıdır.
- `loop` + `break` değer de döndürebilir; `continue` sonraki tura geçer.
- `for` en yaygın döngüdür: `1..4` son hariç, `1..=4` son dahil.
- Dıştaki döngüden çıkmak için `'etiket:` ve `break 'etiket`.
