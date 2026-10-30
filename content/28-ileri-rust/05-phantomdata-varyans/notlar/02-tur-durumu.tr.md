## Tür düzeyinde durum

`PhantomData`'nın en güzel kullanımlarından biri, bir değerin **durumunu türüne yazmaktır** (typestate). Yanlış sıradaki çağrı derlenmez:

```rust
use std::marker::PhantomData;

struct Open;
struct Closed;

struct Door<State> {
    name: String,
    _state: PhantomData<State>,
}

impl Door<Closed> {
    fn open(self) -> Door<Open> {
        Door { name: self.name, _state: PhantomData }
    }
}

impl Door<Open> {
    fn walk_through(&self) -> String {
        format!("through {}", self.name)
    }
}
```

`Door<Closed>` üzerinde `walk_through` yöntemi **yoktur**. Çalışma anı denetimi gerekmez, hata mesajı da gerekmez.

## Ne zaman iyi?

| Durum | Karar |
|---|---|
| Sıralı işlem: Bağlan, yetkilen, sorgula | İyi |
| Kurucu kalıbı: Zorunlu alanlar doldurulmadan `build` yok | İyi |
| Durum dosyadan ya da ağdan geliyor | Kötü: Tür derlerken bilinmeli |
| Durum sayısı çok | Kötü: Kod patlar, `enum` kullan |

## Bedeli

Sıfır: `PhantomData` çalışma anında yok. Yöntem `self` alıp yeni tür döndürür; eski değer kullanılamaz, çünkü taşınmıştır. Sahiplik burada da işe yarıyor: Kapı "hem açık hem kapalı" olamaz.

Standart kütüphane dışında çok yaygındır; web istemcileri ve sürücü kodlarında sık görülür.
