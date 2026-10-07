Anlamsal sürümleme (*Semantic Versioning*, semver.org) üç sayıdan oluşur:
**MAJOR.MINOR.PATCH**. Hangisinin artacağını değişikliğin türü belirler.

| Değişiklik | Örnek | Yeni sürüm (`1.4.2`'den) |
|---|---|---|
| Hata düzeltmesi, kullanan kimse bir şey değiştirmek zorunda değil | Yanlış hesaplanan toplam düzeldi | `1.4.3` (PATCH) |
| Yeni özellik, eskiler aynı çalışıyor | Yeni bir dışa aktarma seçeneği | `1.5.0` (MINOR; PATCH sıfırlanır) |
| Uyumsuz değişiklik, kullananlar kodunu değiştirmeli | Bir fonksiyonun adı ya da parametreleri değişti | `2.0.0` (MAJOR; diğerleri sıfırlanır) |

## Kurallar

- Bir sayı artınca sağındakiler sıfırlanır: `1.9.7` → `2.0.0`.
- `0.x.y` "henüz kararlı değil" demek; her an her şey değişebilir.
  Odyssey'nin `0.9.x` sürümleri bu yüzden 0 ile başlıyor.
- Yayınlanmış bir sürümün içeriği değiştirilmez; düzeltme yeni sürümdür.
- Ön sürümler için ek: `2.0.0-beta.1`, `2.0.0-rc.1` (*release candidate*).

## Etiket adları

Git etiket adına kural koymaz; ama gelenek `v` + sürüm: `v1.4.2`. Ekipçe
tek bir biçimde karar verin; `1.4.2`, `v1.4.2`, `release-1.4.2` karışık
olursa sıralama ve araçlar şaşırır.

## Sürüm notu

Her sürüm için bir **sürüm notu** (*changelog*) yazılır: neler eklendi,
neler değişti, neler düzeldi. `git log --oneline v1.4.2..v1.5.0` yazmaya
başlamak için iyi bir liste verir; ama not commit listesi değildir,
kullanıcının "bende ne değişti?" sorusuna cevap verir.
