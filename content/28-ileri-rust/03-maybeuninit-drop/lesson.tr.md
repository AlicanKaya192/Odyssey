# MaybeUninit ve ManuallyDrop

Rust iki şeyi kendisi yapar: Her değeri kullanılmadan önce başlatmayı zorunlu kılar ve kapsam sonunda değeri düşürür. Kendi veri yapını yazarken bazen ikisine de müdahale etmen gerekir. Bu bölümün iki türü tam bunun için.

## Başlatılmamış bellek

`let x: i32;` yazıp okumak derlenmez. Bu güzel bir kural, ama `Vec` kapasitesindeki boş yerler de başlatılmamıştır. Onları "belki başlatılmış" diye tutacak bir tür gerekir:

```rust
use std::mem::MaybeUninit;

fn main() {
    let mut slot = MaybeUninit::<i32>::uninit();
    slot.write(42);

    // SAFETY: the value was written on the line above.
    let value = unsafe { slot.assume_init() };
    println!("{value}");
}
```

```text
42
```

`MaybeUninit<T>`, `T` kadar yer tutar ama içinin geçerli olduğuna söz vermez:

| Çağrı | Ne yapar |
|---|---|
| `MaybeUninit::uninit()` | Boş yer |
| `.write(v)` | Değeri yazar, eskisini düşürmez |
| `.assume_init()` | "Artık hazır" der, `T` döndürür |
| `.as_ptr()`, `.as_mut_ptr()` | İşaretçi |

`assume_init` `unsafe`'tir: Yazılmamış belleği okumak tanımsız davranıştır.

```rust
use std::mem::{ManuallyDrop, MaybeUninit};

fn main() {
    println!("{}", size_of::<String>());
    println!("{}", size_of::<MaybeUninit<String>>());
    println!("{}", size_of::<ManuallyDrop<String>>());
}
```

```text
24
24
24
```

Boyut aynı, ek bayrak yok. Hangi yerin dolu olduğunu **sen** takip edersin.

## Dizi doldurmak

Başlangıç değeri olmayan türlerle dizi kurmak en yaygın kullanımıdır:

```rust
use std::mem::MaybeUninit;

fn make_names() -> [String; 3] {
    let mut slots: [MaybeUninit<String>; 3] = [const { MaybeUninit::uninit() }; 3];

    for (i, slot) in slots.iter_mut().enumerate() {
        slot.write(format!("item {i}"));
    }

    // SAFETY: the loop wrote every slot, and the two arrays have the same layout.
    unsafe { slots.map(|slot| slot.assume_init()) }
}

fn main() {
    println!("{:?}", make_names());
}
```

```text
["item 0", "item 1", "item 2"]
```

`String`'in sıfır değeri yoktur, `[String::new(); 3]` da derlenmez. Üstelik `array::from_fn` çoğu zaman bu işi güvenli yapar; `MaybeUninit`'i anlamak için buradayız.

## Tuzak: Düşürülmeyen değerler

`MaybeUninit<T>` düşürülünce içini **düşürmez**, çünkü dolu olup olmadığını bilmez:

```rust
use std::mem::MaybeUninit;

struct Noisy;

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("dropped");
    }
}

fn main() {
    {
        let mut slot = MaybeUninit::<Noisy>::uninit();
        slot.write(Noisy);
        println!("end of first block");
    }
    {
        let mut slot = MaybeUninit::<Noisy>::uninit();
        slot.write(Noisy);
        // SAFETY: the value was written on the line above.
        unsafe { slot.assume_init_drop() };
        println!("end of second block");
    }
}
```

```text
end of first block
dropped
end of second block
```

`write` ile yazılan değer, elle okunmazsa sızar. Hata anında da böyledir: Dizi yarısındayken panik olursa dolu olanlar düşmez. Bu, sızıntıdır ama tanımsız davranış değildir.

## ManuallyDrop

`ManuallyDrop<T>` tersini yapar: Değer dolu, ama kapsam sonunda **düşürülmez**. Düşürmek sana kalır:

```rust
use std::mem::ManuallyDrop;

struct Noisy(&'static str);

impl Drop for Noisy {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let mut kept = ManuallyDrop::new(Noisy("kept"));
    let _forgotten = ManuallyDrop::new(Noisy("forgotten"));
    let _normal = Noisy("normal");

    println!("{}", kept.0);
    // SAFETY: kept is not used after this line.
    unsafe { ManuallyDrop::drop(&mut kept) };
    println!("end");
}
```

```text
kept
drop kept
end
drop normal
```

`mem::forget(x)` de düşürmeyi engeller; ikisinin farkı, `ManuallyDrop`'un değere sonradan ulaşmaya izin vermesidir.

Neden gerekir? Bir türün parçalarını farklı sırayla düşürmek ya da sahipliği elle başka yere taşımak için. Örneğin kendi `Vec`'imiz `into_iter` yaparken ana değerin `Drop`'unun çalışmasını istemez.

## Yarım iş güvenliği

Değerleri elle taşırken panik olabilir: Yazdığın `T::clone` panik yaparsa ne olur? Bu **panik güvenliği** sorusudur. Çözüm, durumu her adımda geçerli tutmak:

```rust
use std::panic::{self, AssertUnwindSafe};

struct Guard<'a> {
    list: &'a mut Vec<i32>,
    original_len: usize,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.list.truncate(self.original_len);
    }
}

fn extend_all_or_nothing(list: &mut Vec<i32>, make: impl Fn(i32) -> i32) {
    let original_len = list.len();
    let guard = Guard { list, original_len };
    for n in 0..3 {
        let value = make(n);
        guard.list.push(value);
    }
    std::mem::forget(guard);
}

fn main() {
    panic::set_hook(Box::new(|_| {}));
    let mut list = vec![9];

    let _ = panic::catch_unwind(AssertUnwindSafe(|| {
        extend_all_or_nothing(&mut list, |n| if n == 2 { panic!("no") } else { n });
    }));
    println!("{list:?}");

    extend_all_or_nothing(&mut list, |n| n);
    println!("{list:?}");
}
```

```text
[9]
[9, 0, 1, 2]
```

Koruyucu değer, panikte de düşürülür ve yarım işi toparlar. Standart kütüphanede bu kalıp her yerdedir.

## Özet

- `MaybeUninit<T>`: Aynı boyut, geçerlilik sözü yok, düşürmez.
- `assume_init` ancak yazıldıktan sonra.
- `ManuallyDrop<T>`: Değer geçerli, düşürmesi sende.
- Dolu olanları sen takip edersin; panikte sızıntı olabilir.
- Koruyucu değer yarım işi toparlar.
