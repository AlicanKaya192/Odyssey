## Çift değerlendirme

Şablonda `$x` kaç kez geçiyorsa ifade o kadar çalışır. Yan etkisi olan ifadede (sayaç, dosya okuma) sonuç yanlış çıkar, pahalı ifadede iş iki kat olur. Birden çok geçiyorsa başta `let value = $x;`.

## İki katlı parantez

Şablon birden çok deyim içeriyor ve bir değer üretiyorsa `{{ ... }}` gerekir: Dıştaki makronun sınırı, içteki blok ifadesi. Tek katla `let` içeren şablon, ifade beklenen yerde derlenmez.

## İfadeden sonra ne gelebilir?

`expr` nerede bittiği bilinsin diye arkasından yalnızca belirli işaretler gelebilir:

```rust
macro_rules! pair {
    ($a:expr $b:expr) => {
        ($a, $b)
    };
}

fn main() {
    let _ = pair!(1 2);
}
```

```text
error: `$a:expr` is followed by `$b:expr`, which is not allowed for `expr` fragments
 --> main.rs:2:14
  |
2 |     ($a:expr $b:expr) => {
  |              ^^^^^^^ not allowed after `expr` fragments
  |
  = note: allowed there are: `=>`, `,` or `;`
```

| Parça | Arkasından gelebilen |
|---|---|
| `expr`, `stmt` | `=>`, `,`, `;` |
| `pat` | `=>`, `,`, `=`, `if`, `in` |
| `ty`, `path` | `=>`, `,`, `=`, `;`, `:`, `{`, `[`, `>`, `as`, `where` |
| `ident`, `tt`, `literal`, `block` | Herhangi bir şey |

## Özyineleme sınırı

Kendini çağıran makronun varsayılan sınırı 128 adımdır. 200 token sayan `count!` şöyle durur: `recursion limit reached`. Sınır `#![recursion_limit = "256"]` ile yükseltilebilir, ama çok token işleyen makro derlemeyi yavaşlatır.

## Hijyen neyi kapsamaz?

Hijyen yerel değişkenler ve etiketler içindir. Şablondaki fonksiyon, tür ve modül adları çağrıldığı yerde aranır. `#[macro_export]` ile açılan makroda bu yüzden `$crate::yardimci()` yazılır; `::std::...` de aynı amaçla kullanılır.

## Hata ayıklamak

| Araç | Ne yapar |
|---|---|
| `cargo expand` (ayrı kurulur) | Açılmış kodu gösterir |
| `stringify!` | Yakalanan parçayı yazdırır |
| `compile_error!` | Beklenmeyen kola düşünce mesaj verir |

Hata mesajı çoğu zaman makronun içini gösterir, bu yüzden kalıpları küçük tutmak ve adım adım büyütmek işe yarar.

## Ne zaman yazmamalı?

| İhtiyaç | Daha iyi araç |
|---|---|
| Tek tür üstünde iş | Fonksiyon |
| Birçok tür, aynı davranış | Generic ve trait |
| Sabit değer hesabı | `const fn` |
| Yalnızca kısa yazmak | Yardımcı fonksiyon |

Makro kodu okumayı, otomatik tamamlamayı ve hata mesajlarını zorlaştırır. Bir işi fonksiyon ya da generic çözüyorsa makro yazma. Değişken sayıda argüman, yeni söz dizimi ya da bir türün parçasını (ad, alan) üretmek gerektiğinde yaz.
