## Tipik düzen

```text
my_tool/
├── Cargo.toml
├── src/
│   ├── main.rs      Argümanları oku, lib'i çağır, hatayı yaz
│   ├── lib.rs       Dışarı açılan yüz
│   ├── parser.rs    Bir iş
│   └── report.rs    Başka bir iş
└── tests/
    └── cli.rs       Bütünleşme testleri
```

`tests/` klasöründeki her dosya ayrı bir crate olarak derlenir ve kütüphaneyi dışarıdan kullanan biri gibi yalnızca `pub` olanı görür.

## Modülü nasıl ayırmalı?

| Ölçüt | Örnek |
|---|---|
| Birlikte değişen kod birlikte durur | Ayrıştırıcı ve onun hata türü |
| Sorumluluğa göre, türe göre değil | `parser`, `report`; `structs`, `functions` değil |
| Küçük yüz, büyük iç | Az `pub`, çok gizli |

Tek dosyada başla. Dosya okunmaz hale gelince böl; baştan klasör ağacı kurma.

## Bağımlılık yönü

`main.rs` → `lib.rs` → modüller. İki modül birbirini kullanıyorsa ortak parçayı üçüncü bir modüle taşımayı düşün. Rust buna izin verir ama okumayı zorlaştırır.

## Kaçınılacaklar

- `use a::*;`: Adın nereden geldiği belli olmaz. İstisna: `use super::*;` testlerde.
- Her şeye `pub` yazmak: Gizliliğin faydasını siler.
- Çok derin yol: `a::b::c::d::e`. `pub use` ile düzleştir.
