## Tablo

| Tür | Sahip | Ne için |
|---|---|---|
| `&T`, `&mut T` | Yok, ödünç | Çoğu iş |
| `Box<T>` | Tek | Öbek, özyineleme, `dyn` |
| `Rc<T>` | Çok, tek iş parçacığı | Paylaşım (bölüm 08) |
| `Arc<T>` | Çok, iş parçacıkları arası | Paylaşım (bölüm 11) |
| `RefCell<T>` | Tek, çalışma anı denetimi | İç değişebilirlik |
| `String`, `Vec<T>` | Tek | Büyüyen veri |

## Box yazımları

| İş | Yazım |
|---|---|
| Oluştur | `Box::new(5)` |
| Değeri al | `*boxed` |
| Değiştir | `*boxed = 6` (`mut` ile) |
| Metot | `boxed.len()` (deref ile) |
| İçindekini çıkar | `*boxed` (`T` taşınır) |

## Hatalar

| Kod | Anlamı | Çözüm |
|---|---|---|
| `E0072` | Sonsuz boyutlu tür | `Box` ekle |
| `E0040` | `x.drop()` çağrısı | `drop(x)` |
| `E0382` | `drop(x)` sonrası kullanım | Sırayı değiştir |
| `E0614` | `*` uygulanamaz tür | `Deref` yaz |

## Copy ve Drop

Bir tür ikisini birden alamaz: Silinirken iş yapan değer kopyalanırsa iş iki kez yapılırdı.
