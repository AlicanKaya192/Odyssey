| Terim | Anlamı | Evdeki karşılığı |
|---|---|---|
| **Varlık** (asset) | Korunmaya değer şey | Evdeki eşyalar |
| **Tehdit** (threat) | Varlığa zarar verebilecek şey | Mahallede dolaşan hırsız, yangın |
| **Tehdit aktörü** (threat actor) | Tehdidin arkasındaki kişi ya da grup | Hırsızın kendisi |
| **Açık / zafiyet** (vulnerability) | Tehdidin kullanabileceği zayıflık | Kilitlenmeyen arka pencere |
| **İstismar** (exploit) | Açığı kullanmanın yolu | Pencereyi açıp içeri girmek |
| **Risk** | Olasılık × etki | Hırsızın girme ihtimali ve kaybın büyüklüğü |
| **Önlem / kontrol** (control) | Riski azaltan her şey | Pencere kilidi, alarm, sigorta |
| **Yama** (patch) | Açığı kapatan düzeltilmiş sürüm | Pencerenin tamiri |
| **Sıfırıncı gün** (zero-day) | Henüz yaması olmayan açık | Kimsenin bilmediği gizli kapı |

## CVE ve CVSS

- **CVE:** bilinen her açığa verilen ortak kimlik, `CVE-YIL-NUMARA`;
  numara en az dört basamak.
- **CVSS:** açığın 0–10 arası puanı. Şiddet adları: 0.0 None, 0.1–3.9 Low,
  4.0–6.9 Medium, 7.0–8.9 High, 9.0–10.0 Critical.
- CVSS açığı anlatır, senin riskini değil: aynı açık internete açık bir
  sunucuda acil, kapalı bir test makinesinde daha az acildir.

## Tehdit aktörleri

| Aktör | Amacı | Gücü |
|---|---|---|
| Meraklı / acemi | Denemek, göstermek | Düşük, hazır araçlar |
| Suç grubu | Para | Orta–yüksek, örgütlü |
| İçeriden biri (insider) | İntikam, para ya da yalnızca hata | Yetkisi zaten var |
| Amaç için saldıran (hacktivist) | Mesaj vermek | Değişken |
| Devlet destekli grup | Casusluk, sabotaj | Çok yüksek, sabırlı |

## Hatırla

- Risk için tehdit **ve** açık gerekir; tehdidi çoğu zaman kaldıramazsın,
  açığı kapatabilirsin.
- Her tehdit insan değildir: arıza, yangın ve sel de tehdittir.
