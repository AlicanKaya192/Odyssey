## Hangi yolu seçmeli?

| Soru | Cevap |
|---|---|
| Değer gerçekten olmayabilir mi? | `Option` |
| Sebebi önemli mi? | `Result` |
| Çağıran hatalara göre farklı davranacak mı? | Enum hata türü |
| Yalnızca mesaj yazdırılacak mı? | `Result<T, String>` yeter |
| Bu bir programlama hatası mı? | `panic!` |

## Doğrulayan kurucu

Geçersiz değerin hiç oluşamamasını sağlamak için struct alanları gizlenir ve kurucu `Result` döndürür. Alanı gizlemeyi sonraki bölümde modüllerle göreceğiz; fikir şu:

```rust
#[derive(Debug)]
struct Age(u8);

impl Age {
    fn new(value: i32) -> Result<Age, String> {
        if value < 0 || value > 150 {
            return Err(format!("age must be 0-150, got {value}"));
        }
        Ok(Age(value as u8))
    }
}

fn main() {
    println!("{:?}", Age::new(36));
    println!("{:?}", Age::new(200));
}
```

```text
Ok(Age(36))
Err("age must be 0-150, got 200")
```

Böylece programın geri kalanı "yaş geçerli mi?" diye tekrar tekrar sormaz: `Age` varsa geçerlidir.

## İyi hata mesajı

| Kötü | İyi |
|---|---|
| `error` | `age must be 0-150, got 200` |
| `invalid input` | `line 3: "abc" is not a number` |

Ne bekleniyordu, ne geldi, nerede? Mesaj bu üçünü söylemeli.

## Hatayı yutma

`let _ = risky();` sonucu bilerek atar ve derleyiciyi susturur. Ne yaptığını biliyorsan olur; alışkanlık olursa hatalar sessizce kaybolur.

## Sonraki modülde

`Display`, `std::error::Error`, `From` ile otomatik çeviri (`?` bunu kullanır) ve `Box<dyn Error>`.
