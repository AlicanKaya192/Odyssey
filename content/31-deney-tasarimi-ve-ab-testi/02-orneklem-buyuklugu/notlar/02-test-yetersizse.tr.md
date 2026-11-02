Hesap "bu test altı ay sürer" diyorsa testi yine de başlatıp "bakalım ne
çıkacak" demek en kötü seçenektir: Güç Analizi bölümünde gördüğümüz gibi
düşük güçte anlamlı çıkan sonuç etkiyi abartır. Bunun yerine:

## Seçenekler

| Yol | Ne değişir | Bedeli |
|---|---|---|
| Daha büyük etki hedeflemek | MDE büyür, n küçülür | Küçük ama gerçek iyileştirmeleri kaçırırız |
| Daha duyarlı metrik | değişim katsayısı küçülür | Metrik asıl amaca daha uzak olabilir |
| Uç değerleri kırpmak | gelirin sapması küçülür | Dev siparişlerin etkisi görünmez |
| Varyans azaltma (CUPED) | ön dönem verisiyle gürültü azalır | Ek hesap, geçmiş veri gerekir |
| Daha çok trafik | n hızlı dolar | Başka deneyler bekler |
| Daha uzun süre | n dolar | Karar gecikir, kullanıcı kitlesi değişebilir |

## Yapma

- Gücü düşük bir testi başlatıp anlamlı çıkarsa kabul etmek.
- Test sürerken "biraz daha bekleyelim" diye süreyi uzatmak: süre baştan
  yazılır (Sıralı Bakma Tuzağı ve Ardışık Test bölümü).
- Taban oranını tahminle yazmak; geçmiş veriden ölçülür.
