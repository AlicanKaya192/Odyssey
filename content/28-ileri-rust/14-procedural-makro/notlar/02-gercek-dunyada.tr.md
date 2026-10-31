## syn ve quote

Bu bölümde token'ları elle ayrıştırdık ki kapının arkasını görelim. Gerçek projede neredeyse herkes iki crate kullanır:

| Crate | İşi |
|---|---|
| `syn` | Token'ları tam söz dizimi ağacına çevirir (`DeriveInput`, alanlar, generic'ler, öznitelikler) |
| `quote` | `quote! { ... }` ile kodu kod gibi yazdırır, yer tutucularla |
| `proc-macro2` | Bu ikisinin kullandığı, test edilebilir token türleri |

Bu patikada kurulu değiller, adlarını bilmen yeter. Elle yazdığımız `field_list`'in `enum`, demet yapı ve generic'te yetmemesi tam da bu crate'lerin sebebidir.

## Hazır örnekler

| Makro | Türü | Ne üretir |
|---|---|---|
| `#[derive(Serialize)]` | Derive | Serileştirme kodu |
| `#[tokio::main]` | Attribute | `main`'i çalıştırıcıyla sarar |
| `#[test]` | Yerleşik attribute | Test kaydı |
| `sqlx::query!` | Fonksiyon benzeri | SQL'i derlemede denetler |

## Güvenlik: Derleme sırasında kod çalışır

Procedural makro derleyicinin içinde, senin yetkilerinle çalışır. Dosya okuyabilir, ağa çıkabilir. Yani bir crate eklemek yalnızca "programıma kod katmak" değil, "bilgisayarımda derleme sırasında kod çalıştırmak" demektir. `build.rs` için de aynısı geçerli. Bağımlılık seçerken kimin yazdığına bak ve sürümü `Cargo.lock` ile sabitle.

## Derleme süresi

| Etken | Etkisi |
|---|---|
| Ayrı crate | Önce o derlenir |
| Ayrıştırıcı crate'ler | `syn` kendisi büyüktür |
| Ürettiğin kod | Her çağrı derleyiciye iş verir |

Çok kullanılan derive'lar derleme süresinde görünür bir paya sahip olabilir. `cargo build --timings` hangi crate'in ne kadar sürdüğünü gösterir.

## Hangi aracı seçmeli?

| İhtiyaç | Araç |
|---|---|
| Ortak davranış | Trait ve generic |
| Birçok tür için aynı kod | `macro_rules!` |
| Değişken sayıda argüman | `macro_rules!` |
| Yapının alanlarını okumak | Derive |
| Fonksiyonu sarmak | Attribute |
| Derlemede metin denetlemek | Fonksiyon benzeri |

Sıra bu şekildedir: Önce fonksiyon ve trait, olmazsa `macro_rules!`, o da olmazsa procedural makro.

## Test

Makroyu derleyici dışında çalıştıramazsın, çünkü `proc_macro` yalnızca derleyici içinde var. Üç yol:

| Yol | Nasıl |
|---|---|
| Kullanım testi | Başka crate'te makroyu kullanıp sonucu denetlemek |
| Hata testi | `trybuild` crate'i, beklenen derleme hatası |
| Mantığı ayırmak | İşi `proc-macro2` kullanan fonksiyona koymak |
