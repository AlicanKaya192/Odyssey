## Bir problemi çözerken

1. **Anla:** girdi ne, çıktı ne? Kendi kelimelerinle bir cümlede söyle.
2. **Elle iki üç örnek çöz,** biri uç durum olsun (boş, tek eleman, hepsi eşit).
3. **Bütçeyi kestir:** `n` en fazla kaç? Hangi karmaşıklık sığar?
4. **Önce kaba kuvvet:** yavaş ama doğru bir çözüm. Bazen yeter; yetmezse
   karşılaştırma testi için lazım.
5. **Kalıbı ara:** neyi tekrar tekrar hesaplıyorsun? Sıralamak, hash, yığın,
   ikili arama, DP işe yarar mı?
6. **Sına:** uç durumlar ve kaba kuvvete karşı rastgele girdiler.

## Kalıpların maliyeti

| Kalıp | Maliyet | Ön koşul |
|---|---|---|
| Cevap üzerinde ikili arama | `O(denetim × log aralık)` | denetim tek yönlü |
| Monoton yığın | `O(n)` | her öğe bir kez girer, bir kez çıkar |
| Durum uzayında BFS | `O(durum + hamle)` | durum sayısı makul |
| Ortada buluşma | `O(2^(n/2) · n)` | problem ikiye bölünebiliyor |

## Sık hatalar

- Bütçeye bakmadan en karmaşık çözüme koşmak: `n = 15` ise kaba kuvvet yeter.
- Cevap üzerinde ikili aramada aralığı yanlış kurmak: alt sınır en büyük kutu
  (`max`), üst sınır hepsi (`sum`); `max`'tan küçük bir kapasite hiçbir zaman
  yetmez.
- Monoton yığında `<` ile `<=` farkını düşünmemek: eşit değerler.
- BFS'te görülen durumları işaretlemeyi unutmak: aynı durum sonsuz kez kuyruğa
  girer.
