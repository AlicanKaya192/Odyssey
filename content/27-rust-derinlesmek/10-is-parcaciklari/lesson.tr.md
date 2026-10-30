# İş Parçacıkları ve Kanallar

**İş parçacığı** (thread), aynı programın içinde aynı anda ilerleyen ayrı bir yürütme kolu. Birkaç çekirdeği kullanmak ya da bir iş beklerken başkasını yapmak için kullanılır.

Eşzamanlı program yazmak çoğu dilde zordur: İki kol aynı veriye dokununca ortaya çıkan **veri yarışı** (data race) ancak bazen, üstelik yalnızca müşterinin makinesinde görülür. Rust'ın sözü cesurdur: **Veri yarışı derlenmez.**

## İlk iş parçacığı

`thread::spawn` bir closure alıp yeni kolda çalıştırır:

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        println!("from the branch");
        21 * 2
    });
    let result = handle.join().unwrap();
    println!("result {result}");
}
```

```text
from the branch
result 42
```

`spawn` bir **tutamak** (JoinHandle) döndürür. `join` kolun bitmesini bekler ve sonucunu verir. Her kol kendi hızında ilerlediği için aradaki sıra her çalıştırmada değişebilir, bu yüzden burada önce `join` çağrılıyor.

`join` çağrılmazsa `main` bitince program da biter, kol yarıda kesilir.

## Sonuç ve hata

`join` `Result` döndürür: Kol panik yaptıysa `Err`. Bir kolun paniği programı düşürmez:

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        if 1 + 1 == 2 {
            panic!("branch failed");
        }
        5
    });
    let result = handle.join();
    println!("is error: {}", result.is_err());
    println!("main goes on");
}
```

```text
is error: true
main goes on

thread '<unnamed>' panicked at main.rs:6:13:
branch failed
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

## move: Sahipliği kola vermek

Kol, onu başlatan fonksiyondan uzun yaşayabilir. Bu yüzden derleyici ödünç almaya izin vermez:

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3];
    let handle = thread::spawn(|| {
        println!("{:?}", list);
    });
    handle.join().unwrap();
}
```

```text
error[E0373]: closure may outlive the current function, but it borrows `list`, which is
owned by the current function
 --> main.rs:5:32
  |
5 |     let handle = thread::spawn(|| {
  |                                ^^ may outlive borrowed value `list`
6 |         println!("{:?}", list);
  |                          ---- `list` is borrowed here
  |
note: function requires argument type to outlive `'static`
 --> main.rs:5:18
  |
5 |       let handle = thread::spawn(|| {
  |  __________________^
6 | |         println!("{:?}", list);
7 | |     });
  | |______^
help: to force the closure to take ownership of `list` (and any other referenced
variables), use the `move` keyword
  |
5 |     let handle = thread::spawn(move || {
  |                                ++++
```

`move` ile sahiplik kola geçer:

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        let total: i32 = list.iter().sum();
        total
    });
    println!("{}", handle.join().unwrap());
}
```

```text
6
```

`list` artık kolun. `main` onu kullanmaya çalışırsa `E0382` alır. Sonucu geri almak için closure'dan döndür: `join` onu verir.

## Birkaç kol

```rust
use std::thread;

fn main() {
    let mut handles = Vec::new();
    for n in 0..4 {
        handles.push(thread::spawn(move || n * n));
    }
    let mut results = Vec::new();
    for h in handles {
        results.push(h.join().unwrap());
    }
    println!("{:?}", results);
}
```

```text
[0, 1, 4, 9]
```

Tutamakları toplayıp sırayla `join` etmek sonuçları başlatma sırasında verir, hangi kol önce bitmiş olursa olsun.

## Kapsamlı iş parçacıkları

`thread::scope` içindeki kollar scope bitmeden biter. Bu yüzden `move` olmadan yerel değişkeni **ödünç alabilirler**:

```rust
use std::thread;

fn main() {
    let list = vec![1, 2, 3, 4];
    let (left, right) = list.split_at(2);
    let (a, b) = thread::scope(|s| {
        let x = s.spawn(|| left.iter().sum::<i32>());
        let y = s.spawn(|| right.iter().sum::<i32>());
        (x.join().unwrap(), y.join().unwrap())
    });
    println!("{a} {b}");
    println!("{:?}", list);
}
```

```text
3 7
[1, 2, 3, 4]
```

Çoğu paralel hesap için en sade yol budur.

## Kanallar: Mesajla haberleşmek

Veriyi paylaşmak yerine göndermek. `mpsc` (çok üreten, tek tüketen):

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    thread::spawn(move || {
        for n in 1..=3 {
            tx.send(n * 10).unwrap();
        }
    });
    println!("{}", rx.recv().unwrap());
    for value in rx {
        println!("{value}");
    }
}
```

```text
10
20
30
```

| Parça | Anlamı |
|---|---|
| `tx` | Gönderen (transmitter), `clone` edilebilir |
| `rx` | Alan (receiver), tek |
| `tx.send(v)` | Gönderir, sahiplik geçer |
| `rx.recv()` | Mesaj gelene kadar bekler |
| `for x in rx` | Bütün gönderenler kapanana kadar |

Gönderilen değerin sahipliği geçer. Göndermeden sonra kullanmak derlenmez:

```rust
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();
    let text = String::from("hi");
    tx.send(text).unwrap();
    println!("{text}");
    println!("{}", rx.recv().unwrap());
}
```

```text
error[E0382]: borrow of moved value: `text`
 --> main.rs:7:16
  |
