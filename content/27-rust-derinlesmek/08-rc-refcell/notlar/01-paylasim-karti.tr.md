## Hangisi?

| İhtiyaç | Tür | Denetim |
|---|---|---|
| Tek sahip, öbek | `Box<T>` | Derleme |
| Çok sahip, okuma | `Rc<T>` | Derleme |
| Tek sahip, `&self` ile değiştirme | `RefCell<T>` | Çalışma anı |
| Küçük `Copy` değerde değiştirme | `Cell<T>` | Yok, panik de yok |
| Çok sahip ve değiştirme | `Rc<RefCell<T>>` | Çalışma anı |
| Sahip olmayan bağ | `Weak<T>` | `upgrade` |

## Yazımlar

| İş | Yazım |
|---|---|
| Oluştur | `Rc::new(x)`, `RefCell::new(x)` |
| Paylaş | `Rc::clone(&a)` |
| Sayaç | `Rc::strong_count(&a)` |
| Zayıf bağ | `Rc::downgrade(&a)` |
| Zayıftan güçlüye | `weak.upgrade()` |
| Oku | `cell.borrow()` |
| Yaz | `cell.borrow_mut()` |
| Birlikte | `shared.borrow_mut().push(1)` |

## Cell

`Copy` türde ödünç gerekmez: Değer alınıp konur, panik de olmaz.

```rust
use std::cell::Cell;

fn main() {
    let hits = Cell::new(0);
    hits.set(hits.get() + 1);
    hits.set(hits.get() + 1);
    println!("{}", hits.get());
}
```

```text
2
```

## Hatalar

| Belirti | Sebep |
|---|---|
| `already borrowed: BorrowMutError` | Aynı anda iki `borrow_mut` |
| `already mutably borrowed` | Yazarken okuma |
| `E0594`, `E0596` | `Rc` içeriğini değiştirmeye çalışmak |
| `Rc<...> cannot be sent` | İş parçacığına göndermek: `Arc` |
| Bellek büyüyor, `drop` çalışmıyor | Referans döngüsü: `Weak` |
