## Ölçüm hataları

| Hata | Sonucu | Çare |
|---|---|---|
| Debug'da ölçmek | Anlamsız sayı | `--release` |
| Sonucu kullanmamak | İş silinir | `black_box` |
| Tek çalıştırma | Gürültü | Birçok tekrar, ortanca |
| İlk çalıştırmayı saymak | Önbellek soğuk | Isınma turu |
| Çok küçük veri | Önbelleğe sığar | Gerçek boyut |
| Çok kısa süre | Saat çözünürlüğü | Yeterince tekrar |
| Başka iş açıkken | Dalgalanır | Sakin makine |
| `println!` ölçülen yerde | G/Ç ölçülür | Döngü dışına al |

## Araçlar

| Araç | Ne için |
|---|---|
| `Instant` | Kaba ölçüm, kendi kodun |
| `criterion` | İstatistikli karşılaştırmalı benchmark |
| `hyperfine` | Bütün programın süresi |
| `flamegraph`, `perf` | Zaman nerede geçiyor |
| `dhat` | Ayırmalar nerede |
| `cargo build --timings` | Derleme nerede uzuyor |
| `cargo bloat` | Dosyayı ne büyütüyor |

Bu patikada kurulu değiller, adlarını bilmen yeter. Profiler için `[profile.release]`'e `debug = true` yaz; yoksa çıktıda sembol adları görünmez.

## Süre yerine sayaç

Süre gürültülüdür. Çoğu soru için sayaç daha dürüst bir cevap verir:

| Soru | Sayaç |
|---|---|
| Ayırma azaldı mı? | `GlobalAlloc` sayacı |
| Algoritma iyileşti mi? | Karşılaştırma sayısı |
| Önbellek tuttu mu? | `perf stat` önbellek kaçırma sayısı |

Odyssey'deki alıştırmaların süreye bakmamasının sebebi de budur: Sonuç her makinede aynı.

## Karşılaştırırken

1. Önce temel ölçümü al, kaydet.
2. Bir şeyi değiştir.
3. Aynı veriyle yeniden ölç.
4. Fark gürültüden büyük mü? Değilse iyileştirme yoktur.
5. Kod karmaşıklaştıysa kazanç buna değer mi?

## Ne zaman durmalı?

Hedef belli olmalı: "Bu istek 100 ms altında dönsün" ölçülebilir, "daha hızlı olsun" değildir. Hedefe ulaşınca dur. Paralellik de son çaredir; önce tek kolun gerçekten doygun olduğunu ölç. Eşzamanlılık hataları ve karmaşıklık da bir maliyettir.
