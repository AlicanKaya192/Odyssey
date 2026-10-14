| Terim | Anlamı |
|---|---|
| **RAG** (getirmeyle desteklenen üretim) | İlgili parçaları bulup modele verip cevabı onlara dayandırmak |
| **Getirme** (retrieval) | Soruya en ilgili parçaları bulma adımı |
| **Bağlam** (context) | Prompt'a konan numaralı parçalar |
| **Kaynak gösterme** (citation) | Cevabın hangi parçadan geldiğini numarasıyla yazmak |
| **Çekimser kalma eşiği** | Cevap vermek için gereken en az dayanak; düşükse yanlış, yüksekse kaçırma artar |
| **Yanlış getirme** | Aramanın doğru parçayı bulamaması |
| **Getirileni yanlış kullanma** | Doğru parça varken cevabın yanlış parçaya ya da yanlış yoruma dayanması |

**Akılda tut:**

- Kaynaksız düzenek 24 sorunun hepsini kaçırdı; kaynaklı düzenek eşik 2 ile
  15 doğru, 2 yanlış, 7 kaçırma; eşik 1 ile 17 doğru, 7 yanlış.
- Kaynaklar her çağrıya ortalama 58 token ekledi.
- Bölümün okuyucusu gerçek modelin yerine konmuş kaba bir örnek; sayılar
  düzeneğin davranışını gösteriyor.
