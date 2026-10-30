## Test iskeleti

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds() {
        assert_eq!(add(2, 3), 5);
        assert_ne!(add(2, 3), 6);
        assert!(add(0, 0) == 0);
    }
}

fn main() {}

```

{{F_skeleton}}

## Doğrulama makroları

| Makro | Düşer, eğer |
|---|---|
| `assert!(k)` | `k` `false` ise |
| `assert_eq!(a, b)` | `a != b` ise |
| `assert_ne!(a, b)` | `a == b` ise |

Üçü de sona mesaj alır: `assert!(ok, "beklenen: {}", x)`.

## Ne test edilir?

| Durum | Örnek |
|---|---|
| Olağan | Tek eşleşme |
| Boş | Boş metin, boş liste |
| Sınır | İlk satır, son satır, tam sınırdaki değer |
| Hatalı girdi | Eksik argüman, bozuk sayı |
| Ayrım | Büyük ve küçük harf |

## Kodu bilerek boz

Test yazınca sorulacak soru: **Kod bozulsa bu test düşer miydi?** Örneğin `contains`'i `==` ile değiştir: Yalnızca tam eşleşmeyi deneyen bir test geçmeye devam eder ve hatayı kaçırır.

## Testin yapmaması gerekenler

- Ekrana yazdığına bakmak: Değer döndüren fonksiyonu test et.
- Gerçek dosyalara bağlı olmak: Metni doğrudan ver.
- Birbirine bağlı olmak: Testler aynı anda ve sırasız çalışır.

## Daha fazlası

`#[should_panic]`, `tests/` klasörü ve belgedeki kod örnekleri sonraki modülde.
