| Konu | Ana fikir | Formül / ölçü |
|---|---|---|
| Örnekleme | Cetvel, ters dönüşüm, reddetme | Birikimli olasılık |
| Otomatik kodlayıcı | Dar koddan geri kurma | Geri kurma hatası |
| VAE | Kod bir dağılım, standart normale çekilir | Kayıp = geri kurma + β·KL; $z = \mu + \sigma\varepsilon$ |
| GAN | Üretici ve ayırt edici oyunu | $-\log D(x) - \log(1 - D(G(z)))$; dengede $D = 0{,}5$ |
| Difüzyon | Gürültüyü geri almayı öğren | $x_t = \sqrt{\bar\alpha_t}\, x_0 + \sqrt{1 - \bar\alpha_t}\, \varepsilon$ |
| LLM üretimi | Şablon, sıradaki token, bitiş nedeni | `stop` / `length` |
| Token ve maliyet | Geçmiş her çağrıda gönderilir | giren × fiyat + çıkan × fiyat |
| Halüsinasyon | Akıcı ama dayanaksız | Öz tutarlılık, kaynak denetimi |
| Parçalama ve arama | İlgili parçayı bul | key@k, kosinüs |
| RAG | Kaynakları prompt'a koy, kaynak göster | doğru / yanlış / kaçırılan / çekimser |
| RAG değerlendirme | Getirme ve cevap ayrı | recall@k, MRR, yeniden örnekleme |
| İnce ayar ve hizalama | Unutma, ödül modeli | $\sigma(r(a) - r(b))$ |
| LoRA | Düşük ranklı düzeltme | $\Delta W = AB$, parametre $r(d_{\text{giriş}} + d_{\text{çıkış}})$ |
| Güvenlik | Önyargı, vekil, maskeleme | Seçilme oranı, fırsat eşitliği |
| Bitirme | Maskele → ara → doğrula → kaydet → ölç | Bileşen başına ölçü |

**Bölümlerin ölçülmüş sonuçları:**

- VAE 10 rakamın hepsini, otomatik kodlayıcı 4'ünü üretti (03).
- GAN 0,01 öğrenme oranında 8, 6, 6 küme; difüzyon 8, 8, 8 (04, 05).
- Sekiz mesajda toplam giren token son çağrının 4,5 katı (07).
- RAG hatalarının 9'da 7'si getirmede (11).
- LoRA r = 4: 714 parametreyle %94; tam ince ayar 2410 parametreyle %93 (13).
- Bütün makaleler 979 token, RAG 50 token (16).
