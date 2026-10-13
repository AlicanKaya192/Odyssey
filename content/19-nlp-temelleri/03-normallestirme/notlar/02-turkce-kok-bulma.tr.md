Dersteki Türkçe kök bulucu ekleri listeden kesiyordu. Türkçenin ses
kuralları yüzünden bu yöntem kökün kendisini de bozabilir.

## Ek kesmek kökü bozduğunda

```python
SUFFIXES = ["ları", "leri", "lar", "ler", "ı", "i", "u", "ü"]


def turkish_root(word):
    for suffix in SUFFIXES:
        if word.endswith(suffix) and len(word) > len(suffix) + 1:
            return word[: -len(suffix)]
    return word


for w in ["kitabı", "ağacı", "kitapları", "evi", "köpeği"]:
    print(w, "->", turkish_root(w))
```

```text
kitabı -> kitab
ağacı -> ağac
kitapları -> kitap
evi -> ev
köpeği -> köpeğ
```

- "kitapları" → "kitap" doğru, ama "kitabı" → **"kitab"**: aynı kelimenin iki
  biçimi iki farklı köke düştü.
- "ağacı" → "ağac", "köpeği" → "köpeğ": kök sözlükteki biçim değil.

Sebep **ünsüz yumuşaması**: "kitap" ünlüyle başlayan bir ek alınca "kitab-ı"
olur; p → b, ç → c, k → ğ. Ek kesilince geriye yumuşamış hâl kalıyor.

## Türkçenin kök bulucuyu zorlayan kuralları

| Kural | Örnek | Kök bulucuya etkisi |
|---|---|---|
| Ünlü uyumu | ev-ler, okul-lar; ev-de, okul-da | Her ekin iki ya da dört biçimi var; listeye hepsi yazılmalı |
| Ünsüz benzeşmesi | kitap-ta, ağaç-tan | -de/-da'nın -te/-ta biçimleri de var |
| Ünsüz yumuşaması | kitap → kitabı, ağaç → ağacı | Ek kesilince kök bozuk kalır |
| Kaynaştırma | araba-y-ı, su-y-u | Araya giren harf kökte kalır: "araba-y" |
| Ek sırası | ev-ler-imiz-den | Ekler art arda; döngü gerekir |
| Ek gibi biten kök | dede, kale, bile | Kök yanlışlıkla kesilir |

## Gerçek çözüm

Biçimbilim çözümleyicileri (morphological analyser) kelimeyi ek ek çözer ve
bütün olası çözümlemeleri listeler; "kitabı" için kök "kitap", ek "-ı"
(belirtme ya da iyelik). Türkçe için en bilineni **Zemberek**. Basit
uygulamalarda Snowball'un Türkçe kök bulucusu da kullanılır.

İkinci modülde göreceğimiz **alt kelime parçalama** (BPE) başka bir yol
izliyor: dil kuralı bilmeden, veride sık geçen harf dizilerini (örneğin
"ler", "den") kendiliğinden ayrı parça olarak öğreniyor. Bugünkü dil
modelleri Türkçeyle böyle başa çıkıyor.
