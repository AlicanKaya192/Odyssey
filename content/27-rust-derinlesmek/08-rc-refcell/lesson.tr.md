# Rc, RefCell ve Paylaşım

Sahiplik kuralı "tek sahip" diyor. Çoğu zaman doğru, ama bazen bir değerin gerçekten birden çok sahibi olur: Bir grafikte aynı düğüme iki kenar gelmesi gibi. Ödünç alma kuralı da "aynı anda tek yazıcı" diyor ve bunu derleme zamanında denetliyor. Bazen derleyici doğru kodu kanıtlayamaz. Bu bölümün iki türü bu iki kuralı **güvenli biçimde esnetir.**

## Sorun: İki sahip

```rust
fn main() {
    let a = String::from("shared");
    let list = vec![a];
    let other = vec![a];
    println!("{} {}", list.len(), other.len());
}
```

```text
error[E0382]: use of moved value: `a`
 --> main.rs:4:22
  |
2 |     let a = String::from("shared");
  |         - move occurs because `a` has type `String`, which does not implement the
  `Copy` trait
3 |     let list = vec![a];
  |                     - value moved here
4 |     let other = vec![a];
  |                      ^ value used here after move
  |
help: consider cloning the value if the performance cost is acceptable
  |
3 |     let list = vec![a.clone()];
  |                      ++++++++
```

`list` `a`'yı aldı, `other` alamıyor. Tek çözüm ödünç almak olurdu, ama yaşam süreleri hızla karmaşıklaşır.

## Rc: Sayılan sahiplik

`Rc<T>` (reference counted) değeri öbekte tutar ve **kaç sahip olduğunu sayar.** Sayaç sıfıra inince değer silinir.

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(String::from("shared"));
    let b = Rc::clone(&a);
    let c = Rc::clone(&a);
    println!("{a} {b} {c}");
    println!("{}", a.len());
}
```

```text
shared shared shared
6
```

<figure class="fig"><svg viewBox="0 0 640 226" width="640" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="20" y="24" font-size="13" font-weight="600">yığın (stack)</text><text class="dim" x="390" y="24" font-size="13" font-weight="600">öbek (heap)</text><g><rect class="box" x="20" y="44" width="230" height="44" rx="8"/><text class="ink" x="34" y="71" font-size="14" font-weight="600">a</text><text class="dim" x="110" y="71" font-size="12.5">Rc</text></g><g><rect class="box" x="20" y="102" width="230" height="44" rx="8"/><text class="ink" x="34" y="129" font-size="14" font-weight="600">b</text><text class="dim" x="110" y="129" font-size="12.5">Rc</text></g><g><rect class="box" x="20" y="160" width="230" height="44" rx="8"/><text class="ink" x="34" y="187" font-size="14" font-weight="600">c</text><text class="dim" x="110" y="187" font-size="12.5">Rc</text></g><g><rect class="box" x="390" y="44" width="220" height="44" rx="8"/><text class="ink" x="404" y="71" font-size="14">sayaç 3, &quot;shared&quot;</text></g><path class="curve" d="M250 66 C320 66 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 124 C320 124 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/><path class="curve" d="M250 182 C320 182 320 66 382 66"/><polygon class="dot" points="390,66 380,61 380,71"/></svg><figcaption>Üç sahip, tek değer. Sonuncusu gidince değer silinir.</figcaption></figure>

`Rc::clone(&a)` değeri kopyalamaz, yalnızca sayacı artırır. Bu yüzden `a.clone()` yerine `Rc::clone(&a)` yazmak gelenektir: "Bu pahalı kopya değil" diye okunur.

Sayacı izleyelim:

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(5);
    println!("{}", Rc::strong_count(&a));
    let b = Rc::clone(&a);
    println!("{}", Rc::strong_count(&a));
    {
        let _c = Rc::clone(&a);
        println!("{}", Rc::strong_count(&a));
    }
    println!("{}", Rc::strong_count(&a));
    drop(b);
    println!("{}", Rc::strong_count(&a));
}
```

```text
1
2
3
2
1
```

## Rc yalnızca okur

`Rc` birden çok sahip verdiği için içeriği değiştirmene izin vermez. Değiştirebilseydi ödünç kuralı bozulurdu:

```rust
use std::rc::Rc;

fn main() {
    let a = Rc::new(vec![1]);
    a.push(2);
    println!("{:?}", a);
}
```

```text
error[E0596]: cannot borrow data in an `Rc` as mutable
 --> main.rs:5:5
  |
5 |     a.push(2);
  |     ^ cannot borrow as mutable
  |
  = help: trait `DerefMut` is required to modify through a dereference, but it is not
    implemented for `Rc<Vec<i32>>`
```

Paylaşıp değiştirmek için ikinci parça gerekiyor.

## RefCell: Denetim çalışma anında

