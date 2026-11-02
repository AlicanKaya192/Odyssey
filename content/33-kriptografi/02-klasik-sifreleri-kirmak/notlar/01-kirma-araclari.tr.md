## Ölçütler

| Ölçüt | Hesap | Neye işaret eder? |
|---|---|---|
| Sık kelime sayısı | Çözülen metinde `the`, `and`… | Küçük anahtar uzayında doğru anahtar |
| Harf yüzdesi | `100 * sayı / toplam` | Dilin parmak izi |
| Ki-kare | Σ (görülen − beklenen)² / beklenen | Küçükse metin İngilizceye benziyor |
| Tesadüf indeksi | Σ n(n−1) / (N(N−1)) | İngilizce ≈ 0,066, rastgele ≈ 0,038 |

## Hangi şifreye hangisi?

- **Sezar:** 26 kaydırmanın hepsini dene, ki-kare en küçük olanı seç.
- **Yerine koyma:** harfleri sıklığa göre diz, `etaoin…` ile eşle, sonra
  kelime kalıplarıyla (`the`, `a`, çift harfler) düzelt.
- **Vigenère:** 1'den başlayarak uzunlukları dene; sütunların ortalama
  IoC'si 0,06'yı geçen ilk uzunluk anahtarın uzunluğu. Sonra her sütun bir
  Sezar.
- **Yer karıştırma:** harf yüzdeleri İngilizceyle aynıysa şifre yer
  karıştırmadır; satır sayılarını dene.

## Python kalıpları

- Yalnızca harfler: `[c for c in text.lower() if c.isalpha()]`.
- Sayım: `Counter(letters).most_common(n)`.
- Her `L`'inci harf: `letters[i::L]`.
- Eşitlikte küçük olanı seçmek: `(puan, kaydırma)` demetlerini sırala.

## Akılda tutulacak

Kısa metinde istatistik oynak: birkaç düzine harfle ki-kare yanılabilir,
birkaç yüz harfle neredeyse hiç yanılmaz.
