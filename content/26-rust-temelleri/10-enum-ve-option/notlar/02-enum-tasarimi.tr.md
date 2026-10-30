## Ne zaman enum?

| Soru | Cevap |
|---|---|
| Değer birkaç kesin durumdan biri mi? | Enum |
| Durumlar farklı veri mi taşıyor? | Veri taşıyan enum |
| Bütün alanlar her zaman var mı? | Struct |
| Metin sabiti mi kullanıyorsun (`"red"`)? | Enum'a çevir |

Metin yerine enum kullanmak yazım hatasını derleme hatasına çevirir:

```rust
#[derive(Debug, PartialEq)]
enum Status {
    Draft,
    Published,
}

fn main() {
    let status = Status::Draft;
    println!("{}", status == Status::Published);
    println!("{:?}", status);
}
```

```text
false
Draft
```

## Enum ve struct birlikte

Çoğu gerçek tür ikisinin karışımıdır: Ortak alanlar struct'ta, değişen durum enum'da.

```rust
#[derive(Debug)]
enum State {
    Pending,
    Shipped { tracking: String },
}

#[derive(Debug)]
struct Order {
    id: u32,
    state: State,
}

fn main() {
    let order = Order { id: 7, state: State::Shipped { tracking: String::from("X1") } };
    println!("{:?}", order);
    let other = Order { id: 8, state: State::Pending };
    println!("{} {:?}", other.id, other.state);
}
```

```text
Order { id: 7, state: Shipped { tracking: "X1" } }
8 Pending
```

## Sayısal değerler

Yalnızca adlardan oluşan enum'lar sayıya çevrilebilir:

```rust
#[derive(Clone, Copy)]
enum Level {
    Low = 1,
    High = 10,
}

fn main() {
    println!("{}", Level::Low as i32);
    println!("{}", Level::High as i32);
}
```

```text
1
10
```

## Boyut

Bir enum en büyük seçeneği artı hangi seçenek olduğunu tutan etiket kadar yer kaplar. Çok büyük tek bir seçenek bütün enum'u büyütür. Ölçüm bu makinede:

```rust
use std::mem::size_of;

#[allow(dead_code)]
enum Small {
    A(u8),
    B,
}

#[allow(dead_code)]
enum Big {
    A(u8),
    B([u64; 100]),
}

fn main() {
    println!("{}", size_of::<Small>());
    println!("{}", size_of::<Big>());
}
```

```text
2
808
```