`RefCell<T>`, **iç değişebilirlik** (interior mutability) sağlar: `&self` ile değiştirmeye izin verir. Kurallar aynıdır, yalnızca denetim derleme yerine çalışma anında yapılır:

```rust
use std::cell::RefCell;

struct Notes {
    lines: RefCell<Vec<String>>,
}

impl Notes {
    fn add(&self, line: &str) {
        self.lines.borrow_mut().push(line.to_string());
    }
}

fn main() {
    let notes = Notes { lines: RefCell::new(Vec::new()) };
    notes.add("first");
    notes.add("second");
    println!("{:?}", notes.lines.borrow());
}
```

```text
["first", "second"]
```

| Metot | Ne verir | Karşılığı |
|---|---|---|
| `.borrow()` | Okuma için | `&T` |
| `.borrow_mut()` | Değiştirmek için | `&mut T` |

Kuralı çiğnersen derleyici değil, program durur:

```rust
use std::cell::RefCell;

fn main() {
    let cell = RefCell::new(1);
    let _first = cell.borrow_mut();
    let _second = cell.borrow_mut();
    println!("not reached");
}
```

```text
thread 'main' panicked at main.rs:6:24:
RefCell already borrowed
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Derleyici bu hatayı yakalayamaz, bedeli budur. `try_borrow_mut` panik yerine `Result` döndürür.

## Rc ile RefCell birlikte

Birden çok sahip **ve** değiştirme için en yaygın ikili: `Rc<RefCell<T>>`.

```rust
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let list = Rc::new(RefCell::new(vec![1]));
    let a = Rc::clone(&list);
    let b = Rc::clone(&list);
    a.borrow_mut().push(2);
    b.borrow_mut().push(3);
    println!("{:?}", list.borrow());
    println!("{}", Rc::strong_count(&list));
}
```

```text
[1, 2, 3]
3
```

`a` ve `b` aynı listeyi görüyor. Her ikisi de ekleyebilir.

## Referans döngüsü

`Rc` tek bir yerde çöp toplayıcıya yetişemez: İki değer birbirini tutarsa sayaç hiç sıfıra inmez ve **bellek sızar.** Rust bunu derlemede yakalamaz, çünkü sızıntı "güvensiz" sayılmaz:

```rust
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    name: &'static str,
    next: RefCell<Option<Rc<Node>>>,
}

impl Drop for Node {
    fn drop(&mut self) {
        println!("dropping {}", self.name);
    }
}

fn main() {
    let a = Rc::new(Node { name: "a", next: RefCell::new(None) });
    let b = Rc::new(Node { name: "b", next: RefCell::new(Some(Rc::clone(&a))) });
    *a.next.borrow_mut() = Some(Rc::clone(&b));
    println!("{} {}", Rc::strong_count(&a), Rc::strong_count(&b));
    println!("main ends");
}
```

```text
2 2
main ends
```

"dropping" hiç yazılmadı: İki düğüm birbirini canlı tutuyor.

## Weak: Sahip olmayan bağ

Çözüm: Bir yönü **zayıf** yapmak. `Weak<T>` sayacı artırmaz, değer silinmiş olabilir, bu yüzden `.upgrade()` `Option` döndürür:

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Child {
    parent: RefCell<Weak<Parent>>,
}

struct Parent {
    name: String,
}

fn main() {
    let child = Child { parent: RefCell::new(Weak::new()) };
    println!("{}", child.parent.borrow().upgrade().is_none());
    {
        let parent = Rc::new(Parent { name: String::from("root") });
        *child.parent.borrow_mut() = Rc::downgrade(&parent);
        let up = child.parent.borrow().upgrade();
        println!("{}", up.map(|p| p.name.clone()).unwrap_or_default());
        println!("{}", Rc::strong_count(&parent));
    }
    println!("{}", child.parent.borrow().upgrade().is_none());
}
```

```text
true
root
1
true
```

Tipik kullanım ağaçtır: Ebeveyn çocuğa sahiptir (`Rc`), çocuk ebeveyni yalnızca bilir (`Weak`).

## Tek iş parçacığı

`Rc` ve `RefCell` iş parçacıkları arasında **kullanılamaz**: Sayaç atomik değil. Derleyici engeller. Karşılıkları `Arc` ve `Mutex` (bölüm 11).

## Özet

- `Rc<T>` birden çok sahip: `Rc::clone` sayacı artırır, sıfırda silinir, içeriği yalnızca okunur.
- `RefCell<T>` `&self` ile değiştirme: `borrow`, `borrow_mut`; kural ihlali **panik**.
- `Rc<RefCell<T>>` paylaşıp değiştirmek için.
- Döngü sızıntı yapar; `Weak` bağı sayılmaz, `upgrade` `Option` verir.
- Yalnızca tek iş parçacığında. Çoğu kod bunlara hiç ihtiyaç duymaz: Önce sahiplik ve ödünç dene.
