| Terim | Anlamı |
|---|---|
| **Parça** (chunk) | Belgenin aranıp modele gönderilen küçük bölümü |
| **Parçalama** (chunking) | Belgeyi parçalara bölme yöntemi: makale, cümle, sabit pencere |
| **Örtüşme** (overlap) | Ardışık parçaların paylaştığı kelimeler; sınırda bölünmeyi azaltır |
| **Vektör arama** | Soruya vektörü en yakın parçaları bulmak |
| **Kosinüs benzerliği** | İki vektörün yön benzerliği; boyu 1 olan vektörlerde iç çarpım |
| **Gömme modeli** (embedding model) | Metni anlamı yansıtan sayısal vektöre çeviren model |
| **Vektör veritabanı** | Çok sayıda vektörü saklayıp yaklaşık en yakın komşu araması yapan sistem |
| **Karma arama** (hybrid search) | Kelime aramasını ve gömme aramasını birlikte kullanmak |
| **key@k** | Doğru cevap ifadesinin ilk k parçadan birinde geçme oranı |

**Akılda tut:**

- Bölümde makalenin tamamı 1,0 / 225 token, cümle 0,71 / 50 token,
  24 kelime + 8 örtüşme 0,88 / 106 token verdi.
- Kelime araması, başka kelimelerle sorulan soruyu kaçırır ("money back"
  ile "refund").
- Parçalama ve arama gerçek sorularla ölçülerek seçilir.
