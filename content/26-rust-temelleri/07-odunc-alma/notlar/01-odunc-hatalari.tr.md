Rust öğrenirken göreceğin ödünç hataları ve ilk denenecek çözüm.

| Kod | Ne diyor | İlk çözüm |
|---|---|---|
| `E0382` | Taşınmış değeri kullandın | `&` ile ödünç ver |
| `E0499` | İki `&mut` aynı anda | Birini bitir, sonra ötekini al |
| `E0502` | `&` varken `&mut` | Okumayı önce bitir |
| `E0505` | Ödünç verilmişi taşıdın | Referansla işin bittikten sonra taşı |
| `E0506` | Ödünç verilmişe yeni değer | Referansın son kullanımından sonra ata |
| `E0596` | Değişmezi `&mut` aldın | Değişkene `mut` ekle |
| `E0597` | Değer referanstan önce öldü | Değeri daha dış kapsama al |
| `E0515` | Yerel değere referans döndü | Değerin kendisini döndür |
| `E0106` | Dönen referansın ömrü belirsiz | Değer döndür ya da ömür yaz |

## E0597: Değer yeterince yaşamıyor

```rust
fn main() {
    let r;
    {
        let value = 5;
        r = &value;
    }
    println!("{r}");
}
```

```text
error[E0597]: `value` does not live long enough
 --> main.rs:5:13
  |
4 |         let value = 5;
  |             ----- binding `value` declared here
5 |         r = &value;
  |             ^^^^^^ borrowed value does not live long enough
6 |     }
  |     - `value` dropped here while still borrowed
7 |     println!("{r}");
  |                - borrow later used here
```

`value` iç bloğun sonunda silindi, `r` onu sonra okumaya çalışıyor. Çözüm: `value`'yu dış bloğa al.

## Sık yapılan bir hile: Kopya almak

Sayı gibi `Copy` türlerde referans yerine değeri almak çoğu çakışmayı çözer:

```rust
fn main() {
    let mut list = vec![1, 2, 3];
    let first = list[0];
    list.push(first);
    println!("{:?}", list);
}
```

```text
[1, 2, 3, 1]
```

`first` ilk elemanın kopyası, yani bir referans değil. Listeye eklemek serbest kaldı.

## Derleyiciyle kavga etme

Kural şu: Derleyici bir şeyi reddediyorsa genellikle haklı bir sebebi vardır. `.clone()` yazıp geçmek bazen doğrudur, ama önce kendine şunu sor: **Bu veriye
gerçekten kim sahip olmalı?** Tasarım doğru olunca hataların çoğu kendiliğinden kaybolur.
