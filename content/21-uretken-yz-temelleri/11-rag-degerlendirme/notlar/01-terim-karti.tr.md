| Terim | Anlamı |
|---|---|
| **Değerlendirme kümesi** | Elle etiketlenmiş sorular: doğru belge ve cevap ifadesi |
| **recall@k** | Cevap ifadesinin ilk k parçada bulunduğu soruların oranı |
| **MRR** (mean reciprocal rank) | Doğru parçanın sırasının tersinin ortalaması |
| **Getirme hatası** | Doğru parça prompt'a hiç girmedi |
| **Okuma hatası** | Doğru parça prompt'taydı ama cevap yanlış ya da eksik |
| **Çekimser kalma kesinliği** | "Bulamadım" cevaplarından gerçekten cevapsız sorulara gidenlerin oranı |
| **Çekimser kalma duyarlılığı** | Cevapsız soruların "bulamadım" ile tanınan oranı |
| **Yeniden örnekleme** (bootstrap) | Soruları yerine koyarak çekip ölçüyü tekrar tekrar hesaplamak |
| **Model ile değerlendirme** | Cevabı başka bir modele puanlatmak; o modelin de hataları vardır |

**Akılda tut:**

- Bölümde recall@1 0,71, recall@10 0,96; kaçan 9 cevabın 7'si getirme
  hatasıydı. İlk iş arama.
- Eşik 3'te duyarlılık 1,00 ama kesinlik 0,12: iki ölçü birlikte okunur.
- 24 soruda iki soruluk farkın %90 aralığı 0–4; küçük kümede karar
  vermek güvenli değil.
