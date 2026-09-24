**Ne soruluyor?** İki modelin doğruluk yüzdesi ve bu sayıların ne anlattığı.

**Fikir:** Doğruluk, doğru tahminlerin tüm tahminlere oranı. Hep aynı cevabı veren bir model, o cevabın doğru olduğu bütün örnekleri bilir.

**Adım 1 — Modelin doğruluğu.**

$$
\frac{1\,870}{2\,200} = \frac{187}{220} = \frac{17}{20} = 0{,}85 = \%85
$$

($1\,870$ ve $2\,200$'ü önce $10$'a, sonra $11$'e böldük.)

**Adım 2 — Hep "normal" diyen model.** $2\,090$ normal işlemin hepsini doğru, $110$ sahtekârlığın hepsini yanlış bilir:

$$
\frac{2\,090}{2\,200} = \frac{19}{20} = 0{,}95 = \%95
$$

**Adım 3 — Karşılaştır.** Hiçbir şey öğrenmemiş model, eğitilmiş modelden **daha yüksek** doğruluk aldı.

**Sonucu yorumla:** Veri çok dengesiz: işlemlerin $\%95$'i normal. Böyle bir veride doğruluk tek başına yanıltıcı; asıl önemli olan azınlık sınıfındaki (sahtekârlık) başarı. Hep "normal" diyen model tek bir sahtekârlığı yakalamıyor, yani işe yaramıyor.

**Cevap:** $\%85$ ve $\%95$.
