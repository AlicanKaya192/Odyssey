Girdi okumayı Girdi ve Biçimlendirme bölümünde gördük. Döngüyle birleşince program kullanıcı yazmayı bırakana kadar
çalışabilir.

## Girdi bitene kadar

```rust
use std::io;

fn main() {
    let mut total = 0;
    let mut line = String::new();
    loop {
        line.clear();
        let bytes = io::stdin().read_line(&mut line).expect("could not read");
        if bytes == 0 || line.trim() == "end" {
            break;
        }
        let n: i32 = line.trim().parse().expect("not a number");
        total += n;
    }
    println!("total: {total}");
}
```

Girdi satırları `4`, `5`, `end`, `7` iken:

```text
total: 9
```

| Satır | Neden |
|---|---|
| `line.clear()` | `read_line` sonuna ekler; her turda baştan başlıyoruz |
| `let bytes = ...` | `read_line` okunan bayt sayısını verir |
| `bytes == 0` | Girdi bitti: 0 bayt okundu |
| `line.trim() == "end"` | Kullanıcı bitirmek istedi |

`end`'den sonraki `7` hiç okunmadı, çünkü döngü orada bitti.

## Küçük bir oyun

`if`, `else if` ve `break` birlikte bir tahmin oyunu yapar:

```rust
use std::io;

fn main() {
    let secret = 7;
    let mut line = String::new();
    loop {
        line.clear();
        let bytes = io::stdin().read_line(&mut line).expect("could not read");
        if bytes == 0 {
            println!("no more input");
            break;
        }
        let guess: i32 = line.trim().parse().expect("not a number");
        if guess < secret {
            println!("{guess}: too low");
        } else if guess > secret {
            println!("{guess}: too high");
        } else {
            println!("{guess}: found");
            break;
        }
    }
}
```

Girdi satırları `3`, `9`, `7`, `1` iken:

```text
3: too low
9: too high
7: found
```

## Bu patikada

Girdi isteyen alıştırmalarda Odyssey programına önceden hazırlanmış girdiyi verir. Programın kullanıcı gibi yazmanı beklemez.