5 |     let text = String::from("hi");
  |         ---- move occurs because `text` has type `String`, which does not implement
  the `Copy` trait
6 |     tx.send(text).unwrap();
  |             ---- value moved here
7 |     println!("{text}");
  |                ^^^^ value borrowed here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
6 |     tx.send(text.clone()).unwrap();
  |                 ++++++++
```

Bu, veri yarışının derlenmemesinin küçük bir örneği: İki kol aynı veriye aynı anda erişemez.

## Birden çok gönderen

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    for id in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || {
            tx.send(id * 100).unwrap();
        });
    }
    drop(tx);
    let mut got: Vec<i32> = rx.iter().collect();
    got.sort();
    println!("{:?}", got);
}
```

```text
[0, 100, 200]
```

**Dikkat:** Asıl `tx`'i `drop` etmeyi unutursan `for` hiç bitmez, çünkü hâlâ bir gönderen açık.

Sonuçların hangi sırada geleceği belli değil; bu yüzden sıralıyoruz.

## Send ve Sync

Derleyici bunu iki işaret trait'iyle denetler:

| Trait | Anlamı |
|---|---|
| `Send` | Başka bir kola **taşınabilir** |
| `Sync` | Başka kollardan **ödünç alınabilir** |

Çoğu tür otomatik olarak ikisini de sağlar. `Rc` sağlamaz:

```rust
use std::rc::Rc;
use std::thread;

fn main() {
    let shared = Rc::new(5);
    let handle = thread::spawn(move || {
        println!("{shared}");
    });
    handle.join().unwrap();
}
```

```text
error[E0277]: `Rc<i32>` cannot be sent between threads safely
 --> main.rs:6:32
  |
6 |       let handle = thread::spawn(move || {
  |                    ------------- ^------
  |                    |             |
  |  __________________|_____________within this `{closure@main.rs:6:32: 6:39}`
  | |                  |
  | |                  required by a bound introduced by this call
7 | |         println!("{shared}");
8 | |     });
  | |_____^ `Rc<i32>` cannot be sent between threads safely
  |
  = help: within `{closure@main.rs:6:32: 6:39}`, the trait `Send` is not implemented for
    `Rc<i32>`
note: required because it's used within this closure
 --> main.rs:6:32
  |
6 |     let handle = thread::spawn(move || {
  |                                ^^^^^^^
note: required by a bound in `spawn`
```

Hata uzun görünür, ama özü "`Rc` `Send` değil" demektir. Bir sonraki bölümün konusu.

## Özet

- `thread::spawn(closure)` kol açar, `join` bekleyip sonucu verir. Sıra belirsizdir.
- Panik yalnızca o kolu düşürür; `join` `Err` verir.
- `move` sahipliği verir. `thread::scope` ödünç almaya izin verir.
- `mpsc::channel`: `send` sahipliği taşır, `recv` bekler. Bütün `tx`'ler kapanınca `for` biter.
- `Send` ve `Sync` veri yarışını derleme zamanında engeller.
