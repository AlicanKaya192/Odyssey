## Ne zaman generic yazmalı?

Önce somut tür ile yaz. İkinci tür gerçekten gerekince generic'e çevir: Üç küçük adım.

1. `i32` için yaz, test et.
2. `i32`'yi `T` yap, derleyiciyi dinle.
3. İstediği kısıtları ekle.

Hiç kullanılmayacak genellik kodu okumayı zorlaştırır.

## Sahiplik ile birlikte

```rust
fn first_copy<T: Copy>(list: &[T]) -> T {
    list[0]
}

fn first_clone<T: Clone>(list: &[T]) -> T {
    list[0].clone()
}

fn first_ref<T>(list: &[T]) -> &T {
    &list[0]
}

fn main() {
    println!("{}", first_copy(&[1, 2]));
    let words = [String::from("a"), String::from("b")];
    println!("{}", first_clone(&words));
    println!("{}", first_ref(&words));
}
```

```text
1
a
a
```

| İmza | Ne alır | Kısıt |
|---|---|---|
| `fn f<T>(x: T)` | Sahipliği | Yok |
| `fn f<T>(x: &T)` | Ödünç | Yok |
| `fn f<T: Copy>(x: &[T]) -> T` | Kopyasını döndürür | `Copy` |
| `fn f<T: Clone>(x: &[T]) -> T` | `.clone()` döndürür | `Clone` |

`&T` döndürmek çoğu zaman en az şeyi ister: Ne kopya ne kısıt gerekir.

## Kısıt nereye?

| Yer | Etkisi |
|---|---|
| `struct S<T: Debug>` | Her kullanımda yazılmak zorunda kalır; **kaçın** |
| `impl<T: Debug> S<T>` | Yalnızca o metotlarda; **tercih et** |

## PhantomData

Bazen tür parametresi yalnızca işaret olarak gerekir, alan olarak tutulmaz. Derleyici kullanılmayan parametreyi kabul etmez; `std::marker::PhantomData` bu boşluğu doldurur. İleri modülde göreceğiz.
