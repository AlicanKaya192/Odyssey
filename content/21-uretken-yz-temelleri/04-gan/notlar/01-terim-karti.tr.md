| Terim | Anlamı |
|---|---|
| **GAN** (çekişmeli üretici ağ) | Birbirine karşı eğitilen bir üretici ile bir ayırt ediciden oluşan üretken model |
| **Üretici** (generator, G) | Rastgele gürültüden örnek üreten ağ; gerçek veriyi hiç görmez |
| **Ayırt edici** (discriminator, D) | Bir örneğin gerçek olma olasılığını söyleyen ikili sınıflandırıcı |
| **Çekişmeli kayıp** (adversarial loss) | Üreticinin ayırt ediciyi kandırma ölçüsü; pratikte $-\log D(G(z))$ |
| **Denge** | Ayırt edicinin gerçek ile sahteyi ayıramadığı, her şeye 0,5 dediği durum |
| **En iyi ayırt edici** | $D^*(x) = \frac{p_{\text{veri}}(x)}{p_{\text{veri}}(x) + p_G(x)}$ |
| **Mod** | Dağılımın tepe noktası; bölümde halkadaki sekiz kümeden biri |
| **Mod çöküşü** (mode collapse) | Üreticinin verinin yalnızca bir kısmını üretip gerisini unutması |
| **Logit** | Ayırt edicinin `sigmoid`'den önceki ham çıkışı |

**Akılda tut:**

- İki ağ sırayla eğitilir: önce ayırt edici (gerçek + sahte grup), sonra
  üretici (yeni sahte grup, türev ayırt edicinin içinden geçerek).
- Eski üretici kaybı $\log(1 - D(G(z)))$'nin türevi başta neredeyse sıfır
  ($p = 0{,}01$'de $-0{,}01$); $-\log D(G(z))$'ninki $-0{,}99$.
- Kayıp mod çöküşünü ancak dolaylı gösterir; üretilen örneklere bakılır.
