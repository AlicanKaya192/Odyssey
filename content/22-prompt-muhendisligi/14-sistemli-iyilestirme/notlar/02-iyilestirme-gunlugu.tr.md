Her prompt değişikliği için günlüğe bir satır:

| Sürüm | Değişiklik | Gerekçe (hangi hata türü) | Geliştirme | Bozulan | Token |
|---|---|---|---|---|---|
| v1 | Başlangıç | — | 0,60 | — | 59 |
| v2 | Kategori tanımlarına anlamdan gelen kelimeler | 8 hatanın 8'i `unknown` | 0,90 | 0 | 100 |
| v3 | Kalan hatalardan kopyalanan kelimeler | Kalan 2 hata | 1,00 | 0 | 139 |

Test kümesi yalnızca son seçilen sürüm için ölçülür ve satırın altına
not edilir. Bu tabloda `v3`'ün geliştirme ölçüsü en yüksek; ama
gerekçesi "kalan hatalar" ve eklediği kelimelerin kategoriyle ilgisi
yok: ezberin işareti.

**Kurallar:**

1. Bir satırda tek değişiklik.
2. Gerekçe bir hata türüne bağlansın; "denemek istedim" gerekçe değil.
3. Toplamın yanında bozulan cevap sayısını da yaz.
4. Token sayısını yaz; başarı getirmeyen uzunluk maliyettir.
5. Sürümün tam metnini ya da sürüm özetini sakla; hangi prompt'un hangi
   ölçüyü aldığı sonradan bulunabilsin.

**Sık hatalar:**

- **Test kümesine her değişiklikte bakmak.** Test kümesi gizlice
  geliştirme kümesine dönüşür.
- **Birkaç değişikliği birlikte yapmak.** Hangisinin işe yaradığı ve
  hangisinin bir şeyi bozduğu bilinmez.
- **Yalnızca toplama bakmak.** Toplam aynı kalırken cevaplar değişebilir.
- **Küçük kümede 0,05'lik farka güvenmek.** 20 mesajda bu tek bir mesaj.
- **Geliştirme kümesindeki mesajları örnek olarak prompt'a koymak.** O
  mesajlar artık ölçü değil, cevabı prompt'ta yazılı soru olur.
