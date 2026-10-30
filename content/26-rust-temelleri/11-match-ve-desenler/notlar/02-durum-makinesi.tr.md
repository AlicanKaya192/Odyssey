Enum ve `match` birlikte **durum makinesi** kurmanın en temiz yoludur. Bir sipariş düşün: Hangi olay hangi durumda geçerli?

```rust
#[derive(Debug, Clone, Copy)]
enum State {
    Pending,
    Paid,
    Shipped,
}

#[derive(Clone, Copy)]
enum Event {
    Pay,
    Ship,
    Cancel,
}

impl State {
    fn next(self, event: Event) -> State {
        match (self, event) {
            (State::Pending, Event::Pay) => State::Paid,
            (State::Paid, Event::Ship) => State::Shipped,
            (State::Paid, Event::Cancel) => State::Pending,
            (state, _) => state,
        }
    }
}

fn main() {
    let mut state = State::Pending;
    for event in [Event::Ship, Event::Pay, Event::Ship, Event::Cancel] {
        state = state.next(event);
        println!("{:?}", state);
    }
}
```

```text
Pending
Paid
Shipped
Shipped
```

Dikkat edilecekler:

- Bütün geçişler tek yerde okunuyor.
- `(durum, olay)` demeti üzerinde `match` yazmak iki boyutlu tablo gibi.
- Geçersiz geçişler `_` kolunda: Durum değişmiyor.
- `self` alan metot eski durumu tüketir; aynı anda iki durum olamaz.

## Ne zaman _ kullanmalı?

Burada `_` bilerek kullanıldı: "geri kalan her olay geçersiz" tek bir kuraldır. Ama yeni bir durum eklenince derleyici artık o kolu sormaz. Karar şu:

| Soru | Seçim |
|---|---|
| Yeni seçenek eklenince bu `match`'e bakılmalı mı? | Evet: Seçenekleri tek tek yaz |
| Yeni seçenek de aynı "geri kalan" gruba mı girer? | `_` |

## Sonsuz değil, bütün değerler

`match` sayılarda da kapsayıcı olmalıdır. `u8` için 0'dan 255'e kadar bütün değerleri kapsayan kollar yazarsan `_` gerekmez:

```rust
fn kind(n: u8) -> &'static str {
    match n {
        0..=99 => "small",
        100..=255 => "big",
    }
}

fn main() {
    println!("{} {}", kind(5), kind(200));
}
```

```text
small big
```
